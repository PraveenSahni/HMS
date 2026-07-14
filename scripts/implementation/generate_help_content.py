#!/usr/bin/env python3
"""Generate EN/AR help-content JSON articles with metadata."""

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

ARTICLES = [
    {
        "id": "help-overview",
        "title_en": "Help Centre overview",
        "title_ar": "نظرة عامة على مركز المساعدة",
        "roles": ["*"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["help", "start", "overview"],
        "version": "1.0.0",
        "body_en": "Use search, filters by role and country, and guided workflows. Content is loaded from help-content files — not hardcoded in UI components.",
        "body_ar": "استخدم البحث والتصفية حسب الدور والدولة وسير العمل الإرشادي. يتم تحميل المحتوى من ملفات help-content وليس مضمّناً في مكونات الواجهة.",
    },
    {
        "id": "wf-register-patient",
        "title_en": "Workflow: Register a patient",
        "title_ar": "سير العمل: تسجيل مريض",
        "roles": ["Receptionist", "Physician", "FacilityAdmin"],
        "countries": ["AE", "QA"],
        "routes": ["/patients"],
        "keywords": ["patient", "register", "create", "demographics"],
        "version": "1.0.0",
        "guided": True,
        "steps_en": [
            "Open Patients (/patients).",
            "Choose Create and enter demographics.",
            "Use synthetic IDs only in non-prod (IST-P-##### / SYN-QA- / SYN-AE-).",
            "Save and verify the patient appears in the list.",
        ],
        "steps_ar": [
            "افتح المرضى (/patients).",
            "اختر إنشاء وأدخل البيانات الديموغرافية.",
            "استخدم معرفات اصطناعية فقط خارج الإنتاج.",
            "احفظ وتحقق من ظهور المريض في القائمة.",
        ],
        "body_en": "Reception creates the party + patient record via the React form backed by gnuhealth.patient.",
        "body_ar": "يقوم الاستقبال بإنشاء سجل الطرف والمريض عبر نموذج React المرتبط بـ gnuhealth.patient.",
    },
    {
        "id": "wf-book-appointment",
        "title_en": "Workflow: Book an appointment",
        "title_ar": "سير العمل: حجز موعد",
        "roles": ["Receptionist", "Physician"],
        "countries": ["AE", "QA"],
        "routes": ["/appointments"],
        "keywords": ["appointment", "schedule", "booking"],
        "version": "1.0.0",
        "guided": True,
        "steps_en": [
            "Open Appointments.",
            "Create appointment; select patient and health professional.",
            "Set date/time and state (confirmed).",
            "Save and confirm on day list.",
        ],
        "steps_ar": [
            "افتح المواعيد.",
            "أنشئ موعداً؛ اختر المريض والمهني الصحي.",
            "حدد التاريخ/الوقت والحالة.",
            "احفظ وتحقق من قائمة اليوم.",
        ],
        "body_en": "Appointments map to gnuhealth.appointment.",
        "body_ar": "ترتبط المواعيد بنموذج gnuhealth.appointment.",
    },
    {
        "id": "wf-lab-order",
        "title_en": "Workflow: Place a lab order",
        "title_ar": "سير العمل: طلب مختبر",
        "roles": ["Physician", "LabTech"],
        "countries": ["AE", "QA"],
        "routes": ["/laboratory"],
        "keywords": ["lab", "order", "LIMS"],
        "version": "1.0.0",
        "guided": True,
        "steps_en": [
            "Ensure health_lab is activated (Modules page / SAO).",
            "Open Laboratory.",
            "Create request for patient and test type.",
            "Lab tech completes result entry (SAO if needed).",
        ],
        "steps_ar": [
            "تأكد من تفعيل health_lab.",
            "افتح المختبر.",
            "أنشئ طلباً للمريض ونوع الفحص.",
            "يكمل فني المختبر النتيجة (SAO عند الحاجة).",
        ],
        "body_en": "Requires health_lab models; UI shows module-missing if absent.",
        "body_ar": "يتطلب نماذج health_lab.",
    },
    {
        "id": "wf-prescribe",
        "title_en": "Workflow: Prescribe medication",
        "title_ar": "سير العمل: وصف دواء",
        "roles": ["Physician", "Pharmacist"],
        "countries": ["AE", "QA"],
        "routes": ["/pharmacy", "/medications"],
        "keywords": ["pharmacy", "prescription", "medication"],
        "version": "1.0.0",
        "guided": True,
        "steps_en": [
            "Open Pharmacy or patient chart.",
            "Create prescription order for patient.",
            "Pharmacist reviews and dispenses via stock processes as configured.",
        ],
        "steps_ar": [
            "افتح الصيدلية أو ملف المريض.",
            "أنشئ وصفة للمريض.",
            "يراجع الصيدلي ويصرف وفق إعدادات المخزون.",
        ],
        "body_en": "Uses gnuhealth.prescription.order.",
        "body_ar": "يستخدم gnuhealth.prescription.order.",
    },
    {
        "id": "wf-admit",
        "title_en": "Workflow: Inpatient admission",
        "title_ar": "سير العمل: إدخال للتنويم",
        "roles": ["Physician", "Nurse", "Receptionist"],
        "countries": ["AE", "QA"],
        "routes": ["/beds"],
        "keywords": ["admit", "bed", "inpatient"],
        "version": "1.0.0",
        "guided": True,
        "steps_en": [
            "Open Beds.",
            "Confirm free bed.",
            "Create inpatient registration (SAO wizard if React limited).",
            "Nurse documents rounding under Nursing.",
        ],
        "steps_ar": [
            "افتح الأسرّة.",
            "أكد توفر سرير.",
            "أنشئ تسجيل تنويم.",
            "يوثق التمريض الجولات تحت التمريض.",
        ],
        "body_en": "health_inpatient models.",
        "body_ar": "نماذج health_inpatient.",
    },
    {
        "id": "admin-users",
        "title_en": "Administer users and groups",
        "title_ar": "إدارة المستخدمين والمجموعات",
        "roles": ["SystemAdmin", "FacilityAdmin", "ITSupport"],
        "countries": ["AE", "QA"],
        "routes": ["/users", "/groups"],
        "keywords": ["users", "groups", "acl", "rbac"],
        "version": "1.0.0",
        "body_en": "Create users, assign groups, review model access summaries. Deep record-rule editing remains in SAO.",
        "body_ar": "أنشئ المستخدمين وعيّن المجموعات. تحرير قواعد السجلات المتقدم يبقى في SAO.",
    },
    {
        "id": "uae-hie-readiness",
        "title_en": "UAE HIE readiness (NABIDH / Malaffi / Riayati)",
        "title_ar": "جاهزية تبادل المعلومات الصحية في الإمارات",
        "roles": ["Compliance", "SystemAdmin", "Executive"],
        "countries": ["AE"],
        "routes": ["/help", "/settings"],
        "keywords": ["NABIDH", "Malaffi", "Riayati", "HL7", "FHIR"],
        "version": "1.0.0",
        "body_en": "HIE connectors are not implemented in IST yet. Confirm facility obligations with DHA/DoH/MOHAP before go-live. See docs/integration/interoperability-assessment.md.",
        "body_ar": "موصلات تبادل المعلومات غير منفذة بعد. أكد الالتزامات مع الجهات المختصة قبل الإطلاق.",
    },
    {
        "id": "qatar-privacy",
        "title_en": "Qatar privacy checklist (PDPPL)",
        "title_ar": "قائمة خصوصية قطر (PDPPL)",
        "roles": ["Compliance", "FacilityAdmin", "Executive"],
        "countries": ["QA"],
        "routes": ["/help"],
        "keywords": ["PDPPL", "privacy", "consent", "Qatar"],
        "version": "1.0.0",
        "body_en": "Health data is special-nature under Law 13/2016 summaries — obtain legal confirmation for permits, DPIA, and retention before processing real PHI.",
        "body_ar": "بيانات الصحة ذات طبيعة خاصة — احصل على تأكيد قانوني قبل معالجة بيانات حقيقية.",
    },
    {
        "id": "synthetic-policy",
        "title_en": "Synthetic data policy",
        "title_ar": "سياسة البيانات الاصطناعية",
        "roles": ["*", "Compliance", "ITSupport"],
        "countries": ["AE", "QA"],
        "routes": ["/help"],
        "keywords": ["synthetic", "PII", "demo", "IST-P"],
        "version": "1.0.0",
        "body_en": "Non-production must use synthetic markers only. Production imports require CAB and --allow-production.",
        "body_ar": "يجب استخدام علامات اصطناعية فقط خارج الإنتاج. الاستيراد للإنتاج يتطلب موافقة و--allow-production.",
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
        "body": article[f"body_{lang}"],
    }
    if article.get("guided"):
        base["steps"] = article.get(f"steps_{lang}", [])
    folders = [EN, PUB_EN] if lang == "en" else [AR, PUB_AR]
    for folder in folders:
        path = folder / f"{article['id']}.json"
        path.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    index_en = []
    index_ar = []
    for a in ARTICLES:
        write_article("en", a)
        write_article("ar", a)
        index_en.append(
            {
                "id": a["id"],
                "title": a["title_en"],
                "roles": a["roles"],
                "countries": a["countries"],
                "routes": a["routes"],
                "keywords": a["keywords"],
                "version": a["version"],
                "guided": a.get("guided", False),
            }
        )
        index_ar.append(
            {
                "id": a["id"],
                "title": a["title_ar"],
                "roles": a["roles"],
                "countries": a["countries"],
                "routes": a["routes"],
                "keywords": a["keywords"],
                "version": a["version"],
                "guided": a.get("guided", False),
            }
        )
    (EN / "index.json").write_text(json.dumps(index_en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (AR / "index.json").write_text(json.dumps(index_ar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PUB_EN / "index.json").write_text(json.dumps(index_en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PUB_AR / "index.json").write_text(json.dumps(index_ar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(ARTICLES)} articles x2 languages + indexes (src + public)")


if __name__ == "__main__":
    main()
