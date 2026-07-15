import { useTranslation } from 'react-i18next'

type AppFooterProps = {
  /** Compact bar for /workspace — same legal lines as login, tighter padding. */
  compact?: boolean
}

export function AppFooter({ compact = false }: AppFooterProps) {
  const { t } = useTranslation()

  return (
    <footer className={`ist-app-footer${compact ? ' ist-app-footer--compact' : ''}`}>
      <p className="ist-app-footer__legal">{t('legal.name')}</p>
      <p>{compact ? t('app.location') : t('legal.addressShort')}</p>
    </footer>
  )
}
