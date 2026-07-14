import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { SaoPanel } from '../components/common/SaoPanel'

type SetupModule = {
  id: string
  order: number
  titleKey: string
  purposeKey: string
  reactRoutes: Array<{ to: string; labelKey: string }>
  helpTopic: string
  saoHintKey: string
  statusHintKey: string
}

const MODULES: SetupModule[] = [
  {
    id: 'companies',
    order: 1,
    titleKey: 'setup.mod.companies',
    purposeKey: 'setup.mod.companiesPurpose',
    reactRoutes: [{ to: '/companies', labelKey: 'nav.companies' }],
    helpTopic: 'setup-companies',
    saoHintKey: 'setup.mod.companiesSao',
    statusHintKey: 'setup.mod.companiesStatus',
  },
  {
    id: 'currency',
    order: 2,
    titleKey: 'setup.mod.currency',
    purposeKey: 'setup.mod.currencyPurpose',
    reactRoutes: [{ to: '/currency', labelKey: 'nav.currency' }],
    helpTopic: 'setup-currency',
    saoHintKey: 'setup.mod.currencySao',
    statusHintKey: 'setup.mod.currencyStatus',
  },
  {
    id: 'admin',
    order: 3,
    titleKey: 'setup.mod.admin',
    purposeKey: 'setup.mod.adminPurpose',
    reactRoutes: [
      { to: '/users', labelKey: 'nav.users' },
      { to: '/groups', labelKey: 'setup.link.groups' },
      { to: '/sequences', labelKey: 'setup.link.sequences' },
      { to: '/modules', labelKey: 'nav.modules' },
    ],
    helpTopic: 'setup-admin',
    saoHintKey: 'setup.mod.adminSao',
    statusHintKey: 'setup.mod.adminStatus',
  },
  {
    id: 'party',
    order: 4,
    titleKey: 'setup.mod.party',
    purposeKey: 'setup.mod.partyPurpose',
    reactRoutes: [{ to: '/parties', labelKey: 'nav.parties' }],
    helpTopic: 'setup-party',
    saoHintKey: 'setup.mod.partySao',
    statusHintKey: 'setup.mod.partyStatus',
  },
  {
    id: 'product',
    order: 5,
    titleKey: 'setup.mod.product',
    purposeKey: 'setup.mod.productPurpose',
    reactRoutes: [{ to: '/products', labelKey: 'nav.products' }],
    helpTopic: 'setup-product',
    saoHintKey: 'setup.mod.productSao',
    statusHintKey: 'setup.mod.productStatus',
  },
  {
    id: 'stock',
    order: 6,
    titleKey: 'setup.mod.stock',
    purposeKey: 'setup.mod.stockPurpose',
    reactRoutes: [{ to: '/stock', labelKey: 'nav.stock' }],
    helpTopic: 'setup-stock',
    saoHintKey: 'setup.mod.stockSao',
    statusHintKey: 'setup.mod.stockStatus',
  },
  {
    id: 'calendar',
    order: 7,
    titleKey: 'setup.mod.calendar',
    purposeKey: 'setup.mod.calendarPurpose',
    reactRoutes: [{ to: '/calendar', labelKey: 'nav.calendar' }],
    helpTopic: 'setup-calendar',
    saoHintKey: 'setup.mod.calendarSao',
    statusHintKey: 'setup.mod.calendarStatus',
  },
  {
    id: 'financial',
    order: 8,
    titleKey: 'setup.mod.financial',
    purposeKey: 'setup.mod.financialPurpose',
    reactRoutes: [{ to: '/financial', labelKey: 'nav.financial' }],
    helpTopic: 'setup-financial',
    saoHintKey: 'setup.mod.financialSao',
    statusHintKey: 'setup.mod.financialStatus',
  },
  {
    id: 'health',
    order: 9,
    titleKey: 'setup.mod.health',
    purposeKey: 'setup.mod.healthPurpose',
    reactRoutes: [
      { to: '/settings', labelKey: 'nav.settings' },
      { to: '/patients', labelKey: 'nav.patients' },
      { to: '/appointments', labelKey: 'nav.appointments' },
      { to: '/laboratory', labelKey: 'nav.laboratory' },
      { to: '/pharmacy', labelKey: 'nav.pharmacy' },
      { to: '/beds', labelKey: 'nav.beds' },
    ],
    helpTopic: 'setup-health',
    saoHintKey: 'setup.mod.healthSao',
    statusHintKey: 'setup.mod.healthStatus',
  },
]

