import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import {
  clearPublishOverrides,
  isPublished,
  loadHelpIndex,
  setPublishOverride,
  type HelpIndexEntry,
} from '../../help/helpService'

/**
 * Simple help administration: view publish state from topic metadata
 * and apply local publish/unpublish overrides (no backend CMS).
 */
export function HelpAdminPage() {
  const { i18n, t } = useTranslation()
  const lang = (i18n.language?.startsWith('ar') ? 'ar' : 'en') as 'en' | 'ar'
  const [index, setIndex] = useState<HelpIndexEntry[]>([])
  const [error, setError] = useState<string | null>(null)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    loadHelpIndex(lang)
      .then(setIndex)
      .catch((e) => setError(String(e)))
  }, [lang, tick])

  const toggle = (entry: HelpIndexEntry) => {
    const next = !isPublished(entry)
    setPublishOverride(entry.id, next)
    setTick((n) => n + 1)
  }

  const reset = () => {
    clearPublishOverrides()
    setTick((n) => n + 1)
  }

  return (
    <div className="ist-page" data-testid="help-admin">
      <header className="ist-page__header">
        <h1>{t('help.adminTitle', { defaultValue: 'Help administration' })}</h1>
        <p className="ist-muted">
          {t('help.adminSubtitle', {
            defaultValue:
              'Publish flag comes from topic metadata (published). Overrides are stored locally until content is regenerated.',
          })}
        </p>
        <p>
          <Link to="/help">{t('help.backToCentre', { defaultValue: 'Back to Help Centre' })}</Link>
          {' · '}
          <button type="button" className="ist-btn ist-btn--outline ist-btn--sm" onClick={reset}>
            {t('help.resetOverrides', { defaultValue: 'Reset local overrides' })}
          </button>
        </p>
      </header>

      {error && <p className="ist-error">{error}</p>}

      <table className="ist-table" data-testid="help-admin-table">
        <thead>
          <tr>
            <th>{t('help.topic', { defaultValue: 'Topic' })}</th>
            <th>ID</th>
            <th>{t('help.guided', { defaultValue: 'Guided' })}</th>
            <th>{t('help.published', { defaultValue: 'Published' })}</th>
            <th>{t('help.action', { defaultValue: 'Action' })}</th>
          </tr>
        </thead>
        <tbody>
          {index.map((e) => {
            const pub = isPublished(e)
            return (
              <tr key={e.id}>
                <td>{e.title}</td>
                <td>
                  <code>{e.id}</code>
                </td>
                <td>{e.guided ? 'yes' : 'no'}</td>
                <td data-testid={`publish-state-${e.id}`}>{pub ? 'published' : 'unpublished'}</td>
                <td>
                  <button
                    type="button"
                    className="ist-btn ist-btn--outline ist-btn--sm"
                    onClick={() => toggle(e)}
                    data-testid={`toggle-publish-${e.id}`}
                  >
                    {pub
                      ? t('help.unpublish', { defaultValue: 'Unpublish' })
                      : t('help.publish', { defaultValue: 'Publish' })}
                  </button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
