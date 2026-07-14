import { TrytonClient } from '../lib/tryton/client'
import { routeForModel } from '../lib/tryton/menuRoutes'

export interface MenuRecord {
  id: number
  name: string
  parent: number | null
  childs: number[]
  action: string | null
  active: boolean
  sequence: number
  icon: string | null
}

export interface MenuNode extends MenuRecord {
  children: MenuNode[]
}

export interface ResolvedAction {
  actionType: string
  actionId: number
  resModel: string | null
  name: string | null
  /** Dedicated React route if mapped; otherwise null (use /menu/:id). */
  route: string | null
}

const MENU_FIELDS = [
  'id',
  'name',
  'parent',
  'childs',
  'action',
  'active',
  'sequence',
  'icon',
] as const

function asParentId(value: unknown): number | null {
  if (value == null || value === false) return null
  if (typeof value === 'number' && value > 0) return value
  if (Array.isArray(value) && typeof value[0] === 'number') return value[0]
  const n = Number(value)
  return Number.isFinite(n) && n > 0 ? n : null
}

function asIdArray(value: unknown): number[] {
  if (!Array.isArray(value)) return []
  return value
    .map((v) => (typeof v === 'number' ? v : Number(v)))
    .filter((n) => Number.isFinite(n) && n > 0)
}

function asActionRef(value: unknown): string | null {
  if (value == null || value === false) return null
  if (typeof value === 'string' && value.includes(',')) return value
  if (Array.isArray(value) && value.length >= 2) {
    return `${value[0]},${value[1]}`
  }
  return null
}

function normalizeMenu(row: Record<string, unknown>): MenuRecord {
  return {
    id: Number(row.id),
    name: String(row.name ?? row.rec_name ?? row.id),
    parent: asParentId(row.parent),
    childs: asIdArray(row.childs),
    action: asActionRef(row.action),
    active: row.active !== false,
    sequence: typeof row.sequence === 'number' ? row.sequence : Number(row.sequence) || 0,
    icon: row.icon != null && row.icon !== false ? String(row.icon) : null,
  }
}

/** Fetch all active UI menus and build a rooted tree (SAO order). */
export async function fetchMenuTree(client: TrytonClient): Promise<MenuNode[]> {
  const rows = (await client.call(
    'ir.ui.menu',
    'search_read',
    [['active', '=', true]],
    0,
    null,
    [
      ['sequence', 'ASC'],
      ['id', 'ASC'],
    ],
    [...MENU_FIELDS],
    {},
  )) as Record<string, unknown>[]

  const records = (rows ?? []).map(normalizeMenu)
  return buildMenuTree(records)
}

export function buildMenuTree(records: MenuRecord[]): MenuNode[] {
  const byId = new Map<number, MenuNode>()
  for (const r of records) {
    byId.set(r.id, { ...r, children: [] })
  }

  const roots: MenuNode[] = []
  for (const node of byId.values()) {
    if (node.parent != null && byId.has(node.parent)) {
      byId.get(node.parent)!.children.push(node)
    } else {
      roots.push(node)
    }
  }

  const sortRec = (nodes: MenuNode[]) => {
    nodes.sort((a, b) => a.sequence - b.sequence || a.id - b.id)
    for (const n of nodes) sortRec(n.children)
  }
  sortRec(roots)
  return roots
}

export function parseActionRef(
  action: string | null | undefined,
): { model: string; id: number } | null {
  if (!action || !action.includes(',')) return null
  const [model, idStr] = action.split(',', 2)
  const id = Number(idStr)
  if (!model || !Number.isFinite(id)) return null
  return { model, id }
}

/** Resolve ir.action.* behind a menu item. */
export async function resolveMenuAction(
  client: TrytonClient,
  menu: Pick<MenuRecord, 'action' | 'name'>,
): Promise<ResolvedAction | null> {
  const ref = parseActionRef(menu.action)
  if (!ref) return null

  if (ref.model === 'ir.action.act_window') {
    try {
      const rows = (await client.read('ir.action.act_window', [ref.id], [
        'id',
        'name',
        'res_model',
        'type',
      ])) as Record<string, unknown>[]
      const row = rows[0]
      if (!row) return null
      const resModel = row.res_model ? String(row.res_model) : null
      return {
        actionType: 'ir.action.act_window',
        actionId: ref.id,
        resModel,
        name: row.name != null ? String(row.name) : menu.name,
        route: routeForModel(resModel),
      }
    } catch {
      return {
        actionType: 'ir.action.act_window',
        actionId: ref.id,
        resModel: null,
        name: menu.name,
        route: null,
      }
    }
  }

  return {
    actionType: ref.model,
    actionId: ref.id,
    resModel: null,
    name: menu.name,
    route: null,
  }
}

/** Navigate target for a menu node (mapped route or generic browser). */
export async function resolveMenuHref(
  client: TrytonClient,
  node: MenuRecord,
): Promise<string | null> {
  if (!node.action) return null
  const resolved = await resolveMenuAction(client, node)
  if (!resolved) return `/menu/${node.id}`
  if (resolved.route) return resolved.route
  if (resolved.actionType === 'ir.action.act_window') return `/menu/${node.id}`
  // wizards / reports / urls — open generic page that explains limitation
  return `/menu/${node.id}`
}

export async function fetchMenuById(
  client: TrytonClient,
  menuId: number,
): Promise<MenuRecord | null> {
  try {
    const rows = await client.read('ir.ui.menu', [menuId], [...MENU_FIELDS])
    if (!rows[0]) return null
    return normalizeMenu(rows[0])
  } catch {
    return null
  }
}
