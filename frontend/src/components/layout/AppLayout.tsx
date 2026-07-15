import { useCallback, useState } from 'react'
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
  istNavVisible: boolean
  toggleIstNav: () => void
  setIstNavVisible: (visible: boolean) => void
}

const IST_NAV_STORAGE_KEY = 'ist-workspace-nav-visible'

export function AppLayout() {
  const { t } = useTranslation()
  const { username, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const isWorkspace =
    location.pathname === '/workspace' || location.pathname.startsWith('/workspace/')

  // Workspace: IST sidebar hidden by default (avoids double menu with SAO).
  // Preference persisted so "Show IST menu" sticks for the session/browser.
  const [istNavVisible, setIstNavVisibleState] = useState(() => {
    if (typeof window === 'undefined') return false
    try {
      return window.sessionStorage.getItem(IST_NAV_STORAGE_KEY) === '1'
    } catch {
      return false
    }
  })

  const setIstNavVisible = useCallback((visible: boolean) => {
    setIstNavVisibleState(visible)
    try {
      window.sessionStorage.setItem(IST_NAV_STORAGE_KEY, visible ? '1' : '0')
    } catch {
      /* ignore */
    }
  }, [])

  const toggleIstNav = useCallback(() => {
    setIstNavVisible(!istNavVisible)
  }, [istNavVisible, setIstNavVisible])

  const showSidebar = !isWorkspace || istNavVisible

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const outletContext: AppLayoutOutletContext = {
    isWorkspace,
    istNavVisible,
    toggleIstNav,
    setIstNavVisible,
  }

  const appClass = [
    'ist-app',
    isWorkspace ? 'ist-app--workspace' : '',
    isWorkspace && !istNavVisible ? 'ist-app--workspace-nav-hidden' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <div className={appClass}>
      <div className="ist-watermark" aria-hidden="true">
        <span className="ist-watermark__text">IST</span>
      </div>

      <header className="ist-header">
        <div className="ist-header__start">
          <Logo variant="compact" to="/" />
          {isWorkspace && !istNavVisible && (
            <button
              type="button"
              className="ist-btn ist-btn--outline ist-btn--sm ist-header__nav-toggle"
              onClick={toggleIstNav}
              aria-expanded={false}
            >
              {t('workspace.showIstMenu')}
            </button>
          )}
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

      <div className="ist-app__body">
        {showSidebar && (
          <aside className="ist-sidebar" aria-label={t('nav.menuTree')}>
            <Logo variant="compact" to="/" className="ist-sidebar__logo" />
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
