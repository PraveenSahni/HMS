"""Patient demographic generation."""

from __future__ import annotations

import logging
import random
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class PatientGenerator:
    """Create patient records with Qatar demographics."""

    def __init__(
        self,
        client: TrytonClient,
        config: dict[str, Any],
        generator: DataGenerator,
        context: dict[str, Any],
        idempotent: bool = True,
    ) -> None:
        self.client = client
        self.config = config
        self.generator = generator
        self.context = context
        self.idempotent = idempotent
        self.batch_size = config["data"].get("batch_size", 100)
        self.total = config["data"].get("patients", 4000)

    def run(self) -> list[int]:
        logger.info("Generating %s patients...", self.total)

        patient_ids: list[int] = []
        start_index = 1
        if self.idempotent:
            start_index = self.client.search_count(
                "party.party", [("code", "like", f"{self.generator.code_prefix}-P-%")]
            ) + 1

        party_batch: list[dict] = []
        patient_meta: list[dict] = []

        for i in range(start_index, self.total + 1):
            code = self.generator.patient_code(i)
            if self.idempotent:
                existing = self.client.search("party.party", [("code", "=", code)], limit=1)
                if existing:
                    self._ensure_gh_patient(existing[0])
                    patient_ids.append(existing[0])
                    continue

            name = self.generator.person_name()
            is_child = random.random() < 0.22
            dob = (
                self.generator.dob_child()
                if is_child
                else self.generator.dob_adult()
            )

            party_batch.append({
                "name": name["full_en"],
                "code": code,
                "is_person": True,
                "is_patient": True,
                "fed_country": self.generator.fed_country,
                "create_target": False,
                "gender": "m" if name.get("gender") == "male" else "f",
            })
            patient_meta.append({**name, "code": code, "dob": dob, "is_child": is_child})

            if len(party_batch) >= self.batch_size:
                patient_ids.extend(self._flush_patients(party_batch, patient_meta))
                party_batch, patient_meta = [], []

        if party_batch:
            patient_ids.extend(self._flush_patients(party_batch, patient_meta))

        if self.idempotent and len(patient_ids) < self.total:
            prefix = self.generator.code_prefix
            for party_id in self.client.search(
                "party.party",
                [("code", "like", f"{prefix}-P-%")],
                limit=self.total,
            ):
                if party_id not in patient_ids:
                    self._ensure_gh_patient(party_id)
                    patient_ids.append(party_id)
                if len(patient_ids) >= self.total:
                    break

        logger.info("Patient generation complete: %s records", len(patient_ids))
        return patient_ids[: self.total]

    def _ensure_gh_patient(self, party_id: int, meta: dict | None = None) -> int | None:
        if not self.client.model_exists("gnuhealth.patient"):
            return party_id
        existing = self.client.search(
            "gnuhealth.patient", [("party", "=", party_id)], limit=1
        )
        if existing:
            return existing[0]
        vals: dict[str, Any] = {"party": party_id}
        if meta and meta.get("dob"):
            vals["dob"] = meta["dob"].isoformat()
        try:
            return self.client.create("gnuhealth.patient", vals)
        except Exception as exc:
            logger.debug("Could not create gnuhealth.patient for party %s: %s", party_id, exc)
            return None

    def _flush_patients(
        self,
        party_batch: list[dict],
        patient_meta: list[dict],
    ) -> list[int]:
        party_ids = self.client.batch_create(
            "party.party", party_batch, self.batch_size, "patients"
        )
        if isinstance(party_ids, int):
            party_ids = [party_ids]

        if not self.client.model_exists("gnuhealth.patient"):
            return party_ids

        gh_records: list[dict] = []
        for party_id, meta in zip(party_ids, patient_meta):
            if self.client.search("gnuhealth.patient", [("party", "=", party_id)], limit=1):
                continue
            vals: dict[str, Any] = {"party": party_id}
            if meta.get("dob"):
                vals["dob"] = meta["dob"].isoformat()
            gh_records.append(vals)

        try:
            gh_ids = self.client.batch_create(
                "gnuhealth.patient", gh_records, self.batch_size, "gnuhealth patients"
            )
            if isinstance(gh_ids, int):
                return [gh_ids]
            return party_ids
        except Exception as exc:
            logger.warning("gnuhealth.patient batch create failed: %s — parties created only", exc)
            return party_ids
