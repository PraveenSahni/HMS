import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import {
  fetchBeds,
  fetchEvaluations,
  fetchImaging,
  fetchMedications,
  fetchNursing,
  fetchProcedures,
  formatTrytonDate,
} from '../services/healthApi'
import { formatRpcError } from '../lib/tryton/client'

type ListFetcher = (client: ReturnType<typeof useAuth>['client']) => Promise<{
  records: Record<string, unknown>[]
  total: number
  available: boolean
}>

function ModuleListPage({
  titleKey,
  subtitleKey,
  emptyKey,
  missingKey,
  loadingKey,
  fetchData,
  columns,
}: {
  titleKey: string
  subtitleKey: string
  emptyKey: string
  missingKey: string
  loadingKey: string
  fetchData: ListFetcher
  columns: Array<{ key: string; labelKey: string; format?: (v: unknown, row: Record<string, unknown>) => string }>
}) {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchData(client)
      setRecords(result.records)
      setTotal(result.total)
      setAvailable(result.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, fetchData, t])

  useEffect(() => {
    load()
  }, [load])

  const gridCols = `repeat(${columns.length}, 1fr)`

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t(titleKey)}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t(subtitleKey)}</p>
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={load} />}

      {loading ? (
        <LoadingState message={t(loadingKey)} />
      ) : !available ? (
        <div className="ist-notice">{t(missingKey)}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t(emptyKey)}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
          </p>
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: gridCols }}>
              {columns.map((c) => (
                <span key={c.key}>{t(c.labelKey)}</span>
              ))}
            </div>
            {records.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: gridCols }}
              >
                {columns.map((c, i) => (
                  <span
                    key={c.key}
                    className={i === 0 ? 'ist-patient-name' : 'ist-subtitle'}
                  >
                    {c.format
                      ? c.format(row[c.key], row)
                      : String(row[c.key] ?? row.rec_name ?? '—')}
                  </span>
                ))}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export function EvaluationsPage() {
  return (
    <ModuleListPage
      titleKey="evaluations.title"
      subtitleKey="evaluations.subtitle"
      emptyKey="evaluations.empty"
      missingKey="evaluations.unavailable"
      loadingKey="evaluations.loading"
      fetchData={fetchEvaluations}
      columns={[
        { key: 'rec_name', labelKey: 'evaluations.name' },
        {
          key: 'evaluation_start',
          labelKey: 'evaluations.date',
          format: (v) => formatTrytonDate(v),
        },
        { key: 'state', labelKey: 'evaluations.state' },
        {
          key: 'chief_complaint',
          labelKey: 'evaluations.complaint',
          format: (v) => String(v ?? '—'),
        },
      ]}
    />
  )
}

export function MedicationsPage() {
  return (
    <ModuleListPage
      titleKey="medications.title"
      subtitleKey="medications.subtitle"
      emptyKey="medications.empty"
      missingKey="medications.unavailable"
      loadingKey="medications.loading"
      fetchData={fetchMedications}
      columns={[
        { key: 'rec_name', labelKey: 'medications.name' },
        { key: 'patient', labelKey: 'medications.patient', format: (v) => String(v ?? '—') },
        { key: 'healthprof', labelKey: 'medications.healthprof', format: (v) => String(v ?? '—') },
      ]}
    />
  )
}