/** Hub listing all sidebar Menus setup areas with React routes, SAO hints, and Help topics. */
export function SetupHubPage() {
  const { t } = useTranslation()

  return (
    <div className="ist-patients" data-testid="setup-hub">
      <div className="ist-module-header ist-heading-block">
        <div>
          <p className="ist-tagline">{t('app.company')}</p>
          <h1 className="ist-patients__title">{t('setup.title')}</h1>
          <hr className="ist-divider" />
          <p className="ist-subtitle">{t('setup.subtitle')}</p>
        </div>
        <Link to="/help?topic=wf-system-setup" className="ist-btn ist-btn--primary">
          {t('setup.openGuided')}
        </Link>
      </div>

      <div
        className="ist-card ist-card--bordered"
        style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-6)' }}
        data-testid="setup-order-checklist"
      >
        <h3 style={{ marginBottom: 'var(--space-2)' }}>{t('setup.orderTitle')}</h3>
        <p className="ist-subtitle" style={{ marginBottom: 'var(--space-4)' }}>
          {t('setup.orderHint')}
        </p>
        <ol className="ist-subtitle" style={{ paddingLeft: '1.25rem', marginBottom: 0 }}>
          {MODULES.map((m) => (
            <li key={m.id} style={{ marginBottom: '0.35rem' }}>
              <strong>
                {m.order}. {t(m.titleKey)}
              </strong>
              {' — '}
              {t(m.statusHintKey)}
            </li>
          ))}
        </ol>
      </div>

      <SaoPanel
        title={t('setup.saoTitle')}
        description={t('setup.saoDesc')}
        instructions={[t('setup.saoInstrCoa'), t('setup.saoInstrModules'), t('setup.saoInstrTax')]}
      />

      <div className="ist-patient-list" style={{ marginTop: 'var(--space-6)' }}>
        {MODULES.map((m) => (
          <div
            key={m.id}
            className="ist-card ist-card--bordered"
            style={{ padding: 'var(--space-5)', marginBottom: 'var(--space-4)' }}
            data-testid={`setup-module-${m.id}`}
          >
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'space-between',
                gap: 'var(--space-3)',
                marginBottom: 'var(--space-3)',
              }}
            >
              <div>
                <p className="ist-tagline" style={{ marginBottom: '0.25rem' }}>
                  {t('setup.stepLabel', { n: m.order })}
                </p>
                <h3 style={{ margin: 0 }}>{t(m.titleKey)}</h3>
              </div>
              <Link
                to={`/help?topic=${m.helpTopic}`}
                className="ist-btn ist-btn--outline ist-btn--sm"
              >
                {t('setup.helpTopic')}
              </Link>
            </div>
            <p className="ist-subtitle" style={{ marginBottom: 'var(--space-3)' }}>
              {t(m.purposeKey)}
            </p>
            <p className="ist-subtitle" style={{ marginBottom: 'var(--space-3)' }}>
              <strong>{t('setup.statusLabel')}:</strong> {t(m.statusHintKey)}
            </p>
            <p className="ist-subtitle" style={{ marginBottom: 'var(--space-3)' }}>
              <strong>{t('setup.saoLabel')}:</strong> {t(m.saoHintKey)}
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {m.reactRoutes.map((r) => (
                <Link key={r.to} to={r.to} className="ist-btn ist-btn--outline ist-btn--sm">
                  {t(r.labelKey)}
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>

      <p className="ist-subtitle" style={{ marginTop: 'var(--space-4)' }}>
        <Link to="/help?topic=setup-order">{t('setup.docOrder')}</Link>
        {' · '}
        <Link to="/financial">{t('setup.docFinancial')}</Link>
        {' · '}
        <Link to="/help">{t('nav.help')}</Link>
      </p>
    </div>
  )
}
