import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { AppLayout } from './components/layout/AppLayout'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { PatientsPage } from './pages/PatientsPage'
import { PatientDetailPage } from './pages/PatientDetailPage'
import { AppointmentsPage } from './pages/AppointmentsPage'
import { StaffPage, StaffDetailPage } from './pages/StaffPage'
import { LaboratoryPage } from './pages/LaboratoryPage'
import { PharmacyPage } from './pages/PharmacyPage'
import { SettingsPage } from './pages/SettingsPage'
import {
  BedsPage,
  EvaluationsPage,
  ImagingPage,
  MedicationsPage,
  NursingPage,
  ProceduresPage,
} from './pages/ClinicalPages'
import {
  CalendarPage,
  CompaniesPage,
  CountriesPage,
  CurrencyPage,
  FinancialPage,
  GroupsPage,
  LanguagesPage,
  ModulesPage,
  PartiesPage,
  ProductsPage,
  SequencesPage,
  StockPage,
  UsersPage,
} from './pages/OpsPages'
import { ModelBrowserPage } from './pages/ModelBrowserPage'
import { HelpCentrePage } from './pages/help/HelpCentrePage'
import { HelpAdminPage } from './pages/help/HelpAdminPage'
import { SetupHubPage } from './pages/SetupHubPage'
import { WorkspacePage } from './pages/WorkspacePage'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            {/* One-app UX: post-login home is SAO-in-shell Workspace. */}
            <Route index element={<Navigate to="/workspace" replace />} />
            <Route path="workspace" element={<WorkspacePage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="patients" element={<PatientsPage />} />
            <Route path="patients/:id" element={<PatientDetailPage />} />
            <Route path="appointments" element={<AppointmentsPage />} />
            <Route path="staff" element={<StaffPage />} />
            <Route path="staff/:id" element={<StaffDetailPage />} />
            <Route path="laboratory" element={<LaboratoryPage />} />
            <Route path="pharmacy" element={<PharmacyPage />} />
            <Route path="medications" element={<MedicationsPage />} />
            <Route path="evaluations" element={<EvaluationsPage />} />
            <Route path="beds" element={<BedsPage />} />
            <Route path="nursing" element={<NursingPage />} />
            <Route path="procedures" element={<ProceduresPage />} />
            <Route path="imaging" element={<ImagingPage />} />
            <Route path="parties" element={<PartiesPage />} />
            <Route path="products" element={<ProductsPage />} />
            <Route path="stock" element={<StockPage />} />
            <Route path="financial" element={<FinancialPage />} />
            <Route path="currency" element={<CurrencyPage />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="companies" element={<CompaniesPage />} />
            <Route path="setup" element={<SetupHubPage />} />
            <Route path="users" element={<UsersPage />} />
            <Route path="groups" element={<GroupsPage />} />
            <Route path="modules" element={<ModulesPage />} />
            <Route path="sequences" element={<SequencesPage />} />
            <Route path="countries" element={<CountriesPage />} />
            <Route path="languages" element={<LanguagesPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="help" element={<HelpCentrePage />} />
            <Route path="help/admin" element={<HelpAdminPage />} />
            <Route path="menu/:menuId" element={<ModelBrowserPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/workspace" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
