#!/usr/bin/env python3
"""Markdown -> печатный PDF: две A5-страницы на альбомном A4, с номерами страниц.

Запуск:  venv/bin/python3 build_pdf.py file1.md file2.md ...
Требуется: markdown, pymupdf (в venv) и Google Chrome (headless print-to-pdf).
"""
import os
import re
import subprocess
import sys
import tempfile

import markdown

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: 148mm 210mm; margin: 12mm 11mm 14mm 11mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "PT Serif", Georgia, "Times New Roman", serif;
  font-size: 11.8pt; line-height: 1.34; color: #000; margin: 0;
  orphans: 3; widows: 3; text-align: left; hyphens: auto;
}
p { margin: 0 0 .42em; }
h1, h2, h3, h4 {
  font-family: "PT Sans", "Helvetica Neue", Arial, sans-serif;
  line-height: 1.18; break-after: avoid-page; page-break-after: avoid;
  break-inside: avoid; margin: .75em 0 .3em;
}
h1 { font-size: 17pt; margin-top: 0; }
h2 { font-size: 14.2pt; border-bottom: 1.2pt solid #000; padding-bottom: 2pt; }
/* Секция = глава/блок. Короткие секции пакуются по две на страницу,
   длинные Chrome всё равно перенесёт на новую страницу целиком. */
section { break-inside: avoid; page-break-inside: avoid; }
section + section { margin-top: 1.1em; }
.keep { break-inside: avoid; page-break-inside: avoid; }
h3 { font-size: 12.6pt; }
h4 { font-size: 11.8pt; }
/* заголовок + следующие два абзаца держим вместе */
h2 + *, h3 + *, h4 + * { break-before: avoid-page; page-break-before: avoid; }

ul, ol { margin: .25em 0 .5em; padding-left: 1.15em; }
li { margin: 0 0 .2em; }
li > ul, li > ol { margin: .15em 0 .15em; }

code, kbd { font-family: "Menlo", "DejaVu Sans Mono", monospace; font-size: .92em;
            background: #f0f0f0; padding: 0 .18em; border-radius: 2px; }
pre { background: #f4f4f4; border-left: 2.5pt solid #999; padding: .35em .5em;
      margin: .4em 0; break-inside: avoid; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: .9em; line-height: 1.25; }

blockquote { margin: .5em 0; padding: .35em .6em; border-left: 3pt solid #444;
             background: #f6f6f6; break-inside: avoid; page-break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }

table { border-collapse: collapse; width: 100%; margin: .45em 0 .6em;
        font-size: .95em; break-inside: avoid; page-break-inside: avoid; }
th, td { border: .6pt solid #666; padding: 2.2pt 4pt; vertical-align: top; }
th { background: #e8e8e8; font-family: "PT Sans", Arial, sans-serif; }
/* очень длинные таблицы всё же можно рвать — но с повтором шапки */
table.long { break-inside: auto; page-break-inside: auto; }
table.long thead { display: table-header-group; }
table.long tr { break-inside: avoid; page-break-inside: avoid; }

hr { border: none; border-top: .8pt solid #bbb; margin: .7em 0; }
strong { font-weight: 700; }
img { max-width: 100%; }
"""

HTML = """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>{title}</title><style>{css}</style></head><body>{body}</body></html>"""


def wrap_sections(body):
    """Каждую главу/блок (от h1/h2 до следующего) заворачиваем в <section>,
    чтобы она не рвалась посередине, но короткие соседи ложились на один лист."""
    parts = re.split(r"(?=<h[12][ >])", body)
    head = parts[0] if parts and not parts[0].startswith("<h") else ""
    chunks = parts[1:] if head else parts
    out = [head] if head else []
    for c in chunks:
        # «ЧАСТЬ …» (h1 с коротким подзаголовком) приклеиваем к следующей главе
        out.append("<section>" + c + "</section>")
    html = "".join(out)
    html = re.sub(r"</section>\s*<section>(?=<h1)", "</section><section>", html)
    # h1-«часть» без собственного содержимого сливаем со следующей секцией
    html = re.sub(r"<section>((?:(?!<section>).){0,400}?)</section>\s*<section>(?=<h2)",
                  r"<section>\1", html, flags=re.S)
    return html


def md_to_pdf_a5(md_path, out_pdf):
    text = open(md_path, encoding="utf-8").read()
    # в исходниках списки часто идут сразу за строкой текста, без пустой строки —
    # markdown их тогда не видит; вставляем пустую строку
    text = re.sub(r"(?m)^(?![-*+] |\d+[.)] |\s*$)(.+)\n(?=(?:[-*+] |\d+[.)] ))", r"\1\n\n", text)
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"],
    )
    # таблицы с >14 строк помечаем как «длинные» — им разрешён разрыв
    def mark_long(m):
        html = m.group(0)
        return html.replace("<table>", '<table class="long">', 1) if html.count("<tr") > 14 else html
    body = re.sub(r"<table>.*?</table>", mark_long, body, flags=re.S)
    # линейка-разделитель прямо перед заголовком главы избыточна — он и так виден
    body = re.sub(r"<hr\s*/?>\s*(?=<h[12])", "", body)
    # короткая подпись-номер («3.4») не должна отрываться от своего блока/таблицы
    body = re.sub(
        r"(<p>(?:(?!</p>).){0,90}</p>)\s*(<(?:pre|table)\b.*?</(?:pre|table)>)",
        r'<div class="keep">\1\2</div>', body, flags=re.S)
    body = wrap_sections(body)

    html = HTML.format(title=os.path.basename(md_path), css=CSS, body=body)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        html_path = f.name
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--run-all-compositor-stages-before-draw", "--virtual-time-budget=10000",
         f"--print-to-pdf={out_pdf}", "file://" + html_path],
        check=True, capture_output=True,
    )
    os.unlink(html_path)


def impose_2up(src_pdf, out_pdf):
    """Две A5-страницы рядом на альбомном A4 + номера страниц."""
    import fitz

    A4L = fitz.paper_rect("a4-l")  # 842 x 595 pt
    src = fitz.open(src_pdf)
    n = src.page_count
    if n % 2:
        n += 1  # добьём пустой страницей
    out = fitz.open()
    half = A4L.width / 2

    for i in range(0, n, 2):
        sheet = out.new_page(width=A4L.width, height=A4L.height)
        for k in range(2):
            idx = i + k
            if idx >= src.page_count:
                continue
            sp = src[idx]
            scale = min(half / sp.rect.width, A4L.height / sp.rect.height)
            w, h = sp.rect.width * scale, sp.rect.height * scale
            x0 = k * half + (half - w) / 2
            y0 = (A4L.height - h) / 2
            sheet.show_pdf_page(fitz.Rect(x0, y0, x0 + w, y0 + h), src, idx)
            # номер страницы по центру низа каждой половинки
            sheet.insert_text(
                fitz.Point(x0 + w / 2 - 8, y0 + h - 12),
                str(idx + 1), fontname="helv", fontsize=9, color=(0.25, 0.25, 0.25),
            )
        # тонкая линия сгиба/реза посередине
        sheet.draw_line(fitz.Point(half, 14), fitz.Point(half, A4L.height - 14),
                        color=(0.8, 0.8, 0.8), width=0.4)
    out.save(out_pdf, garbage=3, deflate=True)
    out.close()
    src.close()
    return src_pdf, n


def main():
    for md in sys.argv[1:]:
        base = os.path.splitext(md)[0]
        a5 = base + "_a5.pdf"
        final = base + "_print.pdf"
        md_to_pdf_a5(md, a5)
        impose_2up(a5, final)
        import fitz
        d = fitz.open(final)
        print(f"{md} -> {final}  ({d.page_count} листов A4, {fitz.open(a5).page_count} страниц A5)")
        d.close()


if __name__ == "__main__":
    main()
