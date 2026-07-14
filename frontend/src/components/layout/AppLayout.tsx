import { Outlet, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../../contexts/AuthContext'
import { Logo } from '../common/Logo'
import { LangSwitch } from '../common/LangSwitch'
import { ThemeSwitch } from '../common/ThemeSwitch'
import { AppFooter } from '../common/AppFooter'
import { MenuTree } from './MenuTree'
import { ContextualHelpButton } from '../../pages/help/HelpCentrePage'

export function AppLayout() {
  const { t } = useTranslation()
  const { username, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="ist-app">
      <div className="ist-watermark" aria-hidden="true">
        <span className="ist-watermark__text">IST</span>
      </div>

      <header className="ist-header">
        <div className="ist-header__start">
          <Logo variant="compact" to="/" />
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
        <aside className="ist-sidebar">
          <Logo variant="compact" to="/" className="ist-sidebar__logo" />
          <MenuTree />
        </aside>

        <main className="ist-main">
          <Outlet />
          <AppFooter />
        </main>
      </div>
    </div>
  )
}
