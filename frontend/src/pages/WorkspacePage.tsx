import { useLayoutEffect, useMemo } from 'react'
import { Navigate, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { handoffSaoSession, saoUrl } from '../lib/sao'

/**
 * Primary IST app surface: GNU Health SAO inside login-aligned IST chrome
 * (header + footer from AppLayout; SAO top bar stays hidden via custom.css).
 * Same-origin iframe — loads /sao/#{database} after handoff of ist-health-session
 * into sao_session_{db} so SAO skips its own login dialog.
 * Optional ?path= is reserved for future deep-links; currently ignored (SAO root).
 */
export function WorkspacePage() {
  const { t } = useTranslation()
  const { isAuthenticated, client } = useAuth()
  const [params] = useSearchParams()
  // Reserved for later deep-link support (e.g. ?path=...)
  void params.get('path')

  const session = client.currentSession

  // Re-sync before iframe paints (covers refresh / stale SAO key).
  useLayoutEffect(() => {
    if (session) handoffSaoSession(session)
  }, [session])

  const src = useMemo(() => saoUrl(session?.database), [session?.database])

  if (!isAuthenticated || !session) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="ist-workspace">
      <div className="ist-workspace__frame-wrap">
        <iframe
          className="ist-workspace__frame"
          title={t('workspace.iframeTitle')}
          src={src}
          // Same-origin only; do not allow embedding third-party URLs
          referrerPolicy="same-origin"
        />
      </div>
    </div>
  )
}
