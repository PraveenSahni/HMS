"""Health professional / staff generation."""

from __future__ import annotations

import logging
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class StaffGenerator:
    """Create doctors, nurses, admin, reception, lab, and pharmacy staff."""

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

    def run(self) -> dict[str, list[int]]:
        staff_mix = self._scaled_staff_mix()
        total = self.config["data"].get("staff", 300)
        mix_sum = sum(staff_mix.values())
        if mix_sum > total:
            logger.warning("Staff mix sum (%s) exceeds total (%s) after scaling", mix_sum, total)

        all_staff: dict[str, list[int]] = {}
        specialty_ids = self.context.get("specialty_ids", [])
        institution_id = self.context.get("institution_id")

        for role, count in staff_mix.items():
            if count <= 0:
                continue
            logger.info("Creating %s %s staff...", count, role)
            ids = self._create_role_staff(role, count, specialty_ids, institution_id)
            all_staff[role] = ids
            logger.info("Created %s %s staff members", len(ids), role)

        total_created = sum(len(v) for v in all_staff.values())
        logger.info("Staff generation complete: %s total", total_created)
        return all_staff

    def _scaled_staff_mix(self) -> dict[str, int]:
        staff_mix = self.config["data"].get("staff_mix", {})
        total = self.config["data"].get("staff", 300)
        mix_sum = sum(staff_mix.values())
        if mix_sum <= 0:
            return {}
        if mix_sum <= total:
            return dict(staff_mix)

        scale = total / mix_sum
        scaled: dict[str, int] = {}
        remaining = total
        items = list(staff_mix.items())
        for i, (role, count) in enumerate(items):
            if i == len(items) - 1:
                scaled[role] = remaining
            else:
                n = min(max(0, round(count * scale)), remaining)
                scaled[role] = n
                remaining -= n
        logger.info(
            "Scaled staff mix from %s to %s (target total %s)",
            mix_sum,
            sum(scaled.values()),
            total,
        )
        return scaled

    def _create_role_staff(
        self,
        role: str,
        count: int,
        specialty_ids: list[int],
        institution_id: int | None,
    ) -> list[int]:
        professional_ids: list[int] = []
        records_batch: list[dict] = []
        party_batch: list[dict] = []
        meta: list[dict] = []

        for i in range(1, count + 1):
            staff = self.generator.staff_role_name(role, i)
            code = staff["code"]

            if self.idempotent:
                existing = self.client.search(
                    "party.party", [("code", "=", code)], limit=1
                )
                if existing:
                    prof_id = self._find_professional(existing[0])
                    if prof_id:
                        professional_ids.append(prof_id)
                    else:
                        professional_ids.extend(
                            self._create_professionals(
                                [existing[0]], [staff], role, specialty_ids, institution_id
                            )
                        )
                    continue

            party_vals = {
                "name": f"{staff['title']} {staff['full_en']}",
                "code": code,
                "is_person": True,
                "is_healthprof": True,
                "fed_country": self.generator.fed_country,
                "gender": "m" if staff.get("gender") == "male" else "f",
            }
            party_batch.append(party_vals)
            meta.append(staff)

            if len(party_batch) >= self.batch_size:
                professional_ids.extend(
                    self._flush_staff_batch(party_batch, meta, role, specialty_ids, institution_id)
                )
                party_batch, meta = [], []

        if party_batch:
            professional_ids.extend(
                self._flush_staff_batch(party_batch, meta, role, specialty_ids, institution_id)
            )
        return professional_ids

    def _flush_staff_batch(
        self,
        party_batch: list[dict],
        meta: list[dict],
        role: str,
        specialty_ids: list[int],
        institution_id: int | None,
    ) -> list[int]:
        party_ids = self.client.batch_create("party.party", party_batch, self.batch_size, "staff parties")
        if isinstance(party_ids, int):
            party_ids = [party_ids]

        return self._create_professionals(
            party_ids, meta, role, specialty_ids, institution_id
        )

    def _create_professionals(
        self,
        party_ids: list[int],
        meta: list[dict],
        role: str,
        specialty_ids: list[int],
        institution_id: int | None,
    ) -> list[int]:
        if not self.client.model_exists("gnuhealth.healthprofessional"):
            return party_ids

        prof_ids: list[int] = []
        for party_id, staff in zip(party_ids, meta):
            vals: dict[str, Any] = {
                "party": party_id,
            }
            if institution_id and role in ("doctors", "nurses", "lab", "pharmacy"):
                vals["institution"] = institution_id

            try:
                prof_id = self.client.create("gnuhealth.healthprofessional", vals)
                if isinstance(prof_id, list):
                    prof_id = prof_id[0]
                prof_ids.append(prof_id)
            except Exception as exc:
                logger.debug("Could not create healthprofessional for %s: %s", staff["code"], exc)
                prof_ids.append(party_id)
        return prof_ids

    def _find_professional(self, party_id: int) -> int | None:
        if not self.client.model_exists("gnuhealth.healthprofessional"):
            return party_id
        ids = self.client.search(
            "gnuhealth.healthprofessional", [("party", "=", party_id)], limit=1
        )
        return ids[0] if ids else None
