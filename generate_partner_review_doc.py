"""Generate IST Health Partner Feature Review as a Word .doc file."""
import html
import re
from pathlib import Path

SRC = Path(__file__).parent / "IST_health_module_feature_discussion.html"
OUT = Path(__file__).parent / "IST_Health_Partner_Feature_Review.doc"


def esc(text: str) -> str:
    return html.escape(text or "").replace("\n", "<br/>")


def parse_modules(content: str) -> list[dict]:
    modules = []
    for article in re.finditer(
        r'<article class="card" data-id="([^"]+)"[^>]*>(.*?)</article>',
        content,
        re.DOTALL,
    ):
        block = article.group(2)
        title_m = re.search(r"<h3>(.*?)</h3>", block, re.DOTALL)
        sub_m = re.search(r'<div class="subtitle">(.*?)</div>', block, re.DOTALL)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else article.group(1)
        subtitle = re.sub(r"\s+", " ", sub_m.group(1)).strip() if sub_m else ""

        ist_items = []
        ext_items = []
        lists = re.findall(r"<ul class=\"feature-list\">(.*?)</ul>", block, re.DOTALL)
        if lists:
            for li in re.findall(r"<li>(.*?)</li>", lists[0], re.DOTALL):
                text = re.sub(r"\s+", " ", li).strip()
                if text:
                    ist_items.append(text)
        if len(lists) > 1:
            for li in re.findall(r'<li class="ext-item"[^>]*>(.*?)</li>', lists[1], re.DOTALL):
                text = re.sub(r"\s+", " ", li).strip()
                if text:
                    ext_items.append(text)

        modules.append({
            "id": article.group(1),
            "title": title,
            "subtitle": subtitle,
            "ist": ist_items,
            "ext": ext_items,
        })
    return modules


def feature_rows(items: list[str], kind: str) -> str:
    rows = []
    for item in items:
        rows.append(
            f"""<tr>
  <td width="8%" align="center" style="border:1px solid #999;padding:6px;font-size:11pt;">&#9744;</td>
  <td width="10%" style="border:1px solid #999;padding:6px;font-size:10pt;color:#555;">{esc(kind)}</td>
  <td width="42%" style="border:1px solid #999;padding:6px;font-size:11pt;">{esc(item)}</td>
  <td width="40%" style="border:1px solid #999;padding:6px;font-size:11pt;height:36px;">&nbsp;</td>
</tr>"""
        )
    return "\n".join(rows)


