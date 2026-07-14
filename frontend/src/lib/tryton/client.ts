/**
 * Tryton 7 / GNU Health 5 JSON-RPC client for browser use.
 * Dev: routes through Vite proxy (/api/tryton) to avoid CORS.
 * Prod: nginx proxies /api/tryton/<database>/ → Tryton /<database>/.
 */

export class TrytonError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'TrytonError'
  }
}

/** Prefer real RPC/HTTP message over a generic UI fallback. */
export function formatRpcError(err: unknown, fallback: string): string {
  if (err instanceof TrytonError) return err.message
  if (err instanceof Error && err.message.trim()) return err.message
  return fallback
}

export interface TrytonConfig {
  url: string
  database: string
  username?: string
  password?: string
  language?: string
  useProxy?: boolean
}

export interface AuthSession {
  uid: number
  username: string
  database: string
  language: string
  sessionToken: string
}

type RpcPayload = {
  jsonrpc?: string
  method: string
  params?: unknown[]
  id?: number
}

const DATABASE_KEY = 'ist-health-database'

/** Tryton 7: Authorization: Session base64(login:user_id:session) */
function sessionAuthHeader(username: string, uid: number, sessionToken: string): string {
  const raw = `${username}:${uid}:${sessionToken}`
  // UTF-8–safe base64 (btoa alone throws on non-Latin1)
  const bytes = new TextEncoder().encode(raw)
  let binary = ''
  for (let i = 0; i < bytes.length; i += 1) binary += String.fromCharCode(bytes[i]!)
  return `Session ${btoa(binary)}`
}

/** Normalize Tryton JSON-RPC success/error payloads (envelope or legacy shapes). */
function unwrapRpcPayload(data: unknown, method: string, requestId: number): unknown {
  if (data == null) {
    throw new TrytonError(`RPC ${method} failed: empty response`)
  }

  // Standard Tryton 7: { id, result } | { id, error }
  if (typeof data === 'object' && !Array.isArray(data)) {
    const obj = data as { result?: unknown; error?: unknown }
    if (obj.error != null) {
      const err = obj.error
      const message = Array.isArray(err)
        ? err.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).filter(Boolean).join(' — ')
        : (err as { message?: string; data?: string }).message ??
          (err as { message?: string; data?: string }).data ??
          JSON.stringify(err)
      throw new TrytonError(`RPC ${method} failed: ${message}`)
    }
    if ('result' in obj) return obj.result
  }

  // Login bare result [uid, session] — do not treat as [requestId, result]
  if (
    method === 'common.db.login' &&
    Array.isArray(data) &&
    data.length === 2 &&
    typeof data[0] === 'number' &&
    typeof data[1] === 'string'
  ) {
    return data
  }

  // Legacy Tryton list form: [id, result] or [id, null, error]
  if (Array.isArray(data) && data.length >= 2 && data[0] === requestId) {
    if (data.length >= 3 && data[1] == null) {
      throw new TrytonError(`RPC ${method} failed: ${JSON.stringify(data[2])}`)
    }
    return data[1]
  }

  // Bare result (no envelope)
  return data
}

function defaultDatabase(): string {
  try {
    const stored = localStorage.getItem(DATABASE_KEY)
    if (stored && /^[a-zA-Z0-9_-]+$/.test(stored)) {
      // DB was renamed gnuhealth → isthealth; migrate stale local preference
      if (stored === 'gnuhealth') {
        persistDatabasePreference('isthealth')
        return 'isthealth'
      }
      return stored
    }
  } catch {
    /* ignore */
  }
  return import.meta.env.VITE_TRYTON_DATABASE ?? 'isthealth'
}

export function persistDatabasePreference(database: string): void {
  try {
    localStorage.setItem(DATABASE_KEY, database)
  } catch {
    /* ignore */
  }
}

export function readDatabasePreference(): string {
  return defaultDatabase()
}

let requestId = 0

export class TrytonClient {
  private config: TrytonConfig
  private session: AuthSession | null = null

  constructor(config: TrytonConfig) {
    this.config = config
  }

  get database(): string {
    return this.config.database
  }

  setDatabase(database: string): void {
    const safe = database.trim()
    if (!safe || !/^[a-zA-Z0-9_-]+$/.test(safe)) {
      throw new TrytonError(`Invalid database name: ${database}`)
    }
    this.config.database = safe
    persistDatabasePreference(safe)
  }

  get rpcUrl(): string {
    const db = this.config.database
    if (this.config.useProxy !== false) {
      return `/api/tryton/${db}/`
    }
    const base = this.config.url.replace(/\/$/, '')
    return `${base}/${db}/`
  }

  /** Unauthenticated list endpoint (Tryton server root via proxy). */
  get listRpcUrl(): string {
    if (this.config.useProxy !== false) {
      return '/api/tryton/'
    }
    const base = this.config.url.replace(/\/$/, '')
    return `${base}/`
  }

  get isAuthenticated(): boolean {
    return this.session !== null
  }

  get currentSession(): AuthSession | null {
    return this.session
  }

  restoreSession(raw: string | null): boolean {
    if (!raw) return false
    try {
      const parsed = JSON.parse(raw) as AuthSession
      if (parsed.uid && parsed.database && parsed.sessionToken) {
        // DB rename: drop stale sessions bound to the old name (token is DB-scoped)
        if (parsed.database === 'gnuhealth') {
          return false
        }
        this.config.database = parsed.database
        this.session = {
          uid: parsed.uid,
          username: parsed.username,
          database: parsed.database,
          language: parsed.language ?? 'en',
          sessionToken: parsed.sessionToken,
        }
        return true
      }
    } catch {
      /* ignore */
    }
    return false
  }

