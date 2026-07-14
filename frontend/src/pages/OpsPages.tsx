import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import {
  fetchCalendarData,
  fetchCurrencies,
  fetchParties,
  fetchProductVariants,
  fetchStock,
  formatTrytonDate,
} from '../services/healthApi'
import { formatRpcError } from '../lib/tryton/client'

// Admin Gap 4 pages live in AdminPages.tsx
export {
  CompaniesPage,
  CountriesPage,
  FinancialPage,
  GroupsPage,
  LanguagesPage,
  ModulesPage,
  SequencesPage,
  UsersPage,
} from './AdminPages'

type Col = {
  key: string
  labelKey: string
  format?: (v: unknown, row: Record<string, unknown>) => string
}

function cell(row: Record<string, unknown>, c: Col): string {
  if (c.format) return c.format(row[c.key], row)
  const v = row[c.key] ?? row.rec_name ?? row.name
  return v == null || v === '' ? '—' : String(v)
}

function OpsListPage({
  titleKey,
  subtitleKey,
  emptyKey,
  missingKey,
  loadingKey,
  load,
  columns,
  searchPlaceholder,
}: {
  titleKey: string
  subtitleKey: string
  emptyKey: string
  missingKey: string
  loadingKey: string
  load: (
    client: ReturnType<typeof useAuth>['client'],
    search: string,
  ) => Promise<{ records: Record<string, unknown>[]; total: number; available: boolean }>
  columns: Col[]
  searchPlaceholder?: string
}) {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await load(client, debounced)
      setRecords(result.records)
      setTotal(result.total)
      setAvailable(result.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, load, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const gridCols = `repeat(${columns.length}, minmax(0, 1fr))`

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

      {searchPlaceholder && (
        <div className="ist-split" style={{ marginBottom: 'var(--space-8)' }}>
          <div className="ist-search">
            <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              type="search"
              placeholder={t(searchPlaceholder)}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <span className="ist-subtitle">{t('common.recordCount', { count: total })}</span>
        </div>
      )}

      {error && <ErrorState message={error} onRetry={refresh} />}

      {loading && !records.length ? (
        <LoadingState message={t(loadingKey)} />
      ) : !available ? (
        <div className="ist-notice">{t(missingKey)}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t(emptyKey)}</div>
      ) : (
        <>
          {!searchPlaceholder && (
            <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
              {t('common.recordCount', { count: total })}
            </p>
          )}
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
                  <span key={c.key} className={i === 0 ? 'ist-patient-name' : 'ist-subtitle'}>
                    {cell(row, c)}
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

function TabbedOpsPage({
  titleKey,
  subtitleKey,
  tabs,
}: {
  titleKey: string
  subtitleKey: string
  tabs: Array<{
    key: string
    labelKey: string
    emptyKey: string
    columns: Col[]
    rows: Record<string, unknown>[]
  }>
}) {
  const { t } = useTranslation()
  const [tab, setTab] = useState(tabs[0]?.key ?? '')
  const active = tabs.find((x) => x.key === tab) ?? tabs[0]
  const gridCols = active ? `repeat(${active.columns.length}, minmax(0, 1fr))` : '1fr'

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
      <div className="ist-tabs" style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        {tabs.map((x) => (
          <button
            key={x.key}
            type="button"
            className={`ist-btn ist-btn--sm${tab === x.key ? ' ist-btn--primary' : ' ist-btn--outline'}`}
            onClick={() => setTab(x.key)}
          >
            {t(x.labelKey)}
          </button>
        ))}
      </div>
      {!active || active.rows.length === 0 ? (
        <div className="ist-notice">{t(active?.emptyKey ?? 'common.error')}</div>
      ) : (
        <div className="ist-patient-list">
          <div className="ist-patient-list__head" style={{ gridTemplateColumns: gridCols }}>
            {active.columns.map((c) => (
              <span key={c.key}>{t(c.labelKey)}</span>
            ))}
          </div>
          {active.rows.map((row) => (
            <div
              key={String(row.id)}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: gridCols }}
            >
              {active.columns.map((c, i) => (
                <span key={c.key} className={i === 0 ? 'ist-patient-name' : 'ist-subtitle'}>
                  {cell(row, c)}
                </span>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export function PartiesPage() {
  return (
    <OpsListPage
      titleKey="ops.parties.title"
      subtitleKey="ops.parties.subtitle"
      emptyKey="ops.parties.empty"
      missingKey="ops.parties.missing"
      loadingKey="ops.parties.loading"
      searchPlaceholder="ops.parties.search"
      columns={[
        { key: 'code', labelKey: 'ops.parties.code' },
        { key: 'name', labelKey: 'ops.parties.name' },
        {
          key: 'is_patient',
          labelKey: 'ops.parties.flags',
          format: (_v, row) => {
            const flags = []
            if (row.is_patient) flags.push('Patient')
            if (row.is_healthprof) flags.push('HP')
            return flags.length ? flags.join(', ') : '—'
          },
        },
        {
          key: 'active',
          labelKey: 'ops.parties.status',
          format: (v) => (v === false ? 'Inactive' : 'Active'),
        },
      ]}
      load={async (client, search) => {
        const r = await fetchParties(client, search)
        return { records: r.records as unknown as Record<string, unknown>[], total: r.total, available: r.available }
      }}
    />
  )
}

export function ProductsPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [available, setAvailable] = useState(true)
  const [templates, setTemplates] = useState<Record<string, unknown>[]>([])
  const [variants, setVariants] = useState<Record<string, unknown>[]>([])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchProductVariants(client)
      setTemplates(r.templates)
      setVariants(r.variants)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  if (loading) return <LoadingState message={t('ops.products.loading')} />
  if (error) return <ErrorState message={error} onRetry={refresh} />
  if (!available) return <div className="ist-notice">{t('ops.products.missing')}</div>

  return (
    <TabbedOpsPage
      titleKey="ops.products.title"
      subtitleKey="ops.products.subtitle"
      tabs={[
        {
          key: 'templates',
          labelKey: 'ops.products.tabTemplates',
          emptyKey: 'ops.products.emptyTemplates',
          rows: templates,
          columns: [
            { key: 'name', labelKey: 'ops.products.name' },
            { key: 'code', labelKey: 'ops.products.code' },
            { key: 'type', labelKey: 'ops.products.type' },
            { key: 'list_price', labelKey: 'ops.products.price' },
          ],
        },
        {
          key: 'variants',
          labelKey: 'ops.products.tabVariants',
          emptyKey: 'ops.products.emptyVariants',
          rows: variants,
          columns: [
            { key: 'rec_name', labelKey: 'ops.products.name' },
            { key: 'code', labelKey: 'ops.products.code' },
            { key: 'type', labelKey: 'ops.products.type' },
            { key: 'list_price', labelKey: 'ops.products.price' },
          ],
        },
      ]}
    />
  )
}

export function StockPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [available, setAvailable] = useState(true)
  const [locations, setLocations] = useState<Record<string, unknown>[]>([])
  const [moves, setMoves] = useState<Record<string, unknown>[]>([])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchStock(client)
      setLocations(r.locations)
      setMoves(r.moves)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  if (loading) return <LoadingState message={t('ops.stock.loading')} />
  if (error) return <ErrorState message={error} onRetry={refresh} />
  if (!available) return <div className="ist-notice">{t('ops.stock.missing')}</div>

  return (
    <TabbedOpsPage
      titleKey="ops.stock.title"
      subtitleKey="ops.stock.subtitle"
      tabs={[
        {
          key: 'locations',
          labelKey: 'ops.stock.tabLocations',
          emptyKey: 'ops.stock.emptyLocations',
          rows: locations,
          columns: [
            { key: 'rec_name', labelKey: 'ops.stock.location' },
            { key: 'code', labelKey: 'ops.stock.code' },
            { key: 'type', labelKey: 'ops.stock.type' },
          ],
        },
        {
          key: 'moves',
          labelKey: 'ops.stock.tabMoves',
          emptyKey: 'ops.stock.emptyMoves',
          rows: moves,
          columns: [
            { key: 'rec_name', labelKey: 'ops.stock.move' },
            { key: 'quantity', labelKey: 'ops.stock.qty' },
            { key: 'state', labelKey: 'ops.stock.state' },
          ],
        },
      ]}
    />
  )
}

export function CurrencyPage() {
  return (
    <OpsListPage
      titleKey="ops.currency.title"
      subtitleKey="ops.currency.subtitle"
      emptyKey="ops.currency.empty"
      missingKey="ops.currency.missing"
      loadingKey="ops.currency.loading"
      columns={[
        { key: 'code', labelKey: 'ops.currency.code' },
        { key: 'name', labelKey: 'ops.currency.name' },
        { key: 'symbol', labelKey: 'ops.currency.symbol' },
        {
          key: 'active',
          labelKey: 'ops.currency.status',
          format: (v) => (v === false ? 'Inactive' : 'Active'),
        },
      ]}
      load={async (client) => fetchCurrencies(client)}
    />
  )
}

export function CalendarPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [available, setAvailable] = useState(true)
  const [calendars, setCalendars] = useState<Record<string, unknown>[]>([])
  const [events, setEvents] = useState<Record<string, unknown>[]>([])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchCalendarData(client)
      setCalendars(r.calendars)
      setEvents(r.events)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  if (loading) return <LoadingState message={t('ops.calendar.loading')} />
  if (error) return <ErrorState message={error} onRetry={refresh} />
  if (!available) return <div className="ist-notice">{t('ops.calendar.missing')}</div>

  return (
    <TabbedOpsPage
      titleKey="ops.calendar.title"
      subtitleKey="ops.calendar.subtitle"
      tabs={[
        {
          key: 'calendars',
          labelKey: 'ops.calendar.tabCalendars',
          emptyKey: 'ops.calendar.emptyCalendars',
          rows: calendars,
          columns: [
            { key: 'name', labelKey: 'ops.calendar.name' },
            { key: 'description', labelKey: 'ops.calendar.description' },
          ],
        },
        {
          key: 'events',
          labelKey: 'ops.calendar.tabEvents',
          emptyKey: 'ops.calendar.emptyEvents',
          rows: events,
          columns: [
            { key: 'summary', labelKey: 'ops.calendar.summary' },
            {
              key: 'dtstart',
              labelKey: 'ops.calendar.start',
              format: (v) => formatTrytonDate(v),
            },
            { key: 'status', labelKey: 'ops.calendar.status' },
          ],
        },
      ]}
    />
  )
}
