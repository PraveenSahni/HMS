/**
 * Map Tryton / GNU Health models to dedicated React routes.
 * Unmapped act_window models open the generic ModelBrowser at /menu/:menuId.
 */

export const MODEL_ROUTE_MAP: Record<string, string> = {
  'gnuhealth.patient': '/patients',
  'party.party': '/parties',
  'gnuhealth.appointment': '/appointments',
  'gnuhealth.healthprofessional': '/staff',
  'gnuhealth.patient.lab.test': '/laboratory',
  'gnuhealth.lab': '/laboratory',
  'gnuhealth.lab.test_type': '/laboratory',
  'gnuhealth.prescription.order': '/pharmacy',
  'gnuhealth.prescription': '/pharmacy',
  'gnuhealth.medicament': '/pharmacy',
  'product.template': '/products',
  'product.product': '/products',
  'gnuhealth.patient.medication': '/medications',
  'gnuhealth.patient.evaluation': '/evaluations',
  'gnuhealth.hospital.bed': '/beds',
  'gnuhealth.inpatient.registration': '/beds',
  'gnuhealth.patient.rounding': '/nursing',
  'gnuhealth.patient.ambulatory_care': '/nursing',
  'gnuhealth.surgery': '/procedures',
  'gnuhealth.operation': '/procedures',
  'gnuhealth.patient.procedure': '/procedures',
  'gnuhealth.imaging.test.request': '/imaging',
  'gnuhealth.imaging.test': '/imaging',
  'gnuhealth.imaging.test.result': '/imaging',
  'gnuhealth.institution': '/settings',
  'stock.location': '/stock',
  'stock.move': '/stock',
  'account.invoice': '/financial',
  'currency.currency': '/currency',
  'calendar.calendar': '/calendar',
  'calendar.event': '/calendar',
  'company.company': '/companies',
  'res.user': '/users',
  'res.group': '/groups',
  'ir.module': '/modules',
  'ir.sequence': '/sequences',
  'ir.lang': '/languages',
  'country.country': '/countries',
  'ir.model.access': '/groups',
}

/** Prefer these display fields when browsing an unmapped model. */
export const GENERIC_LIST_FIELDS = [
  'id',
  'rec_name',
  'name',
  'code',
  'state',
  'active',
  'create_date',
  'write_date',
] as const

export function routeForModel(model: string | null | undefined): string | null {
  if (!model) return null
  return MODEL_ROUTE_MAP[model] ?? null
}
