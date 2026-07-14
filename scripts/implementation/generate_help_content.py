#!/usr/bin/env python3
"""Generate EN/AR help-content JSON articles with metadata (Section 9.3 workflows).

Content layout (intentional adaptation of brief folder tree):
  frontend/help-content/{en|ar}/*.json  — flat articles with roles[] metadata
  (Equivalent to en/common, en/admin, … folders; role filtering is metadata-driven.)
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EN = ROOT / "frontend" / "help-content" / "en"
AR = ROOT / "frontend" / "help-content" / "ar"
PUB_EN = ROOT / "frontend" / "public" / "help-content" / "en"
PUB_AR = ROOT / "frontend" / "public" / "help-content" / "ar"
for d in (EN, AR, PUB_EN, PUB_AR):
    d.mkdir(parents=True, exist_ok=True)

# Document adaptation for auditors
STRUCTURE_NOTE = ROOT / "frontend" / "help-content" / "STRUCTURE.md"


def wf(
    id_: str,
    title_en: str,
    title_ar: str,
    roles: list[str],
    routes: list[str],
    keywords: list[str],
    steps_en: list[str],
    steps_ar: list[str],
    body_en: str,
    body_ar: str,
    countries: list[str] | None = None,
) -> dict:
    return {
        "id": id_,
        "title_en": title_en,
        "title_ar": title_ar,
        "roles": roles,
        "countries": countries or ["AE", "QA"],
        "routes": routes,
        "keywords": keywords,
        "version": "1.1.0",
        "guided": True,
        "published": True,
        "steps_en": steps_en,
        "steps_ar": steps_ar,
        "body_en": body_en,
        "body_ar": body_ar,
    }


ARTICLES: list[dict] = [
    {
        "id": "help-overview",
        "title_en": "Help Centre overview",
        "title_ar": "نظرة عامة على مركز المساعدة",
        "roles": ["*"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["help", "start", "overview", "onboarding"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Use search, role/country filters, guided workflows, onboarding checklist, and feedback. Content loads from help-content JSON — not hardcoded in UI.",
        "body_ar": "استخدم البحث والتصفية حسب الدور والدولة وسير العمل الإرشادي وقائمة التهيئة والملاحظات. يُحمَّل المحتوى من ملفات JSON.",
    },
    {
        "id": "onboarding-checklist",
        "title_en": "Onboarding checklist",
        "title_ar": "قائمة التحقق للتأهيل",
        "roles": ["*"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["onboarding", "checklist", "training", "new user"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Complete: (1) Sign in and set language EN/AR. (2) Set Help role + country filters. (3) Open Patients and find a synthetic IST-P-* record. (4) Open Appointments day list. (5) Run one guided workflow for your role. (6) Review synthetic-data policy. Track progress in the Help Centre onboarding panel.",
        "body_ar": "أكمل: تسجيل الدخول وتعيين اللغة، تعيين دور/دولة المساعدة، فتح المرضى الاصطناعيين، المواعيد، سير عمل إرشادي، ومراجعة سياسة البيانات الاصطناعية.",
    },
    # --- Section 9.3 guided workflows (26) ---
    wf(
        "wf-create-company",
        "Workflow: Creating a company",
        "سير العمل: إنشاء شركة",
        ["GroupAdmin", "CountryAdmin", "SystemAdmin"],
        ["/companies"],
        ["company", "legal entity", "multi-company"],
        [
            "Open Companies (/companies).",
            "Create company for UAE (AED) or Qatar (QAR) legal entity.",
            "Set currency and party address (synthetic for non-prod).",
            "Confirm company appears in list; do not mix AE/QA charts without legal basis.",
        ],
        [
            "افتح الشركات (/companies).",
            "أنشئ شركة لكيان قانوني في الإمارات أو قطر.",
            "عيّن العملة والعنوان (اصطناعي خارج الإنتاج).",
            "تحقق من الظهور؛ لا تخلط بيانات الدول دون أساس قانوني.",
        ],
        "Maps to Tryton company.company. Group/Country admins own entity creation.",
        "يرتبط بنموذج company.company.",
    ),
    wf(
        "wf-create-hospital",
        "Workflow: Creating a hospital",
        "سير العمل: إنشاء مستشفى",
        ["FacilityAdmin", "CountryAdmin", "SystemAdmin"],
        ["/settings"],
        ["hospital", "institution", "facility"],
        [
            "Open Settings / institution.",
            "Create gnuhealth.institution linked to the correct country company.",
            "Set facility type Hospital and codes (synthetic in non-prod).",
            "Verify in institution list before adding departments.",
        ],
        [
            "افتح الإعدادات / المؤسسة.",
            "أنشئ مؤسسة مرتبطة بشركة الدولة الصحيحة.",
            "حدد النوع مستشفى والرموز.",
            "تحقق قبل إضافة الأقسام.",
        ],
        "Uses gnuhealth.institution. Confirm MoPH/DHA facility codes with authority.",
        "يستخدم gnuhealth.institution. أكد رموز المنشأة مع الجهة المختصة.",
    ),
    wf(
        "wf-create-clinic",
        "Workflow: Creating a clinic",
        "سير العمل: إنشاء عيادة",
        ["FacilityAdmin", "CountryAdmin"],
        ["/settings"],
        ["clinic", "outpatient", "institution"],
        [
            "Open Settings.",
            "Create institution with type Clinic under the country company.",
            "Link operating hours and specialties as configured.",
            "Save and verify facility isolation (AE vs QA entity).",
        ],
        [
            "افتح الإعدادات.",
            "أنشئ مؤسسة من نوع عيادة تحت شركة الدولة.",
            "اربط ساعات العمل والتخصصات.",
            "احفظ وتحقق من عزل المنشأة.",
        ],
        "Clinic is an institution subtype; keep under correct legal entity.",
        "العيادة نوع مؤسسة؛ أبقها تحت الكيان القانوني الصحيح.",
    ),
    wf(
        "wf-create-department",
        "Workflow: Creating a department",
        "سير العمل: إنشاء قسم",
        ["FacilityAdmin", "DeptManager", "SystemAdmin"],
        ["/settings", "/menu"],
        ["department", "unit", "ward"],
        [
            "Open institution / units (SAO if React limited).",
            "Create department or operational unit under the facility.",
            "Assign manager and specialty as needed.",
            "Confirm beds/stock locations can reference the unit.",
        ],
        [
            "افتح وحدات المؤسسة (SAO عند الحاجة).",
            "أنشئ قسماً تحت المنشأة.",
            "عيّن المدير والتخصص.",
            "أكد ربط الأسرّة/المخزون بالوحدة.",
        ],
        "Departments map to gnuhealth.institution.unit (or equivalent).",
        "ترتبط الأقسام بوحدات المؤسسة.",
    ),
    wf(
        "wf-create-pharmacy",
        "Workflow: Creating a pharmacy",
        "سير العمل: إنشاء صيدلية",
        ["FacilityAdmin", "Pharmacist", "SystemAdmin"],
        ["/pharmacy", "/stock"],
        ["pharmacy", "dispensary", "stock location"],
        [
            "Create pharmacy institution or stock location under facility.",
            "Link formulary products and warehouse parent.",
            "Assign pharmacist group users.",
            "Verify dispense workflow can select the location.",
        ],
        [
            "أنشئ صيدلية أو موقع مخزون تحت المنشأة.",
            "اربط قائمة الأدوية والمخزن الأب.",
            "عيّن مستخدمي مجموعة الصيدلي.",
            "تحقق من إمكانية الصرف من الموقع.",
        ],
        "Pharmacy uses health_stock / stock.location patterns.",
        "تستخدم الصيدلية نماذج المخزون.",
    ),
    wf(
        "wf-create-laboratory",
        "Workflow: Creating a laboratory",
        "سير العمل: إنشاء مختبر",
        ["FacilityAdmin", "LabSupervisor", "SystemAdmin"],
        ["/laboratory", "/settings"],
        ["laboratory", "LIMS", "lab"],
        [
            "Ensure health_lab module is activated.",
            "Configure lab institution/unit and test catalog.",
            "Assign LabTech / LabSupervisor groups.",
            "Place a test order to validate end-to-end.",
        ],
        [
            "تأكد من تفعيل health_lab.",
            "اضبط وحدة المختبر وكتالوج الفحوصات.",
            "عيّن مجموعات فني/مشرف المختبر.",
            "أنشئ طلباً تجريبياً للتحقق.",
        ],
        "Requires health_lab. UI shows module-missing if absent.",
        "يتطلب health_lab.",
    ),
    wf(
        "wf-create-users-roles",
        "Workflow: Creating users and assigning roles",
        "سير العمل: إنشاء مستخدمين وتعيين أدوار",
        ["SystemAdmin", "FacilityAdmin", "ITSupport", "GroupAdmin"],
        ["/users", "/groups"],
        ["users", "groups", "roles", "ACL"],
        [
            "Open Users (/users); create user with synthetic email.",
            "Open Groups (/groups); assign Tryton groups matching IST role packs.",
            "Confirm company/institution access (record rules when deployed).",
            "Have user sign in and verify menu ACL.",
        ],
        [
            "افتح المستخدمين وأنشئ مستخدماً ببريد اصطناعي.",
            "عيّن مجموعات Tryton المطابقة لأدوار IST.",
            "أكد صلاحيات الشركة/المنشأة.",
            "تحقق من القوائم بعد تسجيل الدخول.",
        ],
        "Deep record-rule editing remains in SAO until React admin covers it.",
        "تحرير قواعد السجلات المتقدم يبقى في SAO.",
    ),
    wf(
        "wf-register-patient",
        "Workflow: Registering a patient",
        "سير العمل: تسجيل مريض",
        ["Receptionist", "CallCentre", "Physician", "FacilityAdmin"],
        ["/patients"],
        ["patient", "register", "demographics"],
        [
            "Open Patients (/patients).",
            "Create demographics; use synthetic IDs only in non-prod (IST-P-##### / SYN-AE- / SYN-QA-).",
            "Save and verify the patient appears in the list.",
            "Never enter real Emirates ID / Qatar ID in training DBs.",
        ],
        [
            "افتح المرضى.",
            "أدخل البيانات؛ استخدم معرفات اصطناعية فقط خارج الإنتاج.",
            "احفظ وتحقق من الظهور.",
            "لا تُدخل أرقاماً وطنية حقيقية في قواعد التدريب.",
        ],
        "Reception creates party + gnuhealth.patient via React.",
        "ينشئ الاستقبال الطرف والمريض عبر React.",
    ),
    wf(
        "wf-book-appointment",
        "Workflow: Booking an appointment",
        "سير العمل: حجز موعد",
        ["Receptionist", "CallCentre", "Physician"],
        ["/appointments"],
        ["appointment", "schedule", "booking"],
        [
            "Open Appointments.",
            "Create appointment; select patient and health professional.",
            "Set date/time and state (confirmed).",
            "Save and confirm on day list.",
        ],
        [
            "افتح المواعيد.",
            "أنشئ موعداً؛ اختر المريض والمهني الصحي.",
            "حدد التاريخ/الوقت والحالة.",
            "احفظ وتحقق من قائمة اليوم.",
        ],
        "Maps to gnuhealth.appointment.",
        "يرتبط بـ gnuhealth.appointment.",
    ),
    wf(
        "wf-triage",
        "Workflow: Recording triage",
        "سير العمل: تسجيل الفرز",
        ["TriageNurse", "Nurse", "Physician"],
        ["/nursing", "/evaluations"],
        ["triage", "acuity", "ED", "vitals"],
        [
            "Open Nursing or Evaluations.",
            "Select patient encounter; record acuity and vitals.",
            "Route to doctor/surgeon queue as per facility protocol.",
            "Document synthetic-only patients in non-prod.",
        ],
        [
            "افتح التمريض أو التقييمات.",
            "سجّل درجة الفرز والعلامات الحيوية.",
            "وجّه إلى قائمة الطبيب وفق البروتوكول.",
            "استخدم مرضى اصطناعيين خارج الإنتاج.",
        ],
        "Triage documentation uses nursing/evaluation models; ED protocol is facility-specific.",
        "توثيق الفرز عبر نماذج التمريض/التقييم.",
    ),
    wf(
        "wf-consultation",
        "Workflow: Conducting a consultation",
        "سير العمل: إجراء استشارة",
        ["Physician", "Surgeon", "Nurse"],
        ["/evaluations", "/patients"],
        ["consultation", "evaluation", "SOAP"],
        [
            "Open patient chart or Evaluations.",
            "Create patient evaluation with chief complaint and findings.",
            "Order labs/imaging or prescribe as needed.",
            "Save evaluation; continue to discharge/follow-up.",
        ],
        [
            "افتح ملف المريض أو التقييمات.",
            "أنشئ تقييم مريض بالشكوى والنتائج.",
            "اطلب مختبر/تصوير أو صف دواء حسب الحاجة.",
            "احفظ وأكمل المتابعة.",
        ],
        "Uses gnuhealth.patient.evaluation.",
        "يستخدم gnuhealth.patient.evaluation.",
    ),
    wf(
        "wf-lab-order",
        "Workflow: Ordering laboratory tests",
        "سير العمل: طلب فحوصات مختبر",
        ["Physician", "LabTech", "LabSupervisor"],
        ["/laboratory"],
        ["lab", "order", "LIMS"],
        [
            "Ensure health_lab is activated.",
            "Open Laboratory; create request for patient and test type.",
            "Submit for sample collection.",
            "Lab tech completes processing (next workflow).",
        ],
        [
            "تأكد من تفعيل health_lab.",
            "افتح المختبر وأنشئ طلباً.",
            "أرسل لجمع العينة.",
            "يكمل فني المختبر المعالجة.",
        ],
        "Requires health_lab models.",
        "يتطلب نماذج health_lab.",
    ),
    wf(
        "wf-lab-results",
        "Workflow: Entering and approving laboratory results",
        "سير العمل: إدخال واعتماد نتائج المختبر",
        ["LabTech", "LabSupervisor", "Physician"],
        ["/laboratory"],
        ["lab", "results", "approve", "QC"],
        [
            "Open pending lab requests.",
            "LabTech enters numeric/text results.",
            "LabSupervisor reviews and approves (QC).",
            "Physician views results on patient chart / laboratory list.",
        ],
        [
            "افتح الطلبات المعلقة.",
            "يُدخل الفني النتائج.",
            "يعتمد المشرف بعد ضبط الجودة.",
            "يطّلع الطبيب على النتائج.",
        ],
        "Approval step may use SAO wizards if React is limited.",
        "قد يتم الاعتماد عبر SAO إذا كانت React محدودة.",
    ),
    wf(
        "wf-prescribe",
        "Workflow: Prescribing medicine",
        "سير العمل: وصف دواء",
        ["Physician", "Surgeon", "Pharmacist"],
        ["/pharmacy", "/medications"],
        ["pharmacy", "prescription", "medication"],
        [
            "Open Pharmacy or patient medications.",
            "Create prescription order for patient.",
            "Select products from formulary; avoid real PII notes.",
            "Pharmacist reviews before dispense.",
        ],
        [
            "افتح الصيدلية أو أدوية المريض.",
            "أنشئ وصفة.",
            "اختر من القائمة.",
            "يراجع الصيدلي قبل الصرف.",
        ],
        "Uses gnuhealth.prescription.order.",
        "يستخدم gnuhealth.prescription.order.",
    ),
    wf(
        "wf-dispense",
        "Workflow: Dispensing medicine",
        "سير العمل: صرف دواء",
        ["Pharmacist", "PharmacyAssistant"],
        ["/pharmacy", "/stock"],
        ["dispense", "pharmacy", "stock"],
        [
            "Open pending prescriptions.",
            "Verify patient identity (synthetic codes in non-prod).",
            "Dispense from pharmacy stock location; update lot if required.",
            "Confirm stock move and mark prescription done.",
        ],
        [
            "افتح الوصفات المعلقة.",
            "تحقق من هوية المريض.",
            "اصرف من موقع الصيدلية.",
            "أكد حركة المخزون وأغلق الوصفة.",
        ],
        "Dispense ties prescription to stock moves (health_stock).",
        "يربط الصرف الوصفة بحركات المخزون.",
    ),
    wf(
        "wf-admit",
        "Workflow: Admitting a patient",
        "سير العمل: إدخال مريض للتنويم",
        ["Physician", "Nurse", "Receptionist"],
        ["/beds"],
        ["admit", "bed", "inpatient"],
        [
            "Open Beds; confirm free bed under correct facility.",
            "Create inpatient registration (SAO wizard if React limited).",
            "Assign ward/bed; nurse starts rounding.",
            "Keep AE/QA facilities isolated.",
        ],
        [
            "افتح الأسرّة وتأكد من التوفر.",
            "أنشئ تسجيل تنويم.",
            "عيّن الجناح/السرير.",
            "حافظ على عزل منشآت الإمارات/قطر.",
        ],
        "Uses health_inpatient models.",
        "يستخدم نماذج health_inpatient.",
    ),
    wf(
        "wf-transfer-bed",
        "Workflow: Transferring a bed",
        "سير العمل: نقل سرير",
        ["Nurse", "FacilityAdmin", "DeptManager"],
        ["/beds"],
        ["transfer", "bed", "ward"],
        [
            "Open current inpatient bed assignment.",
            "Select target free bed in destination ward.",
            "Confirm transfer; update nursing location.",
            "Verify history retained on patient chart.",
        ],
        [
            "افتح تعيين السرير الحالي.",
            "اختر سريراً فارغاً في الجناح الهدف.",
            "أكد النقل.",
            "تحقق من سجل المريض.",
        ],
        "Bed transfer may require SAO inpatient wizard.",
        "قد يتطلب النقل معالج SAO.",
    ),
    wf(
        "wf-discharge",
        "Workflow: Discharging a patient",
        "سير العمل: تخريج مريض",
        ["Physician", "Nurse", "Billing", "Cashier"],
        ["/beds", "/financial"],
        ["discharge", "inpatient", "exit"],
        [
            "Physician completes discharge summary / evaluation.",
            "Nurse clears pending tasks and frees bed.",
            "Billing finalizes invoice if applicable.",
            "Confirm bed state Free.",
        ],
        [
            "يكمل الطبيب ملخص التخريج.",
            "يمسح التمريض المهام ويحرر السرير.",
            "يُنهي الفوترة الفاتورة إن لزم.",
            "أكد حالة السرير متاح.",
        ],
        "Coordinate clinical discharge with finance clearance per facility policy.",
        "نسّق التخريج السريري مع المخالصة المالية.",
    ),
    wf(
        "wf-create-invoice",
        "Workflow: Creating an invoice",
        "سير العمل: إنشاء فاتورة",
        ["Billing", "Finance", "Cashier"],
        ["/financial"],
        ["invoice", "billing", "account"],
        [
            "Open Financial.",
            "Create patient invoice from services/products.",
            "Set payer (self-pay or insurance) — confirm schemes with counsel.",
            "Post draft when amounts verified (SAO for complex posting).",
        ],
        [
            "افتح المالية.",
            "أنشئ فاتورة مريض من الخدمات/المنتجات.",
            "حدد جهة الدفع.",
            "رحّل المسودة بعد التحقق.",
        ],
        "Uses account_invoice / health_services patterns; deep posting in SAO.",
        "يستخدم أنماط الفوترة؛ الترحيل العميق في SAO.",
    ),
    wf(
        "wf-receive-payment",
        "Workflow: Receiving patient payment",
        "سير العمل: استلام دفعة مريض",
        ["Cashier", "Billing"],
        ["/financial"],
        ["payment", "cashier", "receipt"],
        [
            "Open open invoice for synthetic patient.",
            "Record payment method and amount.",
            "Issue receipt; close cash line.",
            "Reconcile end-of-day cash session (SAO if needed).",
        ],
        [
            "افتح فاتورة مفتوحة.",
            "سجّل طريقة ومبلغ الدفع.",
            "أصدر إيصالاً.",
            "طابق جلسة النقد اليومية.",
        ],
        "Cashier workflows may rely on SAO account wizards.",
        "قد تعتمد عمليات الصندوق على SAO.",
    ),
    wf(
        "wf-insurance-claim",
        "Workflow: Preparing an insurance claim",
        "سير العمل: إعداد مطالبة تأمين",
        ["InsuranceClaims", "Billing", "Compliance"],
        ["/financial"],
        ["insurance", "claim", "eClaim"],
        [
            "Confirm payer contract data is configured (needs confirmation).",
            "Select invoice/encounter eligible for claim.",
            "Generate claim package (format TBD per UAE/QA scheme).",
            "Do not assume NABIDH/eClaim connectors exist — document gap.",
        ],
        [
            "أكد بيانات عقد الجهة الدافعة.",
            "اختر الفاتورة/الزيارة المؤهلة.",
            "أنشئ حزمة المطالبة.",
            "لا تفترض وجود موصلات eClaim — وثّق الفجوة.",
        ],
        "Claims interfaces are not implemented; legal/format confirmation required.",
        "واجهات المطالبات غير منفذة؛ يلزم تأكيد قانوني.",
    ),
    wf(
        "wf-claim-rejection",
        "Workflow: Processing claim rejection",
        "سير العمل: معالجة رفض مطالبة",
        ["InsuranceClaims", "Billing", "Finance"],
        ["/financial"],
        ["claim", "rejection", "appeal"],
        [
            "Log rejection reason from payer (synthetic sample in UAT).",
            "Correct coding/billing data.",
            "Resubmit or write-off per finance policy.",
            "Keep audit trail for compliance.",
        ],
        [
            "سجّل سبب الرفض.",
            "صحّح بيانات الفوترة/الترميز.",
            "أعد الإرسال أو اشطب وفق السياسة.",
            "احتفظ بمسار التدقيق.",
        ],
        "Manual process until HIE/claims adapter exists.",
        "عملية يدوية حتى يوجد محول مطالبات.",
    ),
    wf(
        "wf-purchase-order",
        "Workflow: Completing a purchase order",
        "سير العمل: إكمال أمر شراء",
        ["Procurement", "Warehouse", "Finance"],
        ["/stock", "/products"],
        ["purchase", "PO", "supplier"],
        [
            "Create/select supplier party (synthetic).",
            "Create purchase order for products.",
            "Obtain approval per facility threshold.",
            "Confirm PO ready for receiving.",
        ],
        [
            "أنشئ/اختر مورّداً اصطناعياً.",
            "أنشئ أمر شراء للمنتجات.",
            "احصل على الموافقة.",
            "أكد جاهزية الاستلام.",
        ],
        "Purchase modules via Tryton purchase/stock; React may open SAO.",
        "أوامر الشراء عبر Tryton؛ قد تُفتح في SAO.",
    ),
    wf(
        "wf-receive-stock",
        "Workflow: Receiving stock",
        "سير العمل: استلام مخزون",
        ["Warehouse", "Procurement", "Pharmacist"],
        ["/stock"],
        ["receiving", "stock", "goods receipt"],
        [
            "Open Stock; select incoming shipment against PO.",
            "Enter quantities and lots.",
            "Validate move into destination location.",
            "Notify pharmacy/lab if destination is specialty store.",
        ],
        [
            "افتح المخزون واختر الشحنة الواردة.",
            "أدخل الكميات والدفعات.",
            "تحقق من الحركة إلى الموقع الهدف.",
            "أبلغ الصيدلية/المختبر إن لزم.",
        ],
        "Uses stock.shipment.in / stock.move patterns.",
        "يستخدم أنماط استلام المخزون.",
    ),
    wf(
        "wf-transfer-inventory",
        "Workflow: Transferring inventory",
        "سير العمل: نقل مخزون",
        ["Warehouse", "Pharmacist", "FacilityAdmin"],
        ["/stock"],
        ["transfer", "inventory", "internal move"],
        [
            "Create internal stock move between locations in same facility/company.",
            "Do not transfer across AE/QA entities without legal approval.",
            "Validate quantities.",
            "Confirm destination on-hand updated.",
        ],
        [
            "أنشئ حركة مخزون داخلية بين مواقع نفس المنشأة/الشركة.",
            "لا تنقل عبر كيانات الإمارات/قطر دون موافقة.",
            "تحقق من الكميات.",
            "أكد تحديث الرصيد.",
        ],
        "Internal moves must respect company isolation.",
        "يجب أن تحترم الحركات الداخلية عزل الشركة.",
    ),
    wf(
        "wf-finance-setup",
        "Workflow: Company financial setup",
        "سير العمل: إعداد المالية للشركة",
        ["Finance", "SystemAdmin", "GroupAdmin", "CountryAdmin"],
        ["/financial", "/companies", "/currency"],
        ["finance", "setup", "CoA", "fiscal", "journal", "tax", "AED", "QAR"],
        [
            "Create/select company for UAE (AED) or Qatar (QAR) on /companies.",
            "Confirm currency list includes AED and/or QAR on /currency.",
            "In SAO: create Chart of Accounts from template for that company.",
            "In SAO: create fiscal year + periods, then journals (sales, purchase, cash/bank).",
            "In SAO: configure taxes only after counsel confirms rates/exemptions — do not invent VAT rules.",
            "Set party receivable/payable accounts; map insurance payers if used.",
            "Smoke-test: create draft invoice from React /financial, then post/pay in SAO.",
        ],
        [
            "أنشئ/اختر شركة للإمارات (AED) أو قطر (QAR) من /companies.",
            "أكد وجود عملتي AED و/أو QAR في /currency.",
            "في SAO: أنشئ دليل الحسابات من قالب لتلك الشركة.",
            "في SAO: أنشئ السنة المالية والفترات ثم الدفاتر (مبيعات، مشتريات، نقد/بنك).",
            "في SAO: اضبط الضرائب فقط بعد تأكيد المستشار القانوني — لا تخترع قواعد ضريبية.",
            "عيّن حسابات القبض/الدفع للأطراف؛ اربط شركات التأمين إن وُجدت.",
            "اختبر: أنشئ مسودة فاتورة من /financial ثم رحّل/ادفع في SAO.",
        ],
        "Financial Setup is SAO-first for CoA, fiscal years, journals, and taxes. React /financial lists invoices and can create a draft stub only. See docs/implementation/financial-setup.md. Tax rates and healthcare exemptions need confirmation — do not assume zero-rated treatment.",
        "إعداد المالية يعتمد على SAO لدليل الحسابات والسنة المالية والدفاتر والضرائب. واجهة React تعرض الفواتير ومسودة فقط. انظر docs/implementation/financial-setup.md. معدلات الضرائب والإعفاءات تحتاج تأكيداً قانونياً.",
    ),
    wf(
        "wf-close-period",
        "Workflow: Closing an accounting period",
        "سير العمل: إغلاق فترة محاسبية",
        ["Finance", "SystemAdmin", "Auditor"],
        ["/financial"],
        ["period", "close", "accounting", "fiscal"],
        [
            "Reconcile open invoices and stock valuation (SAO).",
            "Run period close wizard in SAO account module.",
            "Lock period; document sign-off.",
            "Retain evidence for auditor role pack.",
        ],
        [
            "طابق الفواتير والمخزون.",
            "شغّل معالج إغلاق الفترة في SAO.",
            "اقفل الفترة ووثّق التوقيع.",
            "احتفظ بالأدلة لدور المدقق.",
        ],
        "Period close is SAO-first; React Financial is a stub for deep wizards.",
        "إغلاق الفترة عبر SAO أولاً.",
    ),
    # --- Supporting articles ---
    {
        "id": "admin-users",
        "title_en": "Administer users and groups",
        "title_ar": "إدارة المستخدمين والمجموعات",
        "roles": ["SystemAdmin", "FacilityAdmin", "ITSupport", "GroupAdmin"],
        "countries": ["AE", "QA"],
        "routes": ["/users", "/groups"],
        "keywords": ["users", "groups", "acl", "rbac"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Create users, assign groups, review model access. Deep record-rule editing remains in SAO. See guided workflow wf-create-users-roles.",
        "body_ar": "أنشئ المستخدمين وعيّن المجموعات. انظر سير العمل الإرشادي لإنشاء المستخدمين.",
    },
    {
        "id": "field-help-guide",
        "title_en": "Using field-level help",
        "title_ar": "استخدام مساعدة الحقول",
        "roles": ["*"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["field", "tooltip", "contextual", "hint"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Where forms expose a help icon next to a field, it opens the related Help Centre topic or inline hint. Prefer Help Centre search for full workflows.",
        "body_ar": "عند ظهور أيقونة مساعدة بجانب الحقل تفتح موضوع مركز المساعدة أو تلميحاً مختصراً.",
    },
    {
        "id": "uae-hie-readiness",
        "title_en": "UAE HIE readiness (NABIDH / Malaffi / Riayati)",
        "title_ar": "جاهزية تبادل المعلومات الصحية في الإمارات",
        "roles": ["Compliance", "SystemAdmin", "Executive", "Auditor"],
        "countries": ["AE"],
        "routes": ["/help", "/settings"],
        "keywords": ["NABIDH", "Malaffi", "Riayati", "HL7", "FHIR"],
        "version": "1.1.0",
        "published": True,
        "body_en": "HIE connectors are not implemented in IST yet. Confirm facility obligations with DHA/DoH/MOHAP before go-live. See docs/integration/interoperability-assessment.md.",
        "body_ar": "موصلات تبادل المعلومات غير منفذة بعد. أكد الالتزامات مع الجهات المختصة قبل الإطلاق.",
    },
    {
        "id": "qatar-privacy",
        "title_en": "Qatar privacy checklist (PDPPL)",
        "title_ar": "قائمة خصوصية قطر (PDPPL)",
        "roles": ["Compliance", "FacilityAdmin", "Executive", "Auditor"],
        "countries": ["QA"],
        "routes": ["/help"],
        "keywords": ["PDPPL", "privacy", "consent", "Qatar"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Health data is special-nature under Law 13/2016 summaries — obtain legal confirmation for permits, DPIA, and retention before processing real PHI.",
        "body_ar": "بيانات الصحة ذات طبيعة خاصة — احصل على تأكيد قانوني قبل معالجة بيانات حقيقية.",
    },
    {
        "id": "synthetic-policy",
        "title_en": "Synthetic data policy",
        "title_ar": "سياسة البيانات الاصطناعية",
        "roles": ["*", "Compliance", "ITSupport", "Auditor"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["synthetic", "PII", "demo", "IST-P"],
        "version": "1.1.0",
        "published": True,
        "body_en": "Non-production must use synthetic markers only. Production imports require CAB and --allow-production.",
        "body_ar": "يجب استخدام علامات اصطناعية فقط خارج الإنتاج. الاستيراد للإنتاج يتطلب موافقة و--allow-production.",
    },
    {
        "id": "draft-unpublished-example",
        "title_en": "Draft topic (unpublished example)",
        "title_ar": "موضوع مسودة (مثال غير منشور)",
        "roles": ["SystemAdmin"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["draft", "unpublished", "admin"],
        "version": "1.1.0",
        "published": False,
        "body_en": "This topic is unpublished (published=false). It appears only in Help Admin until published. Used to verify publish/unpublish filtering.",
        "body_ar": "هذا الموضوع غير منشور ويظهر فقط في إدارة المساعدة حتى يتم نشره.",
    },
]


def write_article(lang: str, article: dict) -> None:
    base = {
        "id": article["id"],
        "title": article[f"title_{lang}"],
        "roles": article["roles"],
        "countries": article["countries"],
        "routes": article["routes"],
        "keywords": article["keywords"],
        "version": article["version"],
        "guided": article.get("guided", False),
        "published": article.get("published", True),
        "body": article[f"body_{lang}"],
    }
    if article.get("guided"):
        base["steps"] = article.get(f"steps_{lang}", [])
    folders = [EN, PUB_EN] if lang == "en" else [AR, PUB_AR]
    for folder in folders:
        path = folder / f"{article['id']}.json"
        path.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    STRUCTURE_NOTE.write_text(
        """# Help content structure

