import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { MODULE_SERVER_INSTRUCTIONS, saoUrl } from '../../lib/sao'

type SaoPanelProps = {
  title?: string
  description?: string
  /** Extra bullet instructions shown below the link */
  instructions?: string[]
  compact?: boolean
}

/** Panel for wizard-only / deep admin actions — prefer IST Workspace embed over bare /sao/. */
export function SaoPanel({
  title,
  description,
  instructions,
  compact = false,
}: SaoPanelProps) {
  const { t } = useTranslation()
  const panelTitle = title ?? t('workspace.openInWorkspace')
  const panelDesc =
    description ??
    t('workspace.panelDefaultDesc')
  const primary = saoUrl()

  return (
    <div
      className="ist-notice"
      style={compact ? { marginTop: 'var(--space-4)' } : { marginBottom: 'var(--space-6)' }}
    >
      <p style={{ fontWeight: 600, marginBottom: '0.35rem' }}>{panelTitle}</p>
      <p className="ist-subtitle" style={{ marginBottom: '0.75rem' }}>
        {panelDesc}
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center' }}>
        <Link className="ist-btn ist-btn--primary ist-btn--sm" to="/workspace">
          {t('workspace.openInWorkspace')}
        </Link>
        <a
          className="ist-subtitle"
          href={primary}
          target="_blank"
          rel="noreferrer"
        >
          {t('workspace.openNewTab')}
        </a>
      </div>
      {instructions && instructions.length > 0 && (
        <ul className="ist-subtitle" style={{ marginTop: '0.75rem', paddingLeft: '1.25rem' }}>
          {instructions.map((line) => (
            <li key={line} style={{ marginBottom: '0.25rem' }}>
              {line}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export function ModuleServerInstructions() {
  const { t } = useTranslation()
  return (
    <SaoPanel
      title={t('workspace.moduleActivateTitle')}
      description={t('workspace.moduleActivateDesc')}
      instructions={[...MODULE_SERVER_INSTRUCTIONS]}
    />
  )
}
