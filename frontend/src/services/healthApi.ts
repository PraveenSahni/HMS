import { TrytonClient } from '../lib/tryton/client'
import {
  MODELS,
  FIELDS,
  formatTrytonDate,
  inputToTrytonDate,
  inputToTrytonDateTime,
  type DashboardStats,
  type PartyRecord,
  type AppointmentRecord,
  type HealthProfRecord,
  type InstitutionRecord,
  type PatientRecord,
} from '../lib/tryton/models'

export type PatientFormData = {
  name: string
  code?: string
  gender?: string
  dob?: string
  bloodType?: string
  lastname?: string
  criticalInfo?: string
  active?: boolean
}

export type StaffFormData = {
  name: string
  code?: string
  licenseCode?: string
  institutionId?: number
  info?: string
  active?: boolean
}

export type LabRequestFormData = {
  patientId: number
  doctorId: number
  testTypeId: number
  urgent?: boolean
  date?: string
}

export { formatTrytonDate }

export async function fetchDashboardStats(client: TrytonClient): Promise<DashboardStats> {
  const stats: DashboardStats = {
    patients: 0,
    appointments: 0,
    staff: 0,
    labOrders: 0,
    pharmacyOrders: 0,
  }

  const tasks: Array<Promise<void>> = []

  if (await client.modelExists(MODELS.patient)) {
    tasks.push(client.searchCount(MODELS.patient).then((n) => { stats.patients = n }))
  } else {
    tasks.push(
      client.searchCount(MODELS.party, [['is_patient', '=', true]]).then((n) => {
        stats.patients = n
      }).catch(() =>
        client.searchCount(MODELS.party, [['code', 'like', 'IST-P-%']]).then((n) => {
          stats.patients = n
        }),
      ),
    )
  }

  if (await client.modelExists(MODELS.appointment)) {
    tasks.push(client.searchCount(MODELS.appointment).then((n) => { stats.appointments = n }))
  }
  if (await client.modelExists(MODELS.healthProfessional)) {
    tasks.push(client.searchCount(MODELS.healthProfessional).then((n) => { stats.staff = n }))
  }
  if (await client.modelExists(MODELS.labRequest)) {
    tasks.push(client.searchCount(MODELS.labRequest).then((n) => { stats.labOrders = n }))
  }
  if (await client.modelExists(MODELS.prescriptionOrder)) {
    tasks.push(
      client.searchCount(MODELS.prescriptionOrder).then((n) => { stats.pharmacyOrders = n }),
    )
  } else if (await client.modelExists(MODELS.prescription)) {
    tasks.push(client.searchCount(MODELS.prescription).then((n) => { stats.pharmacyOrders = n }))
  }

  await Promise.allSettled(tasks)
  return stats
}

export async function fetchPatients(
  client: TrytonClient,
  search = '',
  offset = 0,
  limit = 50,
): Promise<{ records: PartyRecord[]; total: number }> {
  // Prefer gnuhealth.patient when available — more accurate patient set
  if (await client.modelExists(MODELS.patient)) {
    const domain: unknown[] = search
      ? ['|', ['rec_name', 'ilike', `%${search}%`], ['puid', 'ilike', `%${search}%`]]
      : []
    const [idsResult, totalResult] = await Promise.allSettled([
      client.search(MODELS.patient, domain, offset, limit, [['id', 'ASC']]),
      client.searchCount(MODELS.patient, domain),
    ])
    if (idsResult.status === 'rejected') throw idsResult.reason
    const ids = idsResult.value
    const total = totalResult.status === 'fulfilled' ? totalResult.value : ids.length

    let patients: PatientRecord[] = []
    try {
      patients = (await client.read(MODELS.patient, ids, [...FIELDS.patientList])) as unknown as PatientRecord[]
    } catch {
      patients = (await client.read(MODELS.patient, ids, [
        'id',
        'rec_name',
        'party',
        'puid',
        'active',
      ])) as unknown as PatientRecord[]
    }

    const partyIds = patients.map((p) => p.party).filter((id): id is number => typeof id === 'number')
    let parties: PartyRecord[] = []
    if (partyIds.length) {
      try {
        parties = (await client.read(MODELS.party, partyIds, [...FIELDS.partyList])) as unknown as PartyRecord[]
      } catch {
        parties = []
      }
    }
    const partyMap = new Map(parties.map((p) => [p.id, p]))

    const records: PartyRecord[] = patients.map((p) => {
      const party = p.party ? partyMap.get(p.party) : undefined
      return {
        id: party?.id ?? p.party ?? p.id,
        name: party?.name ?? p.rec_name ?? String(p.id),
        code: party?.code ?? p.puid,
        active: p.active !== false && party?.active !== false,
      }
    })
    return { records, total }
  }

  const domain: unknown[] = search
    ? ['|', ['name', 'ilike', `%${search}%`], ['code', 'ilike', `%${search}%`]]
    : []

  let ids = await client.search(
    MODELS.party,
    [...domain, ['code', 'like', 'IST-P-%']],
    offset,
    limit,
    [['name', 'ASC']],
  )
  let total = await client.searchCount(MODELS.party, [...domain, ['code', 'like', 'IST-P-%']])

  if (total === 0) {
    const patientDomain = [...domain, ['is_patient', '=', true]]
    try {
      ids = await client.search(MODELS.party, patientDomain, offset, limit, [['name', 'ASC']])
      total = await client.searchCount(MODELS.party, patientDomain)
    } catch {
      ids = await client.search(MODELS.party, domain, offset, limit, [['name', 'ASC']])
      total = await client.searchCount(MODELS.party, domain)
    }
  }

  const records = (await client.read(MODELS.party, ids, [...FIELDS.partyList])) as unknown as PartyRecord[]
  return { records, total }
}

export async function fetchPatientById(
  client: TrytonClient,
  id: number,
): Promise<{ party: PartyRecord; patient: PatientRecord | null }> {
  // id may be party id (from list) — resolve party first, then patient by party
  let partyRows = (await client.read(MODELS.party, [id], [...FIELDS.partyDetail])) as unknown as PartyRecord[]
  let patient: PatientRecord | null = null

  if (await client.modelExists(MODELS.patient)) {
    let ghIds = await client.search(MODELS.patient, [['party', '=', id]], 0, 1)
    if (!ghIds.length) {
      // maybe id is already a patient id
      try {
        const direct = (await client.read(MODELS.patient, [id], [...FIELDS.patientDetail])) as unknown as PatientRecord[]
        if (direct[0]) {
          patient = direct[0]
          if (patient.party) {
            partyRows = (await client.read(MODELS.party, [patient.party], [...FIELDS.partyDetail])) as unknown as PartyRecord[]
          }
        }
      } catch {
        /* ignore */
      }
    } else {
      const ghRows = (await client.read(MODELS.patient, ghIds, [...FIELDS.patientDetail])) as unknown as PatientRecord[]
      patient = ghRows[0] ?? null
    }
  }

  if (!partyRows.length) throw new Error('Not found')
  return { party: partyRows[0], patient }
}

