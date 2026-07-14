import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState, Select } from '../components/ui'
import { createPatient, fetchPatients } from '../services/healthApi'
import { BLOOD_TYPES, type PartyRecord } from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'

const emptyForm = {
  name: '',
  code: '',
  gender: '',
  dob: '',
  bloodType: '',
  lastname: '',
  criticalInfo: '',
}

export function PatientsPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { client } = useAuth()
  const [records, setRecords] = useState<PartyRecord[]>([])
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState(emptyForm)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchPatients(client, debouncedSearch)
      setRecords(result.records)
      setTotal(result.total)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debouncedSearch, t])

  useEffect(() => {
    load()
  }, [load])

  const save = async () => {
    if (!form.name.trim()) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      const { partyId } = await createPatient(client, {
        name: form.name,
        code: form.code || undefined,
        gender: form.gender || undefined,
        dob: form.dob || undefined,
        bloodType: form.bloodType || undefined,
        lastname: form.lastname || undefined,
        criticalInfo: form.criticalInfo || undefined,
      })
      setShowForm(false)
      setForm(emptyForm)
      setSuccess(t('patients.saveSuccess'))
      navigate(`/patients/${partyId}`, { state: { success: t('patients.saveSuccess') } })
    } catch (err) {
      setError(formatRpcError(err, t('patients.saveError')))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('patients.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('patients.subtitle')}</p>
        </div>
        <button type="button" className="ist-btn ist-btn--primary" onClick={() => setShowForm(true)}>
          {t('dashboard.btnNewPatient')}
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
            placeholder={t('patients.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <span className="ist-subtitle">{t('patients.total', { count: total })}</span>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={load} />}

      {showForm && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('patients.createTitle')}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('patients.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                required
              />
            </label>
            <label>
              <div className="ist-label">{t('patients.lastname')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.lastname}
                onChange={(e) => setForm((f) => ({ ...f, lastname: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('patients.code')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.code}
                placeholder="IST-P-…"
                onChange={(e) => setForm((f) => ({ ...f, code: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('patients.dob')}</div>
              <input
                type="date"
                className="ist-input ist-input--boxed"
                value={form.dob}
                onChange={(e) => setForm((f) => ({ ...f, dob: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('patients.gender')}</div>
              <Select
                value={form.gender}
                onChange={(e) => setForm((f) => ({ ...f, gender: e.target.value }))}
              >
                <option value="">{t('patients.genderUnset')}</option>
                <option value="m">{t('patients.genderM')}</option>
                <option value="f">{t('patients.genderF')}</option>
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('patients.bloodType')}</div>
              <Select
                value={form.bloodType}
                onChange={(e) => setForm((f) => ({ ...f, bloodType: e.target.value }))}
              >
                <option value="">{t('patients.bloodUnset')}</option>
                {BLOOD_TYPES.map((bt) => (
                  <option key={bt} value={bt}>{bt}</option>
                ))}
              </Select>
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('patients.criticalInfo')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.criticalInfo}
                onChange={(e) => setForm((f) => ({ ...f, criticalInfo: e.target.value }))}
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
        <LoadingState message={t('patients.loading')} />
      ) : error ? null : records.length === 0 ? (
        <div className="ist-notice">{t('patients.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div className="ist-patient-list__head">
            <span>{t('patients.code')}</span>
            <span>{t('patients.name')}</span>
            <span>{t('patients.phone')}</span>
            <span>{t('patients.status')}</span>
          </div>
          {records.map((row) => (
            <div key={row.id} className="ist-patient-list__row">
              <Link to={`/patients/${row.id}`} className="ist-patient-list__id">
                {row.code ?? row.id}
              </Link>
              <div>
                <Link to={`/patients/${row.id}`} className="ist-patient-name">
                  {row.name}
                </Link>
              </div>
              <span className="ist-patient-list__phone">—</span>
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
