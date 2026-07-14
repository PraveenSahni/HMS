"""Pharmacy products and prescriptions generation."""

from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class PharmacyGenerator:
    """Create medication products and prescriptions."""

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
        self.rx_ratio = config["options"].get("prescription_ratio", 0.5)

    def run(self) -> dict[str, Any]:
        if not self.config["data"]["modules"].get("pharmacy", True):
            logger.info("Pharmacy module disabled — skipping")
            return {"product_ids": [], "prescription_ids": []}

        product_ids = self._setup_medications()
        try:
            prescription_ids = self._create_prescriptions()
        except Exception as exc:
            logger.warning("Prescription creation skipped: %s", exc)
            prescription_ids = []

        logger.info(
            "Pharmacy generation complete: %s products, %s prescriptions",
            len(product_ids),
            len(prescription_ids),
        )
        return {"product_ids": product_ids, "prescription_ids": prescription_ids}

    def _setup_medications(self) -> list[int]:
        # Prefer GNU Health medicament catalog when present.
        if self.client.model_exists("gnuhealth.medicament"):
            meds = self.client.search("gnuhealth.medicament", [], limit=500)
            if meds:
                logger.info("Using %s existing medicaments", len(meds))
                return meds

        if not self.client.model_exists("product.template"):
            logger.warning("product.template not available — skipping medications")
            return []

        uom_id = self._default_uom_id()
        product_ids: list[int] = []
        prefix = self.generator.code_prefix

        for i, med_name in enumerate(self.config["data"].get("medications", []), 1):
            code = self.generator.medication_code(i)
            vals: dict[str, Any] = {
                "name": med_name,
                "code": code,
                "type": "goods",
            }
            if uom_id:
                vals["default_uom"] = uom_id
            # Avoid list_price (requires company multivalue context on some installs).
            template_id, _ = self.client.find_or_create(
                "product.template",
                [("code", "=", code)],
                vals,
                idempotent=self.idempotent,
            )
            product_ids.append(template_id)

        return product_ids

    def _default_uom_id(self) -> int | None:
        if not self.client.model_exists("product.uom"):
            return None
        for name in ("Unit", "Units", "u"):
            ids = self.client.search("product.uom", [("name", "=", name)], limit=1)
            if ids:
                return ids[0]
        ids = self.client.search("product.uom", [], limit=1)
        return ids[0] if ids else None

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

    def _create_prescriptions(self) -> list[int]:
        model = "gnuhealth.prescription.order"
        if not self.client.model_exists(model):
            logger.warning("No prescription model found — skipping prescriptions")
            return []

        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        existing_ids = self.client.search(
            model, [("notes", "like", f"{marker}%")], limit=100000
        )
        patients = self._resolve_gh_patients()
        if not patients:
            return existing_ids

        target = max(1, int(len(patients) * self.rx_ratio))
        if self.idempotent and len(existing_ids) >= target:
            logger.info(
                "Found %s synthetic prescriptions (target %s) — skipping",
                len(existing_ids),
                target,
            )
            return existing_ids

        to_create = target - len(existing_ids) if self.idempotent else target
        doctors = self._doctor_ids()
        if not doctors:
            logger.warning("No health professionals — prescriptions need healthprof")
            return existing_ids

        logger.info("Creating %s prescriptions...", to_create)
        rx_ids: list[int] = list(existing_ids) if self.idempotent else []
        batch: list[dict] = []
        counter = len(existing_ids)

        for i in range(to_create):
            counter += 1
            rx_date = datetime.now() - timedelta(days=random.randint(1, 180))
            # healthprof is UI-readonly but accepted on create via RPC/proxy.
            vals: dict[str, Any] = {
                "patient": patients[i % len(patients)],
                "healthprof": random.choice(doctors),
                "prescription_date": rx_date.isoformat(),
                "prescription_warning_ack": True,
                "notes": f"{marker} {prefix}-RX-{counter:06d}",
            }
            batch.append(vals)
            if len(batch) >= self.batch_size:
                ids = self.client.batch_create(model, batch, self.batch_size, "prescriptions")
                rx_ids.extend(ids)
                batch = []

        if batch:
            ids = self.client.batch_create(model, batch, self.batch_size, "prescriptions")
            rx_ids.extend(ids)

        return rx_ids
