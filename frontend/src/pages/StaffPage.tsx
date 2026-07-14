import { useCallback, useEffect, useState } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { Badge, Card, ErrorState, LoadingState, Select } from '../components/ui'
import {
  createStaff,
  fetchInstitutionOptions,
  fetchStaff,
  fetchStaffById,
  updateStaff,
} from '../services/healthApi'
import type { HealthProfRecord, PartyRecord } from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'

type StaffRow = HealthProfRecord & { specialtyName?: string; institutionName?: string }

const emptyCreate = {
  name: '',
  code: '',
  licenseCode: '',
  institutionId: '',
  info: '',
}

export function StaffPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { client } = useAuth()
  const [records, setRecords] = useState<StaffRow[]>([])
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [institutions, setInstitutions] = useState<Array<{ id: number; label: string }>>([])
  const [form, setForm] = useState(emptyCreate)

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchStaff(client, debounced)
      setRecords(result.records)
      setTotal(result.total)
      if (!result.available) setError(t('staff.unavailable'))
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, t])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!showForm) return
    fetchInstitutionOptions(client)
      .then(setInstitutions)
      .catch(() => setInstitutions([]))
  }, [showForm, client])

  const save = async () => {
    if (!form.name.trim()) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      const { staffId, partyId } = await createStaff(client, {
        name: form.name,
        code: form.code || undefined,
        licenseCode: form.licenseCode || undefined,
        institutionId: form.institutionId ? Number(form.institutionId) : undefined,
        info: form.info || undefined,
      })
      setShowForm(false)
      setForm(emptyCreate)
      setSuccess(t('staff.saveSuccess'))
      if (staffId) {
        navigate(`/staff/${staffId}`, { state: { success: t('staff.saveSuccess') } })
      } else {
        await load()
        void partyId
      }
    } catch (err) {
      setError(formatRpcError(err, t('staff.saveError')))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('staff.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('staff.subtitle')}</p>
        </div>
        <button type="button" className="ist-btn ist-btn--primary" onClick={() => setShowForm(true)}>
          {t('staff.new')}
        </button>
      </div>

      <div className="ist-split" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('staff.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <span className="ist-subtitle">{t('staff.total', { count: total })}</span>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={load} />}

      {showForm && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('staff.createTitle')}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('staff.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                required
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.code')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.code}
                placeholder="IST-STF-…"
                onChange={(e) => setForm((f) => ({ ...f, code: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.license')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.licenseCode}
                onChange={(e) => setForm((f) => ({ ...f, licenseCode: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.institution')}</div>
              <Select
                value={form.institutionId}
                onChange={(e) => setForm((f) => ({ ...f, institutionId: e.target.value }))}
              >
                <option value="">{t('staff.selectInstitution')}</option>
                {institutions.map((i) => (
                  <option key={i.id} value={i.id}>{i.label}</option>
                ))}
              </Select>
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('staff.info')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.info}
                onChange={(e) => setForm((f) => ({ ...f, info: e.target.value }))}
              />
            </label>
          </div>
          <p className="ist-subtitle" style={{ marginTop: 'var(--space-3)' }}>
            {t('staff.specialtyHint')}
          </p>
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
        <LoadingState message={t('staff.loading')} />
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('staff.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div className="ist-patient-list__head" style={{ gridTemplateColumns: '120px 1fr 1fr 100px' }}>
            <span>{t('staff.code')}</span>
            <span>{t('staff.name')}</span>
            <span>{t('staff.specialty')}</span>
            <span>{t('staff.status')}</span>
          </div>
          {records.map((row) => (
            <div
              key={row.id}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: '120px 1fr 1fr 100px' }}
            >
              <Link to={`/staff/${row.id}`} className="ist-patient-list__id">
                {row.puid ?? row.code ?? row.id}
              </Link>
              <div>
                <Link to={`/staff/${row.id}`} className="ist-patient-name">
                  {row.rec_name ?? String(row.id)}
                </Link>
                {row.institutionName && (
                  <div className="ist-patient-meta">{row.institutionName}</div>
                )}
              </div>
              <span className="ist-subtitle">{row.specialtyName ?? '—'}</span>
              <span className={`ist-status${row.active !== false ? ' ist-status--completed' : ''}`}>
                {row.active !== false ? t('patients.active') : t('patients.inactive')}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export function StaffDetailPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const { t } = useTranslation()
  const { client } = useAuth()
  const [staff, setStaff] = useState<(StaffRow & { info?: string }) | null>(null)
  const [party, setParty] = useState<PartyRecord | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(
    (location.state as { success?: string } | null)?.success ?? null,
  )
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [institutions, setInstitutions] = useState<Array<{ id: number; label: string }>>([])
  const [form, setForm] = useState({
    name: '',
    code: '',
    licenseCode: '',
    institutionId: '',
    info: '',
    active: true,
  })

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError(null)
    try {
      const result = await fetchStaffById(client, Number(id))
      setStaff(result.staff)
      setParty(result.party)
      setForm({
        name: result.party?.name ?? result.staff.rec_name ?? '',
        code: result.party?.code ?? '',
        licenseCode: String(result.staff.code ?? ''),
        institutionId: result.staff.institution ? String(result.staff.institution) : '',
        info: String(result.staff.info ?? ''),
        active: result.staff.active !== false,
      })
    } catch {
      setError(t('staff.notFound'))
    } finally {
      setLoading(false)
    }
  }, [client, id, t])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!editing) return
    fetchInstitutionOptions(client)
      .then(setInstitutions)
      .catch(() => setInstitutions([]))
  }, [editing, client])

  const save = async () => {
    if (!staff || !form.name.trim()) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      await updateStaff(client, {
        staffId: staff.id,
        partyId: party?.id ?? staff.party ?? null,
        data: {
          name: form.name,
          code: form.code || undefined,
          licenseCode: form.licenseCode,
          institutionId: form.institutionId ? Number(form.institutionId) : 0,
          info: form.info,
          active: form.active,
        },
      })
      setEditing(false)
      setSuccess(t('staff.updateSuccess'))
      await load()
    } catch (err) {
      setError(formatRpcError(err, t('staff.saveError')))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingState message={t('common.loading')} />
  if (!staff) return <ErrorState message={error ?? t('staff.notFound')} />

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <Link to="/staff" className="ist-link" style={{ display: 'inline-block', marginBottom: 'var(--space-3)' }}>
            ← {t('staff.back')}
          </Link>
          <p className="ist-tagline">{t('staff.detail')}</p>
          <h1 className="ist-patients__title">{staff.rec_name}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle ist-id">{staff.puid ?? staff.code ?? String(staff.id)}</p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
          <Badge variant={staff.active !== false ? 'success' : 'default'}>
            {staff.active !== false ? t('patients.active') : t('patients.inactive')}
          </Badge>
          {!editing && (
            <button type="button" className="ist-btn ist-btn--primary" onClick={() => setEditing(true)}>
              {t('common.edit')}
            </button>
          )}
        </div>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && editing && <ErrorState message={error} />}

      {editing ? (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('staff.editTitle')}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('staff.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.code')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.code}
                onChange={(e) => setForm((f) => ({ ...f, code: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.license')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.licenseCode}
                onChange={(e) => setForm((f) => ({ ...f, licenseCode: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('staff.institution')}</div>
              <Select
                value={form.institutionId}
                onChange={(e) => setForm((f) => ({ ...f, institutionId: e.target.value }))}
              >
                <option value="">{t('staff.selectInstitution')}</option>
                {institutions.map((i) => (
                  <option key={i.id} value={i.id}>{i.label}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('staff.status')}</div>
              <Select
                value={form.active ? '1' : '0'}
                onChange={(e) => setForm((f) => ({ ...f, active: e.target.value === '1' }))}
              >
                <option value="1">{t('patients.active')}</option>
                <option value="0">{t('patients.inactive')}</option>
              </Select>
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('staff.info')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.info}
                onChange={(e) => setForm((f) => ({ ...f, info: e.target.value }))}
              />
            </label>
          </div>
          <p className="ist-subtitle" style={{ marginTop: 'var(--space-3)' }}>
            {t('staff.specialtyHint')}
          </p>
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button type="button" className="ist-btn ist-btn--primary" disabled={saving} onClick={save}>
              {saving ? t('common.loading') : t('common.save')}
            </button>
            <button type="button" className="ist-btn ist-btn--outline" onClick={() => setEditing(false)}>
              {t('common.cancel')}
            </button>
          </div>
        </div>
      ) : (
        <Card>
          <div className="ist-grid ist-grid--2" style={{ padding: 'var(--space-6)' }}>
            <Field label={t('staff.name')} value={staff.rec_name ?? '—'} />
            <Field label={t('staff.code')} value={staff.puid ?? staff.code ?? String(staff.id)} />
            <Field label={t('staff.specialty')} value={staff.specialtyName ?? '—'} />
            <Field label={t('staff.institution')} value={staff.institutionName ?? '—'} />
            {party && <Field label={t('staff.party')} value={party.name} />}
            {party?.code && <Field label={t('patients.code')} value={party.code} />}
            {staff.info && (
              <div style={{ gridColumn: '1 / -1' }}>
                <Field label={t('staff.info')} value={staff.info} />
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}

function Field({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div>
      <div className="ist-label">{label}</div>
      <div className="ist-subtitle" style={{ marginTop: 'var(--space-1)' }}>{value}</div>
    </div>
  )
}
