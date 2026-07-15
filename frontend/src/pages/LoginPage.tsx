import { type FormEvent, useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { Logo } from '../components/common/Logo'
import { LangSwitch } from '../components/common/LangSwitch'
import { ThemeSwitch } from '../components/common/ThemeSwitch'

export function LoginPage() {
  const { t } = useTranslation()
  const {
    login,
    isAuthenticated,
    error,
    clearError,
    database,
    setDatabase,
    listDatabases,
  } = useAuth()

  const [username, setUsername] = useState(import.meta.env.VITE_TRYTON_USERNAME ?? 'admin')
  const [password, setPassword] = useState(import.meta.env.VITE_TRYTON_PASSWORD ?? '')
  const [databases, setDatabases] = useState<string[]>([database])
  const [pickerOpen, setPickerOpen] = useState(false)
  const [dbLoading, setDbLoading] = useState(true)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setDbLoading(true)
      try {
        const list = await listDatabases()
        if (cancelled) return
        setDatabases((prev) => {
          const current = database
          const merged = list.includes(current) ? list : [current, ...list.filter((d) => d !== current)]
          return merged.length ? merged : prev
        })
      } finally {
        if (!cancelled) setDbLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
    // Load once on mount — selected DB is managed separately via setDatabase
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [listDatabases])

  if (isAuthenticated) return <Navigate to="/workspace" replace />

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    clearError()
    setLoading(true)
    try {
      await login(username, password, database)
    } catch {
      /* error set in context */
    } finally {
      setLoading(false)
    }
  }

  const selectDatabase = (name: string) => {
    setDatabase(name)
    setPickerOpen(false)
  }

  const multiple = databases.length > 1

  return (
    <div className="ist-app">
      <header className="ist-header">
        <div className="ist-header__start">
          <Logo variant="compact" to="/login" />
        </div>
        <div className="ist-header__end">
          <LangSwitch />
          <div className="ist-header__divider" />
          <ThemeSwitch />
        </div>
      </header>

      <div className="ist-login-page">
        <div className="ist-login-card">
          <header className="ist-login-card__header">
            <div className="ist-login-card__brand">
              <Logo variant="compact" />
              <span>{t('auth.loginHeaderBrand')}</span>
            </div>
            <p className="ist-login-card__continue">
              <span>{t('auth.loginContinue')}</span>
              <a href="/">{t('app.name')}</a>
            </p>
          </header>

          <div className="ist-login-card__body">
            <div className="ist-login-card__inspire">
              <Logo variant="lg" />
              <p className="ist-tagline">{t('auth.loginTagline')}</p>
              <h2 className="ist-login-card__inspire-title">{t('auth.loginInspireTitle')}</h2>
              <ul className="ist-login-features">
                <li>{t('auth.loginFeature1')}</li>
                <li>{t('auth.loginFeature2')}</li>
                <li>{t('auth.loginFeature3')}</li>
                <li>{t('auth.loginFeature4')}</li>
              </ul>
              <span className="ist-login-card__watermark" aria-hidden="true">
                IST
              </span>
            </div>

            <div className="ist-login-card__divider-v" aria-hidden="true" />

            <div className="ist-login-card__form-col">
              <h2 className="ist-login-card__form-title">{t('auth.loginFormTitle')}</h2>
              <form className="ist-login-form" onSubmit={handleSubmit}>
                {error && (
                  <div className="ist-notice ist-notice--error" role="alert">
                    <strong>
                      {error === 'connection'
                        ? t('auth.connectionError')
                        : error === 'invalid'
                          ? t('auth.invalidCredentials')
                          : error}
                    </strong>
                  </div>
                )}

                <div className="ist-field ist-field--login ist-field--database">
                  <label id="login-database-label">{t('auth.database')}</label>
                  {multiple ? (
                    <div className="ist-db-picker">
                      <button
                        type="button"
                        className="ist-db-picker__trigger"
                        aria-labelledby="login-database-label"
                        aria-expanded={pickerOpen}
                        aria-haspopup="listbox"
                        onClick={() => setPickerOpen((o) => !o)}
                        disabled={dbLoading}
                      >
                        <span className="ist-db-picker__value">{database}</span>
                        <span className="ist-db-picker__chevron" aria-hidden="true">
                          ▾
                        </span>
                      </button>
                      {pickerOpen && (
                        <ul
                          className="ist-db-picker__list"
                          role="listbox"
                          aria-labelledby="login-database-label"
                        >
                          {databases.map((name) => (
                            <li key={name} role="option" aria-selected={name === database}>
                              <button
                                type="button"
                                className={
                                  name === database
                                    ? 'ist-db-picker__option ist-db-picker__option--active'
                                    : 'ist-db-picker__option'
                                }
                                onClick={() => selectDatabase(name)}
                              >
                                {name}
                              </button>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ) : (
                    <button
                      type="button"
                      className="ist-db-link"
                      aria-labelledby="login-database-label"
                      onClick={() => selectDatabase(database)}
                      disabled={dbLoading}
                      title={t('auth.databaseSelected')}
                    >
                      {database}
                    </button>
                  )}
                  <input type="hidden" name="database" value={database} readOnly />
                </div>

                <div className="ist-field ist-field--login">
                  <label htmlFor="login-email">{t('auth.username')}</label>
                  <input
                    className="ist-input ist-input--boxed"
                    type="text"
                    id="login-email"
                    name="login"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="staff@clinic.qa"
                    autoComplete="username"
                    required
                  />
                </div>

                <div className="ist-field ist-field--login">
                  <div className="ist-field__label-row">
                    <label htmlFor="login-password">{t('auth.password')}</label>
                    <a href="#" className="ist-link" onClick={(e) => e.preventDefault()}>
                      {t('auth.forgotPassword')}
                    </a>
                  </div>
                  <input
                    className="ist-input ist-input--boxed"
                    type="password"
                    id="login-password"
                    name="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    autoComplete="current-password"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="ist-btn ist-btn--primary ist-btn--pill"
                  disabled={loading || !database}
                >
                  {loading ? t('auth.signingIn') : t('auth.login')}
                </button>
              </form>
            </div>
          </div>

          <footer className="ist-login-card__footer">
            <p className="ist-login-card__footer-text">{t('auth.loginFooterText')}</p>
            <div className="ist-contact-block">
              <p className="ist-contact-block__legal">{t('legal.name')}</p>
              <address>{t('legal.address')}</address>
            </div>
            <nav className="ist-login-card__footer-links" aria-label="Legal">
              <a href="/legal/privacy.html" target="_blank" rel="noopener noreferrer">
                {t('legal.privacyPolicy')}
              </a>
              <a href="/legal/terms.html" target="_blank" rel="noopener noreferrer">
                {t('legal.termsOfService')}
              </a>
            </nav>
          </footer>
        </div>
      </div>
    </div>
  )
}