The master brief suggested folders such as `en/common`, `en/admin`, `en/clinical`.

**Adaptation:** IST Health stores articles as flat JSON under `frontend/help-content/{en|ar}/`
with `roles[]`, `countries[]`, `routes[]`, `guided`, and `published` metadata.
Role/country filtering is applied in `helpService.ts` — functionally equivalent to
role folders without duplicating files.

Source tree is mirrored to `frontend/public/help-content/` for static serving.
Regenerate with: `python scripts/implementation/generate_help_content.py`
""",
        encoding="utf-8",
    )

    index_en = []
    index_ar = []
    for a in ARTICLES:
        write_article("en", a)
        write_article("ar", a)
        entry = {
            "id": a["id"],
            "title": a["title_en"],
            "roles": a["roles"],
            "countries": a["countries"],
            "routes": a["routes"],
            "keywords": a["keywords"],
            "version": a["version"],
            "guided": a.get("guided", False),
            "published": a.get("published", True),
        }
        index_en.append(entry)
        index_ar.append({**entry, "title": a["title_ar"]})

    for folder, data in (
        (EN, index_en),
        (AR, index_ar),
        (PUB_EN, index_en),
        (PUB_AR, index_ar),
    ):
        (folder / "index.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    guided = sum(1 for a in ARTICLES if a.get("guided"))
    print(f"Wrote {len(ARTICLES)} articles ({guided} guided) x2 languages + indexes")


if __name__ == "__main__":
    main()
