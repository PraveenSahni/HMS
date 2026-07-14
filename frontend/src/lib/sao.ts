/**
 * SAO (legacy Tryton web client) deep-link helpers.
 * Prefer same-origin /sao/ (nginx proxy). Direct :8000 is localhost-only after harden.
 */

export const PRODUCTION_HOST = 'health.irisstar.tech'
export const SAO_PROXY_PATH = '/sao/'
/** @deprecated trytond is bound to 127.0.0.1 — use saoUrl() /sao/ instead */
export const SAO_DIRECT_URL = `https://${PRODUCTION_HOST}${SAO_PROXY_PATH}`

/** Prefer nginx /sao/ on production hosts; same-origin path elsewhere when possible. */
export function saoUrl(): string {
  if (typeof window === 'undefined') return SAO_DIRECT_URL
  const host = window.location.hostname
  if (
    host === PRODUCTION_HOST ||
    host === '34.18.116.146' ||
    host === 'localhost' ||
    host === '127.0.0.1'
  ) {
    return `${window.location.origin}${SAO_PROXY_PATH}`
  }
  // Any other deployed hostname: still prefer same-origin proxy
  if (host && !host.startsWith('192.168.') && host !== '') {
    return `${window.location.origin}${SAO_PROXY_PATH}`
  }
  return SAO_DIRECT_URL
}

export const MODULE_SERVER_INSTRUCTIONS = [
  'SSH to gnuhealth-his-01 as the GNU Health OS user.',
  'Activate / upgrade marked modules, e.g.:',
  '  trytond-admin -c /path/to/trytond.conf -d gnuhealth -u MODULE --activate-dependencies',
  'Or open SAO → Administration → Modules → Mark for activation → Perform pending upgrades.',
  'Restart trytond after major module changes if services do not reload automatically.',
] as const
