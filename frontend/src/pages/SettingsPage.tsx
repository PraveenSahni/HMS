import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import { fetchInstitution } from '../services/healthApi'
import type { InstitutionRecord } from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'
import { saoUrl, SAO_DIRECT_URL } from '../lib/sao'

export function SettingsPage() {
  const { t } = useTranslation()
  const { client, username, uid } = useAuth()
  const [institution, setInstitution] = useState<InstitutionRecord | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const company = import.meta.env.VITE_COMPANY_NAME ?? 'IST Technologies LLC'
  const city = import.meta.env.VITE_COMPANY_CITY ?? 'Doha'
  const country = import.meta.env.VITE_COMPANY_COUNTRY ?? 'Qatar'
  const url = import.meta.env.VITE_TRYTON_URL ?? 'https://health.irisstar.tech'
  const database = import.meta.env.VITE_TRYTON_DATABASE ?? 'isthealth'

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setInstitution(await fetchInstitution(client))
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
          <h1 className="ist-patients__title">{t('nav.settings')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('settings.subtitle')}</p>
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={load} />}
      {loading && <LoadingState message={t('common.loading')} />}

      <h3 style={{ marginBottom: 'var(--space-3)' }}>{t('settings.institution')}</h3>
      <hr className="ist-divider" />
      <div className="ist-grid ist-grid--2" style={{ marginTop: 'var(--space-4)', marginBottom: 'var(--space-9)' }}>
        <InfoCard
          label={t('settings.companyName')}
          value={institution?.rec_name ?? company}
        />
        <InfoCard label={t('settings.code')} value={institution?.code ?? 'IST'} />
        <InfoCard
          label={t('settings.type')}
          value={institution?.institution_type ?? 'clinic'}
        />
        <InfoCard
          label={t('settings.publicLevel')}
          value={institution?.public_level ?? '—'}
        />
        <InfoCard label={t('settings.city')} value={city} />
        <InfoCard label={t('settings.country')} value={country} />
        {institution?.extra_info && (
          <InfoCard label={t('settings.extraInfo')} value={institution.extra_info} />
        )}
      </div>

      <h3 style={{ marginBottom: 'var(--space-3)' }}>{t('settings.profile')}</h3>
      <hr className="ist-divider" />
      <div className="ist-grid ist-grid--2" style={{ marginTop: 'var(--space-4)', marginBottom: 'var(--space-9)' }}>
        <InfoCard label={t('settings.username')} value={username ?? '—'} />
        <InfoCard label={t('settings.userId')} value={uid != null ? String(uid) : '—'} />
      </div>

      <h3 style={{ marginBottom: 'var(--space-3)' }}>{t('settings.backend')}</h3>
      <hr className="ist-divider" />
      <div className="ist-grid ist-grid--2" style={{ marginTop: 'var(--space-4)' }}>
        <InfoCard label={t('settings.serverUrl')} value={url} />
        <InfoCard label={t('settings.database')} value={database} />
        <InfoCard label={t('settings.saoFallback')} value={saoUrl()} />
        <InfoCard label={t('settings.saoDirect')} value={SAO_DIRECT_URL} />
      </div>
    </div>
  )
}

function InfoCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-4)' }}>
      <div className="ist-label">{label}</div>
      <div className="ist-card__value" style={{ marginTop: 'var(--space-2)' }}>{value}</div>
    </div>
  )
}
