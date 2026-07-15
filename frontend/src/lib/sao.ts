/**
 * SAO (legacy Tryton web client) deep-link helpers + IST session handoff.
 * Prefer same-origin /sao/ (nginx proxy). Direct :8000 is localhost-only after harden.
 *
 * Same-origin localStorage bridge:
 *   React: ist-health-session → { uid, username, database, sessionToken }
 *   SAO:   sao_session_{db}  → { login, user_id, session }
 * SAO only auto-restores when the URL hash includes the database (#isthealth).
 */

import type { AuthSession } from './tryton/client'

export const PRODUCTION_HOST = 'health.irisstar.tech'
export const SAO_PROXY_PATH = '/sao/'
/** @deprecated trytond is bound to 127.0.0.1 — use saoUrl() /sao/ instead */
export const SAO_DIRECT_URL = `https://${PRODUCTION_HOST}${SAO_PROXY_PATH}`

export const IST_SESSION_KEY = 'ist-health-session'

export function saoSessionStorageKey(database: string): string {
  return `sao_session_${database}`
}

export function saoContextStorageKey(database: string): string {
  return `sao_context_${database}`
}

/** Write SAO localStorage so Sao.Session.restore() skips the login dialog. */
export function handoffSaoSession(session: AuthSession): void {
  if (typeof window === 'undefined') return
  if (!session.database || !session.username || !session.sessionToken || !session.uid) return
  try {
    localStorage.setItem(
      saoSessionStorageKey(session.database),
      JSON.stringify({
        login: session.username,
        user_id: session.uid,
        session: session.sessionToken,
      }),
    )
  } catch {
    /* private mode / quota */
  }
}

/** Clear SAO session(+context) for a database, or all known sao_session_* keys. */
export function clearSaoSession(database?: string | null): void {
  if (typeof window === 'undefined') return
  try {
    if (database) {
      localStorage.removeItem(saoSessionStorageKey(database))
      try {
        sessionStorage.removeItem(saoContextStorageKey(database))
      } catch {
        /* ignore */
      }
      return
    }
    const toRemove: string[] = []
    for (let i = 0; i < localStorage.length; i += 1) {
      const key = localStorage.key(i)
      if (key && key.startsWith('sao_session_')) toRemove.push(key)
    }
    for (const key of toRemove) localStorage.removeItem(key)
  } catch {
    /* ignore */
  }
}

/**
 * Prefer nginx /sao/ on production hosts; same-origin path elsewhere when possible.
 * Include #database so Sao.Session.get_credentials restores without a second login.
 */
export function saoUrl(database?: string | null): string {
  const db = (database || '').trim()
  const hash = db ? `#${encodeURIComponent(db)}` : ''
  if (typeof window === 'undefined') return `${SAO_DIRECT_URL}${hash}`
  const host = window.location.hostname
  if (
    host === PRODUCTION_HOST ||
    host === '34.18.116.146' ||
    host === 'localhost' ||
    host === '127.0.0.1'
  ) {
    return `${window.location.origin}${SAO_PROXY_PATH}${hash}`
  }
  // Any other deployed hostname: still prefer same-origin proxy
  if (host && !host.startsWith('192.168.') && host !== '') {
    return `${window.location.origin}${SAO_PROXY_PATH}${hash}`
  }
  return `${SAO_DIRECT_URL}${hash}`
}

export const MODULE_SERVER_INSTRUCTIONS = [
  'SSH to gnuhealth-his-01 as the GNU Health OS user.',
  'Activate / upgrade marked modules, e.g.:',
  '  trytond-admin -c /path/to/trytond.conf -d gnuhealth -u MODULE --activate-dependencies',
  'Or open SAO → Administration → Modules → Mark for activation → Perform pending upgrades.',
  'Restart trytond after major module changes if services do not reload automatically.',
] as const