function buildPatientVals(data: PatientFormData): Record<string, unknown> {
  const vals: Record<string, unknown> = { active: data.active !== false }
  if (data.gender) vals.gender = data.gender
  if (data.bloodType) vals.blood_type = data.bloodType
  if (data.lastname != null) vals.lastname = data.lastname.trim()
  if (data.criticalInfo != null) vals.critical_info = data.criticalInfo.trim()
  if (data.dob) {
    const dob = inputToTrytonDate(data.dob)
    if (dob) vals.dob = dob
  }
  return vals
}

export async function createPatient(
  client: TrytonClient,
  data: PatientFormData,
): Promise<{ partyId: number; patientId: number | null }> {
  const code =
    data.code?.trim() ||
    `IST-P-${String(Date.now()).slice(-6)}`

  const partyVals: Record<string, unknown> = {
    name: data.name.trim(),
    code,
    is_patient: true,
    is_person: true,
    active: true,
  }
  // Some GH installs store DoB on party; ignore if field rejected later via patient write
  if (data.dob) {
    const dob = inputToTrytonDate(data.dob)
    if (dob) partyVals.dob = dob
  }
  if (data.gender) partyVals.gender = data.gender

  let partyId: number
  try {
    ;[partyId] = await client.create(MODELS.party, [partyVals])
  } catch {
    delete partyVals.dob
    delete partyVals.gender
    ;[partyId] = await client.create(MODELS.party, [partyVals])
  }

  let patientId: number | null = null
  if (await client.modelExists(MODELS.patient)) {
    const vals = { party: partyId, ...buildPatientVals(data) }
    try {
      const ids = await client.create(MODELS.patient, [vals])
      patientId = ids[0] ?? null
    } catch {
      // Retry with minimal required fields if optional ones are rejected
      const ids = await client.create(MODELS.patient, [{ party: partyId, active: true }])
      patientId = ids[0] ?? null
      if (patientId != null) {
        try {
          await client.write(MODELS.patient, [patientId], buildPatientVals(data))
        } catch {
          /* party + patient shell is enough */
        }
      }
    }
  }

  return { partyId, patientId }
}

export async function updatePatient(
  client: TrytonClient,
  opts: { partyId: number; patientId?: number | null; data: PatientFormData },
): Promise<void> {
  const { partyId, patientId, data } = opts
  const partyVals: Record<string, unknown> = {
    name: data.name.trim(),
  }
  if (data.code?.trim()) partyVals.code = data.code.trim()
  if (data.active != null) partyVals.active = data.active
  await client.write(MODELS.party, [partyId], partyVals)

  if (patientId && (await client.modelExists(MODELS.patient))) {
    try {
      await client.write(MODELS.patient, [patientId], buildPatientVals(data))
    } catch (err) {
      // Retry without dob if related/function field rejects write
      const vals = buildPatientVals(data)
      delete vals.dob
      await client.write(MODELS.patient, [patientId], vals).catch(() => {
        throw err
      })
    }
  }
}

export async function fetchAppointments(
  client: TrytonClient,
  opts: { search?: string; day?: string; offset?: number; limit?: number } = {},
): Promise<{
  records: Array<AppointmentRecord & { patientName?: string; healthprofName?: string }>
  total: number
  available: boolean
}> {
  if (!(await client.modelExists(MODELS.appointment))) {
    return { records: [], total: 0, available: false }
  }

  const domain: unknown[] = []
  if (opts.day) {
    // day = YYYY-MM-DD — filter by date prefix via datetime range approx using string compare on rec_name is weak;
    // use appointment_date >= day 00:00 and < next day when possible
    const start = {
      __class__: 'datetime',
      year: Number(opts.day.slice(0, 4)),
      month: Number(opts.day.slice(5, 7)),
      day: Number(opts.day.slice(8, 10)),
      hour: 0,
      minute: 0,
      second: 0,
      microsecond: 0,
    }
    const endDay = new Date(`${opts.day}T00:00:00`)
    endDay.setDate(endDay.getDate() + 1)
    const end = {
      __class__: 'datetime',
      year: endDay.getFullYear(),
      month: endDay.getMonth() + 1,
      day: endDay.getDate(),
      hour: 0,
      minute: 0,
      second: 0,
      microsecond: 0,
    }
    domain.push(['appointment_date', '>=', start], ['appointment_date', '<', end])
  }
  if (opts.search) {
    domain.push(['rec_name', 'ilike', `%${opts.search}%`])
  }

  const offset = opts.offset ?? 0
  const limit = opts.limit ?? 100
  const ids = await client.search(
    MODELS.appointment,
    domain,
    offset,
    limit,
    [['appointment_date', 'DESC']],
  )
  const total = await client.searchCount(MODELS.appointment, domain)
  const rows = (await client.read(
    MODELS.appointment,
    ids,
    [...FIELDS.appointmentList],
  )) as unknown as AppointmentRecord[]

  const patientNames = await client.resolveNames(
    MODELS.patient,
    rows.map((r) => r.patient),
  )
  const hpNames = await client.resolveNames(
    MODELS.healthProfessional,
    rows.map((r) => r.healthprof),
  )

  const records = rows.map((r) => ({
    ...r,
    patientName: r.patient ? patientNames.get(r.patient) : undefined,
    healthprofName: r.healthprof ? hpNames.get(r.healthprof) : undefined,
  }))

  return { records, total, available: true }
}

export async function createAppointment(
  client: TrytonClient,
  data: {
    patientId: number
    healthprofId: number
    appointmentDate: string
    state?: string
    comments?: string
    visitType?: string
    urgency?: string
  },
): Promise<number> {
  const dt = inputToTrytonDateTime(data.appointmentDate)
  if (!dt) throw new Error('Invalid appointment date')

  const vals: Record<string, unknown> = {
    patient: data.patientId,
    healthprof: data.healthprofId,
    appointment_date: dt,
    state: data.state ?? 'confirmed',
    appointment_type: 'outpatient',
  }
  if (data.comments) vals.comments = data.comments
  if (data.visitType) vals.visit_type = data.visitType
  if (data.urgency) vals.urgency = data.urgency

  const ids = await client.create(MODELS.appointment, [vals])
  return ids[0]
}