def build_doc(modules: list[dict]) -> str:
    module_sections = []
    for mod in modules:
        rows = feature_rows(mod["ist"], "IST Health")
        if mod["ext"]:
            rows += "\n" + feature_rows(mod["ext"], "Extension")
        module_sections.append(
            f"""
<h2 style="font-family:Calibri,sans-serif;font-size:14pt;color:#0F6E56;margin:18pt 0 6pt 0;">{esc(mod["title"])}</h2>
<p style="font-family:Calibri,sans-serif;font-size:10pt;color:#555;margin:0 0 8pt 0;"><b>Module included?</b> &#9744; Yes &nbsp; &#9744; No &nbsp;&nbsp;|&nbsp;&nbsp; {esc(mod["subtitle"])}</p>
<p style="font-family:Calibri,sans-serif;font-size:10pt;margin:0 0 4pt 0;"><b>Module comments:</b></p>
<p style="font-family:Calibri,sans-serif;font-size:11pt;border:1px solid #999;padding:8pt;min-height:28pt;margin:0 0 10pt 0;">&nbsp;</p>
<table border="1" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;font-family:Calibri,sans-serif;">
<tr style="background:#E1F5EE;">
  <td width="8%" align="center" style="border:1px solid #999;padding:6px;font-size:10pt;font-weight:bold;">Include</td>
  <td width="10%" style="border:1px solid #999;padding:6px;font-size:10pt;font-weight:bold;">Type</td>
  <td width="42%" style="border:1px solid #999;padding:6px;font-size:10pt;font-weight:bold;">Feature</td>
  <td width="40%" style="border:1px solid #999;padding:6px;font-size:10pt;font-weight:bold;">Partner comment</td>
</tr>
{rows}
</table>"""
        )

    return f"""<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:w="urn:schemas-microsoft-com:office:word"
xmlns="http://www.w3.org/TR/REC-html40">
<head>
<meta charset="utf-8"/>
<meta name="ProgId" content="Word.Document"/>
<meta name="Generator" content="IST Health Review Generator"/>
<title>IST Health — Partner Feature Review</title>
<!--[if gte mso 9]><xml>
<w:WordDocument>
  <w:View>Print</w:View>
  <w:Zoom>100</w:Zoom>
  <w:DoNotOptimizeForBrowser/>
</w:WordDocument>
</xml><![endif]-->
<style>
@page {{ size: 8.5in 11in; margin: 1in; }}
body {{ font-family: Calibri, sans-serif; font-size: 11pt; color: #1a1a19; line-height: 1.45; }}
h1 {{ font-size: 22pt; color: #0F6E56; margin-bottom: 6pt; }}
.box {{ border: 1px solid #999; padding: 10pt; margin-bottom: 12pt; background: #f7f6f3; }}
.instructions ol {{ margin: 6pt 0 0 18pt; }}
table {{ mso-table-lspace:0pt; mso-table-rspace:0pt; }}
</style>
</head>
<body>

<h1>IST Health — Partner Feature Review</h1>
<p style="font-size:11pt;color:#444;">Interactive scope document for clinic / hospital management platform implementation.<br/>
Please review each module, mark features to include, and add comments where needed. Return the completed document to the sender.</p>

<div class="box">
<p style="font-size:12pt;font-weight:bold;margin:0 0 8pt 0;color:#185FA5;">Partner information</p>
<table border="0" width="100%" style="font-family:Calibri,sans-serif;font-size:11pt;">
<tr>
  <td width="18%"><b>Partner name:</b></td>
  <td width="32%" style="border-bottom:1px solid #999;">&nbsp;</td>
  <td width="18%"><b>Organization:</b></td>
  <td width="32%" style="border-bottom:1px solid #999;">&nbsp;</td>
</tr>
<tr><td colspan="4" style="height:8pt;"></td></tr>
<tr>
  <td><b>Email:</b></td>
  <td style="border-bottom:1px solid #999;">&nbsp;</td>
  <td><b>Review date:</b></td>
  <td style="border-bottom:1px solid #999;">&nbsp;</td>
</tr>
</table>
<p style="margin:10pt 0 4pt 0;font-weight:bold;">Overall comments</p>
<p style="border:1px solid #999;padding:8pt;min-height:48pt;margin:0;">&nbsp;</p>
</div>

<div class="box instructions">
<p style="font-size:12pt;font-weight:bold;margin:0 0 6pt 0;">How to complete this review</p>
<ol style="font-size:11pt;">
  <li>Fill in your name, organization, email, and review date above.</li>
  <li>For each module, tick <b>Include</b> (&#9744;) for every feature you want in scope — or type <b>Yes</b> in the comment column.</li>
  <li>Add comments on any feature where you need clarification, changes, or have questions.</li>
  <li>Save this document and return it to the sender.</li>
</ol>
<p style="font-size:10pt;color:#666;margin:8pt 0 0 0;">Tip: In Word, click a checkbox cell and type <b>X</b> or use Insert &gt; Symbol to mark &#9745; included.</p>
</div>

{"".join(module_sections)}

<p style="margin-top:24pt;font-size:10pt;color:#888;border-top:1px solid #ccc;padding-top:8pt;">
IST Health Partner Feature Review &mdash; generated for partner scope discussion
</p>

</body>
</html>"""


def main() -> None:
    content = SRC.read_text(encoding="utf-8")
    modules = parse_modules(content)
    if not modules:
        raise SystemExit("No modules parsed from HTML source.")
    OUT.write_text(build_doc(modules), encoding="utf-8")
    print(f"Created {OUT} ({len(modules)} modules)")


if __name__ == "__main__":
    main()
