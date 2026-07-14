/**
 * GNU Health / Tryton model mappings for IST Health frontend.
 * See docs/API.md and docs/SAO_MIGRATION.md.
 */

export const MODELS = {
  party: 'party.party',
  patient: 'gnuhealth.patient',
  user: 'res.user',
  company: 'company.company',

  appointment: 'gnuhealth.appointment',
  healthProfessional: 'gnuhealth.healthprofessional',
  institution: 'gnuhealth.institution',
  institutionUnit: 'gnuhealth.institution.unit',
  specialty: 'gnuhealth.specialty',

  labRequest: 'gnuhealth.patient.lab.test',
  labTest: 'gnuhealth.lab',
  labTestType: 'gnuhealth.lab.test_type',
  prescription: 'gnuhealth.prescription',
  prescriptionOrder: 'gnuhealth.prescription.order',
  medicament: 'gnuhealth.medicament',
  productTemplate: 'product.template',

  evaluation: 'gnuhealth.patient.evaluation',
  medication: 'gnuhealth.patient.medication',
  hospitalBed: 'gnuhealth.hospital.bed',
  inpatientRegistration: 'gnuhealth.inpatient.registration',

  nursingRounding: 'gnuhealth.patient.rounding',
  ambulatoryCare: 'gnuhealth.patient.ambulatory_care',

  surgery: 'gnuhealth.surgery',
  procedure: 'gnuhealth.operation',
  patientProcedure: 'gnuhealth.patient.procedure',

  imagingRequest: 'gnuhealth.imaging.test.request',
  imagingTest: 'gnuhealth.imaging.test',
  imagingResult: 'gnuhealth.imaging.test.result',

  // Operations / organization / administration (SAO parity)
  product: 'product.product',
  stockLocation: 'stock.location',
  stockMove: 'stock.move',
  accountInvoice: 'account.invoice',
  currency: 'currency.currency',
  calendar: 'calendar.calendar',
  calendarEvent: 'calendar.event',
  country: 'country.country',
  module: 'ir.module',
  group: 'res.group',
  sequence: 'ir.sequence',
  lang: 'ir.lang',
  modelAccess: 'ir.model.access',
  partyAddress: 'party.address',
} as const

export type ModelName = (typeof MODELS)[keyof typeof MODELS]