export async function updateAppointment(
  client: TrytonClient,
  id: number,
  data: {
    patientId?: number
    healthprofId?: number
    appointmentDate?: string
    state?: string
    comments?: string
    visitType?: string
    urgency?: string
  },
): Promise<void> {
  const vals: Record<string, unknown> = {}
  if (data.patientId != null) vals.patient = data.patientId
  if (data.healthprofId != null) vals.healthprof = data.healthprofId
  if (data.state) vals.state = data.state
  if (data.comments != null) vals.comments = data.comments
  if (data.visitType != null) vals.visit_type = data.visitType || null
  if (data.urgency != null) vals.urgency = data.urgency || null
  if (data.appointmentDate) {
    const dt = inputToTrytonDateTime(data.appointmentDate)
    if (dt) vals.appointment_date = dt
  }
  await client.write(MODELS.appointment, [id], vals)
}

export async function fetchPatientOptions(
  client: TrytonClient,
  limit = 200,
): Promise<Array<{ id: number; label: string }>> {
  if (!(await client.modelExists(MODELS.patient))) return []
  const ids = await client.search(MODELS.patient, [], 0, limit, [['id', 'ASC']])
  const rows = await client.read(MODELS.patient, ids, ['id', 'rec_name'])
  return rows.map((r) => ({ id: Number(r.id), label: String(r.rec_name ?? r.id) }))
}

export async function fetchHealthProfOptions(
  client: TrytonClient,
  limit = 200,
): Promise<Array<{ id: number; label: string }>> {
  if (!(await client.modelExists(MODELS.healthProfessional))) return []
  const ids = await client.search(
    MODELS.healthProfessional,
    [['active', '=', true]],
    0,
    limit,
    [['id', 'ASC']],
  )
  const rows = await client.read(MODELS.healthProfessional, ids, ['id', 'rec_name'])
  return rows.map((r) => ({ id: Number(r.id), label: String(r.rec_name ?? r.id) }))
}

export async function fetchInstitutionOptions(
  client: TrytonClient,
  limit = 50,
): Promise<Array<{ id: number; label: string }>> {
  if (!(await client.modelExists(MODELS.institution))) return []
  const ids = await client.search(MODELS.institution, [], 0, limit, [['id', 'ASC']])
  const rows = await client.read(MODELS.institution, ids, ['id', 'rec_name'])
  return rows.map((r) => ({ id: Number(r.id), label: String(r.rec_name ?? r.id) }))
}

export async function fetchLabTestTypeOptions(
  client: TrytonClient,
  limit = 200,
): Promise<Array<{ id: number; label: string }>> {
  if (!(await client.modelExists(MODELS.labTestType))) return []
  const ids = await client.search(MODELS.labTestType, [], 0, limit, null)
  let rows: Record<string, unknown>[] = []
  try {
    rows = await client.read(MODELS.labTestType, ids, [...FIELDS.labTestType])
  } catch {
    rows = await client.read(MODELS.labTestType, ids, ['id', 'rec_name', 'code'])
  }
  return rows.map((r) => ({
    id: Number(r.id),
    label: String(r.rec_name ?? r.name ?? r.code ?? r.id),
  }))
}

export async function createStaff(
  client: TrytonClient,
  data: StaffFormData,
): Promise<{ partyId: number; staffId: number | null }> {
  const code =
    data.code?.trim() ||
    `IST-STF-${String(Date.now()).slice(-6)}`

  const [partyId] = await client.create(MODELS.party, [
    {
      name: data.name.trim(),
      code,
      is_person: true,
      is_healthprof: true,
      active: true,
    },
  ])

  let staffId: number | null = null
  if (await client.modelExists(MODELS.healthProfessional)) {
    const vals: Record<string, unknown> = {
      party: partyId,
      active: true,
    }
    if (data.licenseCode?.trim()) vals.code = data.licenseCode.trim()
    if (data.institutionId) vals.institution = data.institutionId
    if (data.info?.trim()) vals.info = data.info.trim()
    const ids = await client.create(MODELS.healthProfessional, [vals])
    staffId = ids[0] ?? null
  }

  return { partyId, staffId }
}

export async function updateStaff(
  client: TrytonClient,
  opts: {
    staffId: number
    partyId?: number | null
    data: StaffFormData
  },
): Promise<void> {
  const { staffId, partyId, data } = opts

  if (partyId) {
    const partyVals: Record<string, unknown> = { name: data.name.trim() }
    if (data.code?.trim()) partyVals.code = data.code.trim()
    if (data.active != null) partyVals.active = data.active
    await client.write(MODELS.party, [partyId], partyVals)
  }

  const vals: Record<string, unknown> = {}
  if (data.licenseCode != null) vals.code = data.licenseCode.trim()
  if (data.info != null) vals.info = data.info.trim()
  if (data.active != null) vals.active = data.active
  if (data.institutionId != null) {
    vals.institution = data.institutionId || null
  }
  if (Object.keys(vals).length) {
    await client.write(MODELS.healthProfessional, [staffId], vals)
  }
}

/**
 * Create a lab test request on gnuhealth.patient.lab.test.
 * Field names vary by GH version — try common variants.
 * Throws with a clear message if the model is wizard-only / not writable.
 */
export async function createLabRequest(
  client: TrytonClient,
  data: LabRequestFormData,
): Promise<number> {
  if (!(await client.modelExists(MODELS.labRequest))) {
    throw new Error('Laboratory module is not available on this server')
  }

  const base: Record<string, unknown> = {
    urgent: Boolean(data.urgent),
  }
  if (data.date) {
    const dt = inputToTrytonDateTime(data.date.includes('T') ? data.date : `${data.date}T09:00`)
    if (dt) base.date = dt
  }

  // GNU Health typically uses patient_id / doctor_id / name(test type M2O)
  const variants: Record<string, unknown>[] = [
    {
      ...base,
      patient_id: data.patientId,
      doctor_id: data.doctorId,
      name: data.testTypeId,
    },
    {
      ...base,
      patient_id: data.patientId,
      doctor_id: data.doctorId,
      test_type: data.testTypeId,
    },
    {
      ...base,
      patient: data.patientId,
      doctor: data.doctorId,
      name: data.testTypeId,
    },
  ]

  let lastError: unknown = null
  for (const vals of variants) {
    try {
      const ids = await client.create(MODELS.labRequest, [vals])
      if (ids[0] != null) return ids[0]
    } catch (err) {
      lastError = err
    }
  }

  const msg =
    lastError instanceof Error
      ? lastError.message
      : 'Lab order create failed'
  throw new Error(
    `${msg}. Lab requests may require the SAO wizard (/sao/).`,
  )
}

