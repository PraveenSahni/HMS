"""Realistic data generators for Qatar (English + Arabic)."""

from __future__ import annotations

import random
import string
from datetime import date, datetime, timedelta
from typing import Any

from faker import Faker

# Common Qatari / Gulf Arabic family names (transliterated)
ARABIC_SURNAMES = [
    "Al-Thani", "Al-Attiyah", "Al-Kuwari", "Al-Marri", "Al-Mansouri",
    "Al-Naimi", "Al-Suwaidi", "Al-Hajri", "Al-Malki", "Al-Dosari",
    "Al-Kaabi", "Al-Mohannadi", "Al-Baker", "Al-Sada", "Al-Emadi",
    "Al-Hardan", "Al-Jaber", "Al-Khalifa", "Al-Rumaihi", "Al-Nuaimi",
]

ARABIC_GIVEN_MALE = [
    "Mohammed", "Ahmed", "Abdullah", "Khalid", "Hamad", "Saeed",
    "Rashid", "Fahad", "Sultan", "Nasser", "Youssef", "Omar",
    "Ali", "Hassan", "Ibrahim", "Tariq", "Majed", "Faisal",
]

ARABIC_GIVEN_FEMALE = [
    "Fatima", "Aisha", "Mariam", "Noor", "Hessa", "Latifa",
    "Amna", "Sara", "Layla", "Dana", "Reem", "Noura",
    "Moza", "Wadha", "Shamma", "Aljohara", "Ghada", "Hind",
]

COUNTRY_ALPHA3 = {
    "QA": "QAT",
    "AE": "ARE",
    "SA": "SAU",
    "KW": "KWT",
    "BH": "BHR",
    "OM": "OMN",
}

QATAR_AREAS = [
    "West Bay", "Al Sadd", "Al Waab", "The Pearl", "Lusail",
    "Al Rayyan", "Al Gharrafa", "Muaither", "Al Wakra", "Al Khor",
    "Bin Mahmoud", "Old Airport", "Al Hilal", "Najma", "Madinat Khalifa",
]

STAFF_TITLES = {
    "doctors": ["Dr.", "Dr."],
    "nurses": ["RN", "Staff Nurse"],
    "admin": ["Admin Officer", "Manager"],
    "reception": ["Receptionist", "Front Desk"],
    "lab": ["Lab Technician", "Lab Analyst"],
    "pharmacy": ["Pharmacist", "Pharmacy Tech"],
}


class DataGenerator:
    """Generates bilingual Qatar-appropriate synthetic data."""

    def __init__(self, config: dict[str, Any], seed: int = 42) -> None:
        self.config = config
        self.company = config["company"]
        self.seed = seed
        random.seed(seed)
        Faker.seed(seed)
        self.fake_en = Faker("en")
        self.fake_ar = Faker("ar_SA")

    @property
    def fed_country(self) -> str:
        code = self.company.get("country_code", "QA")
        return COUNTRY_ALPHA3.get(code, code if len(code) == 3 else "XXX")

    @property
    def code_prefix(self) -> str:
        return self.company.get("code", "SYN")

    def qatar_phone(self) -> str:
        prefix = self.company.get("phone_prefix", "+974")
        # Qatar mobile: 3xxx xxxx or 5xxx xxxx, landline: 4xxx xxxx
        first = random.choice(["3", "5", "4", "7"])
        number = "".join(str(random.randint(0, 9)) for _ in range(7))
        return f"{prefix} {first}{number[:3]} {number[3:]}"

    def qatar_address(self, lang: str = "en") -> str:
        area = random.choice(QATAR_AREAS)
        building = random.randint(1, 999)
        street = random.randint(1, 120)
        city = self.company.get("city", "Doha")
        country = self.company.get("country", "Qatar")
        if lang == "ar":
            return f"مبنى {building}، شارع {street}، {area}، {city}، {country}"
        return f"Building {building}, Street {street}, {area}, {city}, {country}"

    def person_name(self, gender: str | None = None) -> dict[str, str]:
        """Return bilingual name dict."""
        if gender is None:
            gender = random.choice(["male", "female"])
        if gender == "male":
            given_en = random.choice(ARABIC_GIVEN_MALE + [self.fake_en.first_name_male()])
            given_ar = random.choice(ARABIC_GIVEN_MALE)
        else:
            given_en = random.choice(ARABIC_GIVEN_FEMALE + [self.fake_en.first_name_female()])
            given_ar = random.choice(ARABIC_GIVEN_FEMALE)
        surname = random.choice(ARABIC_SURNAMES)
        return {
            "given_en": given_en,
            "given_ar": given_ar,
            "surname": surname,
            "full_en": f"{given_en} {surname}",
            "full_ar": f"{given_ar} {surname}",
            "gender": gender,
        }

    def patient_code(self, index: int) -> str:
        return f"{self.code_prefix}-P-{index:05d}"

    def staff_code(self, role: str, index: int) -> str:
        role_abbr = role[:3].upper()
        return f"{self.code_prefix}-ST-{role_abbr}-{index:04d}"

    def email(self, name: str, domain: str | None = None) -> str:
        domain = domain or "isttechnologies.qa"
        slug = name.lower().replace(" ", ".").replace("'", "")
        slug = "".join(c for c in slug if c in string.ascii_lowercase + ".-")
        suffix = random.randint(1, 999) if random.random() > 0.7 else ""
        return f"{slug}{suffix}@{domain}"

    def dob_adult(self) -> date:
        return self.fake_en.date_of_birth(minimum_age=1, maximum_age=90)

    def dob_child(self) -> date:
        return self.fake_en.date_of_birth(minimum_age=0, maximum_age=17)

    def appointment_datetime(self, months_back: int) -> datetime:
        end = datetime.now()
        start = end - timedelta(days=months_back * 30)
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        dt = start + timedelta(seconds=random_seconds)
        # Clinic hours 8am-8pm, weekdays weighted
        hour = random.randint(8, 19)
        minute = random.choice([0, 15, 30, 45])
        return dt.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def appointment_state(self, appt_dt: datetime) -> str:
        if appt_dt > datetime.now():
            return random.choice(["confirmed", "free"])
        return random.choice(["done", "done", "done", "user_cancelled", "no_show"])

    def staff_role_name(self, role: str, index: int) -> dict[str, Any]:
        name = self.person_name()
        titles = STAFF_TITLES.get(role, ["Staff"])
        title = random.choice(titles)
        return {
            **name,
            "title": title,
            "role": role,
            "code": self.staff_code(role, index),
            "phone": self.qatar_phone(),
            "email": self.email(name["full_en"]),
        }

    def medication_code(self, index: int) -> str:
        return f"{self.code_prefix}-MED-{index:04d}"

    def lab_test_code(self, index: int) -> str:
        return f"{self.code_prefix}-LAB-{index:03d}"
