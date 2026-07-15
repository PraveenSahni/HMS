import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { saoUrl } from '../lib/sao'

/**
 * Embeds GNU Health SAO under the IST header only (no Workspace toolbar).
 * Same-origin iframe — loads /sao/ via saoUrl(). SAO top bar is hidden via custom.css
 * when embedded; SAO left menu remains for navigation.
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