export async function fetchStaff(
  client: TrytonClient,
  search = '',
  offset = 0,
  limit = 50,
): Promise<{
  records: Array<HealthProfRecord & { specialtyName?: string; institutionName?: string }>
  total: number
  available: boolean
}> {
  if (!(await client.modelExists(MODELS.healthProfessional))) {
    return { records: [], total: 0, available: false }
  }

  const domain: unknown[] = search
    ? ['|', ['rec_name', 'ilike', `%${search}%`], ['puid', 'ilike', `%${search}%`]]
    : []

  const ids = await client.search(
    MODELS.healthProfessional,
    domain,
    offset,
    limit,
    [['id', 'ASC']],
  )
  const total = await client.searchCount(MODELS.healthProfessional, domain)
  const rows = (await client.read(
    MODELS.healthProfessional,
    ids,
    [...FIELDS.healthProfList],
  )) as unknown as HealthProfRecord[]

  const specialtyNames = await client.resolveNames(
    MODELS.specialty,
    rows.map((r) => r.main_specialty),
  ).catch(async () => new Map<number, string>())

  const institutionNames = await client.resolveNames(
    MODELS.institution,
    rows.map((r) => r.institution),
  )

  return {
    available: true,
    total,
    records: rows.map((r) => ({
      ...r,
      specialtyName: r.main_specialty ? specialtyNames.get(r.main_specialty) : undefined,
      institutionName: r.institution ? institutionNames.get(r.institution) : undefined,
    })),
  }
}

export async function fetchStaffById(
  client: TrytonClient,
  id: number,
): Promise<{
  staff: HealthProfRecord & { specialtyName?: string; institutionName?: string }
  party: PartyRecord | null
}> {
  const rows = (await client.read(
    MODELS.healthProfessional,
    [id],
    [...FIELDS.healthProfList, 'info'],
  )) as unknown as HealthProfRecord[]
  if (!rows.length) throw new Error('Not found')
  const staff = rows[0]

  const specialtyNames = await client.resolveNames(MODELS.specialty, [staff.main_specialty])
  const institutionNames = await client.resolveNames(MODELS.institution, [staff.institution])

  let party: PartyRecord | null = null
  if (staff.party) {
    const parties = (await client.read(MODELS.party, [staff.party], [...FIELDS.partyDetail])) as unknown as PartyRecord[]
    party = parties[0] ?? null
  }

  return {
    staff: {
      ...staff,
      specialtyName: staff.main_specialty ? specialtyNames.get(staff.main_specialty) : undefined,
      institutionName: staff.institution ? institutionNames.get(staff.institution) : undefined,
    },
    party,
  }
}

function asIdList(values: unknown[]): Array<number | null | undefined> {
  return values.map((v) => (typeof v === 'number' ? v : v == null ? null : Number(v)))
}

export async function fetchLaboratory(
  client: TrytonClient,
): Promise<{
  records: Array<Record<string, unknown> & { patientName?: string }>
  results: Array<Record<string, unknown> & { patientName?: string }>
  testTypes: Record<string, unknown>[]
  total: number
  resultsTotal: number
  available: boolean
}> {
  type LabRow = Record<string, unknown> & { patientName?: string }
  const empty = {
    records: [] as LabRow[],
    results: [] as LabRow[],
    testTypes: [] as Record<string, unknown>[],
    total: 0,
    resultsTotal: 0,
    available: false,
  }

  const [reqExists, labExists, typesExists] = await Promise.all([
    client.modelExists(MODELS.labRequest),
    client.modelExists(MODELS.labTest),
    client.modelExists(MODELS.labTestType),
  ])
  if (!reqExists && !labExists) return empty

  const out = { ...empty, available: true }

  const tasks: Array<Promise<void>> = []

  if (reqExists) {
    tasks.push(
      (async () => {
        try {
          const ids = await client.search(MODELS.labRequest, [], 0, 50, [['id', 'DESC']])
          out.total = await client.searchCount(MODELS.labRequest)
          let rows: Record<string, unknown>[] = []
          try {
            rows = await client.read(MODELS.labRequest, ids, [...FIELDS.labRequest])
          } catch {
            rows = await client.read(MODELS.labRequest, ids, ['id', 'rec_name', 'state', 'date'])
          }
          const patientNames = await client.resolveNames(
            MODELS.patient,
            asIdList(rows.map((r) => r.patient_id ?? r.patient)),
          )
          out.records = rows.map((r) => {
            const pid = r.patient_id ?? r.patient
            return {
              ...r,
              patientName: typeof pid === 'number' ? patientNames.get(pid) : undefined,
            }
          })
        } catch {
          /* leave orders empty — do not fail whole page */
        }
      })(),
    )
  }

  if (labExists) {
    tasks.push(
      (async () => {
        try {
          const ids = await client.search(MODELS.labTest, [], 0, 50, [['id', 'DESC']])
          out.resultsTotal = await client.searchCount(MODELS.labTest)
          let rows: Record<string, unknown>[] = []
          try {
            rows = await client.read(MODELS.labTest, ids, [...FIELDS.labTest])
          } catch {
            rows = await client.read(MODELS.labTest, ids, [
              'id',
              'rec_name',
              'date_analysis',
              'state',
              'patient',
            ])
          }
          const patientNames = await client.resolveNames(
            MODELS.patient,
            asIdList(rows.map((r) => r.patient)),
          )
          out.results = rows.map((r) => ({
            ...r,
            patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
          }))
        } catch {
          /* leave results empty */
        }
      })(),
    )
  }

  if (typesExists) {
    tasks.push(
      (async () => {
        try {
          const ids = await client.search(MODELS.labTestType, [], 0, 100, null)
          try {
            out.testTypes = await client.read(MODELS.labTestType, ids, [...FIELDS.labTestType])
          } catch {
            out.testTypes = await client.read(MODELS.labTestType, ids, ['id', 'rec_name', 'code'])
          }
        } catch {
          /* leave types empty */
        }
      })(),
    )
  }

  await Promise.allSettled(tasks)
  return out
}

