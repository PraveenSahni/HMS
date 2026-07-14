import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import {
  contextualHelp,
  loadHelpArticle,
  loadHelpIndex,
  searchHelp,
  type HelpArticle,
  type HelpIndexEntry,
} from '../../help/helpService'

const ROLES = [
  '*',
  'SystemAdmin',
  'FacilityAdmin',
  'Physician',
  'Nurse',
  'Receptionist',
  'LabTech',
  'Pharmacist',
  'Billing',
  'Compliance',
  'Executive',
]

const COUNTRIES = ['*', 'AE', 'QA']

function useHelpPrefs() {
  const [role, setRole] = useState(() => localStorage.getItem('ist-help-role') || '*')
  const [country, setCountry] = useState(() => localStorage.getItem('ist-help-country') || '*')
  useEffect(() => {
    localStorage.setItem('ist-help-role', role)
  }, [role])
  useEffect(() => {
    localStorage.setItem('ist-help-country', country)
  }, [country])
  return { role, setRole, country, setCountry }
}

export function HelpCentrePage() {
  const { i18n, t } = useTranslation()
  const lang = (i18n.language?.startsWith('ar') ? 'ar' : 'en') as 'en' | 'ar'
  const { role, setRole, country, setCountry } = useHelpPrefs()
  const [index, setIndex] = useState<HelpIndexEntry[]>([])
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<HelpArticle | null>(null)
  const [error, setError] = useState<string | null>(null)
  const location = useLocation()

  useEffect(() => {
    let cancelled = false
    loadHelpIndex(lang)
      .then((data) => {
        if (!cancelled) setIndex(data)
      })
      .catch((e) => {
        if (!cancelled) setError(String(e))
      })
    return () => {
      cancelled = true
    }
  }, [lang])

  const results = useMemo(
    () => searchHelp(index, query, { role, country }),
    [index, query, role, country],
  )

  const contextual = useMemo(
    () => contextualHelp(index, { role, country, route: location.pathname }),
    [index, role, country, location.pathname],
  )

  const openArticle = async (id: string) => {
    setError(null)
    try {
      const article = await loadHelpArticle(id, lang)
      setSelected(article)
    } catch (e) {
      setError(String(e))
    }
  }

  return (
    <div className="ist-page" data-testid="help-centre">
      <header className="ist-page__header">
        <h1>{t('help.title', { defaultValue: 'Help Centre' })}</h1>
        <p className="ist-muted">
          {t('help.subtitle', {
            defaultValue: 'Search topics, filter by role and country, follow guided workflows.',
          })}
        </p>
      </header>

      <div className="ist-help-toolbar" style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        <input
          type="search"
          placeholder={t('help.search', { defaultValue: 'Search help…' })}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          data-testid="help-search"
          className="ist-input"
          style={{ minWidth: '220px', flex: 1 }}
        />
        <label>
          {t('help.role', { defaultValue: 'Role' })}{' '}
          <select value={role} onChange={(e) => setRole(e.target.value)} data-testid="help-role">
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t('help.country', { defaultValue: 'Country' })}{' '}
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            data-testid="help-country"
          >
            {COUNTRIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p className="ist-error">{error}</p>}

      {contextual.length > 0 && (
        <section className="ist-help-section">
          <h2>{t('help.contextual', { defaultValue: 'On this page' })}</h2>
          <ul className="ist-help-topics">
            {contextual.map((e) => (
              <li key={e.id} className="ist-help-topics__item">
                <button
                  type="button"
                  className={`ist-help-topic${selected?.id === e.id ? ' is-selected' : ''}`}
                  onClick={() => openArticle(e.id)}
                >
                  {e.guided ? (
                    <span className="ist-help-topic__icon" aria-hidden="true" />
                  ) : (
                    <span className="ist-help-topic__icon ist-help-topic__icon--empty" aria-hidden="true" />
                  )}
                  <span className="ist-help-topic__label">{e.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="ist-help-layout">
        <aside>
          <h2>{t('help.topics', { defaultValue: 'Topics' })}</h2>
          <ul className="ist-help-topics" data-testid="help-results">
            {results.map((e) => (
              <li key={e.id} className="ist-help-topics__item">
                <button
                  type="button"
                  className={`ist-help-topic${selected?.id === e.id ? ' is-selected' : ''}`}
                  onClick={() => openArticle(e.id)}
                >
                  {e.guided ? (
                    <span className="ist-help-topic__icon" aria-hidden="true" />
                  ) : (
                    <span className="ist-help-topic__icon ist-help-topic__icon--empty" aria-hidden="true" />
                  )}
                  <span className="ist-help-topic__label">{e.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </aside>
        <article data-testid="help-article">
          {selected ? (
            <>
              <h2>{selected.title}</h2>
              <p className="ist-muted">
                v{selected.version} · {selected.countries.join(', ')} · {selected.roles.join(', ')}
              </p>
              <p>{selected.body}</p>
              {selected.steps && selected.steps.length > 0 && (
                <ol>
                  {selected.steps.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ol>
              )}
              {selected.routes[0] && selected.routes[0] !== '/help' && (
                <p>
                  <Link to={selected.routes[0]}>
                    {t('help.openRoute', { defaultValue: 'Open related screen' })}
                  </Link>
                </p>
              )}
            </>
          ) : (
            <p>{t('help.selectTopic', { defaultValue: 'Select a topic to read.' })}</p>
          )}
        </article>
      </div>
    </div>
  )
}

/** Compact contextual panel for embedding in layout */
export function ContextualHelpButton() {
  const location = useLocation()
  const { i18n, t } = useTranslation()
  const lang = (i18n.language?.startsWith('ar') ? 'ar' : 'en') as 'en' | 'ar'
  const role = localStorage.getItem('ist-help-role') || '*'
  const country = localStorage.getItem('ist-help-country') || '*'
  const [count, setCount] = useState(0)

  useEffect(() => {
    loadHelpIndex(lang)
      .then((idx) =>
        setCount(contextualHelp(idx, { role, country, route: location.pathname }).length),
      )
      .catch(() => setCount(0))
  }, [lang, role, country, location.pathname])

  const label = t('nav.help', { defaultValue: 'Help' })
  const title = t('help.title', { defaultValue: 'Help Centre' })

  return (
    <Link
      to="/help"
      className="ist-btn ist-btn--outline ist-btn--sm ist-help-launcher"
      title={title}
      aria-label={count > 0 ? `${title} (${count})` : title}
      data-testid="help-launcher"
    >
      <span className="ist-help-launcher__icon" aria-hidden="true">
        ?
      </span>
      <span className="ist-help-launcher__label">{label}</span>
      {count > 0 ? (
        <span className="ist-help-launcher__badge" data-testid="help-contextual-count">
          {count}
        </span>
      ) : null}
    </Link>
  )
}
