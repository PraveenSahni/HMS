import { useCallback, useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState, Select } from '../components/ui'
import {
  createAppointment,
  fetchAppointments,
  fetchHealthProfOptions,
  fetchPatientOptions,
  formatTrytonDate,
  updateAppointment,
} from '../services/healthApi'
import {
  APPOINTMENT_STATES,
  APPOINTMENT_URGENCIES,
  APPOINTMENT_VISIT_TYPES,
  trytonDateToInput,
  type AppointmentRecord,
} from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'

function todayIso(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function statusClass(state: unknown): string {
  const s = String(state ?? '').toLowerCase()
  if (s === 'done' || s === 'checked_in') return ' ist-status--completed'
  if (s === 'confirmed' || s === 'free') return ' ist-status--scheduled'
  if (s === 'no_show' || s === 'cancelled') return ''
  return ' is-pending'
}

export function AppointmentsPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [view, setView] = useState<'list' | 'day'>('list')
  const [day, setDay] = useState(todayIso())
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [records, setRecords] = useState<
    Array<AppointmentRecord & { patientName?: string; healthprofName?: string }>
  >([])
  const [total, setTotal] = useState(0)
  const [showForm, setShowForm] = useState(false)
  const [editId, setEditId] = useState<number | null>(null)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState<string | null>(null)
  const [patients, setPatients] = useState<Array<{ id: number; label: string }>>([])
  const [staff, setStaff] = useState<Array<{ id: number; label: string }>>([])
  const [form, setForm] = useState({
    patientId: '',
    healthprofId: '',
    appointmentDate: `${todayIso()}T09:00`,
    state: 'confirmed',
    urgency: '',
    visitType: '',
    comments: '',
  })

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchAppointments(client, {
        search: debounced || undefined,
        day: view === 'day' ? day : undefined,
        limit: 100,
      })
      setRecords(result.records)
      setTotal(result.total)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, day, view, t])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!showForm) return
    Promise.all([fetchPatientOptions(client), fetchHealthProfOptions(client)])
      .then(([p, s]) => {
        setPatients(p)
        setStaff(s)
      })
      .catch(() => {
        /* ignore */
      })
  }, [showForm, client])

  const openCreate = () => {
    setEditId(null)
    setForm({
      patientId: '',
      healthprofId: '',
      appointmentDate: `${todayIso()}T09:00`,
      state: 'confirmed',
      urgency: '',
      visitType: '',
      comments: '',
    })
    setShowForm(true)
  }

  const openEdit = (row: (typeof records)[0]) => {
    setEditId(Number(row.id))
    setForm({
      patientId: String(row.patient ?? ''),
      healthprofId: String(row.healthprof ?? ''),
      appointmentDate: trytonDateToInput(row.appointment_date) || `${todayIso()}T09:00`,
      state: String(row.state ?? 'confirmed'),
      urgency: String(row.urgency ?? ''),
      visitType: String(row.visit_type ?? ''),
      comments: String(row.comments ?? ''),
    })
    setShowForm(true)
  }

  const save = async () => {
    if (!form.patientId || !form.healthprofId || !form.appointmentDate) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      if (editId) {
        await updateAppointment(client, editId, {
          patientId: Number(form.patientId),
          healthprofId: Number(form.healthprofId),
          appointmentDate: form.appointmentDate,
          state: form.state,
          urgency: form.urgency,
          visitType: form.visitType,
          comments: form.comments,
        })
        setSuccess(t('appointments.updateSuccess'))
      } else {
        await createAppointment(client, {
          patientId: Number(form.patientId),
          healthprofId: Number(form.healthprofId),
          appointmentDate: form.appointmentDate,
          state: form.state,
          urgency: form.urgency || undefined,
          visitType: form.visitType || undefined,
          comments: form.comments,
        })
        setSuccess(t('appointments.saveSuccess'))
      }
      setShowForm(false)
      await load()
    } catch (err) {
      setError(formatRpcError(err, t('appointments.saveError')))
    } finally {
      setSaving(false)
    }
  }

  const dayGroups = useMemo(() => {
    if (view !== 'day') return null
    return records
  }, [view, records])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('appointments.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('appointments.subtitle')}</p>
        </div>
        <button type="button" className="ist-btn ist-btn--primary" onClick={openCreate}>
          {t('appointments.new')}
        </button>
      </div>

      <div className="ist-split" style={{ marginBottom: 'var(--space-6)', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('appointments.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
          <button
            type="button"
            className={`ist-btn ist-btn--sm${view === 'list' ? ' ist-btn--primary' : ' ist-btn--outline'}`}
            onClick={() => setView('list')}
          >
            {t('appointments.viewList')}
          </button>
          <button
            type="button"
            className={`ist-btn ist-btn--sm${view === 'day' ? ' ist-btn--primary' : ' ist-btn--outline'}`}
            onClick={() => setView('day')}
          >
            {t('appointments.viewDay')}
          </button>
          {view === 'day' && (
            <input
              type="date"
              className="ist-input ist-input--boxed"
              value={day}
              onChange={(e) => setDay(e.target.value)}
            />
          )}
          <span className="ist-subtitle">{t('appointments.total', { count: total })}</span>
        </div>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={load} />}

      {showForm && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>
            {editId ? t('appointments.edit') : t('appointments.new')}
          </h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('appointments.patient')}</div>
              <Select
                value={form.patientId}
                onChange={(e) => setForm((f) => ({ ...f, patientId: e.target.value }))}
              >
                <option value="">{t('appointments.selectPatient')}</option>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.label}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('appointments.healthprof')}</div>
              <Select
                value={form.healthprofId}
                onChange={(e) => setForm((f) => ({ ...f, healthprofId: e.target.value }))}
              >
                <option value="">{t('appointments.selectStaff')}</option>
                {staff.map((s) => (
                  <option key={s.id} value={s.id}>{s.label}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('appointments.date')}</div>
              <input
                type="datetime-local"
                className="ist-input ist-input--boxed"
                value={form.appointmentDate}
                onChange={(e) => setForm((f) => ({ ...f, appointmentDate: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('appointments.state')}</div>
              <Select
                value={form.state}
                onChange={(e) => setForm((f) => ({ ...f, state: e.target.value }))}
              >
                {APPOINTMENT_STATES.map((s) => (
                  <option key={s} value={s}>{t(`appointments.states.${s}`)}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('appointments.urgency')}</div>
              <Select
                value={form.urgency}
                onChange={(e) => setForm((f) => ({ ...f, urgency: e.target.value }))}
              >
                <option value="">{t('appointments.urgencyUnset')}</option>
                {APPOINTMENT_URGENCIES.map((u) => (
                  <option key={u} value={u}>{t(`appointments.urgencies.${u}`)}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('appointments.visitType')}</div>
              <Select
                value={form.visitType}
                onChange={(e) => setForm((f) => ({ ...f, visitType: e.target.value }))}
              >
                <option value="">{t('appointments.visitUnset')}</option>
                {APPOINTMENT_VISIT_TYPES.map((v) => (
                  <option key={v} value={v}>{t(`appointments.visits.${v}`)}</option>
                ))}
              </Select>
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('appointments.comments')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.comments}
                onChange={(e) => setForm((f) => ({ ...f, comments: e.target.value }))}
              />
            </label>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button type="button" className="ist-btn ist-btn--primary" disabled={saving} onClick={save}>
              {saving ? t('common.loading') : t('common.save')}
            </button>
            <button type="button" className="ist-btn ist-btn--outline" onClick={() => setShowForm(false)}>
              {t('common.cancel')}
            </button>
          </div>
        </div>
      )}

      {loading && !records.length ? (
        <LoadingState message={t('appointments.loading')} />
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('appointments.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div className="ist-patient-list__head" style={{ gridTemplateColumns: '140px 1fr 1fr 100px 80px' }}>
            <span>{t('appointments.date')}</span>
            <span>{t('appointments.patient')}</span>
            <span>{t('appointments.healthprof')}</span>
            <span>{t('appointments.state')}</span>
            <span />
          </div>
          {(dayGroups ?? records).map((row) => (
            <div
              key={String(row.id)}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: '140px 1fr 1fr 100px 80px' }}
            >
              <span className="ist-patient-list__date">{formatTrytonDate(row.appointment_date)}</span>
              <span className="ist-patient-name">{row.patientName ?? String(row.patient ?? '—')}</span>
              <span className="ist-subtitle">{row.healthprofName ?? String(row.healthprof ?? '—')}</span>
              <span className={`ist-status${statusClass(row.state)}`}>
                {row.state ? t(`appointments.states.${String(row.state)}`, { defaultValue: String(row.state) }) : '—'}
              </span>
              <button type="button" className="ist-btn ist-btn--outline ist-btn--sm" onClick={() => openEdit(row)}>
                {t('common.edit')}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
