import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../../contexts/AuthContext'
import { Logo } from '../common/Logo'
import { LangSwitch } from '../common/LangSwitch'
import { ThemeSwitch } from '../common/ThemeSwitch'
import { AppFooter } from '../common/AppFooter'
import { MenuTree } from './MenuTree'
import { ContextualHelpButton } from '../../pages/help/HelpCentrePage'

export type AppLayoutOutletContext = {
  isWorkspace: boolean
}

export function AppLayout() {
  const { t } = useTranslation()
  const { username, database, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const isWorkspace =
    location.pathname === '/workspace' || location.pathname.startsWith('/workspace/')

  // Workspace: IST sidebar always hidden (SAO left menu is the only nav inside the iframe).
  const showSidebar = !isWorkspace

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const outletContext: AppLayoutOutletContext = {
    isWorkspace,
  }

  const appClass = ['ist-app', isWorkspace ? 'ist-app--workspace' : ''].filter(Boolean).join(' ')
  const sessionHint = [database, username].filter(Boolean).join(' · ')

  return (
    <div className={appClass}>
      {!isWorkspace && (
        <div className="ist-watermark" aria-hidden="true">
          <span className="ist-watermark__text">IST</span>
        </div>
      )}

      {/* Full IST chrome outside /workspace (lang / theme / help). */}
      {!isWorkspace && (
        <header className="ist-header">
          <div className="ist-header__start">
            <Logo variant="compact" to="/workspace" />
          </div>
          <div className="ist-header__end">
            <span className="ist-header__user">{username}</span>
            <div className="ist-header__divider" />
            <LangSwitch />
            <div className="ist-header__divider" />
            <ThemeSwitch />
            <div className="ist-header__divider" />
            <ContextualHelpButton />
            <button type="button" className="ist-btn ist-btn--outline ist-btn--sm" onClick={handleLogout}>
              {t('auth.logout')}
            </button>
          </div>
        </header>
      )}

      {/* Workspace: single login-aligned chrome — logo + product name left, Sign out right. */}
      {isWorkspace && (
        <header className="ist-header ist-header--workspace">
          <div className="ist-header__start">
            <Logo variant="compact" to="/workspace" />
            <span className="ist-header__product">{t('app.name')}</span>
            {sessionHint ? (
              <span className="ist-header__session" title={sessionHint}>
                {sessionHint}
              </span>
            ) : null}
          </div>
          <div className="ist-header__end">
            <button
              type="button"
              className="ist-btn ist-btn--outline ist-btn--sm"
              onClick={handleLogout}
            >
              {t('auth.logout')}
            </button>
          </div>
        </header>
      )}

      <div className="ist-app__body">
        {showSidebar && (
          <aside className="ist-sidebar" aria-label={t('nav.menuTree')}>
            <Logo variant="compact" to="/workspace" className="ist-sidebar__logo" />
            <MenuTree />
          </aside>
        )}

        <main className={`ist-main${isWorkspace ? ' ist-main--workspace' : ''}`}>
          <Outlet context={outletContext} />
          {isWorkspace ? (
            <AppFooter compact />
          ) : (
            <AppFooter />
          )}
        </main>
      </div>
    </div>
  )
}
