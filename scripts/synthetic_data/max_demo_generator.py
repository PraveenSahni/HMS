#!/usr/bin/env python3
"""Deterministic max-demo synthetic dataset builder (UAE + Qatar).

Produces a connected local JSON dataset mapped to known GNU Health model names.
Does not invent Tryton fields beyond codes/markers used by existing generators.
Never emits real Emirates ID / Qatar ID / passport / phones / emails.
"""

from __future__ import annotations

import json
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SYN_EMAIL_DOMAIN = "synthetic.isthealth.example"
SYN_PHONE_AE = "+971 50 000 {seq:04d}"
SYN_PHONE_QA = "+974 5000 {seq:04d}"

GIVEN_M = [
    "Mohammed", "Ahmed", "Abdullah", "Khalid", "Hamad", "Omar", "Ali", "Hassan",
]
GIVEN_F = [
    "Fatima", "Aisha", "Mariam", "Noor", "Sara", "Layla", "Reem", "Noura",
]
SURNAMES = [
    "Al-Thani", "Al-Attiyah", "Al-Kuwari", "Al-Marri", "Al-Mansouri",
    "Al-Naimi", "Al-Suwaidi", "Al-Hajri", "Al-Malki", "Al-Dosari",
]


def _seed_rng(seed: int) -> random.Random:
    rng = random.Random(seed)
    return rng


def _name(rng: random.Random, gender: str) -> dict[str, str]:
    given = rng.choice(GIVEN_M if gender == "m" else GIVEN_F)
    family = rng.choice(SURNAMES)
    return {
        "given": given,
        "family": family,
        "full": f"{given} {family}",
        "gender": gender,
    }


def _dob(rng: random.Random, child: bool) -> str:
    today = date(2026, 7, 14)
    if child:
        days = rng.randint(30, 365 * 14)
    else:
        days = rng.randint(365 * 18, 365 * 75)
    return (today - timedelta(days=days)).isoformat()


