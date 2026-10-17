"""Convierte un Markdown simple (headers, **bold**, `code`, ---, >, listas) a PDF via xhtml2pdf.
Uso: python md_to_pdf.py entrada.md salida.pdf "Titulo del documento"
"""
import re
import sys
from xhtml2pdf import pisa


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<code>\1</code>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def convert(md_text: str, title: str) -> str:
    lines = md_text.replace("\r\n", "\n").split("\n")
    html_parts = []
    in_ul = False
    in_quote = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

    def close_quote():
        nonlocal in_quote
        if in_quote:
            html_parts.append("</div>")
            in_quote = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if stripped == "":
            close_ul()
            close_quote()
            continue

        if stripped == "---":
            close_ul()
            close_quote()
            html_parts.append('<hr/>')
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_ul()
            close_quote()
            level = len(m.group(1))
            html_parts.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        if stripped.startswith(">"):
            if not in_quote:
                html_parts.append('<div class="quote">')
                in_quote = True
            html_parts.append(f"<p>{inline(stripped.lstrip('> ').strip())}</p>")
            continue
        else:
            close_quote()

        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{inline(m.group(1))}</li>")
            continue
        else:
            close_ul()

        html_parts.append(f"<p>{inline(stripped)}</p>")

    close_ul()
    close_quote()

    body = "\n".join(html_parts)

    css = """
    @page { size: A4; margin: 2cm 1.8cm; }
    body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1c2430; }
    h1 { font-size: 18pt; color: #123a7a; border-bottom: 2px solid #2a5db0; padding-bottom: 6px; margin-top: 0; }
    h2 { font-size: 14pt; color: #123a7a; border-bottom: 1px solid #c9c2b3; padding-bottom: 3px; margin-top: 20px; }
    h3 { font-size: 11.5pt; color: #2a5db0; margin-top: 14px; margin-bottom: 4px; }
    p { margin: 4px 0 8px 0; text-align: justify; }
    code { font-family: Courier, monospace; background: #eef1e8; color: #123a7a; padding: 1px 3px; font-size: 9.5pt; }
    hr { border: none; border-top: 1px solid #c9c2b3; margin: 14px 0; }
    ul { margin: 4px 0 10px 18px; padding: 0; }
    li { margin-bottom: 3px; }
    .quote { background: #f3f1ea; border-left: 3px solid #2a5db0; padding: 6px 10px; margin: 8px 0; font-size: 9.5pt; color: #4c5568; }
    a { color: #2a5db0; }
    """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    if len(sys.argv) < 4:
        print("Uso: python md_to_pdf.py entrada.md salida.pdf \"Titulo\"")
        sys.exit(1)

    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(src, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = convert(md_text, title)

    with open(dst, "wb") as out:
        result = pisa.CreatePDF(html, dest=out, encoding="utf-8")

    if result.err:
        print(f"Error generando PDF (código {result.err})")
        sys.exit(1)

    print(f"PDF generado: {dst}")


if __name__ == "__main__":
    main()
