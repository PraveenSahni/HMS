import { useTranslation } from 'react-i18next'
import { setLanguage } from '../../i18n'

export function LangSwitch() {
  const { i18n } = useTranslation()
  const lang = i18n.language.startsWith('ar') ? 'ar' : 'en'

  return (
    <div className="ist-lang-switch" role="group" aria-label="Language">
      <button
        type="button"
        className={lang === 'en' ? 'is-active' : undefined}
        onClick={() => setLanguage('en')}
      >
        EN
      </button>
      <button
        type="button"
        className={lang === 'ar' ? 'is-active' : undefined}
        onClick={() => setLanguage('ar')}
      >
        AR
      </button>
    </div>
  )
}
