import { clsx } from '../clsx'



interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {

  variant?: 'default' | 'primary' | 'outline' | 'danger'

  size?: 'sm' | 'md'

}



export function Button({

  variant = 'default',

  size = 'md',

  className,

  children,

  ...props

}: ButtonProps) {

  return (

    <button

      type="button"

      className={clsx(

        'ist-btn',

        size === 'sm' && 'ist-btn--sm',

        variant === 'primary' && 'ist-btn--primary',

        variant === 'outline' && 'ist-btn--outline',

        variant === 'danger' && 'ist-btn--outline',

        className,

      )}

      {...props}

    >

      {children}

    </button>

  )

}



export function Badge({

  children,

  variant = 'default',

  className,

}: {

  children: React.ReactNode

  variant?: 'default' | 'success' | 'warning' | 'info'

  className?: string

}) {

  return (

    <span

      className={clsx(

        'ist-status',

        variant === 'success' && 'ist-status--completed',

        variant === 'warning' && 'is-pending',

        className,

      )}

    >

      {children}

    </span>

  )

}



export function SectionTitle({ children }: { children: React.ReactNode }) {

  return (

    <div className="ist-section">

      <h3>{children}</h3>

      <hr className="ist-divider" />

    </div>

  )

}



export function Card({

  children,

  className,

}: {

  children: React.ReactNode

  className?: string

  enabled?: boolean

}) {

  return <div className={clsx('ist-card', className)}>{children}</div>

}



export function Notice({ children }: { children: React.ReactNode }) {

  return <div className="ist-notice">{children}</div>

}



export function Input({

  className,

  ...props

}: React.InputHTMLAttributes<HTMLInputElement>) {

  return <input className={clsx('ist-input ist-input--boxed', className)} {...props} />

}



export function Select({

  className,

  children,

  ...props

}: React.SelectHTMLAttributes<HTMLSelectElement>) {

  return (

    <select className={clsx('ist-input ist-input--boxed', className)} {...props}>

      {children}

    </select>

  )

}



export function LoadingState({ message }: { message?: string }) {

  return <div className="ist-loading">{message ?? 'Loading…'}</div>

}



export function ErrorState({

  message,

  onRetry,

}: {

  message: string

  onRetry?: () => void

}) {

  return (

    <div className="ist-notice ist-notice--error">

      <p>{message}</p>

      {onRetry && (

        <Button variant="primary" className="ist-btn--sm" onClick={onRetry} style={{ marginTop: 'var(--space-3)' }}>

          Retry

        </Button>

      )}

    </div>

  )

}



export function StubPage({
  title,
  description,
}: {
  title: string
  description?: string
  models?: string[]
}) {
  return (
    <>
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">IST Technologies LLC</p>
          <h1>{title}</h1>
          <hr className="ist-divider" />
        </div>
      </div>
      {description && <div className="ist-notice">{description}</div>}
    </>
  )
}



export function Metric({

  label,

  value,

  loading = false,

}: {

  label: string

  value: string | number

  highlight?: boolean

  loading?: boolean

}) {

  return (

    <div className="ist-stat">

      <div className="ist-stat__label">{label}</div>

      <div className="ist-stat__value">{loading ? '—' : value}</div>

    </div>

  )

}

