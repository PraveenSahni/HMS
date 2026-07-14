"""Laboratory tests and results generation."""

from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class LaboratoryGenerator:
    """Create lab test types, orders (gnuhealth.patient.lab.test), and results."""

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
        self.lab_ratio = config["options"].get("lab_orders_ratio", 0.4)
        self.results_ratio = config["options"].get("lab_results_ratio", 0.6)

    def run(self) -> dict[str, Any]:
        if not self.config["data"]["modules"].get("laboratory", True):
            logger.info("Laboratory module disabled — skipping")
            return {"test_type_ids": [], "lab_order_ids": [], "lab_result_ids": []}

        test_type_ids = self._setup_test_types()
        lab_order_ids = self._create_lab_orders(test_type_ids)
        lab_result_ids = self._create_lab_results(test_type_ids)

        logger.info(
            "Laboratory generation complete: %s test types, %s orders, %s results",
            len(test_type_ids),
            len(lab_order_ids),
            len(lab_result_ids),
        )
        return {
            "test_type_ids": test_type_ids,
            "lab_order_ids": lab_order_ids,
            "lab_result_ids": lab_result_ids,
        }

    def _setup_test_types(self) -> list[int]:
        model = "gnuhealth.lab.test_type"
        if not self.client.model_exists(model):
            logger.warning("No lab test type model found — skipping lab test types")
            return []

        # Prefer existing catalog (module XML often ships many types).
        existing = self.client.search(model, [], limit=500)
        if existing:
            logger.info("Using %s existing lab test types", len(existing))
            return existing

        test_ids: list[int] = []
        prefix = self.generator.code_prefix
        for i, test_name in enumerate(self.config["data"].get("lab_tests", []), 1):
            code = self.generator.lab_test_code(i)
            test_id, _ = self.client.find_or_create(
                model,
                [("name", "=", test_name)],
                {"name": test_name, "code": code},
                idempotent=self.idempotent,
            )
            test_ids.append(test_id)
        return test_ids

    def _doctor_ids(self) -> list[int]:
        doctors = list(self.staff_ids.get("doctors", []))
        if doctors:
            return doctors
        lab = list(self.staff_ids.get("lab", []))
        if lab:
            return lab
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

    def _create_lab_orders(self, test_type_ids: list[int]) -> list[int]:
        model = "gnuhealth.patient.lab.test"
        if not self.client.model_exists(model):
            logger.warning("Model gnuhealth.patient.lab.test not found — skipping lab orders")
            return []
        if not test_type_ids:
            logger.warning("No lab test types — skipping lab orders")
            return []

        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        existing_ids = self.client.search(
            model, [("comment", "like", f"{marker}%")], limit=100000
        )
        patients = self._resolve_gh_patients()
        if not patients:
            logger.warning("No patients for lab orders")
            return existing_ids

        target = max(1, int(len(patients) * self.lab_ratio))
        # Multiple tests per selected patient
        target = max(target, int(len(patients) * self.lab_ratio * 1.5))

        if self.idempotent and len(existing_ids) >= target:
            logger.info(
                "Found %s synthetic lab orders (target %s) — skipping",
                len(existing_ids),
                target,
            )
            return existing_ids

        to_create = target - len(existing_ids) if self.idempotent else target
        doctors = self._doctor_ids()
        logger.info("Creating %s lab orders...", to_create)

        order_ids: list[int] = list(existing_ids) if self.idempotent else []
        batch: list[dict] = []
        counter = len(existing_ids)

        for i in range(to_create):
            counter += 1
            patient = patients[i % len(patients)]
            order_date = datetime.now() - timedelta(days=random.randint(1, 180))
            vals: dict[str, Any] = {
                "test_type": random.choice(test_type_ids),
                "patient_id": patient,
                "date": order_date.isoformat(),
                "source_type": "patient",
                "urgent": random.random() < 0.15,
                "comment": f"{marker} {prefix}-LABORD-{counter:06d}",
            }
            if doctors:
                vals["doctor_id"] = random.choice(doctors)

            batch.append(vals)
            if len(batch) >= self.batch_size:
                ids = self.client.batch_create(model, batch, self.batch_size, "lab orders")
                order_ids.extend(ids)
                batch = []

        if batch:
            ids = self.client.batch_create(model, batch, self.batch_size, "lab orders")
            order_ids.extend(ids)

        return order_ids

    def _create_lab_results(self, test_type_ids: list[int]) -> list[int]:
        model = "gnuhealth.lab"
        if not self.client.model_exists(model):
            logger.info("gnuhealth.lab not available — skipping results")
            return []
        if not test_type_ids:
            return []

        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        existing_ids = self.client.search(
            model, [("results", "like", f"{marker}%")], limit=100000
        )
        patients = self._resolve_gh_patients()
        if not patients:
            return existing_ids

        target = max(1, int(len(patients) * self.lab_ratio * self.results_ratio))
        if self.idempotent and len(existing_ids) >= target:
            logger.info(
                "Found %s synthetic lab results (target %s) — skipping",
                len(existing_ids),
                target,
            )
            return existing_ids

        to_create = target - len(existing_ids) if self.idempotent else target
        doctors = self._doctor_ids()
        logger.info("Creating %s lab results...", to_create)

        result_ids: list[int] = list(existing_ids) if self.idempotent else []
        batch: list[dict] = []
        counter = len(existing_ids)

        for i in range(to_create):
            counter += 1
            requested = datetime.now() - timedelta(days=random.randint(2, 180))
            analyzed = requested + timedelta(hours=random.randint(4, 72))
            vals: dict[str, Any] = {
                "test": random.choice(test_type_ids),
                "patient": patients[i % len(patients)],
                "source_type": "patient",
                "date_requested": requested.isoformat(),
                "date_analysis": analyzed.isoformat(),
                "results": (
                    f"{marker} {prefix}-LABRES-{counter:06d} — "
                    f"{random.choice(['Within normal limits', 'Mild elevation', 'Borderline', 'Normal'])}"
                ),
            }
            if doctors:
                vals["requestor"] = random.choice(doctors)
                if random.random() < 0.5:
                    vals["pathologist"] = random.choice(doctors)

            batch.append(vals)
            if len(batch) >= self.batch_size:
                ids = self.client.batch_create(model, batch, self.batch_size, "lab results")
                result_ids.extend(ids)
                batch = []

        if batch:
            ids = self.client.batch_create(model, batch, self.batch_size, "lab results")
            result_ids.extend(ids)

        return result_ids
