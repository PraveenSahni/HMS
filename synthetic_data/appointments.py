"""Appointment generation (outpatient)."""

from __future__ import annotations

import logging
import random
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class AppointmentGenerator:
    """Create outpatient appointments over configured history period."""

    def __init__(
        self,
        client: TrytonClient,
        config: dict[str, Any],
        generator: DataGenerator,
        context: dict[str, Any],
        patient_ids: list[int],
        staff_ids: dict[str, list[int]],
        idempotent: bool = True,
    ) -> None:
        self.client = client
        self.config = config
        self.generator = generator
        self.context = context
        self.patient_ids = patient_ids
        self.staff_ids = staff_ids
        self.idempotent = idempotent
        self.batch_size = config["data"].get("batch_size", 100)
        self.months = config["data"].get("appointment_months", 6)
        self.appts_per_patient = config["options"].get("create_appointments_per_patient", 3)

    def run(self) -> list[int]:
        if not self.config["data"]["modules"].get("outpatient", True):
            logger.info("Outpatient module disabled — skipping appointments")
            return []

        if not self.client.model_exists("gnuhealth.appointment"):
            logger.warning("Model gnuhealth.appointment not available — skipping")
            return []

        doctor_ids = self.staff_ids.get("doctors", [])
        if not doctor_ids:
            logger.warning("No doctors in staff_ids — loading health professionals")
            doctor_ids = self._all_staff_prof_ids()

        institution_id = self.context.get("institution_id")
        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        target = max(1, len(self.patient_ids) * self.appts_per_patient)

        existing_ids = self.client.search(
            "gnuhealth.appointment",
            [("comments", "like", f"{marker}%")],
            limit=100000,
        )
        existing = len(existing_ids)

        # Idempotent top-up: only skip when we already have enough synthetic appts.
        # (Previous bug: any existing > 0 skipped the entire step.)
        if self.idempotent and existing >= target:
            logger.info(
                "Found %s synthetic appointments (target %s) — skipping",
                existing,
                target,
            )
            return existing_ids

        to_create = target - existing if self.idempotent else target
        logger.info(
            "Creating %s appointments (%s months history; existing synthetic=%s, target=%s)...",
            to_create,
            self.months,
            existing,
            target,
        )

        # Prefer gnuhealth.patient ids; fall back to resolving party ids.
        gh_patients = self._resolve_gh_patients(self.patient_ids)
        if not gh_patients:
            logger.warning("No patients available for appointments")
            return existing_ids

        appointment_ids: list[int] = list(existing_ids) if self.idempotent else []
        batch: list[dict] = []
        apt_counter = existing

        for i in range(to_create):
            apt_counter += 1
            gh_patient_id = gh_patients[i % len(gh_patients)]
            appt_dt = self.generator.appointment_datetime(self.months)
            state = self.generator.appointment_state(appt_dt)
            code = f"{prefix}-APT-{apt_counter:06d}"

            vals: dict[str, Any] = {
                "patient": gh_patient_id,
                "healthprof": random.choice(doctor_ids),
                "appointment_date": appt_dt.isoformat(),
                "state": state,
                "appointment_type": "outpatient",
                "visit_type": random.choice(["new", "followup", "followup", "new"]),
                "urgency": random.choice(["a", "a", "a", "b", "c"]),
                "comments": f"{marker} {code}",
            }
            if institution_id:
                vals["institution"] = institution_id

            batch.append(vals)
            if len(batch) >= self.batch_size:
                ids = self.client.batch_create(
                    "gnuhealth.appointment", batch, self.batch_size, "appointments"
                )
                appointment_ids.extend(ids)
                batch = []

        if batch:
            ids = self.client.batch_create(
                "gnuhealth.appointment", batch, self.batch_size, "appointments"
            )
            appointment_ids.extend(ids)

        logger.info("Appointment generation complete: %s total synthetic", len(appointment_ids))
        return appointment_ids

    def _all_staff_prof_ids(self) -> list[int]:
        all_ids: list[int] = []
        for ids in self.staff_ids.values():
            all_ids.extend(ids)
        if all_ids:
            return all_ids
        if self.client.model_exists("gnuhealth.healthprofessional"):
            return self.client.search("gnuhealth.healthprofessional", [], limit=500) or [1]
        return [1]

    def _resolve_gh_patients(self, ids: list[int]) -> list[int]:
        """Accept either gnuhealth.patient ids or party.party ids."""
        if not ids:
            if self.client.model_exists("gnuhealth.patient"):
                return self.client.search("gnuhealth.patient", [], limit=5000)
            return []
        if not self.client.model_exists("gnuhealth.patient"):
            return ids

        # Heuristic: if records exist on gnuhealth.patient with these ids, use as-is.
        as_patients = self.client.search(
            "gnuhealth.patient", [("id", "in", ids[:50])], limit=50
        )
        if len(as_patients) >= min(10, len(ids)):
            return self.client.search("gnuhealth.patient", [("id", "in", ids)], limit=10000)

        resolved: list[int] = []
        for party_id in ids:
            found = self.client.search(
                "gnuhealth.patient", [("party", "=", party_id)], limit=1
            )
            if found:
                resolved.append(found[0])
        return resolved
