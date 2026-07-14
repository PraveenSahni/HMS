import { useId, useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface FieldHelpProps {
  /** Help Centre article id, or free-text hint */
  topicId?: string
  hint?: string
  children?: ReactNode
}

/**
 * Field-level help: compact "?" control that shows inline hint and/or links to Help Centre.
 */
export function FieldHelp({ topicId, hint, children }: FieldHelpProps) {
  const [open, setOpen] = useState(false)
  const id = useId()

  return (
    <span className="ist-field-help" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}>
      {children}
      <button
        type="button"
        className="ist-btn ist-btn--outline ist-btn--sm"
        aria-expanded={open}
        aria-controls={id}
        title="Field help"
        data-testid="field-help-toggle"
        onClick={() => setOpen((v) => !v)}
        style={{ padding: '0 0.4rem', minWidth: '1.5rem', lineHeight: 1.2 }}
      >
        ?
      </button>
      {open && (
        <span
          id={id}
          role="note"
          className="ist-muted"
          data-testid="field-help-panel"
          style={{ fontSize: '0.85rem' }}
        >
          {hint}
          {topicId && (
            <>
              {hint ? ' ' : null}
              <Link to={`/help?topic=${encodeURIComponent(topicId)}`}>Open help topic</Link>
            </>
          )}
        </span>
      )}
    </span>
  )
}