def build_max_demo_dataset(cfg: dict[str, Any]) -> dict[str, Any]:
    """Build full connected synthetic dataset from max-demo config."""
    seed = int(cfg.get("seed", 20260714))
    rng = _seed_rng(seed)
    batch_id = str(cfg.get("synthetic_batch_id", "ISTHIS-MAXDEMO-20260714"))
    code = (cfg.get("company") or {}).get("code", "IST")
    data = cfg.get("data") or {}
    opts = cfg.get("options") or {}
    n_patients = int(data.get("patients", 4000))
    n_staff = int(data.get("staff", 300))
    staff_mix = dict(data.get("staff_mix") or {})
    facilities = list(cfg.get("facilities") or [])
    entities = list(cfg.get("entities") or [])
    departments = list(data.get("departments") or [])
    specialties = list(data.get("specialties") or [])
    lab_tests = list(data.get("lab_tests") or ["CBC"])
    meds = list(data.get("medications") or ["Paracetamol 500mg"])
    imaging_tests = list(data.get("imaging_tests") or ["Chest X-Ray"])
    surgeries = list(data.get("surgery_procedures") or ["Appendectomy"])
    packs_cfg = dict(cfg.get("packs") or {})

    marker = {
        "synthetic_data": True,
        "synthetic_batch_id": batch_id,
        "synthetic_seed": seed,
    }

    # --- Org tree ---
    group = cfg.get("group") or {"name": "IST Healthcare Group", "code": "IST-HC-GRP"}
    companies = []
    for ent in entities:
        companies.append({
            "model": "company.company" if ent.get("type") != "Group" else "party.party",
            "code": ent["code"],
            "name": ent["name"],
            "country": ent.get("country"),
            "parent": ent.get("parent"),
            "type": ent.get("type", "LegalEntity"),
            **marker,
        })

    institutions = []
    for fac in facilities:
        institutions.append({
            "model": "gnuhealth.institution",
            "code": fac["code"],
            "name": fac["name"],
            "country": fac.get("country"),
            "entity": fac.get("entity"),
            "facility_type": fac.get("type", "hospital"),
            **marker,
        })

    # --- Users / staff ---
    role_order = ["doctors", "nurses", "admin", "reception", "lab", "pharmacy"]
    role_map = {
        "doctors": "DOC",
        "nurses": "NUR",
        "admin": "ADM",
        "reception": "REC",
        "lab": "LAB",
        "pharmacy": "PHR",
    }
    staff: list[dict[str, Any]] = []
    users: list[dict[str, Any]] = []
    seq = 0
    for role in role_order:
        count = int(staff_mix.get(role, 0))
        for _ in range(count):
            if len(staff) >= n_staff:
                break
            seq += 1
            gender = "m" if rng.random() < 0.55 else "f"
            nm = _name(rng, gender)
            country = "AE" if seq % 2 == 0 else "QA"
            st_code = f"{code}-ST-{role_map[role]}-{seq:04d}"
            fac = facilities[(seq - 1) % len(facilities)] if facilities else None
            staff.append({
                "model": "gnuhealth.healthprofessional",
                "code": st_code,
                "name": nm["full"],
                "role": role,
                "specialty": rng.choice(specialties) if specialties else None,
                "facility_code": fac["code"] if fac else None,
                "country": country,
                "phone": (SYN_PHONE_AE if country == "AE" else SYN_PHONE_QA).format(seq=seq),
                "email": f"{st_code.lower()}@{SYN_EMAIL_DOMAIN}",
                **marker,
            })
            users.append({
                "model": "res.user",
                "login": st_code.lower(),
                "name": nm["full"],
                "email": f"{st_code.lower()}@{SYN_EMAIL_DOMAIN}",
                "healthprofessional_code": st_code,
                "active": True,
                **marker,
            })
        if len(staff) >= n_staff:
            break
    # Top up if mix undershoots
    while len(staff) < n_staff:
        seq += 1
        gender = "m" if rng.random() < 0.5 else "f"
        nm = _name(rng, gender)
        st_code = f"{code}-ST-GEN-{seq:04d}"
        fac = facilities[(seq - 1) % len(facilities)] if facilities else None
        staff.append({
            "model": "gnuhealth.healthprofessional",
            "code": st_code,
            "name": nm["full"],
            "role": "admin",
            "facility_code": fac["code"] if fac else None,
            "country": "QA",
            "phone": SYN_PHONE_QA.format(seq=seq),
            "email": f"{st_code.lower()}@{SYN_EMAIL_DOMAIN}",
            **marker,
        })

    doctors = [s for s in staff if s["role"] == "doctors"]
    nurses = [s for s in staff if s["role"] == "nurses"]

    # --- Patients ---
    patients: list[dict[str, Any]] = []
    for i in range(1, n_patients + 1):
        gender = "m" if rng.random() < 0.5 else "f"
        nm = _name(rng, gender)
        country = "AE" if i % 2 == 0 else "QA"
        nid_fmt = (cfg.get("id_formats") or {}).get(
            "national_id_ae" if country == "AE" else "national_id_qa",
            f"SYN-{country}-{{seq:08d}}",
        )
        national_id = nid_fmt.format(seq=i)
        fac = facilities[(i - 1) % len(facilities)] if facilities else None
        p_code = f"{code}-P-{i:05d}"
        patients.append({
            "model": "gnuhealth.patient",
            "party_model": "party.party",
            "code": p_code,
            "name": nm["full"],
            "gender": gender,
            "dob": _dob(rng, child=rng.random() < 0.22),
            "country": country,
            "national_id_synthetic": national_id,
            "facility_code": fac["code"] if fac else None,
            "phone": (SYN_PHONE_AE if country == "AE" else SYN_PHONE_QA).format(seq=i),
            "email": f"{p_code.lower()}@{SYN_EMAIL_DOMAIN}",
            **marker,
        })

    # --- Clinical volumes ---
    apt_per = int(opts.get("create_appointments_per_patient", 3))
    lab_ratio = float(opts.get("lab_orders_ratio", 0.4))
    lab_res_ratio = float(opts.get("lab_results_ratio", 0.6))
    rx_ratio = float(opts.get("prescription_ratio", 0.5))
    eval_ratio = float(opts.get("evaluation_ratio", 0.6))
    ip_ratio = float(opts.get("inpatient_ratio", 0.25))
    img_ratio = float(opts.get("imaging_ratio", 0.2))
    surg_ratio = float(opts.get("surgery_ratio", 0.05))
    nurse_ratio = float(opts.get("nursing_rounding_ratio", 0.8))
    icu_ratio = float(opts.get("icu_ratio", 0.08))
    ins_ratio = float(opts.get("insurance_ratio", 0.7))
    svc_ratio = float(opts.get("services_ratio", 0.5))
    months = int(data.get("appointment_months", 6))
    beds_per = int(opts.get("inpatient_beds_per_hospital", 24))

    hospitals = [f for f in facilities if f.get("type") == "hospital"]
    if not hospitals:
        hospitals = facilities[:2] or [{"code": "FAC-DEMO", "name": "Demo", "country": "QA"}]

    beds: list[dict[str, Any]] = []
    bed_seq = 0
    for h in hospitals:
        for b in range(1, beds_per + 1):
            bed_seq += 1
            beds.append({
                "model": "gnuhealth.hospital.bed",
                "code": f"{h['code']}-BED-{b:03d}",
                "facility_code": h["code"],
                "name": f"Bed {b}",
                "state": "free",
                **marker,
            })

    appointments: list[dict[str, Any]] = []
    apt_seq = 0
    base_day = date(2026, 1, 14)
    for p in patients:
        for _ in range(apt_per):
            apt_seq += 1
            day_off = rng.randint(0, max(months * 30 - 1, 0))
            doc = rng.choice(doctors) if doctors else None
            appointments.append({
                "model": "gnuhealth.appointment",
                "code": f"{code}-APT-{apt_seq:06d}",
                "patient_code": p["code"],
                "hp_code": doc["code"] if doc else None,
                "facility_code": p.get("facility_code"),
                "appointment_date": (base_day + timedelta(days=day_off)).isoformat(),
                "comments": f"{code} synthetic: {code}-APT-{apt_seq:06d}",
                **marker,
            })

    evaluations: list[dict[str, Any]] = []
    eval_seq = 0
    for p in patients:
        if rng.random() > eval_ratio:
            continue
        eval_seq += 1
        doc = rng.choice(doctors) if doctors else None
        evaluations.append({
            "model": "gnuhealth.patient.evaluation",
            "code": f"{code}-EVAL-{eval_seq:06d}",
            "patient_code": p["code"],
            "hp_code": doc["code"] if doc else None,
            "chief_complaint": f"{code} synthetic: routine evaluation {eval_seq}",
            **marker,
        })

    lab_orders: list[dict[str, Any]] = []
    lab_results: list[dict[str, Any]] = []
    lab_seq = 0
    for p in patients:
        if rng.random() > lab_ratio:
            continue
        lab_seq += 1
        test = rng.choice(lab_tests)
        order = {
            "model": "gnuhealth.patient.lab.test",
            "code": f"{code}-LABORD-{lab_seq:06d}",
            "patient_code": p["code"],
            "test_name": test,
            "comment": f"{code} synthetic: {code}-LABORD-{lab_seq:06d}",
            **marker,
        }
        lab_orders.append(order)
        if rng.random() <= lab_res_ratio:
            lab_results.append({
                "model": "gnuhealth.lab",
                "code": f"{code}-LABRES-{lab_seq:06d}",
                "patient_code": p["code"],
                "test_name": test,
                "results": f"{code} synthetic: {code}-LABRES-{lab_seq:06d} within reference",
                "order_code": order["code"],
                **marker,
            })

    prescriptions: list[dict[str, Any]] = []
    rx_seq = 0
    for p in patients:
        if rng.random() > rx_ratio:
            continue
        rx_seq += 1
        doc = rng.choice(doctors) if doctors else None
        prescriptions.append({
            "model": "gnuhealth.prescription.order",
            "code": f"{code}-RX-{rx_seq:06d}",
            "patient_code": p["code"],
            "hp_code": doc["code"] if doc else None,
            "medication": rng.choice(meds),
            "notes": f"{code} synthetic: {code}-RX-{rx_seq:06d}",
            **marker,
        })

    admissions: list[dict[str, Any]] = []
    adm_seq = 0
    for p in patients:
        if rng.random() > ip_ratio:
            continue
        adm_seq += 1
        bed = beds[(adm_seq - 1) % len(beds)] if beds else None
        h = hospitals[(adm_seq - 1) % len(hospitals)]
        admissions.append({
            "model": "gnuhealth.inpatient.registration",
            "code": f"{code}-ADM-{adm_seq:06d}",
            "patient_code": p["code"],
            "facility_code": h["code"],
            "bed_code": bed["code"] if bed else None,
            "info": f"{code} synthetic: {code}-ADM-{adm_seq:06d}",
            **marker,
        })

    nursing: list[dict[str, Any]] = []
    nurse_seq = 0
    for adm in admissions:
        if rng.random() > nurse_ratio:
            continue
        nurse_seq += 1
        nurse = rng.choice(nurses) if nurses else None
        nursing.append({
            "model": "gnuhealth.patient.rounding",
            "code": f"{code}-NUR-{nurse_seq:06d}",
            "admission_code": adm["code"],
            "patient_code": adm["patient_code"],
            "hp_code": nurse["code"] if nurse else None,
            "notes": f"{code} synthetic: nursing round {nurse_seq}",
            **marker,
        })

    icu: list[dict[str, Any]] = []
    icu_seq = 0
    for adm in admissions:
        if rng.random() > icu_ratio:
            continue
        icu_seq += 1
        icu.append({
            "model": "gnuhealth.icu.glasgow",
            "code": f"{code}-ICU-{icu_seq:05d}",
            "admission_code": adm["code"],
            "patient_code": adm["patient_code"],
            "notes": f"{code} synthetic: ICU score stub {icu_seq}",
            **marker,
        })

    imaging: list[dict[str, Any]] = []
    img_seq = 0
    for p in patients:
        if rng.random() > img_ratio:
            continue
        img_seq += 1
        imaging.append({
            "model": "gnuhealth.imaging.test.request",
            "code": f"{code}-IMG-{img_seq:06d}",
            "patient_code": p["code"],
            "test_name": rng.choice(imaging_tests),
            "comment": f"{code} synthetic: {code}-IMG-{img_seq:06d}",
            **marker,
        })

    surgery_recs: list[dict[str, Any]] = []
    surg_seq = 0
    for p in patients:
        if rng.random() > surg_ratio:
            continue
        surg_seq += 1
        doc = rng.choice(doctors) if doctors else None
        surgery_recs.append({
            "model": "gnuhealth.surgery",
            "code": f"{code}-SURG-{surg_seq:05d}",
            "patient_code": p["code"],
            "hp_code": doc["code"] if doc else None,
            "procedure": rng.choice(surgeries),
            "notes": f"{code} synthetic: {code}-SURG-{surg_seq:05d}",
            **marker,
        })

    # Insurance plans + patient coverage
    insurers = [
        {"code": f"{code}-INS-AE-01", "name": "SYN UAE Demo Payer", "country": "AE"},
        {"code": f"{code}-INS-QA-01", "name": "SYN Qatar Demo Payer", "country": "QA"},
    ]
    plans = []
    for ins in insurers:
        plans.append({
            "model": "gnuhealth.insurance.plan",
            "code": f"{ins['code']}-PLAN",
            "name": f"{ins['name']} Standard",
            "insurer_code": ins["code"],
            "country": ins["country"],
            **marker,
        })
    insurance_parties = [
        {
            "model": "party.party",
            "code": i["code"],
            "name": i["name"],
            "is_insurance_company": True,
            "country": i["country"],
            **marker,
        }
        for i in insurers
    ]
    patient_insurance: list[dict[str, Any]] = []
    ins_seq = 0
    for p in patients:
        if rng.random() > ins_ratio:
            continue
        ins_seq += 1
        plan = plans[0] if p["country"] == "AE" else plans[1]
        patient_insurance.append({
            "model": "gnuhealth.insurance",
            "code": f"{code}-PIN-{ins_seq:06d}",
            "patient_code": p["code"],
            "plan_code": plan["code"],
            "number": f"SYN-POL-{ins_seq:08d}",
            **marker,
        })

    # Stock locations per store/pharmacy/lab
    stock_locations: list[dict[str, Any]] = []
    stock_moves: list[dict[str, Any]] = []
    for fac in facilities:
        if fac.get("type") not in {"store", "pharmacy", "laboratory", "hospital"}:
            continue
        loc_code = f"{fac['code']}-LOC"
        stock_locations.append({
            "model": "stock.location",
            "code": loc_code,
            "name": f"{fac['name']} Stock",
            "facility_code": fac["code"],
            **marker,
        })
        for mi, med in enumerate(meds, start=1):
            stock_moves.append({
                "model": "stock.move",
                "code": f"{loc_code}-MV-{mi:03d}",
                "location_code": loc_code,
                "product_name": med,
                "quantity": 50 + (mi * 10),
                "notes": f"{code} synthetic stock",
                **marker,
            })

    # Services + accounting markers (invoice drafts linked to patients)
    services: list[dict[str, Any]] = []
    invoices: list[dict[str, Any]] = []
    svc_seq = 0
    for p in patients:
        if rng.random() > svc_ratio:
            continue
        svc_seq += 1
        svc_code = f"{code}-SVC-{svc_seq:06d}"
        services.append({
            "model": "gnuhealth.health_service",
            "code": svc_code,
            "patient_code": p["code"],
            "description": f"{code} synthetic: outpatient service",
            **marker,
        })
        invoices.append({
            "model": "account.invoice",
            "code": f"{code}-INV-{svc_seq:06d}",
            "party_code": p["code"],
            "service_code": svc_code,
            "state": "draft",
            "notes": f"{code} synthetic invoice draft",
            **marker,
        })

    reporting_markers = [
        {
            "model": "gnuhealth.top_diseases",
            "code": f"{code}-RPT-TOPDIS",
            "notes": f"{code} synthetic: reporting pack marker — use live evaluations for disease mix",
            **marker,
        }
    ]
    federation_markers = [
        {
            "model": "gnuhealth.federation",
            "code": f"{code}-FED-MARKER",
            "notes": f"{code} synthetic: federation pack stub — no live federation writes",
            **marker,
        }
    ]

    dept_recs = [
        {
            "model": "gnuhealth.institution.unit",
            "code": f"{code}-DEPT-{i:02d}",
            "name": d.get("name"),
            "name_ar": d.get("name_ar"),
            **marker,
        }
        for i, d in enumerate(departments, start=1)
    ]

    counts = {
        "entities": len(companies),
        "facilities_institutions": len(institutions),
        "departments": len(dept_recs),
        "users": len(users),
        "health_professionals": len(staff),
        "patients": len(patients),
        "appointments": len(appointments),
        "evaluations": len(evaluations),
        "lab_orders": len(lab_orders),
        "lab_results": len(lab_results),
        "prescriptions": len(prescriptions),
        "beds": len(beds),
        "admissions": len(admissions),
        "nursing_roundings": len(nursing),
        "icu_scores": len(icu),
        "imaging_requests": len(imaging),
        "surgeries": len(surgery_recs),
        "insurance_companies": len(insurance_parties),
        "insurance_plans": len(plans),
        "patient_insurance": len(patient_insurance),
        "stock_locations": len(stock_locations),
        "stock_moves": len(stock_moves),
        "health_services": len(services),
        "invoices_draft": len(invoices),
        "reporting_markers": len(reporting_markers),
        "federation_markers": len(federation_markers),
    }

    pack_status = {}
    for pack_name, meta in packs_cfg.items():
        mode = (meta or {}).get("mode", "stub_marker")
        pack_status[pack_name] = {
            "mode": mode,
            "live_engine": mode == "engine_live",
            "local_records": mode in {"local_connected", "engine_live", "stub_marker"},
        }

    return {
        "meta": {
            "synthetic_data": True,
            "synthetic_batch_id": batch_id,
            "seed": seed,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "group": group,
            "company": cfg.get("company"),
            "ceiling_note": (
                "4000 patients / 300 staff — proven run_synthetic_data.py scale; "
                "test validate refuses >5000; 50k deferred to sized VM"
            ),
            "packs": pack_status,
            "id_policy": cfg.get("id_formats"),
        },
        "counts": counts,
        "records": {
            "companies_entities": companies,
            "institutions": institutions,
            "departments": dept_recs,
            "users": users,
            "health_professionals": staff,
            "patients": patients,
            "appointments": appointments,
            "evaluations": evaluations,
            "lab_orders": lab_orders,
            "lab_results": lab_results,
            "prescriptions": prescriptions,
            "beds": beds,
            "admissions": admissions,
            "nursing_roundings": nursing,
            "icu_scores": icu,
            "imaging_requests": imaging,
            "surgeries": surgery_recs,
            "insurance_companies": insurance_parties,
            "insurance_plans": plans,
            "patient_insurance": patient_insurance,
            "stock_locations": stock_locations,
            "stock_moves": stock_moves,
            "health_services": services,
            "invoices_draft": invoices,
            "reporting_markers": reporting_markers,
            "federation_markers": federation_markers,
        },
    }


def write_dataset(
    dataset: dict[str, Any],
    out_dir: Path,
    *,
    write_full: bool = True,
) -> dict[str, Path]:
    """Write summary (always) and optional full dataset (gitignored path)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    summary = {
        "meta": dataset["meta"],
        "counts": dataset["counts"],
        "samples": {
            k: (v[:3] if isinstance(v, list) else v)
            for k, v in dataset["records"].items()
        },
    }
    summary_path = out_dir / "max-demo-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    paths["summary"] = summary_path

    report_path = out_dir / "generate-max-demo-report.json"
    report_path.write_text(
        json.dumps(
            {
                "command": "generate_synthetic",
                "profile": "uae_qatar_max_demo",
                "counts": dataset["counts"],
                "seed": dataset["meta"]["seed"],
                "synthetic_batch_id": dataset["meta"]["synthetic_batch_id"],
                "packs": dataset["meta"]["packs"],
                "timestamp": dataset["meta"]["generated_at"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["report"] = report_path

    if write_full:
        full_dir = out_dir / "generated"
        full_dir.mkdir(parents=True, exist_ok=True)
        full_path = full_dir / "uae_qatar_max_demo_full.json"
        full_path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
        paths["full"] = full_path

    return paths