export const FIELDS = {
  partyList: ['id', 'name', 'code', 'active', 'is_patient', 'is_healthprof'] as const,
  partyDetail: ['id', 'name', 'code', 'active', 'is_patient', 'is_healthprof'] as const,
  patientList: ['id', 'rec_name', 'puid', 'dob', 'gender', 'active', 'party'] as const,
  patientDetail: [
    'id', 'rec_name', 'puid', 'dob', 'gender', 'active', 'party',
    'critical_info', 'lastname', 'age', 'blood_type',
  ] as const,
  appointmentList: [
    'id', 'rec_name', 'patient', 'healthprof', 'appointment_date',
    'state', 'urgency', 'visit_type', 'appointment_type', 'comments', 'institution',
  ] as const,
  healthProfList: [
    'id', 'rec_name', 'code', 'puid', 'party', 'main_specialty',
    'institution', 'active',
  ] as const,
  institution: [
    'id', 'rec_name', 'code', 'party', 'institution_type', 'public_level', 'extra_info',
  ] as const,
  specialty: ['id', 'name', 'code', 'rec_name'] as const,
  prescriptionOrder: [
    'id', 'rec_name', 'patient', 'healthprof', 'prescription_date', 'state', 'prescription_id',
  ] as const,
  medicament: ['id', 'rec_name', 'active'] as const,
  product: ['id', 'name', 'code', 'rec_name', 'active', 'list_price', 'type'] as const,
  evaluation: [
    'id', 'rec_name', 'patient', 'healthprof', 'evaluation_start', 'state',
    'chief_complaint', 'diagnosis', 'specialty',
  ] as const,
  medication: ['id', 'rec_name', 'patient', 'healthprof'] as const,
  hospitalBed: ['id', 'rec_name', 'state', 'institution', 'bed_type'] as const,
  labRequest: [
    // `name` is invalid on gnuhealth.patient.lab.test — use rec_name / request
    'id', 'rec_name', 'state', 'date', 'patient_id', 'doctor_id', 'test_type', 'urgent', 'request',
  ] as const,
  companyList: ['id', 'rec_name', 'party'] as const,
  partyOpsList: ['id', 'name', 'code', 'active', 'is_patient', 'is_healthprof'] as const,
  productList: ['id', 'rec_name', 'code', 'active'] as const,
  stockLocationList: ['id', 'rec_name', 'code', 'type'] as const,
  stockMoveList: ['id', 'rec_name', 'product', 'quantity', 'from_location', 'to_location', 'state'] as const,
  invoiceList: ['id', 'rec_name', 'number', 'party', 'invoice_date', 'total_amount', 'state', 'type'] as const,
  currencyList: ['id', 'rec_name', 'name', 'code', 'symbol'] as const,
  calendarList: ['id', 'rec_name', 'name', 'description'] as const,
  calendarEventList: ['id', 'rec_name', 'summary', 'dtstart', 'dtend', 'status'] as const,
  userList: ['id', 'rec_name', 'name', 'login', 'active', 'email', 'groups'] as const,
  userDetail: ['id', 'rec_name', 'name', 'login', 'active', 'email', 'groups'] as const,
  groupList: ['id', 'rec_name', 'name'] as const,
  groupDetail: ['id', 'rec_name', 'name', 'users'] as const,
  modelAccessList: [
    'id', 'rec_name', 'model', 'group', 'perm_read', 'perm_write', 'perm_create', 'perm_delete',
  ] as const,
  sequenceList: [
    'id', 'rec_name', 'name', 'code', 'prefix', 'suffix', 'number_next', 'padding', 'type',
  ] as const,
  langList: [
    'id', 'rec_name', 'name', 'code', 'translatable', 'active', 'direction',
  ] as const,
  moduleList: ['id', 'rec_name', 'name', 'state'] as const,
  countryList: ['id', 'rec_name', 'name', 'code', 'code3'] as const,
  companyDetail: ['id', 'rec_name', 'party', 'header', 'footer', 'currency'] as const,
  labTest: [
    'id', 'rec_name', 'name', 'date_analysis', 'date_requested', 'state', 'patient', 'requestor', 'pathologist', 'test',
  ] as const,
  labTestType: ['id', 'rec_name', 'name', 'code', 'active'] as const,
  inpatientRegistration: [
    'id', 'rec_name', 'name', 'patient', 'hospitalization_date', 'discharge_date',
    'state', 'bed', 'attending_physician', 'admission_type',
  ] as const,
  nursingRounding: [
    'id', 'rec_name', 'code', 'registration', 'evaluation_start', 'evaluation_end',
    'health_professional', 'state',
  ] as const,
  ambulatoryCare: [
    'id', 'rec_name', 'name', 'patient', 'session_start', 'session_end',
    'health_professional', 'state',
  ] as const,
  surgery: [
    'id', 'rec_name', 'patient', 'surgery_date', 'state', 'surgeon',
    'classification', 'pathology', 'code',
  ] as const,
  procedure: [
    'id', 'rec_name', 'name', 'procedure', 'patient',
  ] as const,
  patientProcedure: [
    'id', 'rec_name', 'name', 'patient', 'procedure',
  ] as const,
  imagingRequest: [
    'id', 'rec_name', 'patient', 'date', 'state', 'doctor', 'urgent', 'comment', 'requested_test',
  ] as const,
  imagingTest: ['id', 'rec_name', 'name', 'code', 'active'] as const,
  imagingResult: [
    'id', 'rec_name', 'patient', 'date', 'number', 'doctor', 'comment', 'requested_test',
  ] as const,
} as const

export const MODULE_MAP = {
  dashboard: { models: [] as string[], status: 'live' as const },
  patients: { models: [MODELS.party, MODELS.patient], status: 'live' as const },
  appointments: { models: [MODELS.appointment], status: 'live' as const },
  staff: { models: [MODELS.healthProfessional], status: 'live' as const },
  laboratory: { models: [MODELS.labRequest, MODELS.labTest, MODELS.labTestType], status: 'live' as const },
  pharmacy: {
    models: [MODELS.prescriptionOrder, MODELS.medicament, MODELS.productTemplate],
    status: 'live' as const,
  },
  medications: { models: [MODELS.medication], status: 'live' as const },
  evaluations: { models: [MODELS.evaluation], status: 'live' as const },
  beds: { models: [MODELS.hospitalBed, MODELS.inpatientRegistration], status: 'live' as const },
  nursing: { models: [MODELS.nursingRounding, MODELS.ambulatoryCare], status: 'live' as const },
  procedures: { models: [MODELS.surgery, MODELS.procedure], status: 'live' as const },
  imaging: { models: [MODELS.imagingRequest, MODELS.imagingTest, MODELS.imagingResult], status: 'live' as const },
  surgery: { models: [MODELS.surgery], status: 'live' as const },
  settings: { models: [MODELS.institution], status: 'live' as const },
} as const

export interface PartyRecord {
  id: number
  name: string
  code?: string
  active?: boolean
  is_patient?: boolean
  is_healthprof?: boolean
}

