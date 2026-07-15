import { useMemo } from 'react'
import { useOutletContext, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { saoUrl } from '../lib/sao'
import type { AppLayoutOutletContext } from '../components/layout/AppLayout'

/**
 * Embeds GNU Health SAO inside the IST AppLayout (header; sidebar collapsed by default).
 * Same-origin iframe only — loads /sao/ via saoUrl().
 * Optional ?path= is reserved for future deep-links; currently ignored (SAO root).
 */
export function WorkspacePage() {
  const { t } = useTranslation()
  const [params] = useSearchParams()
  // Reserved for later deep-link support (e.g. ?path=...)
  void params.get('path')

  const { istNavVisible, toggleIstNav } = useOutletContext<AppLayoutOutletContext>()
  const src = useMemo(() => saoUrl(), [])

  return (
    <div className="ist-workspace">
      <div className="ist-workspace__toolbar">
        <div className="ist-workspace__toolbar-text">
          <h1 className="ist-workspace__title">{t('workspace.title')}</h1>
          <p className="ist-workspace__subtitle">{t('workspace.subtitle')}</p>
        </div>
        <div className="ist-workspace__toolbar-actions">
          <button
            type="button"
            className="ist-btn ist-btn--outline ist-btn--sm"
            onClick={toggleIstNav}
            aria-pressed={istNavVisible}
          >
            {istNavVisible ? t('workspace.hideIstMenu') : t('workspace.showIstMenu')}
          </button>
          <a
            className="ist-btn ist-btn--outline ist-btn--sm"
            href={src}
            target="_blank"
            rel="noreferrer"
          >
            {t('workspace.openNewTab')}
          </a>
        </div>
      </div>
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
