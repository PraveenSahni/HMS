import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState, Select } from '../components/ui'
import {
  createLabRequest,
  fetchHealthProfOptions,
  fetchLaboratory,
  fetchLabTestTypeOptions,
  fetchPatientOptions,
  formatTrytonDate,
} from '../services/healthApi'
import { formatRpcError } from '../lib/tryton/client'

type Tab = 'orders' | 'results' | 'types'

function todayIso(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export function LaboratoryPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [tab, setTab] = useState<Tab>('orders')
  const [orders, setOrders] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [results, setResults] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [testTypes, setTestTypes] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [resultsTotal, setResultsTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [patients, setPatients] = useState<Array<{ id: number; label: string }>>([])
  const [doctors, setDoctors] = useState<Array<{ id: number; label: string }>>([])
  const [typeOptions, setTypeOptions] = useState<Array<{ id: number; label: string }>>([])
  const [form, setForm] = useState({
    patientId: '',
    doctorId: '',
    testTypeId: '',
    date: `${todayIso()}T09:00`,
    urgent: false,
  })

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchLaboratory(client)
      setOrders(result.records)
      setResults(result.results)
      setTestTypes(result.testTypes)
      setTotal(result.total)
      setResultsTotal(result.resultsTotal)
      setAvailable(result.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!showForm) return
    Promise.all([
      fetchPatientOptions(client),
      fetchHealthProfOptions(client),
      fetchLabTestTypeOptions(client),
    ])
      .then(([p, d, types]) => {
        setPatients(p)
        setDoctors(d)
        setTypeOptions(types)
      })
      .catch(() => {
        /* ignore option load errors — form still usable if empty */
      })
  }, [showForm, client])

  const openCreate = () => {
    setForm({
      patientId: '',
      doctorId: '',
      testTypeId: '',
      date: `${todayIso()}T09:00`,
      urgent: false,
    })
    setShowForm(true)
    setTab('orders')
  }

  const save = async () => {
    if (!form.patientId || !form.doctorId || !form.testTypeId) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      await createLabRequest(client, {
        patientId: Number(form.patientId),
        doctorId: Number(form.doctorId),
        testTypeId: Number(form.testTypeId),
        date: form.date,
        urgent: form.urgent,
      })
      setShowForm(false)
      setSuccess(t('laboratory.saveSuccess'))
      await load()
    } catch (err) {
      setError(formatRpcError(err, t('laboratory.saveError')))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('laboratory.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('laboratory.subtitle')}</p>
        </div>
        {available && (
          <button type="button" className="ist-btn ist-btn--primary" onClick={openCreate}>
            {t('laboratory.new')}
          </button>
        )}
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={load} />}

      {showForm && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('laboratory.createTitle')}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('laboratory.patient')}</div>
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
              <div className="ist-label">{t('laboratory.doctor')}</div>
              <Select
                value={form.doctorId}
                onChange={(e) => setForm((f) => ({ ...f, doctorId: e.target.value }))}
              >
                <option value="">{t('appointments.selectStaff')}</option>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>{d.label}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('laboratory.testType')}</div>
              <Select
                value={form.testTypeId}
                onChange={(e) => setForm((f) => ({ ...f, testTypeId: e.target.value }))}
              >
                <option value="">{t('laboratory.selectTestType')}</option>
                {typeOptions.map((tt) => (
                  <option key={tt.id} value={tt.id}>{tt.label}</option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('laboratory.date')}</div>
              <input
                type="datetime-local"
                className="ist-input ist-input--boxed"
                value={form.date}
                onChange={(e) => setForm((f) => ({ ...f, date: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('laboratory.urgent')}</div>
              <Select
                value={form.urgent ? '1' : '0'}
                onChange={(e) => setForm((f) => ({ ...f, urgent: e.target.value === '1' }))}
              >
                <option value="0">{t('common.no')}</option>
                <option value="1">{t('common.yes')}</option>
              </Select>
            </label>
          </div>
          <p className="ist-subtitle" style={{ marginTop: 'var(--space-3)' }}>
            {t('laboratory.wizardHint')}
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

      {loading ? (
        <LoadingState message={t('laboratory.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('laboratory.moduleMissing')}</div>
      ) : (
        <>
          <div className="ist-tabs" style={{ display: 'flex', gap: '0.5rem', marginBottom: 'var(--space-4)' }}>
            {(
              [
                ['orders', t('laboratory.tabOrders'), total],
                ['results', t('laboratory.tabResults'), resultsTotal],
                ['types', t('laboratory.tabTypes'), testTypes.length],
              ] as const
            ).map(([key, label, count]) => (
              <button
                key={key}
                type="button"
                className={`ist-btn ist-btn--sm ${tab === key ? '' : 'ist-btn--outline'}`}
                onClick={() => setTab(key)}
              >
                {label} ({count})
              </button>
            ))}
          </div>

          {tab === 'orders' && (
            orders.length === 0 ? (
              <div className="ist-notice">{t('laboratory.empty')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span>{t('laboratory.name')}</span>
                  <span>{t('laboratory.patient')}</span>
                  <span>{t('laboratory.date')}</span>
                  <span>{t('laboratory.state')}</span>
                </div>
                {orders.map((row) => (
                  <div
                    key={String(row.id)}
                    className="ist-patient-list__row"
                    style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}
                  >
                    <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? row.id)}</span>
                    <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                    <span className="ist-subtitle">{formatTrytonDate(row.date ?? row.date_requested)}</span>
                    <span className="ist-status">{String(row.state ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          )}

          {tab === 'results' && (
            results.length === 0 ? (
              <div className="ist-notice">{t('laboratory.emptyResults')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span>{t('laboratory.name')}</span>
                  <span>{t('laboratory.patient')}</span>
                  <span>{t('laboratory.date')}</span>
                  <span>{t('laboratory.state')}</span>
                </div>
                {results.map((row) => (
                  <div
                    key={String(row.id)}
                    className="ist-patient-list__row"
                    style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}
                  >
                    <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? row.id)}</span>
                    <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                    <span className="ist-subtitle">{formatTrytonDate(row.date_analysis ?? row.date)}</span>
                    <span className="ist-status">{String(row.state ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          )}

          {tab === 'types' && (
            testTypes.length === 0 ? (
              <div className="ist-notice">{t('laboratory.emptyTypes')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '120px 1fr' }}>
                  <span>{t('laboratory.code')}</span>
                  <span>{t('laboratory.testType')}</span>
                </div>
                {testTypes.map((row) => (
                  <div
                    key={String(row.id)}
                    className="ist-patient-list__row"
                    style={{ gridTemplateColumns: '120px 1fr' }}
                  >
                    <span className="ist-patient-list__id">{String(row.code ?? row.id)}</span>
                    <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          )}
        </>
      )}
    </div>
  )
}
