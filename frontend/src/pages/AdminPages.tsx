import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState, Select } from '../components/ui'
import { ModuleServerInstructions, SaoPanel } from '../components/common/SaoPanel'
import { formatRpcError } from '../lib/tryton/client'
import {
  createCompanySetup,
  createInvoiceStub,
  createUser,
  fetchCompanies,
  fetchCountries,
  fetchGroupDetail,
  fetchGroups,
  fetchInvoices,
  fetchLanguages,
  fetchModules,
  fetchParties,
  fetchSequences,
  fetchUsers,
  formatTrytonDate,
  IST_COMPANY_DEFAULTS,
  markModulesAction,
  resetUserPassword,
  updateSequence,
  updateUser,
  type UserFormData,
} from '../services/healthApi'

function asIdList(value: unknown): number[] {
  if (!Array.isArray(value)) return []
  return value
    .map((v) => {
      if (typeof v === 'number') return v
      if (Array.isArray(v) && typeof v[0] === 'number') return v[0]
      return Number(v)
    })
    .filter((n) => Number.isFinite(n) && n > 0)
}

function groupNames(
  groups: unknown,
  groupMap: Map<number, string>,
): string {
  const ids = asIdList(groups)
  if (!ids.length) return '—'
  return ids.map((id) => groupMap.get(id) ?? String(id)).join(', ')
}

/* ─── Users ─────────────────────────────────────────────────────────────── */

