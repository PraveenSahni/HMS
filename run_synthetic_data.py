#!/usr/bin/env python3
"""
GNU Health Synthetic Data Engine
================================
Edit config.yaml (company name, counts, server URL) then run:

    python run_synthetic_data.py
    python run_synthetic_data.py --config config.yaml
    python run_synthetic_data.py --force
    python run_synthetic_data.py --dry-run
    python run_synthetic_data.py --only company,patients
    python run_synthetic_data.py --only appointments,laboratory,pharmacy,inpatient,evaluations
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import yaml

from synthetic_data.appointments import AppointmentGenerator
from synthetic_data.client import TrytonClient, TrytonError
from synthetic_data.company import CompanySetup
from synthetic_data.evaluations import EvaluationGenerator
from synthetic_data.generators import DataGenerator
from synthetic_data.inpatient import InpatientGenerator
from synthetic_data.laboratory import LaboratoryGenerator
from synthetic_data.patients import PatientGenerator
from synthetic_data.pharmacy import PharmacyGenerator
from synthetic_data.staff import StaffGenerator

STEPS = (
    "company",
    "staff",
    "patients",
    "appointments",
    "laboratory",
    "pharmacy",
    "inpatient",
    "evaluations",
)

CLINICAL_STEPS = {
    "appointments",
    "laboratory",
    "pharmacy",
    "inpatient",
    "evaluations",
}


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic data for GNU Health from config.yaml",
    )
    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Path to config file (default: config.yaml)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Disable idempotency — may create duplicates",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Connect and validate only — do not create data",
    )
    parser.add_argument(
        "--only",
        default="",
        help=f"Comma-separated steps to run: {','.join(STEPS)}",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Debug logging",
    )
    return parser.parse_args()


def load_existing_context(client: TrytonClient, generator: DataGenerator) -> dict:
    """Load institution (and related) when company step is skipped."""
    context: dict = {}
    if client.model_exists("gnuhealth.institution"):
        ids = client.search("gnuhealth.institution", [], limit=1)
        if ids:
            context["institution_id"] = ids[0]
    if client.model_exists("gnuhealth.specialty"):
        context["specialty_ids"] = client.search("gnuhealth.specialty", [], limit=50)
    if client.model_exists("company.company"):
        ids = client.search("company.company", [], limit=1)
        if ids:
            context["company_id"] = ids[0]
    context["code_prefix"] = generator.code_prefix
    return context


def load_patient_ids(client: TrytonClient, generator: DataGenerator, limit: int) -> list[int]:
    """Prefer gnuhealth.patient ids; fall back to synthetic party codes."""
    if client.model_exists("gnuhealth.patient"):
        # Prefer patients whose party code matches our prefix
        prefix = generator.code_prefix
        if client.model_exists("party.party"):
            party_ids = client.search(
                "party.party",
                [("code", "like", f"{prefix}-P-%")],
                limit=limit,
            )
            if party_ids:
                gh_ids: list[int] = []
                for party_id in party_ids:
                    found = client.search(
                        "gnuhealth.patient", [("party", "=", party_id)], limit=1
                    )
                    if found:
                        gh_ids.append(found[0])
                if gh_ids:
                    return gh_ids
        return client.search("gnuhealth.patient", [], limit=limit)
    return []


def load_staff_ids(client: TrytonClient) -> dict[str, list[int]]:
    if not client.model_exists("gnuhealth.healthprofessional"):
        return {}
    all_hp = client.search("gnuhealth.healthprofessional", [], limit=500)
    return {"doctors": all_hp, "all": all_hp}


def count_safe(client: TrytonClient, model: str, domain: list | None = None) -> int | str:
    try:
        if not client.model_exists(model):
            return "n/a"
        return client.search_count(model, domain or [])
    except TrytonError:
        return "error"


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger("run_synthetic_data")

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        return 1

    config = load_config(config_path)
    company_name = config["company"]["name"]
    idempotent = config.get("options", {}).get("idempotent", True) and not args.force

    steps = set(STEPS)
    if args.only:
        steps = {s.strip() for s in args.only.split(",") if s.strip()}
        unknown = steps - set(STEPS)
        if unknown:
            logger.error("Unknown steps: %s", unknown)
            return 1

    logger.info("=" * 60)
    logger.info("GNU Health Synthetic Data Engine")
    logger.info("Company: %s", company_name)
    logger.info("Location: %s, %s", config["company"]["city"], config["company"]["country"])
    logger.info(
        "Patients: %s | Staff: %s | Appointments: %s months",
        config["data"]["patients"],
        config["data"]["staff"],
        config["data"]["appointment_months"],
    )
    logger.info("Steps: %s", ", ".join(s for s in STEPS if s in steps))
    logger.info("Idempotent: %s | Dry run: %s", idempotent, args.dry_run)
    logger.info("=" * 60)

    srv = config["server"]
    client = TrytonClient(
        url=srv["url"],
        database=srv["database"],
        username=srv["username"],
        password=srv["password"],
        language=srv.get("language", "en"),
    )

    try:
        client.connect()
    except TrytonError as exc:
        logger.error("Connection failed: %s", exc)
        logger.error("Check server.url, credentials, and that GNU Health is running.")
        return 1

    if args.dry_run:
        logger.info("Dry run OK — connected to %s / %s", srv["url"], srv["database"])
        for model in (
            "party.party",
            "gnuhealth.patient",
            "gnuhealth.institution",
            "gnuhealth.appointment",
            "gnuhealth.healthprofessional",
            "gnuhealth.patient.lab.test",
            "gnuhealth.lab",
            "gnuhealth.prescription.order",
            "gnuhealth.patient.evaluation",
            "gnuhealth.hospital.bed",
            "gnuhealth.inpatient.registration",
        ):
            exists = client.model_exists(model)
            logger.info("  Model %-40s %s", model, "available" if exists else "not found")
        return 0

    generator = DataGenerator(config, seed=config["data"].get("seed", 42))
    started = time.time()
    context: dict = {}
    staff_ids: dict = {}
    patient_ids: list = []

    needs_clinical_context = bool(steps & CLINICAL_STEPS)

    if "company" in steps:
        context = CompanySetup(client, config, generator, idempotent).run()
    elif needs_clinical_context:
        context = load_existing_context(client, generator)

    if "staff" in steps:
        staff_ids = StaffGenerator(client, config, generator, context, idempotent).run()
    elif needs_clinical_context:
        staff_ids = load_staff_ids(client)

    if "patients" in steps:
        patient_ids = PatientGenerator(client, config, generator, context, idempotent).run()
    elif needs_clinical_context:
        patient_ids = load_patient_ids(
            client, generator, limit=config["data"].get("patients", 4000)
        )
        logger.info("Loaded %s existing patients for clinical seeding", len(patient_ids))

    if "appointments" in steps:
        AppointmentGenerator(
            client, config, generator, context, patient_ids, staff_ids, idempotent
        ).run()

    if "laboratory" in steps:
        LaboratoryGenerator(
            client, config, generator, context, patient_ids, staff_ids, idempotent
        ).run()

    if "pharmacy" in steps:
        PharmacyGenerator(
            client, config, generator, context, patient_ids, staff_ids, idempotent
        ).run()

    if "inpatient" in steps:
        try:
            InpatientGenerator(
                client, config, generator, context, patient_ids, staff_ids, idempotent
            ).run()
        except Exception as exc:
            logger.warning("Inpatient generation failed (continuing): %s", exc)

    if "evaluations" in steps:
        try:
            EvaluationGenerator(
                client, config, generator, context, patient_ids, staff_ids, idempotent
            ).run()
        except Exception as exc:
            logger.warning("Evaluation generation failed (continuing): %s", exc)

    elapsed = time.time() - started
    prefix = generator.code_prefix
    marker = f"{prefix} synthetic:"

    logger.info("=" * 60)
    logger.info("COMPLETE in %.1f minutes", elapsed / 60)
    logger.info("Summary for %s:", company_name)
    for label, model, domain in [
        ("Patients", "gnuhealth.patient", []),
        ("Staff", "gnuhealth.healthprofessional", []),
        ("Appointments", "gnuhealth.appointment", [("comments", "like", f"{marker}%")]),
        ("Lab orders", "gnuhealth.patient.lab.test", [("comment", "like", f"{marker}%")]),
        ("Lab results", "gnuhealth.lab", [("results", "like", f"{marker}%")]),
        ("Prescriptions", "gnuhealth.prescription.order", [("notes", "like", f"{marker}%")]),
        ("Evaluations", "gnuhealth.patient.evaluation", [("chief_complaint", "like", f"{marker}%")]),
        ("Beds", "gnuhealth.hospital.bed", []),
        ("Admissions", "gnuhealth.inpatient.registration", [("info", "like", f"{marker}%")]),
    ]:
        count = count_safe(client, model, domain)
        logger.info("  %-15s %s", label + ":", count)
    logger.info("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
