import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import { fetchPharmacy, formatTrytonDate } from '../services/healthApi'
import { formatRpcError } from '../lib/tryton/client'

export function PharmacyPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [tab, setTab] = useState<'rx' | 'products' | 'medicaments'>('products')
  const [prescriptions, setPrescriptions] = useState<Record<string, unknown>[]>([])
  const [products, setProducts] = useState<Record<string, unknown>[]>([])
  const [medicaments, setMedicaments] = useState<Record<string, unknown>[]>([])
  const [rxTotal, setRxTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [available, setAvailable] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchPharmacy(client)
      setPrescriptions(result.prescriptions)
      setProducts(result.products)
      setMedicaments(result.medicaments)
      setRxTotal(result.prescriptionTotal)
      setAvailable(result.available)
      if (result.products.length) setTab('products')
      else if (result.prescriptions.length) setTab('rx')
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
          <h1 className="ist-patients__title">{t('pharmacy.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('pharmacy.subtitle')}</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 'var(--space-3)', marginBottom: 'var(--space-6)', flexWrap: 'wrap' }}>
        <button
          type="button"
          className={`ist-btn ist-btn--sm${tab === 'products' ? ' ist-btn--primary' : ' ist-btn--outline'}`}
          onClick={() => setTab('products')}
        >
          {t('pharmacy.tabProducts')} ({products.length})
        </button>
        <button
          type="button"
          className={`ist-btn ist-btn--sm${tab === 'rx' ? ' ist-btn--primary' : ' ist-btn--outline'}`}
          onClick={() => setTab('rx')}
        >
          {t('pharmacy.tabRx')} ({rxTotal})
        </button>
        <button
          type="button"
          className={`ist-btn ist-btn--sm${tab === 'medicaments' ? ' ist-btn--primary' : ' ist-btn--outline'}`}
          onClick={() => setTab('medicaments')}
        >
          {t('pharmacy.tabMeds')} ({medicaments.length})
        </button>
      </div>

      {error && <ErrorState message={error} onRetry={load} />}

      {loading ? (
        <LoadingState message={t('pharmacy.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('pharmacy.unavailable')}</div>
      ) : tab === 'products' ? (
        products.length === 0 ? (
          <div className="ist-notice">{t('pharmacy.emptyProducts')}</div>
        ) : (
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: '120px 1fr 100px 100px' }}>
              <span>{t('pharmacy.code')}</span>
              <span>{t('pharmacy.product')}</span>
              <span>{t('pharmacy.type')}</span>
              <span>{t('pharmacy.status')}</span>
            </div>
            {products.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '120px 1fr 100px 100px' }}
              >
                <span className="ist-patient-list__id">{String(row.code ?? row.id)}</span>
                <span className="ist-patient-name">{String(row.name ?? row.rec_name ?? '—')}</span>
                <span className="ist-subtitle">{String(row.type ?? '—')}</span>
                <span className={`ist-status${row.active !== false ? ' ist-status--completed' : ''}`}>
                  {row.active !== false ? t('patients.active') : t('patients.inactive')}
                </span>
              </div>
            ))}
          </div>
        )
      ) : tab === 'rx' ? (
        prescriptions.length === 0 ? (
          <div className="ist-notice">{t('pharmacy.emptyRx')}</div>
        ) : (
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: '140px 1fr 120px' }}>
              <span>{t('pharmacy.date')}</span>
              <span>{t('pharmacy.prescription')}</span>
              <span>{t('pharmacy.state')}</span>
            </div>
            {prescriptions.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '140px 1fr 120px' }}
              >
                <span className="ist-patient-list__date">{formatTrytonDate(row.prescription_date)}</span>
                <span className="ist-patient-name">{String(row.rec_name ?? row.prescription_id ?? row.id)}</span>
                <span className="ist-status">{String(row.state ?? '—')}</span>
              </div>
            ))}
          </div>
        )
      ) : medicaments.length === 0 ? (
        <div className="ist-notice">{t('pharmacy.emptyMeds')}</div>
      ) : (
        <div className="ist-patient-list">
          {medicaments.map((row) => (
            <div key={String(row.id)} className="ist-patient-list__row" style={{ gridTemplateColumns: '1fr' }}>
              <span className="ist-patient-name">{String(row.rec_name ?? row.id)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
