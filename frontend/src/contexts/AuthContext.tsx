import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { createClient, TrytonClient, TrytonError } from '../lib/tryton/client'

const SESSION_KEY = 'ist-health-session'

interface AuthContextValue {
  client: TrytonClient
  isAuthenticated: boolean
  username: string | null
  uid: number | null
  database: string
  login: (username: string, password: string, database?: string) => Promise<void>
  logout: () => void
  setDatabase: (database: string) => void
  listDatabases: () => Promise<string[]>
  error: string | null
  clearError: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const client = useMemo(() => createClient(), [])
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const restored = client.restoreSession(localStorage.getItem(SESSION_KEY))
    if (!restored) localStorage.removeItem(SESSION_KEY)
    return restored
  })
  const [username, setUsername] = useState<string | null>(
    () => client.currentSession?.username ?? null,
  )
  const [uid, setUid] = useState<number | null>(
    () => client.currentSession?.uid ?? null,
  )
  const [database, setDatabaseState] = useState(() => client.database)
  const [error, setError] = useState<string | null>(null)

  const setDatabase = useCallback(
    (db: string) => {
      client.setDatabase(db)
      setDatabaseState(client.database)
    },
    [client],
  )

  const listDatabases = useCallback(() => client.listDatabases(), [client])

  const login = useCallback(
    async (user: string, password: string, db?: string) => {
      setError(null)
      try {
        if (db) {
          client.setDatabase(db)
          setDatabaseState(client.database)
        }
        const session = await client.authenticate(user, password)
        localStorage.setItem(SESSION_KEY, client.serializeSession()!)
        setIsAuthenticated(true)
        setUsername(session.username)
        setUid(session.uid)
        setDatabaseState(session.database)
      } catch (err) {
        if (err instanceof TrytonError) {
          const msg = err.message.toLowerCase()
          if (
            msg.includes('authentication failed') ||
            msg.includes('401') ||
            msg.includes('unauthorized')
          ) {
            setError('invalid')
          } else if (msg.includes('http') || msg.includes('non-json') || msg.includes('reach')) {
            setError('connection')
          } else {
            setError(err.message)
          }
        } else {
          setError('connection')
        }
        throw err
      }
    },
    [client],
  )

  const logout = useCallback(() => {
    client.logout()
    localStorage.removeItem(SESSION_KEY)
    try {
      sessionStorage.removeItem('ist-health-menu-tree')
    } catch {
      /* ignore */
    }
    setIsAuthenticated(false)
    setUsername(null)
    setUid(null)
    setError(null)
  }, [client])

  const clearError = useCallback(() => setError(null), [])

  const value = useMemo(
    () => ({
      client,
      isAuthenticated,
      username,
      uid,
      database,
      login,
      logout,
      setDatabase,
      listDatabases,
      error,
      clearError,
    }),
    [
      client,
      isAuthenticated,
      username,
      uid,
      database,
      login,
      logout,
      setDatabase,
      listDatabases,
      error,
      clearError,
    ],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
