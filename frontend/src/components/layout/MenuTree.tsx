import { useCallback, useEffect, useMemo, useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../../contexts/AuthContext'
import {
  fetchMenuTree,
  resolveMenuHref,
  type MenuNode,
} from '../../services/menuApi'

const EXPANDED_KEY = 'ist-health-menu-expanded'
const CACHE_KEY = 'ist-health-menu-tree'

function loadExpanded(): Set<number> {
  try {
    const raw = localStorage.getItem(EXPANDED_KEY)
    if (!raw) return new Set()
    const ids = JSON.parse(raw) as number[]
    return new Set(ids.filter((n) => typeof n === 'number'))
  } catch {
    return new Set()
  }
}

function saveExpanded(ids: Set<number>) {
  try {
    localStorage.setItem(EXPANDED_KEY, JSON.stringify([...ids]))
  } catch {
    /* ignore */
  }
}

function IconChevron({ open }: { open: boolean }) {
  return (
    <span className={`ist-menu-tree__chevron${open ? ' is-open' : ''}`} aria-hidden="true">
      <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
        <path
          d="M3.2 1.5L7.2 5L3.2 8.5"
          stroke="currentColor"
          strokeWidth="1.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </span>
  )
}

function IconFolder({ open }: { open: boolean }) {
  return (
    <span className="ist-menu-tree__icon" aria-hidden="true">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        {open ? (
          <path
            d="M1.5 4.5h11v6.2a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1V4.5Zm0 0V3.2a1 1 0 0 1 1-1H5l1.2 1.3H11.5a1 1 0 0 1 1 1v.999"
            stroke="currentColor"
            strokeWidth="1.1"
            strokeLinejoin="round"
          />
        ) : (
          <path
            d="M1.5 3.5a1 1 0 0 1 1-1H5l1.2 1.3H11.5a1 1 0 0 1 1 1V10.5a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1V3.5Z"
            stroke="currentColor"
            strokeWidth="1.1"
            strokeLinejoin="round"
          />
        )}
      </svg>
    </span>
  )
}

function IconLeaf() {
  return (
    <span className="ist-menu-tree__icon" aria-hidden="true">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <rect x="2.5" y="2" width="9" height="10" rx="1" stroke="currentColor" strokeWidth="1.1" />
        <path d="M4.5 5h5M4.5 7.5h5M4.5 10h3" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" />
      </svg>
    </span>
  )
}

function MenuTreeNode({
  node,
  depth,
  expanded,
  onToggle,
  onLeafClick,
}: {
  node: MenuNode
  depth: number
  expanded: Set<number>
  onToggle: (id: number) => void
  onLeafClick: (node: MenuNode) => void
}) {
  const hasChildren = node.children.length > 0
  const isOpen = expanded.has(node.id)
  const isLeaf = !hasChildren

  const handleClick = () => {
    if (hasChildren) {
      onToggle(node.id)
      return
    }
    onLeafClick(node)
  }

  const padStyle = { paddingInlineStart: `calc(var(--space-3) + ${depth * 0.85}rem)` }

  if (isLeaf && node.action) {
    // Leaves with actions: use button that resolves route (may be async)
    return (
      <li className="ist-menu-tree__item">
        <button
          type="button"
          className="ist-menu-tree__row ist-menu-tree__row--leaf"
          style={padStyle}
          onClick={() => onLeafClick(node)}
          title={node.name}
        >
          <span className="ist-menu-tree__chevron ist-menu-tree__chevron--spacer" aria-hidden="true" />
          <IconLeaf />
          <span className="ist-menu-tree__label">{node.name}</span>
        </button>
      </li>
    )
  }

  return (
    <li className="ist-menu-tree__item">
      <button
        type="button"
        className={`ist-menu-tree__row${hasChildren ? '' : ' ist-menu-tree__row--leaf'}`}
        style={padStyle}
        onClick={handleClick}
        aria-expanded={hasChildren ? isOpen : undefined}
        title={node.name}
      >
        {hasChildren ? <IconChevron open={isOpen} /> : (
          <span className="ist-menu-tree__chevron ist-menu-tree__chevron--spacer" aria-hidden="true" />
        )}
        {hasChildren ? <IconFolder open={isOpen} /> : <IconLeaf />}
        <span className="ist-menu-tree__label">{node.name}</span>
      </button>
      {hasChildren && isOpen && (
        <ul className="ist-menu-tree__children">
          {node.children.map((child) => (
            <MenuTreeNode
              key={child.id}
              node={child}
              depth={depth + 1}
              expanded={expanded}
              onToggle={onToggle}
              onLeafClick={onLeafClick}
            />
          ))}
        </ul>
      )}
    </li>
  )
}

const QUICK_LINKS: Array<{ to: string; key: string; end?: boolean }> = [
  { to: '/', key: 'dashboard', end: true },
  { to: '/setup', key: 'setup' },
  { to: '/workspace', key: 'workspace' },
  { to: '/patients', key: 'patients' },
  { to: '/appointments', key: 'appointments' },
  { to: '/laboratory', key: 'laboratory' },
  { to: '/help', key: 'help' },
]

export function MenuTree() {
  const { t } = useTranslation()
  const { client, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [tree, setTree] = useState<MenuNode[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<Set<number>>(() => loadExpanded())
  const [pendingId, setPendingId] = useState<number | null>(null)

  const load = useCallback(async () => {
    if (!isAuthenticated) return
    setLoading(true)
    setError(null)
    try {
      // Prefer fresh tree; fall back to session cache on failure
      const nodes = await fetchMenuTree(client)
      setTree(nodes)
      try {
        sessionStorage.setItem(CACHE_KEY, JSON.stringify(nodes))
      } catch {
        /* ignore */
      }
      // Auto-expand first level roots once if nothing stored
      if (loadExpanded().size === 0 && nodes.length) {
        const initial = new Set(nodes.map((n) => n.id))
        setExpanded(initial)
        saveExpanded(initial)
      }
    } catch {
      try {
        const cached = sessionStorage.getItem(CACHE_KEY)
        if (cached) {
          setTree(JSON.parse(cached) as MenuNode[])
          setError(null)
        } else {
          setError(t('nav.menuLoadError'))
        }
      } catch {
        setError(t('nav.menuLoadError'))
      }
    } finally {
      setLoading(false)
    }
  }, [client, isAuthenticated, t])

  useEffect(() => {
    load()
  }, [load])

  const onToggle = useCallback((id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      saveExpanded(next)
      return next
    })
  }, [])

  const onLeafClick = useCallback(
    async (node: MenuNode) => {
      if (!node.action) {
        navigate(`/menu/${node.id}`)
        return
      }
      setPendingId(node.id)
      try {
        const href = await resolveMenuHref(client, node)
        navigate(href ?? `/menu/${node.id}`)
      } catch {
        navigate(`/menu/${node.id}`)
      } finally {
        setPendingId(null)
      }
    },
    [client, navigate],
  )

  const rootCount = useMemo(() => tree.length, [tree])

  return (
    <div className="ist-menu-tree">
      <div className="ist-menu-tree__quick">
        <div className="ist-nav-group__label">{t('nav.favorites')}</div>
        <ul className="ist-nav ist-menu-tree__favorites">
          {QUICK_LINKS.map(({ to, key, end }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={end}
                className={({ isActive }) =>
                  `ist-nav__link${isActive ? ' is-active' : ''}`
                }
              >
                {t(`nav.${key}`)}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>

      <div className="ist-nav-group__label">
        {t('nav.menuTree')}
        {rootCount > 0 ? ` · ${rootCount}` : ''}
      </div>

      {loading && <div className="ist-menu-tree__status">{t('nav.menuLoading')}</div>}
      {error && (
        <div className="ist-menu-tree__status ist-menu-tree__status--error">
          {error}
          <button type="button" className="ist-btn ist-btn--outline ist-btn--sm" onClick={load}>
            {t('common.retry')}
          </button>
        </div>
      )}
      {!loading && !error && tree.length === 0 && (
        <div className="ist-menu-tree__status">{t('nav.menuEmpty')}</div>
      )}

      <nav className="ist-menu-tree__nav" aria-label={t('nav.menuTree')}>
        <ul className="ist-menu-tree__list">
          {tree.map((node) => (
            <MenuTreeNode
              key={node.id}
              node={node}
              depth={0}
              expanded={expanded}
              onToggle={onToggle}
              onLeafClick={onLeafClick}
            />
          ))}
        </ul>
      </nav>
      {pendingId != null && (
        <div className="ist-menu-tree__pending" aria-live="polite">
          {t('common.loading')}
        </div>
      )}
    </div>
  )
}