export function BedsPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [beds, setBeds] = useState<Record<string, unknown>[]>([])
  const [admissions, setAdmissions] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [total, setTotal] = useState(0)
  const [admissionsTotal, setAdmissionsTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<'beds' | 'admissions'>('beds')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchBeds(client)
      setBeds(result.records)
      setAdmissions(result.admissions)
      setTotal(result.total)
      setAdmissionsTotal(result.admissionsTotal)
      setAvailable(result.available)
      if (result.admissionsTotal > 0 && result.total === 0) setTab('admissions')
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('beds.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('beds.subtitle')}</p>
        </div>
      </div>
      {error && <ErrorState message={error} onRetry={load} />}
      {loading ? (
        <LoadingState message={t('beds.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('beds.unavailable')}</div>
      ) : (
        <>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: 'var(--space-4)' }}>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'beds' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('beds')}>
              {t('beds.tabBeds')} ({total})
            </button>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'admissions' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('admissions')}>
              {t('beds.tabAdmissions')} ({admissionsTotal})
            </button>
          </div>
          {tab === 'beds' ? (
            beds.length === 0 ? (
              <div className="ist-notice">{t('beds.empty')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
                  <span>{t('beds.name')}</span>
                  <span>{t('beds.state')}</span>
                  <span>{t('beds.type')}</span>
                </div>
                {beds.map((row) => (
                  <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
                    <span className="ist-patient-name">{String(row.rec_name ?? '—')}</span>
                    <span className="ist-status">{String(row.state ?? '—')}</span>
                    <span className="ist-subtitle">{String(row.bed_type ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          ) : admissions.length === 0 ? (
            <div className="ist-notice">{t('beds.emptyAdmissions')}</div>
          ) : (
            <div className="ist-patient-list">
              <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                <span>{t('beds.admission')}</span>
                <span>{t('beds.patient')}</span>
                <span>{t('beds.admitted')}</span>
                <span>{t('beds.state')}</span>
              </div>
              {admissions.map((row) => (
                <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? row.id)}</span>
                  <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                  <span className="ist-subtitle">{formatTrytonDate(row.hospitalization_date)}</span>
                  <span className="ist-status">{String(row.state ?? '—')}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export function NursingPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [ambulatory, setAmbulatory] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<'rounds' | 'ambulatory'>('ambulatory')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchNursing(client)
      setRecords(result.records)
      setAmbulatory(result.ambulatory)
      setTotal(result.total)
      setAvailable(result.available)
      if (result.records.length && !result.ambulatory.length) setTab('rounds')
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('nursing.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('nursing.subtitle')}</p>
        </div>
      </div>
      {error && <ErrorState message={error} onRetry={load} />}
      {loading ? (
        <LoadingState message={t('nursing.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('nursing.moduleMissing')}</div>
      ) : (
        <>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: 'var(--space-4)' }}>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'ambulatory' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('ambulatory')}>
              {t('nursing.tabAmbulatory')} ({ambulatory.length})
            </button>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'rounds' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('rounds')}>
              {t('nursing.tabRounds')} ({total})
            </button>
          </div>
          {tab === 'ambulatory' ? (
            ambulatory.length === 0 ? (
              <div className="ist-notice">{t('nursing.empty')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span>{t('nursing.name')}</span>
                  <span>{t('nursing.patient')}</span>
                  <span>{t('nursing.started')}</span>
                  <span>{t('nursing.state')}</span>
                </div>
                {ambulatory.map((row) => (
                  <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                    <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? row.id)}</span>
                    <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                    <span className="ist-subtitle">{formatTrytonDate(row.session_start)}</span>
                    <span className="ist-status">{String(row.state ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          ) : records.length === 0 ? (
            <div className="ist-notice">{t('nursing.emptyRounds')}</div>
          ) : (
            <div className="ist-patient-list">
              <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1fr 100px' }}>
                <span>{t('nursing.name')}</span>
                <span>{t('nursing.started')}</span>
                <span>{t('nursing.state')}</span>
              </div>
              {records.map((row) => (
                <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1fr 100px' }}>
                  <span className="ist-patient-name">{String(row.rec_name ?? row.code ?? row.id)}</span>
                  <span className="ist-subtitle">{formatTrytonDate(row.evaluation_start)}</span>
                  <span className="ist-status">{String(row.state ?? '—')}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export function ProceduresPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [surgeries, setSurgeries] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<'procedures' | 'surgeries'>('procedures')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchProcedures(client)
      setRecords(result.records)
      setSurgeries(result.surgeries)
      setTotal(result.total)
      setAvailable(result.available)
      if (!result.records.length && result.surgeries.length) setTab('surgeries')
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('procedures.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('procedures.subtitle')}</p>
        </div>
      </div>
      {error && <ErrorState message={error} onRetry={load} />}
      {loading ? (
        <LoadingState message={t('procedures.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('procedures.moduleMissing')}</div>
      ) : (
        <>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: 'var(--space-4)' }}>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'procedures' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('procedures')}>
              {t('procedures.tabProcedures')} ({total})
            </button>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'surgeries' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('surgeries')}>
              {t('procedures.tabSurgeries')} ({surgeries.length})
            </button>
          </div>
          {tab === 'procedures' ? (
            records.length === 0 ? (
              <div className="ist-notice">{t('procedures.empty')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr' }}>
                  <span>{t('procedures.name')}</span>
                  <span>{t('procedures.patient')}</span>
                </div>
                {records.map((row) => (
                  <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr' }}>
                    <span className="ist-patient-name">{String(row.rec_name ?? row.name ?? row.id)}</span>
                    <span className="ist-subtitle">{row.patientName ?? String(row.patient ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          ) : surgeries.length === 0 ? (
            <div className="ist-notice">{t('procedures.emptySurgeries')}</div>
          ) : (
            <div className="ist-patient-list">
              <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                <span>{t('procedures.surgery')}</span>
                <span>{t('procedures.patient')}</span>
                <span>{t('procedures.date')}</span>
                <span>{t('procedures.state')}</span>
              </div>
              {surgeries.map((row) => (
                <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span className="ist-patient-name">{String(row.rec_name ?? row.code ?? row.id)}</span>
                  <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                  <span className="ist-subtitle">{formatTrytonDate(row.surgery_date)}</span>
                  <span className="ist-status">{String(row.state ?? '—')}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export function ImagingPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [requests, setRequests] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [results, setResults] = useState<Array<Record<string, unknown> & { patientName?: string }>>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<'requests' | 'results'>('requests')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchImaging(client)
      setRequests(result.records)
      setResults(result.results)
      setTotal(result.total)
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

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('imaging.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('imaging.subtitle')}</p>
        </div>
      </div>
      {error && <ErrorState message={error} onRetry={load} />}
      {loading ? (
        <LoadingState message={t('imaging.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('imaging.moduleMissing')}</div>
      ) : (
        <>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: 'var(--space-4)' }}>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'requests' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('requests')}>
              {t('imaging.tabRequests')} ({total})
            </button>
            <button type="button" className={`ist-btn ist-btn--sm ${tab === 'results' ? '' : 'ist-btn--outline'}`} onClick={() => setTab('results')}>
              {t('imaging.tabResults')} ({results.length})
            </button>
          </div>
          {tab === 'requests' ? (
            requests.length === 0 ? (
              <div className="ist-notice">{t('imaging.empty')}</div>
            ) : (
              <div className="ist-patient-list">
                <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                  <span>{t('imaging.name')}</span>
                  <span>{t('imaging.patient')}</span>
                  <span>{t('imaging.date')}</span>
                  <span>{t('imaging.state')}</span>
                </div>
                {requests.map((row) => (
                  <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr 1fr 100px' }}>
                    <span className="ist-patient-name">{String(row.rec_name ?? row.id)}</span>
                    <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                    <span className="ist-subtitle">{formatTrytonDate(row.date)}</span>
                    <span className="ist-status">{String(row.state ?? '—')}</span>
                  </div>
                ))}
              </div>
            )
          ) : results.length === 0 ? (
            <div className="ist-notice">{t('imaging.emptyResults')}</div>
          ) : (
            <div className="ist-patient-list">
              <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 1.2fr 1fr' }}>
                <span>{t('imaging.name')}</span>
                <span>{t('imaging.patient')}</span>
                <span>{t('imaging.date')}</span>
              </div>
              {results.map((row) => (
                <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr 1.2fr 1fr' }}>
                  <span className="ist-patient-name">{String(row.rec_name ?? row.number ?? row.id)}</span>
                  <span className="ist-subtitle">{row.patientName ?? '—'}</span>
                  <span className="ist-subtitle">{formatTrytonDate(row.date)}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
