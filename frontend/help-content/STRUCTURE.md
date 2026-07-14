# Help content structure

The master brief suggested folders such as `en/common`, `en/admin`, `en/clinical`.

**Adaptation:** IST Health stores articles as flat JSON under `frontend/help-content/{en|ar}/`
with `roles[]`, `countries[]`, `routes[]`, `guided`, and `published` metadata.
Role/country filtering is applied in `helpService.ts` — functionally equivalent to
role folders without duplicating files.

Source tree is mirrored to `frontend/public/help-content/` for static serving.
Regenerate with: `python scripts/implementation/generate_help_content.py`
