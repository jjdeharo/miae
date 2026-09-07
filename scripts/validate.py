#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("es", "ca", "eu", "gl", "en")
errors = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

for lang in LANGUAGES:
    source = ROOT / "content" / "v2.1" / f"{lang}.md"
    text = source.read_text(encoding="utf-8")
    require(len(text.splitlines()) == 261, f"{lang}: unexpected source line count")
    require(len(re.findall(r"^### (?!#)", text, re.M)) == 7, f"{lang}: expected classification heading and six levels")
    require("ZXQ" not in text and "\u200b" not in text, f"{lang}: translation artefact")
    require(len(re.findall(r"https?://", text)) == 4, f"{lang}: expected four reference URLs")

    html_path = ROOT / "v2.1" / lang / "index.html"
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    require(soup.html.get("lang") == lang, f"{lang}: wrong HTML language")
    require(len(soup.select("article h1")) == 1, f"{lang}: missing document title")
    require(len(soup.select("h3[id^='nivel-']")) == 6, f"{lang}: missing level anchors")
    require(len(soup.select("link[rel='alternate']")) == 6, f"{lang}: incomplete hreflang set")

    pdf = ROOT / "output" / "pdf" / f"miae-v2.1-{lang}.pdf"
    require(pdf.exists() and pdf.stat().st_size > 40_000, f"{lang}: PDF missing or too small")
    if pdf.exists():
        info = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True).stdout
        pages_match = re.search(r"^Pages:\s+(\d+)", info, re.M)
        pages = int(pages_match.group(1)) if pages_match else 0
        require(10 <= pages <= 16, f"{lang}: unexpected PDF page count")
        extracted = subprocess.run(
            ["pdftotext", str(pdf), "-"], check=True, text=True, capture_output=True
        ).stdout
        require("2.1" in extracted and len(extracted) > 20_000, f"{lang}: incomplete PDF text")

if errors:
    print("Validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Validated five sources, five web editions and five PDF editions.")
