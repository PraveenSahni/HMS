/**
 * Help content loader — reads JSON from /help-content/{lang}/ (not hardcoded bodies).
 */

export type HelpCountry = 'AE' | 'QA' | '*'
export type HelpRole = string

export interface HelpIndexEntry {
  id: string
  title: string
  roles: string[]
  countries: string[]
  routes: string[]
  keywords: string[]
  version: string
  guided?: boolean
}

export interface HelpArticle extends HelpIndexEntry {
  body: string
  steps?: string[]
}

export interface HelpContext {
  role?: string
  country?: string
  route?: string
  lang?: 'en' | 'ar'
}

const cache = new Map<string, HelpIndexEntry[]>()
const articleCache = new Map<string, HelpArticle>()

function basePath(lang: string): string {
  return `/help-content/${lang}`
}

export async function loadHelpIndex(lang: 'en' | 'ar' = 'en'): Promise<HelpIndexEntry[]> {
  const key = `index:${lang}`
  if (cache.has(key)) return cache.get(key)!
  const res = await fetch(`${basePath(lang)}/index.json`)
  if (!res.ok) throw new Error(`Help index missing for ${lang}`)
  const data = (await res.json()) as HelpIndexEntry[]
  cache.set(key, data)
  return data
}

export async function loadHelpArticle(
  id: string,
  lang: 'en' | 'ar' = 'en',
): Promise<HelpArticle> {
  const key = `${lang}:${id}`
  if (articleCache.has(key)) return articleCache.get(key)!
  const res = await fetch(`${basePath(lang)}/${id}.json`)
  if (!res.ok) throw new Error(`Help article ${id} missing`)
  const data = (await res.json()) as HelpArticle
  articleCache.set(key, data)
  return data
}

export function matchesContext(entry: HelpIndexEntry, ctx: HelpContext): boolean {
  const role = ctx.role || '*'
  const country = (ctx.country || '*').toUpperCase()
  const route = ctx.route || ''

  const roleOk =
    entry.roles.includes('*') ||
    role === '*' ||
    entry.roles.map((r) => r.toLowerCase()).includes(role.toLowerCase())

  const countryOk =
    entry.countries.includes('*') ||
    country === '*' ||
    entry.countries.map((c) => c.toUpperCase()).includes(country)

  const routeOk =
    !route ||
    entry.routes.some((r) => route === r || route.startsWith(r + '/') || r === '/help')

  return roleOk && countryOk && (routeOk || !ctx.route)
}

export function searchHelp(
  entries: HelpIndexEntry[],
  query: string,
  ctx: HelpContext = {},
): HelpIndexEntry[] {
  const q = query.trim().toLowerCase()
  return entries
    .filter((e) => matchesContext(e, { ...ctx, route: undefined }))
    .filter((e) => {
      if (!q) return true
      const hay = [e.title, e.id, ...e.keywords, ...e.routes].join(' ').toLowerCase()
      return hay.includes(q)
    })
}

export function contextualHelp(
  entries: HelpIndexEntry[],
  ctx: HelpContext,
): HelpIndexEntry[] {
  const route = ctx.route || ''
  return entries.filter((e) => {
    if (!matchesContext(e, { ...ctx, route: undefined })) return false
    return e.routes.some((r) => route === r || (r !== '/help' && route.startsWith(r)))
  })
}

/** Pure helpers exported for unit tests without fetch */
export const helpTestUtils = {
  matchesContext,
  searchHelp,
  contextualHelp,
}
