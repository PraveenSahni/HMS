"""Inpatient beds and admissions generation."""

from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class InpatientGenerator:
    """Create hospital building/ward/beds and inpatient registrations."""

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
        self.bed_count = config["options"].get("inpatient_beds", 12)
        self.admission_ratio = config["options"].get("inpatient_ratio", 0.25)

    def run(self) -> dict[str, Any]:
        if not self.config["data"]["modules"].get("inpatient", True):
            logger.info("Inpatient module disabled — skipping")
            return {"bed_ids": [], "admission_ids": []}

        required = (
            "gnuhealth.hospital.bed",
            "gnuhealth.inpatient.registration",
            "gnuhealth.hospital.ward",
            "gnuhealth.hospital.building",
        )
        missing = [m for m in required if not self.client.model_exists(m)]
        if missing:
            logger.warning("Inpatient models missing %s — skipping", missing)
            return {"bed_ids": [], "admission_ids": [], "skipped": missing}

        institution_id = self.context.get("institution_id") or self._first_institution()
        if not institution_id:
            logger.warning("No institution — skipping inpatient")
            return {"bed_ids": [], "admission_ids": []}

        building_id = self._ensure_building(institution_id)
        ward_id = self._ensure_ward(institution_id, building_id)
        bed_ids = self._ensure_beds(institution_id, ward_id)
        admission_ids = self._create_admissions(bed_ids)

        logger.info(
            "Inpatient generation complete: %s beds, %s admissions",
            len(bed_ids),
            len(admission_ids),
        )
        return {
            "building_id": building_id,
            "ward_id": ward_id,
            "bed_ids": bed_ids,
            "admission_ids": admission_ids,
        }

    def _first_institution(self) -> int | None:
        if not self.client.model_exists("gnuhealth.institution"):
            return None
        ids = self.client.search("gnuhealth.institution", [], limit=1)
        return ids[0] if ids else None

    def _ensure_building(self, institution_id: int) -> int:
        prefix = self.generator.code_prefix
        code = f"{prefix}-BLD-01"
        name = f"{prefix} Main Building"

        # Match by code, name, or any existing building for this institution.
        for domain in (
            [("code", "=", code)],
            [("name", "=", name), ("institution", "=", institution_id)],
            [("institution", "=", institution_id)],
            [],
        ):
            existing = self.client.search(
                "gnuhealth.hospital.building", domain, limit=1
            )
            if existing:
                logger.info("Building id=%s (existing)", existing[0])
                return existing[0]

        bid = self.client.create(
            "gnuhealth.hospital.building",
            {
                "name": name,
                "code": code,
                "institution": institution_id,
                "extra_info": f"{prefix} synthetic building",
            },
        )
        bid = bid[0] if isinstance(bid, list) else bid
        logger.info("Building id=%s (created)", bid)
        return bid

    def _ensure_ward(self, institution_id: int, building_id: int) -> int:
        prefix = self.generator.code_prefix
        name = f"{prefix}-WARD-A"

        for domain in (
            [("name", "=", name), ("institution", "=", institution_id)],
            [("institution", "=", institution_id)],
            [],
        ):
            existing = self.client.search("gnuhealth.hospital.ward", domain, limit=1)
            if existing:
                logger.info("Ward id=%s (existing)", existing[0])
                return existing[0]

        wid = self.client.create(
            "gnuhealth.hospital.ward",
            {
                "name": name,
                "institution": institution_id,
                "building": building_id,
                "gender": "unisex",
                "number_of_beds": self.bed_count,
                "state": "beds_available",
                "extra_info": f"{prefix} synthetic ward",
            },
        )
        wid = wid[0] if isinstance(wid, list) else wid
        logger.info("Ward id=%s (created)", wid)
        return wid

    def _default_uom_id(self) -> int | None:
        if not self.client.model_exists("product.uom"):
            return None
        for name in ("Unit", "Units", "u"):
            ids = self.client.search("product.uom", [("name", "=", name)], limit=1)
            if ids:
                return ids[0]
        ids = self.client.search("product.uom", [], limit=1)
        return ids[0] if ids else None

    def _ensure_bed_product(self, label: str) -> int | None:
        """Create product.template (+ variant) marked is_bed=True. No list_price."""
        if not self.client.model_exists("product.template"):
            return None
        if not self.client.model_exists("product.product"):
            return None

        templates = self.client.search(
            "product.template", [("name", "=", label)], limit=1
        )
        if templates:
            tmpl_id = templates[0]
        else:
            vals: dict[str, Any] = {"name": label, "type": "service"}
            uom = self._default_uom_id()
            if uom:
                vals["default_uom"] = uom
            created = self.client.create("product.template", vals)
            tmpl_id = created[0] if isinstance(created, list) else created

        products = self.client.search(
            "product.product", [("template", "=", tmpl_id)], limit=1
        )
        if products:
            pid = products[0]
            try:
                self.client.write("product.product", [pid], {"is_bed": True})
            except Exception:
                pass
            return pid

        created = self.client.create(
            "product.product", {"template": tmpl_id, "is_bed": True}
        )
        return created[0] if isinstance(created, list) else created

    def _ensure_beds(self, institution_id: int, ward_id: int) -> list[int]:
        prefix = self.generator.code_prefix
        existing = self.client.search("gnuhealth.hospital.bed", [], limit=500)
        if self.idempotent and len(existing) >= self.bed_count:
            logger.info("Found %s beds (target %s) — skipping bed create", len(existing), self.bed_count)
            return existing[: self.bed_count]

        bed_ids = list(existing)
        start = len(existing) + 1
        for i in range(start, self.bed_count + 1):
            label = f"{prefix} Bed {i:02d}"
            product_id = self._ensure_bed_product(label)
            if not product_id:
                logger.warning("Could not create bed product for %s", label)
                continue
            already = self.client.search(
                "gnuhealth.hospital.bed",
                [("product", "=", product_id), ("institution", "=", institution_id)],
                limit=1,
            )
            if already:
                bed_ids.append(already[0])
                continue
            new_id = self.client.create(
                "gnuhealth.hospital.bed",
                {
                    "product": product_id,
                    "institution": institution_id,
                    "ward": ward_id,
                    "bed_type": random.choice(["gatch", "electric", "low"]),
                    "extra_info": f"{prefix} synthetic bed",
                },
            )
            bed_ids.append(new_id[0] if isinstance(new_id, list) else new_id)

        logger.info("Beds available: %s", len(bed_ids))
        return bed_ids

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

    def _create_admissions(self, bed_ids: list[int]) -> list[int]:
        model = "gnuhealth.inpatient.registration"
        prefix = self.generator.code_prefix
        marker = f"{prefix} synthetic:"
        existing_ids = self.client.search(
            model, [("info", "like", f"{marker}%")], limit=100000
        )
        patients = self._resolve_gh_patients()
        doctors = self._doctor_ids()
        if not patients or not bed_ids:
            return existing_ids

        target = max(1, int(len(patients) * self.admission_ratio))
        target = min(target, len(bed_ids) * 3)  # reuse beds over time
        if self.idempotent and len(existing_ids) >= target:
            logger.info(
                "Found %s synthetic admissions (target %s) — skipping",
                len(existing_ids),
                target,
            )
            return existing_ids

        to_create = target - len(existing_ids) if self.idempotent else target
        logger.info("Creating %s inpatient admissions...", to_create)
        admission_ids: list[int] = list(existing_ids) if self.idempotent else []
        counter = len(existing_ids)

        for i in range(to_create):
            counter += 1
            admit = datetime.now() - timedelta(days=random.randint(5, 120))
            discharge = admit + timedelta(days=random.randint(1, 14))
            vals: dict[str, Any] = {
                "patient": patients[i % len(patients)],
                "admission_type": random.choice(
                    ["routine", "elective", "urgent", "emergency"]
                ),
                "hospitalization_date": admit.isoformat(),
                "discharge_date": discharge.isoformat(),
                "bed": bed_ids[i % len(bed_ids)],
                "info": f"{marker} {prefix}-ADM-{counter:06d}",
            }
            if doctors:
                vals["attending_physician"] = random.choice(doctors)
            try:
                new_id = self.client.create(model, vals)
                admission_ids.append(new_id[0] if isinstance(new_id, list) else new_id)
            except Exception as exc:
                logger.warning("Admission create failed (%s): %s", counter, exc)

        return admission_ids
