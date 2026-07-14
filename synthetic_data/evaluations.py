"""Patient evaluation generation."""

from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)

CHIEF_COMPLAINTS = [
    "Mild headache",
    "Fever and cough",
    "Abdominal pain",
    "Back pain",
    "Follow-up diabetes",
    "Hypertension review",
    "Sore throat",
    "Fatigue",
    "Chest discomfort",
    "Routine checkup",
]


class EvaluationGenerator:
    """Create gnuhealth.patient.evaluation records."""

    def __init__(
        self,
        client: TrytonClient,
        config: dict[str, Any],
        generator: DataGenerator,
        context: dict[str, Any],
        patient_ids: list[int],
        staff_ids: dict[str, list[int]] | None = None,
        idempotent: bool = True,
    ) -> None:
        self.client = client
        self.config = config
        self.generator = generator
        self.context = context
        self.patient_ids = patient_ids
        self.staff_ids = staff_ids or {}
        self.idempotent = idempotent
        self.batch_size = config["data"].get("batch_size", 100)
        self.eval_ratio = config["options"].get("evaluation_ratio", 0.6)

    def run(self) -> list[int]:
        if not self.config["data"]["modules"].get("evaluations", True):
            logger.info("Evaluations module disabled — skipping")
            return []

        model = "gnuhealth.patient.evaluation"
        if not self.client.model_exists(model):
            logger.warning("Model %s not available — skipping", model)
            return []

        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        existing_ids = self.client.search(
            model, [("chief_complaint", "like", f"{marker}%")], limit=100000
        )
        patients = self._resolve_gh_patients()
        doctors = self._doctor_ids()
        if not patients:
            logger.warning("No patients for evaluations")
            return existing_ids
        if not doctors:
            logger.warning("No health professionals — evaluations need healthprof")
            return existing_ids

        target = max(1, int(len(patients) * self.eval_ratio))
        if self.idempotent and len(existing_ids) >= target:
            logger.info(
                "Found %s synthetic evaluations (target %s) — skipping",
                len(existing_ids),
                target,
            )
            return existing_ids

        to_create = target - len(existing_ids) if self.idempotent else target
        logger.info("Creating %s patient evaluations...", to_create)

        eval_ids: list[int] = list(existing_ids) if self.idempotent else []
        batch: list[dict] = []
        counter = len(existing_ids)
        institution_id = self.context.get("institution_id")

        for i in range(to_create):
            counter += 1
            start = datetime.now() - timedelta(days=random.randint(1, 180))
            complaint = random.choice(CHIEF_COMPLAINTS)
            vals: dict[str, Any] = {
                "patient": patients[i % len(patients)],
                "healthprof": random.choice(doctors),
                "evaluation_start": start.isoformat(),
                "chief_complaint": f"{marker} {complaint} ({prefix}-EVAL-{counter:06d})",
                "evaluation_summary": f"{marker} Synthetic evaluation note {counter}",
                "visit_type": random.choice(["new", "followup", "followup"]),
                "urgency": random.choice(["a", "a", "a", "b"]),
                "evaluation_type": "outpatient",
            }
            if institution_id:
                vals["institution"] = institution_id

            batch.append(vals)
            if len(batch) >= self.batch_size:
                ids = self.client.batch_create(model, batch, self.batch_size, "evaluations")
                eval_ids.extend(ids)
                batch = []

        if batch:
            ids = self.client.batch_create(model, batch, self.batch_size, "evaluations")
            eval_ids.extend(ids)

        logger.info("Evaluation generation complete: %s records", len(eval_ids))
        return eval_ids

    def _doctor_ids(self) -> list[int]:
        doctors = list(self.staff_ids.get("doctors", []))
        if doctors:
            return doctors
        if self.client.model_exists("gnuhealth.healthprofessional"):
            return self.client.search("gnuhealth.healthprofessional", [], limit=200)
        return []

    def _resolve_gh_patients(self) -> list[int]:
        if not self.client.model_exists("gnuhealth.patient"):
            return []
        if not self.patient_ids:
            return self.client.search("gnuhealth.patient", [], limit=5000)
        as_patients = self.client.search(
            "gnuhealth.patient", [("id", "in", self.patient_ids[:50])], limit=50
        )
        if len(as_patients) >= min(10, len(self.patient_ids)):
            return self.client.search(
                "gnuhealth.patient", [("id", "in", self.patient_ids)], limit=10000
            )
        resolved: list[int] = []
        for party_id in self.patient_ids:
            found = self.client.search(
                "gnuhealth.patient", [("party", "=", party_id)], limit=1
            )
            if found:
                resolved.append(found[0])
        return resolved or self.client.search("gnuhealth.patient", [], limit=5000)
