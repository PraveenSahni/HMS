import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { saoUrl } from '../lib/sao'

/**
 * Primary IST app surface: GNU Health SAO full-viewport (no IST header chrome).
 * Same-origin iframe — loads /sao/ via saoUrl(). Escape hatch lives in AppLayout.
 * Optional ?path= is reserved for future deep-links; currently ignored (SAO root).
 */
export function WorkspacePage() {
  const { t } = useTranslation()
  const [params] = useSearchParams()
  // Reserved for later deep-link support (e.g. ?path=...)
  void params.get('path')

  const src = useMemo(() => saoUrl(), [])

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
