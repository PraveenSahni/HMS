import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { ErrorState, LoadingState } from '../components/ui'
import {
  fetchDashboardStats,
  fetchRecentAppointments,
  formatTrytonDate,
} from '../services/healthApi'

import type { AppointmentRecord, DashboardStats } from '../lib/tryton/models'
import { formatRpcError } from '../lib/tryton/client'



function formatDate(): string {

  return new Intl.DateTimeFormat(undefined, {

    weekday: 'long',

    day: 'numeric',

    month: 'long',

    year: 'numeric',

  }).format(new Date())

}



function scheduleStatusClass(state: unknown): string {

  const s = String(state ?? '').toLowerCase()

  if (s.includes('consult') || s.includes('progress')) return ' is-active'

  if (s.includes('wait') || s.includes('pending')) return ' is-pending'

  return ''

}



export function DashboardPage() {

  const { t } = useTranslation()

  const { client, username } = useAuth()

  const [stats, setStats] = useState<DashboardStats | null>(null)

  const [recent, setRecent] = useState<Array<AppointmentRecord & { patientName?: string }>>([])

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState<string | null>(null)



  const load = async () => {

    setLoading(true)

    setError(null)

    try {
      const [s, r] = await Promise.allSettled([
        fetchDashboardStats(client),
        fetchRecentAppointments(client),
      ])
      if (s.status === 'fulfilled') setStats(s.value)
      else setStats({ patients: 0, appointments: 0, staff: 0, labOrders: 0, pharmacyOrders: 0 })
      if (r.status === 'fulfilled') setRecent(r.value)
      else setRecent([])
      if (s.status === 'rejected' && r.status === 'rejected') {
        setError(formatRpcError(s.reason, t('dashboard.error')))
      }
    } catch (err) {
      setError(formatRpcError(err, t('dashboard.error')))
    } finally {

      setLoading(false)

    }

  }



  useEffect(() => {

    load()

  }, [client])



  if (loading && !stats) return <LoadingState message={t('dashboard.loading')} />

  if (error) return <ErrorState message={error} onRetry={load} />



  const company = import.meta.env.VITE_COMPANY_NAME ?? t('app.company')

  const displayName = username ?? t('dashboard.defaultUser')



  return (

    <div className="ist-dashboard">

      <div className="ist-dashboard__welcome ist-heading-block">

        <p className="ist-tagline">{t('app.company')}</p>

        <h1>{t('dashboard.greeting', { name: displayName })}</h1>

        <hr className="ist-divider" />

        <p className="ist-subtitle">{t('dashboard.dateLine', { date: formatDate(), company })}</p>

      </div>



      <div className="ist-stats">

        <div className="ist-stat">

          <div className="ist-stat__label">{t('dashboard.statAppts')}</div>

          <div className="ist-stat__value">{loading ? '—' : (stats?.appointments ?? 0)}</div>

          <div className="ist-stat__meta">{t('dashboard.statApptsMeta')}</div>

        </div>

        <div className="ist-stat">

          <div className="ist-stat__label">{t('dashboard.statPatients')}</div>

          <div className="ist-stat__value">{loading ? '—' : (stats?.patients ?? 0)}</div>

          <div className="ist-stat__meta">{t('dashboard.statPatientsMeta')}</div>

        </div>

        <div className="ist-stat">

          <div className="ist-stat__label">{t('dashboard.statStaff')}</div>

          <div className="ist-stat__value">{loading ? '—' : (stats?.staff ?? 0)}</div>

          <div className="ist-stat__meta">{t('dashboard.statStaffMeta')}</div>

        </div>

        <div className="ist-stat">

          <div className="ist-stat__label">{t('dashboard.statLab')}</div>

          <div className="ist-stat__value">{loading ? '—' : (stats?.labOrders ?? 0)}</div>

          <div className="ist-stat__meta">{t('dashboard.statLabMeta', { rx: stats?.pharmacyOrders ?? 0 })}</div>

        </div>

      </div>



      {stats?.patients === 0 && (

        <div className="ist-notice">{t('dashboard.noData')}</div>

      )}



      <div className="ist-quick-actions">

        <Link to="/patients" className="ist-btn ist-btn--primary">{t('dashboard.btnNewPatient')}</Link>

        <Link to="/appointments" className="ist-btn ist-btn--outline">

          {t('dashboard.btnBookAppt')}

        </Link>

        <Link to="/setup" className="ist-btn ist-btn--outline">

          {t('dashboard.btnSetup')}

        </Link>

      </div>



      <div className="ist-dashboard-grid">

        <div className="ist-schedule">

          <div className="ist-schedule__head">

            <h2>{t('dashboard.todaySchedule')}</h2>

            <hr className="ist-divider" />

          </div>

          {recent.length === 0 ? (

            <p className="ist-subtitle">{t('dashboard.noSchedule')}</p>

          ) : (

            recent.map((row) => (

              <div key={String(row.id)} className="ist-schedule__row">

                <span className="ist-schedule__time">

                  {formatTrytonDate(row.appointment_date)}

                </span>

                <span className="ist-schedule__name">
                  {String(
                    (row as { patientName?: string }).patientName ??
                      row.patient ??
                      row.rec_name ??
                      '—',
                  )}
                </span>

                <span className={`ist-schedule__status${scheduleStatusClass(row.state)}`}>

                  {String(row.state ?? t('dashboard.scheduled'))}

                </span>

              </div>

            ))

          )}

        </div>



        <div>

          <h3>{t('dashboard.quickStats')}</h3>

          <hr className="ist-divider" />

          <div className="ist-quick-list">

            <div className="ist-quick-list__item">

              <span className="ist-quick-list__label">{t('dashboard.labPending')}</span>

              <span className="ist-quick-list__value">{stats?.labOrders ?? 0}</span>

            </div>

            <div className="ist-quick-list__item">

              <span className="ist-quick-list__label">{t('dashboard.rxQueue')}</span>

              <span className="ist-quick-list__value">{stats?.pharmacyOrders ?? 0}</span>

            </div>

            <div className="ist-quick-list__item">

              <span className="ist-quick-list__label">{t('dashboard.staffCount')}</span>

              <span className="ist-quick-list__value">{stats?.staff ?? 0}</span>

            </div>

          </div>

        </div>

      </div>

    </div>

  )

}

