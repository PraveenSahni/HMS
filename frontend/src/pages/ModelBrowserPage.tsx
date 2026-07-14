import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import { SaoPanel } from '../components/common/SaoPanel'
import { TrytonClient } from '../lib/tryton/client'
import { GENERIC_LIST_FIELDS } from '../lib/tryton/menuRoutes'
import { formatTrytonDate } from '../lib/tryton/models'
import { saoUrl } from '../lib/sao'
import {
  fetchMenuById,
  resolveMenuAction,
  type MenuRecord,
  type ResolvedAction,
} from '../services/menuApi'

const PAGE_SIZE = 50

function formatCell(value: unknown): string {
  if (value == null || value === false) return '—'
  if (typeof value === 'boolean') return value ? '✓' : '—'
  if (typeof value === 'number') return String(value)
  if (typeof value === 'string') return value || '—'
  if (Array.isArray(value)) {
    if (value.length >= 2 && (typeof value[1] === 'string' || typeof value[1] === 'number')) {
      return String(value[1])
    }
    return value.map(formatCell).join(', ')
  }
  if (typeof value === 'object' && value !== null && '__class__' in value) {
    return formatTrytonDate(value)
  }
  try {
    return JSON.stringify(value)
  } catch {
    return String(value)
  }
}

async function readWithFallback(
  client: TrytonClient,
  model: string,
  ids: number[],
): Promise<{ fields: string[]; rows: Record<string, unknown>[] }> {
  if (!ids.length) return { fields: ['id'], rows: [] }

  try {
    const rows = await client.read(model, ids, ['id', 'rec_name'])
    return { fields: ['id', 'rec_name'], rows }
  } catch {
    /* continue */
  }

  const candidates = [...GENERIC_LIST_FIELDS]
  try {
    const rows = await client.read(model, ids, candidates as unknown as string[])
    const present = candidates.filter((f) => rows.some((r) => f in r))
    return { fields: present.length ? present : ['id'], rows }
  } catch {
    /* continue */
  }

  try {
    const rows = await client.read(model, ids, ['id'])
    return { fields: ['id'], rows }
  } catch {
    return { fields: ['id'], rows: ids.map((id) => ({ id })) }
  }
}

export function ModelBrowserPage() {
  const { menuId: menuIdParam } = useParams()
  const menuId = Number(menuIdParam)
  const { t } = useTranslation()
  const { client } = useAuth()

  const [menu, setMenu] = useState<MenuRecord | null>(null)
  const [action, setAction] = useState<ResolvedAction | null>(null)
  const [rows, setRows] = useState<Record<string, unknown>[]>([])
  const [fields, setFields] = useState<string[]>(['id'])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [unsupported, setUnsupported] = useState<string | null>(null)

  const load = useCallback(async () => {
    if (!Number.isFinite(menuId) || menuId <= 0) {
      setError(t('modelBrowser.invalidMenu'))
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)
    setUnsupported(null)
    try {
      const menuRow = await fetchMenuById(client, menuId)
      if (!menuRow) {
        setError(t('modelBrowser.menuNotFound'))
        return
      }
      setMenu(menuRow)

      if (!menuRow.action) {
        setUnsupported(t('modelBrowser.folderOnly'))
        setAction(null)
        setRows([])
        setTotal(0)
        return
      }

      const resolved = await resolveMenuAction(client, menuRow)
      setAction(resolved)

      if (!resolved) {
        setUnsupported(t('modelBrowser.noAction'))
        return
      }

      if (resolved.route) {
        // Should normally navigate from MenuTree; still allow deep links
        setUnsupported(null)
      }

      if (resolved.actionType !== 'ir.action.act_window' || !resolved.resModel) {
        setUnsupported(
          t('modelBrowser.unsupportedAction', {
            type: resolved.actionType,
            sao: saoUrl(),
          }),
        )
        setRows([])
        setTotal(0)
        return
      }

      const model = resolved.resModel
      const ids = await client.search(model, [], 0, PAGE_SIZE, [['id', 'DESC']])
      const count = await client.searchCount(model, [])
      setTotal(count)
      const result = await readWithFallback(client, model, ids)
      setFields(result.fields)
      setRows(result.rows)
    } catch {
      setError(t('common.error'))
    } finally {
      setLoading(false)
    }
  }, [client, menuId, t])

  useEffect(() => {
    load()
  }, [load])

  const title = useMemo(
    () => menu?.name ?? action?.name ?? t('modelBrowser.title'),
    [menu, action, t],
  )

  const displayFields = useMemo(
    () => fields.filter((f) => f !== 'id' || fields.length === 1),
    [fields],
  )

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{title}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">
            {action?.resModel
              ? t('modelBrowser.subtitleModel', { model: action.resModel })
              : t('modelBrowser.subtitle')}
          </p>
        </div>
        {action?.route && (
          <Link to={action.route} className="ist-btn ist-btn--outline ist-btn--sm">
            {t('modelBrowser.openDedicated')}
          </Link>
        )}
      </div>

      {error && <ErrorState message={error} onRetry={load} />}

      {loading ? (
        <LoadingState message={t('modelBrowser.loading')} />
      ) : unsupported ? (
        <SaoPanel
          title={t('modelBrowser.openSao')}
          description={unsupported}
        />
      ) : rows.length === 0 ? (
        <div className="ist-notice">{t('modelBrowser.empty')}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
            {total > PAGE_SIZE ? ` · ${t('modelBrowser.showing', { count: rows.length })}` : ''}
          </p>
          <div className="ist-patient-list ist-model-browser">
            <div
              className="ist-patient-list__head"
              style={{
                gridTemplateColumns: `72px repeat(${displayFields.length}, minmax(100px, 1fr))`,
              }}
            >
              <span>ID</span>
              {displayFields.map((f) => (
                <span key={f}>{f === 'rec_name' ? t('modelBrowser.name') : f}</span>
              ))}
            </div>
            {rows.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{
                  gridTemplateColumns: `72px repeat(${displayFields.length}, minmax(100px, 1fr))`,
                }}
              >
                <span className="ist-patient-list__id">{String(row.id)}</span>
                {displayFields.map((f) => (
                  <span
                    key={f}
                    className={f === 'rec_name' || f === 'name' ? 'ist-patient-name' : 'ist-subtitle'}
                  >
                    {formatCell(row[f])}
                  </span>
                ))}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
