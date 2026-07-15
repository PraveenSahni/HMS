/**
 * Help content loader — reads JSON from /help-content/{lang}/ (not hardcoded bodies).
 *
 * Layout adaptation: flat JSON + roles[] metadata (equivalent to en/common, en/admin folders).
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
  published?: boolean
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
  includeUnpublished?: boolean
}

const PUBLISH_OVERRIDE_KEY = 'ist-help-publish-overrides'

const cache = new Map<string, HelpIndexEntry[]>()
const articleCache = new Map<string, HelpArticle>()

function basePath(lang: string): string {
  return `/help-content/${lang}`
}

export function getPublishOverrides(): Record<string, boolean> {
  try {
    return JSON.parse(localStorage.getItem(PUBLISH_OVERRIDE_KEY) || '{}') as Record<string, boolean>
  } catch {
    return {}
  }
}

export function setPublishOverride(id: string, published: boolean): void {
  const map = getPublishOverrides()
  map[id] = published
  localStorage.setItem(PUBLISH_OVERRIDE_KEY, JSON.stringify(map))
  cache.clear()
  articleCache.clear()
}

export function clearPublishOverrides(): void {
  localStorage.removeItem(PUBLISH_OVERRIDE_KEY)
  cache.clear()
  articleCache.clear()
}

export function isPublished(entry: HelpIndexEntry): boolean {
  const overrides = getPublishOverrides()
  if (Object.prototype.hasOwnProperty.call(overrides, entry.id)) {
    return overrides[entry.id]
  }
  return entry.published !== false
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

  if (!ctx.includeUnpublished && !isPublished(entry)) return false

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

export const ONBOARDING_ITEMS = [
  { id: 'login-lang', label_en: 'Sign in and set language EN/AR', label_ar: 'تسجيل الدخول وتعيين اللغة' },
  { id: 'help-filters', label_en: 'Set Help role and country filters', label_ar: 'تعيين دور ودولة المساعدة' },
  {
    id: 'using-workspace',
    label_en: 'Open Workspace (/workspace) for SAO wizards inside IST',
    label_ar: 'فتح مساحة العمل للمعالجات داخل IST',
  },
  { id: 'setup-hub', label_en: 'Open Setup Hub (/setup) and review order', label_ar: 'فتح مركز الإعداد ومراجعة الترتيب' },
  {
    id: 'setup-companies',
    label_en: '1. Companies — UAE AED and/or Qatar QAR entity',
    label_ar: '1. الشركات — كيان الإمارات AED و/أو قطر QAR',
  },
  {
    id: 'setup-currency',
    label_en: '2. Currency — confirm AED / QAR',
    label_ar: '2. العملات — تأكيد AED / QAR',
  },
  {
    id: 'setup-admin',
    label_en: '3. Administration — users, groups, sequences',
    label_ar: '3. الإدارة — المستخدمون والمجموعات والتسلسلات',
  },
  { id: 'setup-party', label_en: '4. Party — master parties (synthetic in non-prod)', label_ar: '4. الأطراف — بيانات رئيسية اصطناعية خارج الإنتاج' },
  { id: 'setup-product', label_en: '5. Product — catalogs for services/pharmacy', label_ar: '5. المنتجات — كتالوجات الخدمات/الصيدلية' },
  { id: 'setup-stock', label_en: '6. Inventory & Stock — locations under company', label_ar: '6. المخزون — مواقع تحت الشركة' },
  { id: 'setup-calendar', label_en: '7. Calendar — calendars if module used', label_ar: '7. التقويم — إن كان مفعّلاً' },
  {
    id: 'setup-financial',
    label_en: '8. Financial — CoA/FY in SAO; draft invoice smoke',
    label_ar: '8. المالية — دليل الحسابات في SAO واختبار مسودة فاتورة',
  },
  {
    id: 'setup-health',
    label_en: '9. Health — institution, patients, appointments (+ lab/Rx/beds)',
    label_ar: '9. الصحة — المؤسسة والمرضى والمواعيد (+ مختبر/صيدلية/أسرة)',
  },
  { id: 'find-patient', label_en: 'Find a synthetic IST-P-* patient', label_ar: 'العثور على مريض اصطناعي' },
  { id: 'appointments', label_en: 'Open Appointments day list', label_ar: 'فتح قائمة المواعيد' },
  { id: 'guided-wf', label_en: 'Complete guided workflow wf-system-setup', label_ar: 'إكمال سير العمل الإرشادي لإعداد النظام' },
  { id: 'synthetic-policy', label_en: 'Read synthetic data policy', label_ar: 'قراءة سياسة البيانات الاصطناعية' },
] as const

export function getOnboardingState(): Record<string, boolean> {
  try {
    return JSON.parse(localStorage.getItem('ist-help-onboarding') || '{}') as Record<string, boolean>
  } catch {
    return {}
  }
}

export function setOnboardingItem(id: string, done: boolean): void {
  const state = getOnboardingState()
  state[id] = done
  localStorage.setItem('ist-help-onboarding', JSON.stringify(state))
}

export function getFeedback(id: string): 'yes' | 'no' | null {
  try {
    const map = JSON.parse(localStorage.getItem('ist-help-feedback') || '{}') as Record<string, string>
    const v = map[id]
    return v === 'yes' || v === 'no' ? v : null
  } catch {
    return null
  }
}

export function setFeedback(id: string, value: 'yes' | 'no'): void {
  const map = JSON.parse(localStorage.getItem('ist-help-feedback') || '{}') as Record<string, string>
  map[id] = value
  localStorage.setItem('ist-help-feedback', JSON.stringify(map))
}

/** Pure helpers exported for unit tests without fetch */
export const helpTestUtils = {
  matchesContext,
  searchHelp,
  contextualHelp,
  isPublished,
}
