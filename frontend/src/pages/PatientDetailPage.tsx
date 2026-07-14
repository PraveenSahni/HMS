import { useCallback, useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { Badge, Card, ErrorState, LoadingState, Select } from '../components/ui'
import { fetchPatientById, formatTrytonDate, updatePatient } from '../services/healthApi'
import {
  BLOOD_TYPES,
  trytonDateToDateInput,
  type PartyRecord,
  type PatientRecord,
} from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'

export function PatientDetailPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const { t } = useTranslation()
  const { client } = useAuth()
  const [party, setParty] = useState<PartyRecord | null>(null)
  const [patient, setPatient] = useState<PatientRecord | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(
    (location.state as { success?: string } | null)?.success ?? null,
  )
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({
    name: '',
    code: '',
    gender: '',
    dob: '',
    bloodType: '',
    lastname: '',
    criticalInfo: '',
    active: true,
  })

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError(null)
    try {
      const result = await fetchPatientById(client, Number(id))
      setParty(result.party)
      setPatient(result.patient)
      setForm({
        name: result.party.name ?? '',
        code: result.party.code ?? '',
        gender: String(result.patient?.gender ?? ''),
        dob: trytonDateToDateInput(result.patient?.dob),
        bloodType: String(result.patient?.blood_type ?? ''),
        lastname: String(result.patient?.lastname ?? ''),
        criticalInfo: String(result.patient?.critical_info ?? ''),
        active: result.party.active !== false,
      })
    } catch (err) {
      setError(formatRpcError(err, t('patients.notFound')))
    } finally {
      setLoading(false)
    }
  }, [client, id, t])

  useEffect(() => {
    load()
  }, [load])

  const save = async () => {
    if (!party || !form.name.trim()) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      await updatePatient(client, {
        partyId: party.id,
        patientId: patient?.id ?? null,
        data: {
          name: form.name,
          code: form.code || undefined,
          gender: form.gender || undefined,
          dob: form.dob || undefined,
          bloodType: form.bloodType || undefined,
          lastname: form.lastname,
          criticalInfo: form.criticalInfo,
          active: form.active,
        },
      })
      setEditing(false)
      setSuccess(t('patients.updateSuccess'))
      await load()
    } catch (err) {
      setError(formatRpcError(err, t('patients.saveError')))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingState message={t('common.loading')} />
  if ((error && !party) || !party) return <ErrorState message={error ?? t('patients.notFound')} />

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <Link to="/patients" className="ist-link" style={{ display: 'inline-block', marginBottom: 'var(--space-3)' }}>
            ← {t('patients.back')}
          </Link>
          <p className="ist-tagline">{t('patients.detail')}</p>
          <h1 className="ist-patients__title">{party.name}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle ist-id">{party.code ?? String(party.id)}</p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
          <Badge variant={party.active !== false ? 'success' : 'default'}>
            {party.active !== false ? t('patients.active') : t('patients.inactive')}
          </Badge>
          {!editing && (
            <button type="button" className="ist-btn ist-btn--primary" onClick={() => setEditing(true)}>
              {t('common.edit')}
            </button>
          )}
        </div>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={load} />}

      {editing ? (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('patients.editTitle')}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('patients.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
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
            <label>
              <div className="ist-label">{t('patients.status')}</div>
              <Select
                value={form.active ? '1' : '0'}
                onChange={(e) => setForm((f) => ({ ...f, active: e.target.value === '1' }))}
              >
                <option value="1">{t('patients.active')}</option>
                <option value="0">{t('patients.inactive')}</option>
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
            <button
              type="button"
              className="ist-btn ist-btn--outline"
              onClick={() => {
                setEditing(false)
                setError(null)
              }}
            >
              {t('common.cancel')}
            </button>
          </div>
        </div>
      ) : (
        <Card>
          <div className="ist-grid ist-grid--2" style={{ padding: 'var(--space-6)' }}>
            <Field label={t('patients.code')} value={party.code ?? String(party.id)} />
            <Field label={t('patients.name')} value={party.name} />
            {patient?.puid != null && <Field label="PUID" value={String(patient.puid)} />}
            {patient?.dob != null && <Field label={t('patients.dob')} value={formatTrytonDate(patient.dob)} />}
            {patient?.age != null && <Field label={t('patients.age')} value={String(patient.age)} />}
            {patient?.gender != null && (
              <Field
                label={t('patients.gender')}
                value={
                  patient.gender === 'm'
                    ? t('patients.genderM')
                    : patient.gender === 'f'
                      ? t('patients.genderF')
                      : String(patient.gender)
                }
              />
            )}
            {patient?.blood_type != null && (
              <Field label={t('patients.bloodType')} value={String(patient.blood_type)} />
            )}
            {patient?.lastname != null && (
              <Field label={t('patients.lastname')} value={String(patient.lastname)} />
            )}
            {patient?.critical_info != null && String(patient.critical_info) && (
              <div style={{ gridColumn: '1 / -1' }}>
                <Field label={t('patients.criticalInfo')} value={String(patient.critical_info)} />
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
