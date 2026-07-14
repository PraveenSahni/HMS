"""Company and institution setup for GNU Health."""

from __future__ import annotations

import logging
from typing import Any

from synthetic_data.client import TrytonClient
from synthetic_data.generators import DataGenerator

logger = logging.getLogger(__name__)


class CompanySetup:
    """Configure company, institution, and departments."""

    def __init__(
        self,
        client: TrytonClient,
        config: dict[str, Any],
        generator: DataGenerator,
        idempotent: bool = True,
    ) -> None:
        self.client = client
        self.config = config
        self.company_cfg = config["company"]
        self.data_cfg = config["data"]
        self.generator = generator
        self.idempotent = idempotent
        self.context: dict[str, Any] = {}

    def run(self) -> dict[str, Any]:
        logger.info("Setting up company: %s", self.company_cfg["name"])
        country_id = self._get_country()
        currency_id = self._get_currency()
        company_id, institution_id = self._setup_institution(country_id)
        department_ids = self._setup_departments(institution_id)
        specialty_ids = self._setup_specialties()

        self.context = {
            "country_id": country_id,
            "currency_id": currency_id,
            "company_id": company_id,
            "institution_id": institution_id,
            "department_ids": department_ids,
            "specialty_ids": specialty_ids,
        }
        logger.info(
            "Company setup complete — institution id=%s, departments=%s",
            institution_id,
            len(department_ids),
        )
        return self.context

    def _get_country(self) -> int:
        code = self.company_cfg.get("country_code", "QA")
        existing = self.client.search("country.country", [("code", "=", code)], limit=1)
        if existing:
            return existing[0]
        # Qatar should exist after import_countries; fallback create
        return self.client.create(
            "country.country",
            {"name": self.company_cfg["country"], "code": code},
        )

    def _get_currency(self) -> int:
        code = "QAR"
        existing = self.client.search("currency.currency", [("code", "=", code)], limit=1)
        if existing:
            return existing[0]
        return self.client.create(
            "currency.currency",
            {"name": "Qatari Riyal", "code": code, "symbol": "QR"},
        )

    def _primary_address(self) -> str:
        """Return formatted primary (Qatar) office address from config."""
        offices = self.company_cfg.get("offices", {})
        qatar = offices.get("qatar", {})
        if qatar.get("address_lines"):
            parts: list[str] = list(qatar["address_lines"])
            if qatar.get("po_box"):
                parts.append(f"PO Box {qatar['po_box']}")
            city = qatar.get("city", self.company_cfg.get("city", "Doha"))
            country = qatar.get("country", self.company_cfg.get("country", "Qatar"))
            parts.append(f"{city}, {country}")
            return ", ".join(parts)
        return self.company_cfg.get("address_en", "")

    def _setup_institution(self, country_id: int) -> tuple[int | None, int]:
        name = self.company_cfg["name"]
        code = self.company_cfg.get("code", "IST")

        if self.client.model_exists("gnuhealth.institution"):
            if self.idempotent:
                existing = self.client.search(
                    "gnuhealth.institution", [("code", "=", code)], limit=1
                )
                if existing:
                    logger.info("Institution '%s' already exists (id=%s)", name, existing[0])
                    company_id = self._get_company_for_institution(existing[0])
                    return company_id, existing[0]

            inst_id = self._create_institution(name, code, country_id)
            company_id = self._ensure_company(name, code, country_id, currency_id=None)
            return company_id, inst_id

        # Fallback: company only
        company_id = self._ensure_company(name, code, country_id, currency_id=None)
        return company_id, company_id

    def _create_institution(self, name: str, code: str, country_id: int) -> int:
        party_id, _ = self.client.find_or_create(
            "party.party",
            [("code", "=", f"{code}-CO")],
            {
                "name": name,
                "code": f"{code}-CO",
                "is_institution": True,
                "is_person": False,
                "fed_country": self.generator.fed_country,
            },
            idempotent=self.idempotent,
        )
        if self.idempotent:
            self.client.write("party.party", [party_id], {"is_institution": True})

        values = {
            "party": party_id,
            "code": code,
            "institution_type": "clinic",
            "public_level": "private",
            "extra_info": (
                f"{self.company_cfg.get('facility_type', 'Clinic')} — "
                f"{self._primary_address()}\n"
                f"Legal: {self.company_cfg.get('legal_name', name)}\n"
                f"AR: {self.company_cfg.get('name_ar', name)}"
            ),
        }
        inst_id = self.client.create("gnuhealth.institution", values)
        if isinstance(inst_id, list):
            inst_id = inst_id[0]
        logger.info("Created institution '%s' (id=%s)", name, inst_id)
        return inst_id

    def _ensure_company(
        self,
        name: str,
        code: str,
        country_id: int,
        currency_id: int | None,
    ) -> int:
        if not self.client.model_exists("company.company"):
            return 0
        existing = self.client.search("company.company", [("code", "=", code)], limit=1)
        if existing:
            return existing[0]

        party_id, _ = self.client.find_or_create(
            "party.party",
            [("code", "=", f"{code}-CO")],
            {
                "name": name,
                "code": f"{code}-CO",
            },
            idempotent=self.idempotent,
        )
        values: dict[str, Any] = {
            "party": party_id,
            "code": code,
            "currency": currency_id or self._get_currency(),
        }
        company_id = self.client.create("company.company", values)
        if isinstance(company_id, list):
            company_id = company_id[0]
        logger.info("Created company '%s' (id=%s)", name, company_id)
        return company_id

    def _get_company_for_institution(self, institution_id: int) -> int | None:
        if not self.client.model_exists("company.company"):
            return None
        # GNU Health may link institution to company indirectly
        return None

    def _setup_departments(self, institution_id: int) -> list[int]:
        if not self.client.model_exists("gnuhealth.institution.unit"):
            logger.warning("Model gnuhealth.institution.unit not available — skipping departments")
            return []

        dept_ids: list[int] = []
        for dept in self.data_cfg.get("departments", []):
            name = dept["name"]
            code = f"{self.company_cfg.get('code', 'IST')}-{name[:4].upper().replace(' ', '')}"
            domain = [("name", "=", name), ("institution", "=", institution_id)]
            dept_id, created = self.client.find_or_create(
                "gnuhealth.institution.unit",
                domain,
                {
                    "name": name,
                    "code": code,
                    "institution": institution_id,
                    "comment": dept.get("name_ar", ""),
                },
                idempotent=self.idempotent,
            )
            dept_ids.append(dept_id)
            if created:
                logger.debug("Created department: %s", name)
        return dept_ids

    def _setup_specialties(self) -> list[int]:
        if not self.client.model_exists("gnuhealth.specialty"):
            logger.warning("Model gnuhealth.specialty not available — skipping specialties")
            return []

        specialty_ids: list[int] = []
        for spec_name in self.data_cfg.get("specialties", []):
            code = spec_name[:6].upper().replace(" ", "")
            spec_id, _ = self.client.find_or_create(
                "gnuhealth.specialty",
                [("name", "=", spec_name)],
                {"name": spec_name, "code": code},
                idempotent=self.idempotent,
            )
            specialty_ids.append(spec_id)
        return specialty_ids