export async function fetchPharmacy(
  client: TrytonClient,
): Promise<{
  prescriptions: Record<string, unknown>[]
  products: Record<string, unknown>[]
  medicaments: Record<string, unknown>[]
  prescriptionTotal: number
  available: boolean
}> {
  const result = {
    prescriptions: [] as Record<string, unknown>[],
    products: [] as Record<string, unknown>[],
    medicaments: [] as Record<string, unknown>[],
    prescriptionTotal: 0,
    available: false,
  }

  const tasks: Array<Promise<void>> = []

  tasks.push(
    (async () => {
      if (!(await client.modelExists(MODELS.prescriptionOrder))) return
      result.available = true
      try {
        const ids = await client.search(MODELS.prescriptionOrder, [], 0, 50, [['id', 'DESC']])
        const [totalSettled, rowsSettled] = await Promise.allSettled([
          client.searchCount(MODELS.prescriptionOrder),
          client.read(MODELS.prescriptionOrder, ids, [...FIELDS.prescriptionOrder]),
        ])
        if (totalSettled.status === 'fulfilled') result.prescriptionTotal = totalSettled.value
        if (rowsSettled.status === 'fulfilled') result.prescriptions = rowsSettled.value
        else if (ids.length) {
          result.prescriptions = await client.read(MODELS.prescriptionOrder, ids, ['id', 'rec_name', 'state'])
        }
      } catch {
        /* leave prescriptions empty */
      }
    })(),
  )

  tasks.push(
    (async () => {
      if (!(await client.modelExists(MODELS.productTemplate))) return
      result.available = true
      try {
        const ids = await client.search(MODELS.productTemplate, [], 0, 100, [['name', 'ASC']])
        try {
          result.products = await client.read(MODELS.productTemplate, ids, [...FIELDS.product])
        } catch {
          result.products = await client.read(MODELS.productTemplate, ids, ['id', 'name', 'rec_name', 'active'])
        }
      } catch {
        /* leave products empty */
      }
    })(),
  )

  tasks.push(
    (async () => {
      if (!(await client.modelExists(MODELS.medicament))) return
      result.available = true
      try {
        const ids = await client.search(MODELS.medicament, [], 0, 50, null)
        try {
          result.medicaments = await client.read(MODELS.medicament, ids, [...FIELDS.medicament])
        } catch {
          result.medicaments = await client.read(MODELS.medicament, ids, ['id', 'rec_name', 'active'])
        }
      } catch {
        /* leave medicaments empty */
      }
    })(),
  )

  await Promise.allSettled(tasks)
  return result
}

export async function fetchEvaluations(
  client: TrytonClient,
): Promise<{ records: Record<string, unknown>[]; total: number; available: boolean }> {
  if (!(await client.modelExists(MODELS.evaluation))) {
    return { records: [], total: 0, available: false }
  }
  const ids = await client.search(MODELS.evaluation, [], 0, 50, [['id', 'DESC']])
  const total = await client.searchCount(MODELS.evaluation)
  const records = await client.read(MODELS.evaluation, ids, [...FIELDS.evaluation])
  return { records, total, available: true }
}

export async function fetchMedications(
  client: TrytonClient,
): Promise<{ records: Record<string, unknown>[]; total: number; available: boolean }> {
  if (!(await client.modelExists(MODELS.medication))) {
    return { records: [], total: 0, available: false }
  }
  const ids = await client.search(MODELS.medication, [], 0, 50, [['id', 'DESC']])
  const total = await client.searchCount(MODELS.medication)
  const records = await client.read(MODELS.medication, ids, [...FIELDS.medication])
  return { records, total, available: true }
}

export async function fetchBeds(
  client: TrytonClient,
): Promise<{
  records: Record<string, unknown>[]
  admissions: Array<Record<string, unknown> & { patientName?: string }>
  total: number
  admissionsTotal: number
  available: boolean
}> {
  const hasBeds = await client.modelExists(MODELS.hospitalBed)
  const hasInpatient = await client.modelExists(MODELS.inpatientRegistration)
  if (!hasBeds && !hasInpatient) {
    return { records: [], admissions: [], total: 0, admissionsTotal: 0, available: false }
  }

  const result = {
    records: [] as Record<string, unknown>[],
    admissions: [] as Array<Record<string, unknown> & { patientName?: string }>,
    total: 0,
    admissionsTotal: 0,
    available: true,
  }

  const tasks: Array<Promise<void>> = []

  if (hasBeds) {
    tasks.push(
      (async () => {
        try {
          const ids = await client.search(MODELS.hospitalBed, [], 0, 100, [['id', 'ASC']])
          result.total = await client.searchCount(MODELS.hospitalBed)
          try {
            result.records = await client.read(MODELS.hospitalBed, ids, [...FIELDS.hospitalBed])
          } catch {
            result.records = await client.read(MODELS.hospitalBed, ids, ['id', 'rec_name', 'state'])
          }
        } catch {
          /* leave beds empty */
        }
      })(),
    )
  }

  if (hasInpatient) {
    tasks.push(
      (async () => {
        try {
          const ids = await client.search(
            MODELS.inpatientRegistration,
            [],
            0,
            50,
            [['id', 'DESC']],
          )
          result.admissionsTotal = await client.searchCount(MODELS.inpatientRegistration)
          let rows: Record<string, unknown>[] = []
          try {
            rows = await client.read(MODELS.inpatientRegistration, ids, [...FIELDS.inpatientRegistration])
          } catch {
            rows = await client.read(MODELS.inpatientRegistration, ids, ['id', 'rec_name', 'patient', 'state'])
          }
          const patientNames = await client.resolveNames(
            MODELS.patient,
            asIdList(rows.map((r) => r.patient)),
          )
          result.admissions = rows.map((r) => ({
            ...r,
            patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
          }))
        } catch {
          /* leave admissions empty */
        }
      })(),
    )
  }

  await Promise.allSettled(tasks)
  return result
}

export async function fetchNursing(
  client: TrytonClient,
): Promise<{
  records: Array<Record<string, unknown> & { patientName?: string }>
  ambulatory: Array<Record<string, unknown> & { patientName?: string }>
  total: number
  available: boolean
}> {
  const hasRounding = await client.modelExists(MODELS.nursingRounding)
  const hasAmbulatory = await client.modelExists(MODELS.ambulatoryCare)
  if (!hasRounding && !hasAmbulatory) {
    return { records: [], ambulatory: [], total: 0, available: false }
  }

  const result = {
    records: [] as Array<Record<string, unknown> & { patientName?: string }>,
    ambulatory: [] as Array<Record<string, unknown> & { patientName?: string }>,
    total: 0,
    available: true,
  }

  if (hasRounding) {
    const ids = await client.search(MODELS.nursingRounding, [], 0, 50, [['id', 'DESC']])
    result.total = await client.searchCount(MODELS.nursingRounding)
    const rows = await client.read(MODELS.nursingRounding, ids, [...FIELDS.nursingRounding])
    result.records = rows.map((r) => ({ ...r }))
  }

  if (hasAmbulatory) {
    const ids = await client.search(MODELS.ambulatoryCare, [], 0, 50, [['id', 'DESC']])
    const rows = await client.read(MODELS.ambulatoryCare, ids, [...FIELDS.ambulatoryCare])
    const patientNames = await client.resolveNames(
      MODELS.patient,
      asIdList(rows.map((r) => r.patient)),
    )
    result.ambulatory = rows.map((r) => ({
      ...r,
      patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
    }))
  }

  return result
}