export function UsersPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [groups, setGroups] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({
    login: '',
    name: '',
    email: '',
    password: '',
    active: true,
    groupIds: [] as number[],
  })

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const groupMap = useMemo(() => {
    const m = new Map<number, string>()
    for (const g of groups) {
      m.set(Number(g.id), String(g.name ?? g.rec_name ?? g.id))
    }
    return m
  }, [groups])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [users, grp] = await Promise.all([
        fetchUsers(client, debounced),
        fetchGroups(client),
      ])
      setRecords(users.records)
      setTotal(users.total)
      setAvailable(users.available)
      setGroups(grp.records)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const openCreate = () => {
    setEditingId(null)
    setForm({ login: '', name: '', email: '', password: '', active: true, groupIds: [] })
    setShowForm(true)
    setSuccess(null)
  }

  const openEdit = (row: Record<string, unknown>) => {
    setEditingId(Number(row.id))
    setForm({
      login: String(row.login ?? ''),
      name: String(row.name ?? ''),
      email: String(row.email ?? ''),
      password: '',
      active: row.active !== false,
      groupIds: asIdList(row.groups),
    })
    setShowForm(true)
    setSuccess(null)
  }

  const save = async () => {
    if (!form.login.trim() || !form.name.trim()) return
    if (!editingId && !form.password) {
      setError(t('ops.users.passwordRequired'))
      return
    }
    setSaving(true)
    setError(null)
    setSuccess(null)
    const data: UserFormData = {
      login: form.login,
      name: form.name,
      email: form.email,
      active: form.active,
      groupIds: form.groupIds,
      password: form.password || undefined,
    }
    try {
      if (editingId) {
        await updateUser(client, editingId, data)
        setSuccess(t('ops.users.updateSuccess'))
      } else {
        await createUser(client, data)
        setSuccess(t('ops.users.createSuccess'))
      }
      setShowForm(false)
      await refresh()
    } catch (err) {
      setError(formatRpcError(err, t('ops.users.saveError')))
    } finally {
      setSaving(false)
    }
  }

  const doResetPassword = async (id: number) => {
    const pwd = window.prompt(t('ops.users.resetPrompt'))
    if (!pwd) return
    setError(null)
    setSuccess(null)
    try {
      await resetUserPassword(client, id, pwd)
      setSuccess(t('ops.users.resetSuccess'))
    } catch (err) {
      setError(formatRpcError(err, t('ops.users.resetError')))
    }
  }

  const toggleGroup = (gid: number) => {
    setForm((f) => ({
      ...f,
      groupIds: f.groupIds.includes(gid)
        ? f.groupIds.filter((x) => x !== gid)
        : [...f.groupIds, gid],
    }))
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.users.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.users.subtitle')}</p>
        </div>
        <button type="button" className="ist-btn ist-btn--primary" onClick={openCreate}>
          {t('ops.users.create')}
        </button>
      </div>

      <div className="ist-split" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('ops.users.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <span className="ist-subtitle">{t('common.recordCount', { count: total })}</span>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={refresh} />}

      {showForm && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>
            {editingId ? t('ops.users.editTitle') : t('ops.users.createTitle')}
          </h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('ops.users.login')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.login}
                onChange={(e) => setForm((f) => ({ ...f, login: e.target.value }))}
                required
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.users.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                required
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.users.email')}</div>
              <input
                className="ist-input ist-input--boxed"
                type="email"
                value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">
                {editingId ? t('ops.users.newPassword') : t('ops.users.password')}
              </div>
              <input
                className="ist-input ist-input--boxed"
                type="password"
                autoComplete="new-password"
                value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                placeholder={editingId ? t('ops.users.passwordLeaveBlank') : undefined}
              />
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input
                type="checkbox"
                checked={form.active}
                onChange={(e) => setForm((f) => ({ ...f, active: e.target.checked }))}
              />
              <span className="ist-label" style={{ margin: 0 }}>{t('ops.users.active')}</span>
            </label>
          </div>
          {groups.length > 0 && (
            <div style={{ marginTop: 'var(--space-4)' }}>
              <div className="ist-label">{t('ops.users.groups')}</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.35rem' }}>
                {groups.map((g) => {
                  const gid = Number(g.id)
                  const on = form.groupIds.includes(gid)
                  return (
                    <button
                      key={gid}
                      type="button"
                      className={`ist-btn ist-btn--sm${on ? ' ist-btn--primary' : ' ist-btn--outline'}`}
                      onClick={() => toggleGroup(gid)}
                    >
                      {String(g.name ?? g.rec_name)}
                    </button>
                  )
                })}
              </div>
            </div>
          )}
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button type="button" className="ist-btn ist-btn--primary" disabled={saving} onClick={save}>
              {saving ? t('common.loading') : t('common.save')}
            </button>
            <button type="button" className="ist-btn ist-btn--outline" onClick={() => setShowForm(false)}>
              {t('common.cancel')}
            </button>
          </div>
        </div>
      )}

      {loading && !records.length ? (
        <LoadingState message={t('ops.users.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.users.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.users.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div
            className="ist-patient-list__head"
            style={{ gridTemplateColumns: '1fr 1.2fr 1.4fr 0.7fr 1.2fr' }}
          >
            <span>{t('ops.users.login')}</span>
            <span>{t('ops.users.name')}</span>
            <span>{t('ops.users.groups')}</span>
            <span>{t('ops.users.status')}</span>
            <span>{t('common.actions')}</span>
          </div>
          {records.map((row) => (
            <div
              key={String(row.id)}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: '1fr 1.2fr 1.4fr 0.7fr 1.2fr' }}
            >
              <span className="ist-patient-name">{String(row.login ?? '—')}</span>
              <span className="ist-subtitle">{String(row.name ?? '—')}</span>
              <span className="ist-subtitle">{groupNames(row.groups, groupMap)}</span>
              <span className="ist-subtitle">{row.active === false ? 'Inactive' : 'Active'}</span>
              <span style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                <button type="button" className="ist-btn ist-btn--sm ist-btn--outline" onClick={() => openEdit(row)}>
                  {t('common.edit')}
                </button>
                <button
                  type="button"
                  className="ist-btn ist-btn--sm ist-btn--outline"
                  onClick={() => void doResetPassword(Number(row.id))}
                >
                  {t('ops.users.resetPassword')}
                </button>
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ─── Groups ────────────────────────────────────────────────────────────── */

export function GroupsPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [detailUsers, setDetailUsers] = useState<string[]>([])
  const [access, setAccess] = useState<Record<string, unknown>[]>([])
  const [detailLoading, setDetailLoading] = useState(false)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchGroups(client)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const openDetail = async (id: number) => {
    setSelectedId(id)
    setDetailLoading(true)
    try {
      const { group, access: acc } = await fetchGroupDetail(client, id)
      const userIds = asIdList(group?.users)
      if (userIds.length) {
        const names = await client.resolveNames('res.user', userIds)
        setDetailUsers(userIds.map((uid) => names.get(uid) ?? String(uid)))
      } else {
        setDetailUsers([])
      }
      setAccess(acc)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setDetailLoading(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.groups.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.groups.subtitle')}</p>
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={refresh} />}

      {loading && !records.length ? (
        <LoadingState message={t('ops.groups.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.groups.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.groups.empty')}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
          </p>
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1fr 120px' }}>
              <span>{t('ops.groups.name')}</span>
              <span>{t('common.actions')}</span>
            </div>
            {records.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '1fr 120px' }}
              >
                <span className="ist-patient-name">{String(row.name ?? row.rec_name ?? '—')}</span>
                <button
                  type="button"
                  className="ist-btn ist-btn--sm ist-btn--outline"
                  onClick={() => void openDetail(Number(row.id))}
                >
                  {t('ops.groups.view')}
                </button>
              </div>
            ))}
          </div>
        </>
      )}

      {selectedId != null && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginTop: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>
            {t('ops.groups.detailTitle')} #{selectedId}
          </h3>
          {detailLoading ? (
            <LoadingState message={t('common.loading')} />
          ) : (
            <>
              <p className="ist-label">{t('ops.groups.linkedUsers')}</p>
              <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
                {detailUsers.length ? detailUsers.join(', ') : t('ops.groups.noUsers')}
              </p>
              <p className="ist-label">{t('ops.groups.modelAccess')}</p>
              {access.length === 0 ? (
                <p className="ist-subtitle">{t('ops.groups.noAccess')}</p>
              ) : (
                <div className="ist-patient-list" style={{ marginTop: '0.5rem' }}>
                  <div
                    className="ist-patient-list__head"
                    style={{ gridTemplateColumns: '2fr repeat(4, 0.5fr)' }}
                  >
                    <span>{t('ops.groups.model')}</span>
                    <span>R</span>
                    <span>W</span>
                    <span>C</span>
                    <span>D</span>
                  </div>
                  {access.map((a) => (
                    <div
                      key={String(a.id)}
                      className="ist-patient-list__row"
                      style={{ gridTemplateColumns: '2fr repeat(4, 0.5fr)' }}
                    >
                      <span className="ist-subtitle">
                        {Array.isArray(a.model) ? String(a.model[1] ?? a.model[0]) : String(a.model ?? a.rec_name ?? '—')}
                      </span>
                      <span>{a.perm_read ? '✓' : '—'}</span>
                      <span>{a.perm_write ? '✓' : '—'}</span>
                      <span>{a.perm_create ? '✓' : '—'}</span>
                      <span>{a.perm_delete ? '✓' : '—'}</span>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  )
}

/* ─── Modules ───────────────────────────────────────────────────────────── */

export function ModulesPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchModules(client, debounced)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const toggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const runAction = async (action: 'activate' | 'upgrade' | 'deactivate') => {
    const ids = [...selected]
    if (!ids.length) return
    setBusy(true)
    setNotice(null)
    setError(null)
    const result = await markModulesAction(client, ids, action)
    setNotice(result.message)
    if (result.ok) await refresh()
    setBusy(false)
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.modules.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.modules.subtitle')}</p>
        </div>
      </div>

      <ModuleServerInstructions />

      <div className="ist-split" style={{ marginBottom: 'var(--space-6)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('ops.modules.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            className="ist-btn ist-btn--sm ist-btn--primary"
            disabled={busy || !selected.size}
            onClick={() => void runAction('activate')}
          >
            {t('ops.modules.activate')}
          </button>
          <button
            type="button"
            className="ist-btn ist-btn--sm ist-btn--outline"
            disabled={busy || !selected.size}
            onClick={() => void runAction('upgrade')}
          >
            {t('ops.modules.upgrade')}
          </button>
        </div>
      </div>

      {notice && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{notice}</div>}
      {error && <ErrorState message={error} onRetry={refresh} />}

      {loading && !records.length ? (
        <LoadingState message={t('ops.modules.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.modules.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.modules.empty')}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })} · {t('ops.modules.selected', { count: selected.size })}
          </p>
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: '40px 2fr 1fr' }}>
              <span />
              <span>{t('ops.modules.name')}</span>
              <span>{t('ops.modules.state')}</span>
            </div>
            {records.map((row) => {
              const id = Number(row.id)
              return (
                <div
                  key={String(id)}
                  className="ist-patient-list__row"
                  style={{ gridTemplateColumns: '40px 2fr 1fr' }}
                >
                  <input type="checkbox" checked={selected.has(id)} onChange={() => toggle(id)} />
                  <span className="ist-patient-name">{String(row.name ?? row.rec_name ?? '—')}</span>
                  <span className="ist-subtitle">{String(row.state ?? '—')}</span>
                </div>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}

/* ─── Sequences ─────────────────────────────────────────────────────────── */

export function SequencesPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')
  const [editingId, setEditingId] = useState<number | null>(null)
  const [editForm, setEditForm] = useState({ number_next: '', prefix: '', suffix: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchSequences(client, debounced)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const openEdit = (row: Record<string, unknown>) => {
    setEditingId(Number(row.id))
    setEditForm({
      number_next: row.number_next != null ? String(row.number_next) : '',
      prefix: String(row.prefix ?? ''),
      suffix: String(row.suffix ?? ''),
    })
    setSuccess(null)
  }

  const save = async () => {
    if (editingId == null) return
    setSaving(true)
    setError(null)
    try {
      await updateSequence(client, editingId, {
        number_next: editForm.number_next === '' ? undefined : Number(editForm.number_next),
        prefix: editForm.prefix,
        suffix: editForm.suffix,
      })
      setSuccess(t('ops.sequences.saveSuccess'))
      setEditingId(null)
      await refresh()
    } catch (err) {
      setError(formatRpcError(err, t('ops.sequences.saveError')))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.sequences.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.sequences.subtitle')}</p>
        </div>
      </div>

      <div className="ist-split" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('ops.sequences.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <span className="ist-subtitle">{t('common.recordCount', { count: total })}</span>
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={refresh} />}

      {editingId != null && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>{t('ops.sequences.editTitle')} #{editingId}</h3>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('ops.sequences.next')}</div>
              <input
                className="ist-input ist-input--boxed"
                type="number"
                value={editForm.number_next}
                onChange={(e) => setEditForm((f) => ({ ...f, number_next: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.sequences.prefix')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={editForm.prefix}
                onChange={(e) => setEditForm((f) => ({ ...f, prefix: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.sequences.suffix')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={editForm.suffix}
                onChange={(e) => setEditForm((f) => ({ ...f, suffix: e.target.value }))}
              />
            </label>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button type="button" className="ist-btn ist-btn--primary" disabled={saving} onClick={save}>
              {saving ? t('common.loading') : t('common.save')}
            </button>
            <button type="button" className="ist-btn ist-btn--outline" onClick={() => setEditingId(null)}>
              {t('common.cancel')}
            </button>
          </div>
        </div>
      )}

      {loading && !records.length ? (
        <LoadingState message={t('ops.sequences.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.sequences.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.sequences.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div
            className="ist-patient-list__head"
            style={{ gridTemplateColumns: '1.5fr 1fr 0.8fr 0.8fr 0.7fr 100px' }}
          >
            <span>{t('ops.sequences.name')}</span>
            <span>{t('ops.sequences.code')}</span>
            <span>{t('ops.sequences.prefix')}</span>
            <span>{t('ops.sequences.suffix')}</span>
            <span>{t('ops.sequences.next')}</span>
            <span>{t('common.actions')}</span>
          </div>
          {records.map((row) => (
            <div
              key={String(row.id)}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: '1.5fr 1fr 0.8fr 0.8fr 0.7fr 100px' }}
            >
              <span className="ist-patient-name">{String(row.name ?? row.rec_name ?? '—')}</span>
              <span className="ist-subtitle">{String(row.code ?? '—')}</span>
              <span className="ist-subtitle">{String(row.prefix ?? '—')}</span>
              <span className="ist-subtitle">{String(row.suffix ?? '—')}</span>
              <span className="ist-subtitle">{row.number_next != null ? String(row.number_next) : '—'}</span>
              <button
                type="button"
                className="ist-btn ist-btn--sm ist-btn--outline"
                onClick={() => openEdit(row)}
              >
                {t('common.edit')}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ─── Languages ─────────────────────────────────────────────────────────── */

export function LanguagesPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchLanguages(client)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.languages.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.languages.subtitle')}</p>
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={refresh} />}

      {loading && !records.length ? (
        <LoadingState message={t('ops.languages.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.languages.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.languages.empty')}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
          </p>
          <div className="ist-patient-list">
            <div
              className="ist-patient-list__head"
              style={{ gridTemplateColumns: '0.7fr 1.5fr 0.8fr 0.8fr 0.8fr' }}
            >
              <span>{t('ops.languages.code')}</span>
              <span>{t('ops.languages.name')}</span>
              <span>{t('ops.languages.direction')}</span>
              <span>{t('ops.languages.translatable')}</span>
              <span>{t('ops.languages.status')}</span>
            </div>
            {records.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '0.7fr 1.5fr 0.8fr 0.8fr 0.8fr' }}
              >
                <span className="ist-patient-name">{String(row.code ?? '—')}</span>
                <span className="ist-subtitle">{String(row.name ?? row.rec_name ?? '—')}</span>
                <span className="ist-subtitle">{String(row.direction ?? '—')}</span>
                <span className="ist-subtitle">{row.translatable ? 'Yes' : 'No'}</span>
                <span className="ist-subtitle">{row.active === false ? 'Inactive' : 'Active'}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

/* ─── Countries (polished) ──────────────────────────────────────────────── */

export function CountriesPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [debounced, setDebounced] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(search), 300)
    return () => clearTimeout(timer)
  }, [search])

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchCountries(client, debounced)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, debounced, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.countries.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.countries.subtitle')}</p>
        </div>
      </div>

      <div className="ist-split" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="ist-search">
          <svg className="ist-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="search"
            placeholder={t('ops.countries.search')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <span className="ist-subtitle">{t('common.recordCount', { count: total })}</span>
      </div>

      {error && <ErrorState message={error} onRetry={refresh} />}

      {loading && !records.length ? (
        <LoadingState message={t('ops.countries.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.countries.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.countries.empty')}</div>
      ) : (
        <div className="ist-patient-list">
          <div className="ist-patient-list__head" style={{ gridTemplateColumns: '0.6fr 0.6fr 2fr' }}>
            <span>{t('ops.countries.code')}</span>
            <span>{t('ops.countries.code3')}</span>
            <span>{t('ops.countries.name')}</span>
          </div>
          {records.map((row) => (
            <div
              key={String(row.id)}
              className="ist-patient-list__row"
              style={{ gridTemplateColumns: '0.6fr 0.6fr 2fr' }}
            >
              <span className="ist-patient-name">{String(row.code ?? '—')}</span>
              <span className="ist-subtitle">{String(row.code3 ?? '—')}</span>
              <span className="ist-subtitle">{String(row.name ?? row.rec_name ?? '—')}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ─── Companies + setup wizard lite ─────────────────────────────────────── */

export function CompaniesPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showWizard, setShowWizard] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState<{
    name: string
    code: string
    street: string
    city: string
    email: string
    website: string
  }>({
    name: IST_COMPANY_DEFAULTS.name,
    code: IST_COMPANY_DEFAULTS.code,
    street: IST_COMPANY_DEFAULTS.street,
    city: IST_COMPANY_DEFAULTS.city,
    email: IST_COMPANY_DEFAULTS.email,
    website: IST_COMPANY_DEFAULTS.website,
  })

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchCompanies(client)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
      if (r.available && r.total === 0) setShowWizard(true)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const save = async () => {
    if (!form.name.trim()) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      await createCompanySetup(client, form)
      setSuccess(t('ops.companies.setupSuccess'))
      setShowWizard(false)
      await refresh()
    } catch (err) {
      setError(formatRpcError(err, t('ops.companies.setupError')))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.companies.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.companies.subtitle')}</p>
        </div>
        {available && total === 0 && (
          <button type="button" className="ist-btn ist-btn--primary" onClick={() => setShowWizard(true)}>
            {t('ops.companies.setup')}
          </button>
        )}
      </div>

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={refresh} />}

      {showWizard && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-2)' }}>{t('ops.companies.setupTitle')}</h3>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('ops.companies.setupHint')}
          </p>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('ops.companies.name')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.companies.code')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.code}
                onChange={(e) => setForm((f) => ({ ...f, code: e.target.value }))}
              />
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('ops.companies.street')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.street}
                onChange={(e) => setForm((f) => ({ ...f, street: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.companies.city')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.city}
                onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
              />
            </label>
            <label>
              <div className="ist-label">{t('ops.companies.email')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
              />
            </label>
            <label style={{ gridColumn: '1 / -1' }}>
              <div className="ist-label">{t('ops.companies.website')}</div>
              <input
                className="ist-input ist-input--boxed"
                value={form.website}
                onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
              />
            </label>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button type="button" className="ist-btn ist-btn--primary" disabled={saving} onClick={save}>
              {saving ? t('common.loading') : t('ops.companies.createCompany')}
            </button>
            {total > 0 && (
              <button type="button" className="ist-btn ist-btn--outline" onClick={() => setShowWizard(false)}>
                {t('common.cancel')}
              </button>
            )}
          </div>
        </div>
      )}

      {loading && !records.length ? (
        <LoadingState message={t('ops.companies.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.companies.missing')}</div>
      ) : records.length === 0 && !showWizard ? (
        <div className="ist-notice">{t('ops.companies.empty')}</div>
      ) : records.length > 0 ? (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
          </p>
          <div className="ist-patient-list">
            <div className="ist-patient-list__head" style={{ gridTemplateColumns: '1.5fr 1fr' }}>
              <span>{t('ops.companies.name')}</span>
              <span>{t('ops.companies.party')}</span>
            </div>
            {records.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '1.5fr 1fr' }}
              >
                <span className="ist-patient-name">{String(row.rec_name ?? '—')}</span>
                <span className="ist-subtitle">
                  {Array.isArray(row.party) ? String(row.party[1] ?? row.party[0]) : String(row.party ?? '—')}
                </span>
              </div>
            ))}
          </div>
        </>
      ) : null}

      <SaoPanel
        compact
        title={t('ops.companies.saoTitle')}
        description={t('ops.companies.saoDesc')}
        instructions={[
          'Chart of accounts from template',
          'Fiscal years, periods, journals, taxes',
          'Employee / payroll company linking',
        ]}
      />
    </div>
  )
}

/* ─── Financial (list + invoice stub / SAO) ─────────────────────────────── */

export function FinancialPage() {
  const { t } = useTranslation()
  const { client } = useAuth()
  const [records, setRecords] = useState<Record<string, unknown>[]>([])
  const [total, setTotal] = useState(0)
  const [available, setAvailable] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showStub, setShowStub] = useState(false)
  const [parties, setParties] = useState<Record<string, unknown>[]>([])
  const [partyId, setPartyId] = useState('')
  const [invoiceType, setInvoiceType] = useState<'out' | 'in'>('out')
  const [saving, setSaving] = useState(false)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetchInvoices(client)
      setRecords(r.records)
      setTotal(r.total)
      setAvailable(r.available)
    } catch (err) {
      setError(formatRpcError(err, t('common.error')))
    } finally {
      setLoading(false)
    }
  }, [client, t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const openStub = async () => {
    setShowStub(true)
    setSuccess(null)
    try {
      const p = await fetchParties(client, '', 0, 80)
      setParties(p.records as unknown as Record<string, unknown>[])
    } catch {
      setParties([])
    }
  }

  const createStub = async () => {
    const pid = Number(partyId)
    if (!pid) return
    setSaving(true)
    setError(null)
    setSuccess(null)
    try {
      const id = await createInvoiceStub(client, { partyId: pid, type: invoiceType })
      setSuccess(t('ops.financial.stubSuccess', { id }))
      setShowStub(false)
      await refresh()
    } catch (err) {
      setError(
        formatRpcError(
          err,
          t('ops.financial.stubError'),
        ),
      )
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ist-patients">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('ops.financial.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('ops.financial.subtitle')}</p>
        </div>
        <button type="button" className="ist-btn ist-btn--primary" onClick={() => void openStub()}>
          {t('ops.financial.createStub')}
        </button>
      </div>

      <div
        className="ist-card ist-card--bordered"
        style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-6)' }}
        data-testid="financial-setup-checklist"
      >
        <h3 style={{ marginBottom: 'var(--space-2)' }}>{t('ops.financial.setupTitle')}</h3>
        <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
          {t('ops.financial.setupHint')}
        </p>
        <ol className="ist-subtitle" style={{ paddingLeft: '1.25rem', marginBottom: 'var(--space-4)' }}>
          <li style={{ marginBottom: '0.35rem' }}>
            <Link to="/companies">{t('ops.financial.setupStepCompany')}</Link>
          </li>
          <li style={{ marginBottom: '0.35rem' }}>
            <Link to="/currency">{t('ops.financial.setupStepCurrency')}</Link>
          </li>
          <li style={{ marginBottom: '0.35rem' }}>{t('ops.financial.setupStepCoa')}</li>
          <li style={{ marginBottom: '0.35rem' }}>{t('ops.financial.setupStepFiscal')}</li>
          <li style={{ marginBottom: '0.35rem' }}>{t('ops.financial.setupStepTax')}</li>
          <li style={{ marginBottom: '0.35rem' }}>{t('ops.financial.setupStepParty')}</li>
          <li style={{ marginBottom: '0.35rem' }}>{t('ops.financial.setupStepSmoke')}</li>
        </ol>
        <p className="ist-subtitle" style={{ marginBottom: 0 }}>
          <Link to="/setup">{t('setup.title')}</Link>
          {' · '}
          <Link to="/help?topic=wf-finance-setup">{t('ops.financial.setupHelpLink')}</Link>
          {' · '}
          <Link to="/help?topic=wf-close-period">{t('ops.financial.setupCloseLink')}</Link>
        </p>
      </div>

      <SaoPanel
        title={t('ops.financial.saoTitle')}
        description={t('ops.financial.saoDesc')}
        instructions={[
          t('ops.financial.saoInstrCoa'),
          t('ops.financial.saoInstrPost'),
          t('ops.financial.saoInstrJournals'),
        ]}
      />

      {success && <div className="ist-notice" style={{ marginBottom: 'var(--space-4)' }}>{success}</div>}
      {error && <ErrorState message={error} onRetry={refresh} />}

      {showStub && (
        <div className="ist-card ist-card--bordered" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h3 style={{ marginBottom: 'var(--space-2)' }}>{t('ops.financial.stubTitle')}</h3>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('ops.financial.stubHint')}
          </p>
          <div className="ist-grid ist-grid--2" style={{ gap: 'var(--space-4)' }}>
            <label>
              <div className="ist-label">{t('ops.financial.party')}</div>
              <Select value={partyId} onChange={(e) => setPartyId(e.target.value)}>
                <option value="">{t('ops.financial.selectParty')}</option>
                {parties.map((p) => (
                  <option key={String(p.id)} value={String(p.id)}>
                    {String(p.name ?? p.rec_name ?? p.id)}
                  </option>
                ))}
              </Select>
            </label>
            <label>
              <div className="ist-label">{t('ops.financial.type')}</div>
              <Select
                value={invoiceType}
                onChange={(e) => setInvoiceType(e.target.value as 'out' | 'in')}
              >
                <option value="out">{t('ops.financial.typeOut')}</option>
                <option value="in">{t('ops.financial.typeIn')}</option>
              </Select>
            </label>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
            <button
              type="button"
              className="ist-btn ist-btn--primary"
              disabled={saving || !partyId}
              onClick={() => void createStub()}
            >
              {saving ? t('common.loading') : t('common.save')}
            </button>
            <button type="button" className="ist-btn ist-btn--outline" onClick={() => setShowStub(false)}>
              {t('common.cancel')}
            </button>
          </div>
        </div>
      )}

      {loading && !records.length ? (
        <LoadingState message={t('ops.financial.loading')} />
      ) : !available ? (
        <div className="ist-notice">{t('ops.financial.missing')}</div>
      ) : records.length === 0 ? (
        <div className="ist-notice">{t('ops.financial.empty')}</div>
      ) : (
        <>
          <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
            {t('common.recordCount', { count: total })}
          </p>
          <div className="ist-patient-list">
            <div
              className="ist-patient-list__head"
              style={{ gridTemplateColumns: '0.8fr 1.2fr 0.6fr 0.9fr 0.7fr 0.7fr' }}
            >
              <span>{t('ops.financial.number')}</span>
              <span>{t('ops.financial.name')}</span>
              <span>{t('ops.financial.type')}</span>
              <span>{t('ops.financial.date')}</span>
              <span>{t('ops.financial.amount')}</span>
              <span>{t('ops.financial.state')}</span>
            </div>
            {records.map((row) => (
              <div
                key={String(row.id)}
                className="ist-patient-list__row"
                style={{ gridTemplateColumns: '0.8fr 1.2fr 0.6fr 0.9fr 0.7fr 0.7fr' }}
              >
                <span className="ist-patient-name">{String(row.number ?? '—')}</span>
                <span className="ist-subtitle">{String(row.rec_name ?? '—')}</span>
                <span className="ist-subtitle">{String(row.type ?? '—')}</span>
                <span className="ist-subtitle">{formatTrytonDate(row.invoice_date)}</span>
                <span className="ist-subtitle">{row.total_amount != null ? String(row.total_amount) : '—'}</span>
                <span className="ist-subtitle">{String(row.state ?? '—')}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
