import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import {
  contextualHelp,
  getFeedback,
  getOnboardingState,
  loadHelpArticle,
  loadHelpIndex,
  ONBOARDING_ITEMS,
  searchHelp,
  setFeedback,
  setOnboardingItem,
  type HelpArticle,
  type HelpIndexEntry,
} from '../../help/helpService'

const ROLES = [
  '*',
  'GroupAdmin',
  'CountryAdmin',
  'FacilityAdmin',
  'SystemAdmin',
  'Receptionist',
  'CallCentre',
  'Nurse',
  'TriageNurse',
  'Physician',
  'Surgeon',
  'LabTech',
  'LabSupervisor',
  'ImagingTech',
  'Radiologist',
  'Pharmacist',
  'PharmacyAssistant',
  'Cashier',
  'Billing',
  'InsuranceClaims',
  'Finance',
  'Procurement',
  'Warehouse',
  'HR',
  'DeptManager',
  'Executive',
  'ITSupport',
  'Auditor',
  'Compliance',
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
  const [feedback, setFeedbackState] = useState<'yes' | 'no' | null>(null)
  const [onboarding, setOnboarding] = useState<Record<string, boolean>>(() => getOnboardingState())
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

  const guidedCount = useMemo(() => results.filter((e) => e.guided).length, [results])

  const openArticle = async (id: string) => {
    setError(null)
    try {
      const article = await loadHelpArticle(id, lang)
      setSelected(article)
      setFeedbackState(getFeedback(id))
    } catch (e) {
      setError(String(e))
    }
  }

  const onFeedback = (value: 'yes' | 'no') => {
    if (!selected) return
    setFeedback(selected.id, value)
    setFeedbackState(value)
  }

  const toggleOnboarding = (id: string) => {
    const next = !onboarding[id]
    setOnboardingItem(id, next)
    setOnboarding({ ...onboarding, [id]: next })
  }

  const onboardingDone = ONBOARDING_ITEMS.filter((i) => onboarding[i.id]).length

  return (
    <div className="ist-page" data-testid="help-centre">
      <header className="ist-page__header">
        <h1>{t('help.title', { defaultValue: 'Help Centre' })}</h1>
        <p className="ist-muted">
          {t('help.subtitle', {
            defaultValue: 'Search topics, filter by role and country, follow guided workflows.',
          })}
        </p>
        <p className="ist-muted" data-testid="help-guided-count">
          {t('help.guidedAvailable', {
            defaultValue: '{{count}} guided workflows in view',
            count: guidedCount,
          })}
          {' · '}
          <Link to="/help/admin">{t('help.adminLink', { defaultValue: 'Help admin' })}</Link>
        </p>
      </header>

      <section className="ist-help-section" data-testid="help-onboarding">
        <h2>
          {t('help.onboarding', { defaultValue: 'Onboarding checklist' })} ({onboardingDone}/
          {ONBOARDING_ITEMS.length})
        </h2>
        <ul className="ist-help-topics">
          {ONBOARDING_ITEMS.map((item) => (
            <li key={item.id} className="ist-help-topics__item">
              <label className="ist-help-topic" style={{ cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={!!onboarding[item.id]}
                  onChange={() => toggleOnboarding(item.id)}
                  data-testid={`onboarding-${item.id}`}
                />
                <span className="ist-help-topic__label">
                  {lang === 'ar' ? item.label_ar : item.label_en}
                </span>
              </label>
            </li>
          ))}
        </ul>
      </section>

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
              <div className="ist-help-feedback" data-testid="help-feedback" style={{ marginTop: '1.25rem' }}>
                <p>{t('help.wasHelpful', { defaultValue: 'Was this helpful?' })}</p>
                <button
                  type="button"
                  className="ist-btn ist-btn--outline ist-btn--sm"
                  aria-pressed={feedback === 'yes'}
                  onClick={() => onFeedback('yes')}
                  data-testid="help-feedback-yes"
                >
                  {t('help.yes', { defaultValue: 'Yes' })}
                </button>{' '}
                <button
                  type="button"
                  className="ist-btn ist-btn--outline ist-btn--sm"
                  aria-pressed={feedback === 'no'}
                  onClick={() => onFeedback('no')}
                  data-testid="help-feedback-no"
                >
                  {t('help.no', { defaultValue: 'No' })}
                </button>
                {feedback && (
                  <span className="ist-muted" style={{ marginInlineStart: '0.5rem' }}>
                    {t('help.thanksFeedback', { defaultValue: 'Thanks for your feedback.' })}
                  </span>
                )}
              </div>
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
