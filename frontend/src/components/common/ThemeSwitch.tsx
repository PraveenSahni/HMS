import { useTheme } from '../../hooks/useTheme'

export function ThemeSwitch() {
  const { isDark, toggleTheme } = useTheme()

  return (
    <label className="ist-theme-switch" title="Toggle light / dark mode">
      <input
        type="checkbox"
        checked={isDark}
        onChange={toggleTheme}
        aria-label="Toggle dark mode"
      />
      <span className="ist-theme-switch__track">
        <span
          className={`ist-theme-switch__icon ist-theme-switch__icon--sun${!isDark ? ' is-active' : ''}`}
          aria-hidden="true"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
          </svg>
        </span>
        <span className="ist-theme-switch__thumb" />
        <span
          className={`ist-theme-switch__icon ist-theme-switch__icon--moon${isDark ? ' is-active' : ''}`}
          aria-hidden="true"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        </span>
      </span>
    </label>
  )
}
