import { Link } from 'react-router-dom'

type LogoVariant = 'default' | 'compact' | 'lg'

const VARIANT_CLASS: Record<LogoVariant, string> = {
  default: 'ist-logo',
  compact: 'ist-logo ist-logo--compact',
  lg: 'ist-logo ist-logo--lg',
}

interface LogoProps {
  variant?: LogoVariant
  to?: string
  className?: string
}

export function Logo({ variant = 'default', to, className }: LogoProps) {
  const classes = [VARIANT_CLASS[variant], className].filter(Boolean).join(' ')
  const isCompact = variant === 'compact'
  const src = isCompact ? '/assets/logo-symbol.svg' : '/assets/logo-full.svg'

  const content = (
    <>
      <img className="ist-logo__img" src={src} alt="" />
      {isCompact && <span className="ist-logo__compact-text" aria-hidden="true">IST</span>}
    </>
  )

  if (to) {
    return (
      <Link to={to} className={classes} aria-label="Iris Star Technologies">
        {content}
      </Link>
    )
  }

  return (
    <span className={classes} aria-label="Iris Star Technologies">
      {content}
    </span>
  )
}