export async function fetchSurgeries(
  client: TrytonClient,
): Promise<{
  records: Array<Record<string, unknown> & { patientName?: string }>
  total: number
  available: boolean
}> {
  if (!(await client.modelExists(MODELS.surgery))) {
    return { records: [], total: 0, available: false }
  }
  const ids = await client.search(MODELS.surgery, [], 0, 50, [['id', 'DESC']])
  const total = await client.searchCount(MODELS.surgery)
  const rows = await client.read(MODELS.surgery, ids, [...FIELDS.surgery])
  const patientNames = await client.resolveNames(
    MODELS.patient,
    asIdList(rows.map((r) => r.patient)),
  )
  return {
    available: true,
    total,
    records: rows.map((r) => ({
      ...r,
      patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
    })),
  }
}

export async function fetchProcedures(
  client: TrytonClient,
): Promise<{
  records: Array<Record<string, unknown> & { patientName?: string }>
  surgeries: Array<Record<string, unknown> & { patientName?: string }>
  total: number
  available: boolean
}> {
  const hasPatientProc = await client.modelExists(MODELS.patientProcedure)
  const hasOperation = await client.modelExists(MODELS.procedure)
  const hasSurgery = await client.modelExists(MODELS.surgery)
  if (!hasPatientProc && !hasOperation && !hasSurgery) {
    return { records: [], surgeries: [], total: 0, available: false }
  }

  const result = {
    records: [] as Array<Record<string, unknown> & { patientName?: string }>,
    surgeries: [] as Array<Record<string, unknown> & { patientName?: string }>,
    total: 0,
    available: true,
  }

  const procModel = hasPatientProc ? MODELS.patientProcedure : hasOperation ? MODELS.procedure : null
  if (procModel) {
    const fields = hasPatientProc ? FIELDS.patientProcedure : FIELDS.procedure
    const ids = await client.search(procModel, [], 0, 50, [['id', 'DESC']])
    result.total = await client.searchCount(procModel)
    const rows = await client.read(procModel, ids, [...fields])
    const patientNames = await client.resolveNames(
      MODELS.patient,
      asIdList(rows.map((r) => r.patient)),
    )
    result.records = rows.map((r) => ({
      ...r,
      patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
    }))
  }

  if (hasSurgery) {
    const surg = await fetchSurgeries(client)
    result.surgeries = surg.records
    if (!procModel) result.total = surg.total
  }

  return result
}

export async function fetchImaging(
  client: TrytonClient,
): Promise<{
  records: Array<Record<string, unknown> & { patientName?: string }>
  results: Array<Record<string, unknown> & { patientName?: string }>
  tests: Record<string, unknown>[]
  total: number
  available: boolean
}> {
  const hasRequest = await client.modelExists(MODELS.imagingRequest)
  const hasResult = await client.modelExists(MODELS.imagingResult)
  const hasTest = await client.modelExists(MODELS.imagingTest)
  if (!hasRequest && !hasResult) {
    return { records: [], results: [], tests: [], total: 0, available: false }
  }

  const out = {
    records: [] as Array<Record<string, unknown> & { patientName?: string }>,
    results: [] as Array<Record<string, unknown> & { patientName?: string }>,
    tests: [] as Record<string, unknown>[],
    total: 0,
    available: true,
  }

  if (hasRequest) {
    const ids = await client.search(MODELS.imagingRequest, [], 0, 50, [['id', 'DESC']])
    out.total = await client.searchCount(MODELS.imagingRequest)
    const rows = await client.read(MODELS.imagingRequest, ids, [...FIELDS.imagingRequest])
    const patientNames = await client.resolveNames(
      MODELS.patient,
      asIdList(rows.map((r) => r.patient)),
    )
    out.records = rows.map((r) => ({
      ...r,
      patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
    }))
  }

  if (hasResult) {
    const ids = await client.search(MODELS.imagingResult, [], 0, 50, [['id', 'DESC']])
    const rows = await client.read(MODELS.imagingResult, ids, [...FIELDS.imagingResult])
    const patientNames = await client.resolveNames(
      MODELS.patient,
      asIdList(rows.map((r) => r.patient)),
    )
    out.results = rows.map((r) => ({
      ...r,
      patientName: typeof r.patient === 'number' ? patientNames.get(r.patient) : undefined,
    }))
  }

  if (hasTest) {
    const ids = await client.search(MODELS.imagingTest, [], 0, 100, [['name', 'ASC']])
    out.tests = await client.read(MODELS.imagingTest, ids, [...FIELDS.imagingTest])
  }

  return out
}

export async function fetchInstitution(
  client: TrytonClient,
): Promise<InstitutionRecord | null> {
  if (!(await client.modelExists(MODELS.institution))) return null
  const ids = await client.search(MODELS.institution, [], 0, 1)
  if (!ids.length) return null
  const rows = (await client.read(
    MODELS.institution,
    ids,
    [...FIELDS.institution],
  )) as unknown as InstitutionRecord[]
  return rows[0] ?? null
}

export async function fetchRecentAppointments(
  client: TrytonClient,
  limit = 5,
): Promise<Array<AppointmentRecord & { patientName?: string }>> {
  if (!(await client.modelExists(MODELS.appointment))) return []
  try {
    const ids = await client.search(
      MODELS.appointment,
      [],
      0,
      limit,
      [['appointment_date', 'DESC']],
    )
    if (!ids.length) return []
    const rows = (await client.read(
      MODELS.appointment,
      ids,
      [...FIELDS.appointmentList],
    )) as unknown as AppointmentRecord[]
    const patientNames = await client.resolveNames(
      MODELS.patient,
      rows.map((r) => r.patient),
    )
    return rows.map((r) => ({
      ...r,
      patientName: r.patient ? patientNames.get(r.patient) : undefined,
    }))
  } catch {
    return []
  }
}