  serializeSession(): string | null {
    if (!this.session) return null
    return JSON.stringify(this.session)
  }

  /**
   * List PostgreSQL databases Tryton can use (no auth).
   * Uses server root (/api/tryton/) — DB path returns 401 for list.
   * Falls back to the configured default if the call fails.
   */
  async listDatabases(): Promise<string[]> {
    try {
      const result = await this.rpcAt(this.listRpcUrl, 'common.db.list', [], true)
      const list = Array.isArray(result)
        ? result.map((d) => String(d)).filter(Boolean)
        : []
      if (list.length) return list
    } catch {
      /* proxy / server may be unavailable during first paint */
    }
    return [this.config.database || 'isthealth']
  }

  async authenticate(username: string, password: string): Promise<AuthSession> {
    const language = this.config.language ?? 'en'
    const params: unknown[] = [username, { password }, language]
    const result = await this.rpc('common.db.login', params, true)
    const [uid, sessionToken] = Array.isArray(result) ? result : [result, null]
    if (!uid || !sessionToken) {
      throw new TrytonError(`Authentication failed for '${username}'`)
    }

    this.session = {
      uid: Number(uid),
      username,
      database: this.config.database,
      language,
      sessionToken: String(sessionToken),
    }
    persistDatabasePreference(this.config.database)
    return this.session
  }

  logout(): void {
    this.session = null
  }

  async call(model: string, method: string, ...args: unknown[]): Promise<unknown> {
    if (!this.session) throw new TrytonError('Not authenticated')
    return this.rpc(`model.${model}.${method}`, args)
  }

  async search(
    model: string,
    domain: unknown[] = [],
    offset = 0,
    limit: number | null = null,
    order: unknown[] | null = null,
    context: Record<string, unknown> = {},
  ): Promise<number[]> {
    try {
      const result = await this.call(model, 'search', domain, offset, limit, order, context)
      return result as number[]
    } catch (err) {
      // Tryton rejects ORDER BY on Function fields (e.g. rec_name) with opaque errors —
      // retry unordered so list pages still load.
      if (order != null) {
        const result = await this.call(model, 'search', domain, offset, limit, null, context)
        return result as number[]
      }
      throw err
    }
  }

  async searchCount(model: string, domain: unknown[] = []): Promise<number> {
    const result = await this.call(model, 'search_count', domain, {})
    return Number(result)
  }

  async read(
    model: string,
    ids: number[],
    fields?: string[],
    context: Record<string, unknown> = {},
  ): Promise<Record<string, unknown>[]> {
    if (!ids.length) return []
    // Tryton 7 requires a trailing context dict on model.read
    const result = await this.call(model, 'read', ids, fields ?? [], context)
    return result as Record<string, unknown>[]
  }

  async create(model: string, values: Record<string, unknown>[]): Promise<number[]> {
    if (!values.length) return []
    const result = await this.call(model, 'create', values, {})
    return result as number[]
  }

  async write(
    model: string,
    ids: number[],
    values: Record<string, unknown>,
  ): Promise<boolean> {
    if (!ids.length) return true
    await this.call(model, 'write', ids, values, {})
    return true
  }

  async modelExists(model: string): Promise<boolean> {
    try {
      await this.search(model, [], 0, 1)
      return true
    } catch {
      return false
    }
  }

  /** Batch-resolve Many2One ids → display labels via rec_name/name */
  async resolveNames(
    model: string,
    ids: Array<number | null | undefined>,
  ): Promise<Map<number, string>> {
    const unique = [...new Set(ids.filter((id): id is number => typeof id === 'number' && id > 0))]
    const map = new Map<number, string>()
    if (!unique.length) return map
    try {
      // Prefer rec_name only — many GNU Health models have no `name` field
      const rows = await this.read(model, unique, ['id', 'rec_name'])
      for (const row of rows) {
        const id = Number(row.id)
        map.set(id, String(row.rec_name ?? id))
      }
    } catch {
      for (const id of unique) map.set(id, String(id))
    }
    return map
  }

  private async rpc(method: string, params: unknown[], authAttempt = false): Promise<unknown> {
    return this.rpcAt(this.rpcUrl, method, params, authAttempt)
  }

  private async rpcAt(
    url: string,
    method: string,
    params: unknown[],
    authAttempt = false,
  ): Promise<unknown> {
    requestId += 1
    const payload: RpcPayload = { method, params, id: requestId }
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }

    if (!authAttempt && this.session) {
      headers.Authorization = sessionAuthHeader(
        this.session.username,
        this.session.uid,
        this.session.sessionToken,
      )
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify(payload),
    })

    if (response.status === 401 && !authAttempt) {
      throw new TrytonError('Session expired or unauthorized')
    }
    if (response.status >= 400) {
      throw new TrytonError(
        `HTTP ${response.status}: ${(await response.text()).slice(0, 300)}`,
      )
    }

    let data: unknown
    try {
      data = await response.json()
    } catch {
      throw new TrytonError('Non-JSON response from server')
    }

    return unwrapRpcPayload(data, method, requestId)
  }
}

export function createClient(overrides?: Partial<TrytonConfig>): TrytonClient {
  return new TrytonClient({
    url: import.meta.env.VITE_TRYTON_URL ?? 'https://health.irisstar.tech',
    database: readDatabasePreference(),
    language: 'en',
    useProxy: import.meta.env.VITE_USE_PROXY !== 'false',
    ...overrides,
  })
}
