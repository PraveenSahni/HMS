#!/usr/bin/env python3
from generator import generate
from validation import validate_record


def test_generate_dry_run():
    out = generate(dry_run=True)
    assert out["synthetic_data"] is True
    assert out["pack"] == "19_reporting"


def test_validation_flags_bad_id():
    errs = validate_record({"synthetic_data": True, "synthetic_batch_id": "x", "synthetic_seed": 1, "national_id": "784-1990-1234567-1"})
    assert errs