async function safeModelList(
  client: TrytonClient,
  model: string,
  fields: readonly string[],
  order: unknown[] | null = [['id', 'DESC']],
  limit = 100,
): Promise<{ records: Record<string, unknown>[]; total: number; available: boolean }> {
  if (!(await client.modelExists(model))) {
    return { records: [], total: 0, available: false }
  }
  try {
    const ids = await client.search(model, [], 0, limit, order)
    const total = await client.searchCount(model)
    const records = ids.length ? await client.read(model, ids, [...fields]) : []
    return { records, total, available: true }
  } catch {
    return { records: [], total: 0, available: false }
  }
}

export async function fetchParties(client: TrytonClient, search = '', offset = 0, limit = 50) {
  const domain: unknown[] = search
    ? ['|', ['name', 'ilike', `%${search}%`], ['code', 'ilike', `%${search}%`]]
    : []
  if (!(await client.modelExists(MODELS.party))) {
    return { records: [] as PartyRecord[], total: 0, available: false }
  }
  try {
    const [idsResult, totalResult] = await Promise.allSettled([
      client.search(MODELS.party, domain, offset, limit, [['name', 'ASC']]),
      client.searchCount(MODELS.party, domain),
    ])
    if (idsResult.status === 'rejected') throw idsResult.reason
    const ids = idsResult.value
    const total = totalResult.status === 'fulfilled' ? totalResult.value : ids.length
    let records: PartyRecord[] = []
    try {
      records = (await client.read(
        MODELS.party,
        ids,
        [...FIELDS.partyOpsList],
      )) as unknown as PartyRecord[]
    } catch {
      records = (await client.read(MODELS.party, ids, [
        'id',
        'name',
        'code',
        'active',
      ])) as unknown as PartyRecord[]
    }
    return { records, total, available: true }
  } catch {
    return { records: [] as PartyRecord[], total: 0, available: false }
  }
}

export async function fetchCompanies(client: TrytonClient) {
  return safeModelList(client, MODELS.company, FIELDS.companyList, [['id', 'ASC']], 50)
}

export async function fetchProductVariants(client: TrytonClient) {
  const templates = await safeModelList(
    client,
    MODELS.productTemplate,
    FIELDS.product,
    [['id', 'ASC']],
    100,
  )
  const variants = await safeModelList(
    client,
    MODELS.product,
    FIELDS.productList,
    [['id', 'ASC']],
    100,
  )
  return {
    templates: templates.records,
    variants: variants.records,
    total: variants.total || templates.total,
    available: templates.available || variants.available,
  }
}

export async function fetchStock(client: TrytonClient) {
  const locations = await safeModelList(
    client,
    MODELS.stockLocation,
    FIELDS.stockLocationList,
    [['id', 'ASC']],
    100,
  )
  const moves = await safeModelList(
    client,
    MODELS.stockMove,
    FIELDS.stockMoveList,
    [['id', 'DESC']],
    50,
  )
  return {
    locations: locations.records,
    moves: moves.records,
    total: locations.total,
    movesTotal: moves.total,
    available: locations.available || moves.available,
  }
}

export async function fetchInvoices(client: TrytonClient) {
  return safeModelList(client, MODELS.accountInvoice, FIELDS.invoiceList, [['id', 'DESC']], 50)
}

export async function fetchCurrencies(client: TrytonClient) {
  return safeModelList(client, MODELS.currency, FIELDS.currencyList, [['code', 'ASC']], 100)
}

export async function fetchCalendarData(client: TrytonClient) {
  const calendars = await safeModelList(
    client,
    MODELS.calendar,
    FIELDS.calendarList,
    [['name', 'ASC']],
    50,
  )
  const events = await safeModelList(
    client,
    MODELS.calendarEvent,
    FIELDS.calendarEventList,
    [['id', 'DESC']],
    50,
  )
  return {
    calendars: calendars.records,
    events: events.records,
    total: events.total || calendars.total,
    available: calendars.available || events.available,
  }
}