export interface PatientRecord {
  id: number
  party?: number
  rec_name?: string
  puid?: string
  dob?: string | TrytonDate
  gender?: string
  active?: boolean
  critical_info?: string
  lastname?: string
  age?: string
  blood_type?: string
}

export interface AppointmentRecord {
  id: number
  rec_name?: string
  patient?: number
  healthprof?: number
  appointment_date?: string | TrytonDateTime
  state?: string
  urgency?: string
  visit_type?: string
  appointment_type?: string
  comments?: string
  institution?: number
}

export interface HealthProfRecord {
  id: number
  rec_name?: string
  code?: string
  puid?: string
  party?: number
  main_specialty?: number
  institution?: number
  active?: boolean
  specialtyName?: string
  institutionName?: string
  info?: string
}

export interface InstitutionRecord {
  id: number
  rec_name?: string
  code?: string
  party?: number
  institution_type?: string
  public_level?: string
  extra_info?: string
}

export interface DashboardStats {
  patients: number
  appointments: number
  staff: number
  labOrders: number
  pharmacyOrders: number
}

/** Tryton JSON-RPC serializes dates/datetimes as class-tagged objects */
export interface TrytonDate {
  __class__: 'date'
  year: number
  month: number
  day: number
}

export interface TrytonDateTime {
  __class__: 'datetime'
  year: number
  month: number
  day: number
  hour?: number
  minute?: number
  second?: number
  microsecond?: number
}

export function isTrytonTemporal(v: unknown): v is TrytonDate | TrytonDateTime {
  return (
    typeof v === 'object' &&
    v !== null &&
    '__class__' in v &&
    ((v as { __class__: string }).__class__ === 'date' ||
      (v as { __class__: string }).__class__ === 'datetime')
  )
}

export function formatTrytonDate(v: unknown): string {
  if (v == null || v === '') return '—'
  if (typeof v === 'string') return v.slice(0, 16).replace('T', ' ')
  if (isTrytonTemporal(v)) {
    const y = String(v.year).padStart(4, '0')
    const m = String(v.month).padStart(2, '0')
    const d = String(v.day).padStart(2, '0')
    if (v.__class__ === 'date') return `${y}-${m}-${d}`
    const hh = String(v.hour ?? 0).padStart(2, '0')
    const mm = String(v.minute ?? 0).padStart(2, '0')
    return `${y}-${m}-${d} ${hh}:${mm}`
  }
  return String(v)
}

export function trytonDateToInput(v: unknown): string {
  if (typeof v === 'string') return v.slice(0, 16)
  if (isTrytonTemporal(v) && v.__class__ === 'datetime') {
    const y = String(v.year).padStart(4, '0')
    const m = String(v.month).padStart(2, '0')
    const d = String(v.day).padStart(2, '0')
    const hh = String(v.hour ?? 0).padStart(2, '0')
    const mm = String(v.minute ?? 0).padStart(2, '0')
    return `${y}-${m}-${d}T${hh}:${mm}`
  }
  return ''
}

/** Convert HTML datetime-local value to Tryton datetime dict */
export function inputToTrytonDateTime(local: string): TrytonDateTime | null {
  if (!local) return null
  const [datePart, timePart = '00:00'] = local.split('T')
  const [y, m, d] = datePart.split('-').map(Number)
  const [hh, mm] = timePart.split(':').map(Number)
  if (!y || !m || !d) return null
  return {
    __class__: 'datetime',
    year: y,
    month: m,
    day: d,
    hour: hh || 0,
    minute: mm || 0,
    second: 0,
    microsecond: 0,
  }
}

/** Convert HTML date value (YYYY-MM-DD) to Tryton date dict */
export function inputToTrytonDate(local: string): TrytonDate | null {
  if (!local) return null
  const [y, m, d] = local.split('-').map(Number)
  if (!y || !m || !d) return null
  return { __class__: 'date', year: y, month: m, day: d }
}

/** Convert Tryton date/datetime to HTML date input value */
export function trytonDateToDateInput(v: unknown): string {
  if (typeof v === 'string') return v.slice(0, 10)
  if (isTrytonTemporal(v)) {
    const y = String(v.year).padStart(4, '0')
    const m = String(v.month).padStart(2, '0')
    const d = String(v.day).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  return ''
}

export const BLOOD_TYPES = ['A', 'B', 'AB', 'O'] as const
export const APPOINTMENT_STATES = [
  'confirmed',
  'free',
  'checked_in',
  'done',
  'no_show',
  'cancelled',
] as const
export const APPOINTMENT_URGENCIES = ['a', 'b', 'c'] as const
export const APPOINTMENT_VISIT_TYPES = [
  'new',
  'followup',
  'well_child',
  'well_woman',
] as const
