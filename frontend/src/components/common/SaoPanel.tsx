import { MODULE_SERVER_INSTRUCTIONS, SAO_DIRECT_URL, saoUrl } from '../../lib/sao'

type SaoPanelProps = {
  title?: string
  description?: string
  /** Extra bullet instructions shown below the link */
  instructions?: string[]
  compact?: boolean
}

/** Panel for wizard-only / deep admin actions that remain SAO-only. */
export function SaoPanel({
  title = 'Open in SAO',
  description = 'This action uses a Tryton wizard or deep configuration screen that is not fully mirrored in React yet.',
  instructions,
  compact = false,
}: SaoPanelProps) {
  const primary = saoUrl()
  const fallback = SAO_DIRECT_URL

  return (
    <div
      className="ist-notice"
      style={compact ? { marginTop: 'var(--space-4)' } : { marginBottom: 'var(--space-6)' }}
    >
      <p style={{ fontWeight: 600, marginBottom: '0.35rem' }}>{title}</p>
      <p className="ist-subtitle" style={{ marginBottom: '0.75rem' }}>
        {description}
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center' }}>
        <a
          className="ist-btn ist-btn--primary ist-btn--sm"
          href={primary}
          target="_blank"
          rel="noreferrer"
        >
          Open GNU Health SAO
        </a>
        {primary !== fallback && (
          <a className="ist-subtitle" href={fallback} target="_blank" rel="noreferrer">
            Direct :8000 fallback
          </a>
        )}
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
  return (
    <SaoPanel
      title="Module activate / upgrade"
      description="Marking modules in React (when available) only queues state changes. Applying upgrades usually requires trytond-admin or SAO."
      instructions={[...MODULE_SERVER_INSTRUCTIONS]}
    />
  )
}
