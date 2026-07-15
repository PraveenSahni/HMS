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
  const { username, logout } = useAuth()
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

  return (
    <div className={appClass}>
      {!isWorkspace && (
        <div className="ist-watermark" aria-hidden="true">
          <span className="ist-watermark__text">IST</span>
        </div>
      )}

      {/* Full IST chrome only outside /workspace — SAO wrapper is the primary post-login app. */}
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

      {/* Tiny Sign out only — clears IST session and returns to React login. */}
      {isWorkspace && (
        <div className="ist-workspace-escape" role="navigation" aria-label={t('workspace.escapeLabel')}>
          <button
            type="button"
            className="ist-btn ist-btn--outline ist-btn--sm ist-workspace-escape__logout"
            onClick={handleLogout}
          >
            {t('auth.logout')}
          </button>
        </div>
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
          {!isWorkspace && <AppFooter />}
        </main>
      </div>
    </div>
  )
}
