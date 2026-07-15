#!/usr/bin/env python3
"""Generate SCREEN_BY_SCREEN_PARITY.xlsx from P0 seed rows."""
from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "docs" / "ist-his" / "SCREEN_BY_SCREEN_PARITY.xlsx"

ROWS = [
    ("Screen ID", "Menu path", "SAO available", "React route", "Status", "Priority", "Compare notes", "Build next action", "Owner", "Updated"),
    ("P0-LOGIN", "Auth / Login", "Y", "/login", "Partial", "P0", "IST login works; SAO has own login if session missing in iframe", "Share session / SSO note; document dual login", "Frontend", "2026-07-15"),
    ("P0-DASH", "Health / Dashboard", "Y", "/", "Partial", "P0", "React dashboard cards; SAO home richer", "Align KPIs with demo script", "Frontend", "2026-07-15"),
    ("P0-CO", "Administration / Companies", "Y", "/companies", "Partial", "P0", "List/create OK; deep CoA link via Workspace", "Harden multi-company switch UX", "Frontend", "2026-07-15"),
    ("P0-CUR", "Financial / Currency", "Y", "/currency", "Partial", "P0", "List AED/QAR; rates in SAO", "Confirm rates UX if needed", "Frontend", "2026-07-15"),
    ("P0-PARTY", "Party / Parties", "Y", "/parties", "Partial", "P0", "List/basic; deep tabs SAO", "Party categories/address depth", "Frontend", "2026-07-15"),
    ("P0-PAT", "Health / Patients", "Y", "/patients", "Partial", "P0", "List + detail; insurance/family SAO", "Deep demographics Hybrid", "Frontend", "2026-07-15"),
    ("P0-APT", "Health / Appointments", "Y", "/appointments", "Partial", "P0", "Create/list; specialty links Hybrid", "Product/insurance linking", "Frontend", "2026-07-15"),
    ("P0-LAB", "Health / Laboratory", "Y", "/laboratory", "Stub", "P0", "Orders list; create-test/results SAO", "Workspace CTA + result view later", "Frontend", "2026-07-15"),
    ("P0-RX", "Health / Prescriptions", "Y", "/medications;/pharmacy", "Stub", "P0", "Lists; create/dispense wizards SAO", "Rx create + stock-move Hybrid", "Frontend", "2026-07-15"),
    ("P0-EVAL", "Health / Evaluations", "Y", "/evaluations", "Stub", "P0", "List/create thin; full form SAO", "Harden consultation form", "Frontend", "2026-07-15"),
    ("P0-BED", "Health / Beds / Inpatient", "Y", "/beds", "Stub", "P0", "Bed board thin; admit/transfer SAO", "Admit/discharge basics", "Frontend", "2026-07-15"),
    ("P0-FIN", "Financial / Invoices", "Y", "/financial", "Stub", "P0", "List + draft stub; post/pay SAO", "Guided Workspace for CoA/post", "Frontend", "2026-07-15"),
    ("P0-USR", "Administration / Users", "Y", "/users", "Partial", "P0", "CRUD light; ACL depth SAO", "Groups permissions summary", "Frontend", "2026-07-15"),
    ("P0-SETUP", "IST / Setup Hub", "N*", "/setup", "Partial", "P0", "IST-only hub; SAO for wizards", "Keep; link Workspace", "Frontend", "2026-07-15"),
    ("P0-HELP", "IST / Help Centre", "N*", "/help", "Partial", "P0", "React Help; screenshots backlog", "Screenshot pack", "Docs", "2026-07-15"),
    ("P0-WS", "IST / Workspace (SAO embed)", "Y", "/workspace", "Partial", "P0", "Embed live; theming via custom.css", "Optional ?path= deep-link", "Frontend", "2026-07-15"),
    ("P0-STAFF", "Health / Health Professionals", "Y", "/staff", "Partial", "P0", "List/detail; specialty O2M SAO", "Specialty linking", "Frontend", "2026-07-15"),
    ("P0-IMG", "Health / Imaging", "Y", "/imaging", "Stub", "P0", "List; generate-result/Orthanc SAO", "Workspace CTA", "Frontend", "2026-07-15"),
    ("P0-NUR", "Health / Nursing", "Y", "/nursing", "Stub", "P0", "List; rounding/stock SAO", "Document Hybrid", "Frontend", "2026-07-15"),
    ("P0-PROC", "Health / Procedures", "Y", "/procedures", "Stub", "P0", "List thin", "Workspace for deep form", "Frontend", "2026-07-15"),
    ("P0-PROD", "Product / Products", "Y", "/products", "Partial", "P0", "Catalog list; UoM/accounts SAO", "Account categories after CoA", "Frontend", "2026-07-15"),
    ("P0-STK", "Stock / Inventory", "Y", "/stock", "Partial", "P0", "Locations/moves list; wizards SAO", "Adjustment wizards Workspace", "Frontend", "2026-07-15"),
    ("P0-CAL", "Calendar", "Y", "/calendar", "Stub", "P0", "Thin; events often SAO", "Optional if module empty", "Frontend", "2026-07-15"),
    ("P0-MOD", "Administration / Modules", "Y", "/modules", "Stub", "P0", "Mark-only; apply = SAO/admin", "Keep Workspace + trytond-admin", "Ops", "2026-07-15"),
    ("P0-GRP", "Administration / Groups", "Y", "/groups", "Stub", "P0", "List; ACL matrix SAO", "Summary view", "Frontend", "2026-07-15"),
    ("P0-SEQ", "Administration / Sequences", "Y", "/sequences", "Partial", "P0", "List/edit light", "Confirm numbering per company", "Frontend", "2026-07-15"),
    ("P0-CTR", "Administration / Countries", "Y", "/countries", "Partial", "P0", "Read/list", "Rarely change", "Frontend", "2026-07-15"),
    ("P0-LANG", "Administration / Languages", "Y", "/languages", "Partial", "P0", "Read/list", "Rarely change", "Frontend", "2026-07-15"),
    ("P0-SET", "IST / Settings", "N*", "/settings", "Partial", "P0", "Client settings + SAO URL", "Point to Workspace", "Frontend", "2026-07-15"),
    ("P0-MENU", "Menus / Model browser", "Y", "/menu/:id", "Partial", "P0", "Generic act_window; wizards to Workspace", "Extend model coverage", "Frontend", "2026-07-15"),
]


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main() -> None:
    try:
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = "P0 Parity"
        for row in ROWS:
            ws.append(list(row))
        for col in ws.columns:
            maxlen = max(len(str(c.value or "")) for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(maxlen + 2, 48)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        wb.save(OUT)
        print(f"Wrote {OUT} via openpyxl")
        return
    except ImportError:
        pass

    sheet_rows = []
    for ri, row in enumerate(ROWS, 1):
        cells = []
        for ci, val in enumerate(row, 1):
            ref = f"{col_letter(ci)}{ri}"
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(val))}</t></is></c>')
        sheet_rows.append(f'<row r="{ri}">{"".join(cells)}</row>')
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    wbxml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="P0 Parity" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    wbrels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wbxml)
        z.writestr("xl/_rels/workbook.xml.rels", wbrels)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    print(f"Wrote {OUT} via minimal OOXML")


if __name__ == "__main__":
    main()