export async function fetchUsers(client: TrytonClient, search = '') {
  if (!(await client.modelExists(MODELS.user))) {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
  const domain: unknown[] = search
    ? [
        '|',
        ['login', 'ilike', `%${search}%`],
        ['name', 'ilike', `%${search}%`],
      ]
    : []
  try {
    const ids = await client.search(MODELS.user, domain, 0, 100, [['login', 'ASC']])
    const total = await client.searchCount(MODELS.user, domain)
    let records: Record<string, unknown>[] = []
    if (ids.length) {
      try {
        records = await client.read(MODELS.user, ids, [...FIELDS.userList])
      } catch {
        records = await client.read(MODELS.user, ids, ['id', 'rec_name', 'name', 'login', 'active'])
      }
    }
    return { records, total, available: true }
  } catch {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
}

export async function fetchGroups(client: TrytonClient) {
  return safeModelList(client, MODELS.group, FIELDS.groupList, [['name', 'ASC']], 200)
}

export async function fetchGroupDetail(client: TrytonClient, id: number) {
  const rows = await client.read(MODELS.group, [id], [...FIELDS.groupDetail]).catch(() =>
    client.read(MODELS.group, [id], ['id', 'rec_name', 'name']),
  )
  const group = rows[0] ?? null
  let access: Record<string, unknown>[] = []
  if (await client.modelExists(MODELS.modelAccess)) {
    try {
      const accessIds = await client.search(
        MODELS.modelAccess,
        [['group', '=', id]],
        0,
        40,
        [['id', 'ASC']],
      )
      if (accessIds.length) {
        access = await client.read(MODELS.modelAccess, accessIds, [...FIELDS.modelAccessList])
      }
    } catch {
      access = []
    }
  }
  return { group, access }
}

export type UserFormData = {
  login: string
  name: string
  active?: boolean
  email?: string
  password?: string
  groupIds?: number[]
}

function m2mSet(ids: number[]): Array<['add' | 'set' | 'remove', number[]]> {
  return [['set', ids]]
}

export async function createUser(client: TrytonClient, data: UserFormData): Promise<number> {
  const vals: Record<string, unknown> = {
    login: data.login.trim(),
    name: data.name.trim(),
    active: data.active !== false,
  }
  if (data.email?.trim()) vals.email = data.email.trim()
  if (data.password) vals.password = data.password
  if (data.groupIds?.length) vals.groups = m2mSet(data.groupIds)
  const [id] = await client.create(MODELS.user, [vals])
  return id
}

export async function updateUser(
  client: TrytonClient,
  id: number,
  data: UserFormData,
): Promise<void> {
  const vals: Record<string, unknown> = {
    login: data.login.trim(),
    name: data.name.trim(),
    active: data.active !== false,
  }
  if (data.email != null) vals.email = data.email.trim()
  if (data.password) vals.password = data.password
  if (data.groupIds) vals.groups = m2mSet(data.groupIds)
  await client.write(MODELS.user, [id], vals)
}

export async function resetUserPassword(
  client: TrytonClient,
  id: number,
  password: string,
): Promise<void> {
  await client.write(MODELS.user, [id], { password })
}

export async function fetchModules(client: TrytonClient, search = '') {
  if (!(await client.modelExists(MODELS.module))) {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
  const domain: unknown[] = search ? [['name', 'ilike', `%${search}%`]] : []
  try {
    const ids = await client.search(MODELS.module, domain, 0, 300, [['name', 'ASC']])
    const total = await client.searchCount(MODELS.module, domain)
    const records = ids.length
      ? await client.read(MODELS.module, ids, [...FIELDS.moduleList])
      : []
    return { records, total, available: true }
  } catch {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
}

/** Mark modules for activation / upgrade via model buttons when exposed. */
export async function markModulesAction(
  client: TrytonClient,
  ids: number[],
  action: 'activate' | 'upgrade' | 'deactivate',
): Promise<{ ok: boolean; message: string }> {
  if (!ids.length) return { ok: false, message: 'No modules selected' }
  try {
    await client.call(MODELS.module, action, ids, {})
    return {
      ok: true,
      message: `Marked ${ids.length} module(s) for ${action}. Apply with trytond-admin or SAO pending upgrades.`,
    }
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err)
    return {
      ok: false,
      message: `Could not call ir.module.${action}: ${msg}. Use trytond-admin on the server or SAO.`,
    }
  }
}

export async function fetchSequences(client: TrytonClient, search = '') {
  if (!(await client.modelExists(MODELS.sequence))) {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
  const domain: unknown[] = search
    ? [
        '|',
        ['name', 'ilike', `%${search}%`],
        ['code', 'ilike', `%${search}%`],
      ]
    : []
  try {
    const ids = await client.search(MODELS.sequence, domain, 0, 150, [['name', 'ASC']])
    const total = await client.searchCount(MODELS.sequence, domain)
    let records: Record<string, unknown>[] = []
    if (ids.length) {
      try {
        records = await client.read(MODELS.sequence, ids, [...FIELDS.sequenceList])
      } catch {
        records = await client.read(MODELS.sequence, ids, [
          'id',
          'rec_name',
          'name',
          'code',
          'prefix',
          'number_next',
        ])
      }
    }
    return { records, total, available: true }
  } catch {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
}

export async function updateSequence(
  client: TrytonClient,
  id: number,
  vals: { number_next?: number; prefix?: string; suffix?: string },
): Promise<void> {
  const payload: Record<string, unknown> = {}
  if (vals.number_next != null && Number.isFinite(vals.number_next)) {
    payload.number_next = vals.number_next
  }
  if (vals.prefix != null) payload.prefix = vals.prefix
  if (vals.suffix != null) payload.suffix = vals.suffix
  await client.write(MODELS.sequence, [id], payload)
}

export async function fetchLanguages(client: TrytonClient) {
  return safeModelList(client, MODELS.lang, FIELDS.langList, [['code', 'ASC']], 100)
}

export async function fetchCountries(client: TrytonClient, search = '') {
  if (!(await client.modelExists(MODELS.country))) {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
  const domain: unknown[] = search
    ? [
        '|',
        ['name', 'ilike', `%${search}%`],
        ['code', 'ilike', `%${search}%`],
      ]
    : []
  try {
    const ids = await client.search(MODELS.country, domain, 0, 250, [['code', 'ASC']])
    const total = await client.searchCount(MODELS.country, domain)
    let records: Record<string, unknown>[] = []
    if (ids.length) {
      try {
        records = await client.read(MODELS.country, ids, [...FIELDS.countryList])
      } catch {
        records = await client.read(MODELS.country, ids, ['id', 'rec_name', 'name', 'code'])
      }
    }
    return { records, total, available: true }
  } catch {
    return { records: [] as Record<string, unknown>[], total: 0, available: false }
  }
}

/** IST Technologies LLC defaults from config.yaml (Qatar office). */
export const IST_COMPANY_DEFAULTS = {
  name: 'IST Technologies LLC',
  code: 'IST',
  street: 'Office 214/215, 2nd Floor, Regus D-Ring Building no 65, D-Ring Road',
  city: 'Doha',
  countryCode: 'QA',
  email: 'info@isttechnologies.qa',
  website: 'https://www.isttechnologies.qa',
} as const

export type CompanySetupData = {
  name: string
  code?: string
  street?: string
  city?: string
  email?: string
  website?: string
}

export async function createCompanySetup(
  client: TrytonClient,
  data: CompanySetupData,
): Promise<{ partyId: number; companyId: number }> {
  const partyVals: Record<string, unknown> = {
    name: data.name.trim(),
    is_company: true,
    active: true,
  }
  if (data.code?.trim()) partyVals.code = data.code.trim()
  if (data.email?.trim()) partyVals.email = data.email.trim()
  if (data.website?.trim()) partyVals.website = data.website.trim()

  let partyId: number
  try {
    ;[partyId] = await client.create(MODELS.party, [partyVals])
  } catch {
    delete partyVals.email
    delete partyVals.website
    ;[partyId] = await client.create(MODELS.party, [partyVals])
  }

  // Optional address (best-effort)
  if (await client.modelExists(MODELS.partyAddress)) {
    try {
      let countryId: number | null = null
      if (await client.modelExists(MODELS.country)) {
        const cids = await client.search(
          MODELS.country,
          [['code', '=', IST_COMPANY_DEFAULTS.countryCode]],
          0,
          1,
        )
        countryId = cids[0] ?? null
      }
      const addr: Record<string, unknown> = {
        party: partyId,
        street: data.street?.trim() || IST_COMPANY_DEFAULTS.street,
        city: data.city?.trim() || IST_COMPANY_DEFAULTS.city,
      }
      if (countryId) addr.country = countryId
      await client.create(MODELS.partyAddress, [addr])
    } catch {
      /* address optional */
    }
  }

  const [companyId] = await client.create(MODELS.company, [{ party: partyId }])
  return { partyId, companyId }
}

/** Draft invoice stub — creates minimal out invoice when chart allows; else throws. */
export async function createInvoiceStub(
  client: TrytonClient,
  opts: { partyId: number; type?: 'out' | 'in' },
): Promise<number> {
  const vals: Record<string, unknown> = {
    type: opts.type ?? 'out',
    party: opts.partyId,
  }
  const [id] = await client.create(MODELS.accountInvoice, [vals])
  return id
}
