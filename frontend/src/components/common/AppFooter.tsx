import { useTranslation } from 'react-i18next'

export function AppFooter() {
  const { t } = useTranslation()

  return (
    <footer className="ist-app-footer">
      <p className="ist-app-footer__legal">{t('legal.name')}</p>
      <p>{t('legal.addressShort')}</p>
    </footer>
  )
}
