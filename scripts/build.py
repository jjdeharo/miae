#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://jjdeharo.github.io/miae"

LANGUAGES = {
    "es": {"native": "Castellano", "label": "Español"},
    "ca": {"native": "Català", "label": "Catalán"},
    "eu": {"native": "Euskara", "label": "Euskera"},
    "gl": {"native": "Galego", "label": "Gallego"},
    "en": {"native": "English", "label": "Inglés"},
}

UI = {
    "es": {
        "skip": "Saltar al contenido", "brand_subtitle": "Marco de integración de la IA",
        "navigation": "Navegación principal", "home": "Inicio", "language": "Idioma",
        "current_version": "Versión vigente", "resources": "Recursos", "document": "Documento",
        "read_download": "Leer o descargar", "download_pdf": "Descargar PDF",
        "summary_image": "Infografía resumen", "blog_article": "Artículo en Bilateria",
        "levels": "Acceso a los niveles", "full_framework": "Texto completo",
        "more_resources": "Otros formatos", "podcast": "Pódcast", "podcast_note": "34 minutos · español",
        "video": "Vídeo", "video_note": "Explicación visual · español", "assistant": "Asistente MIAE",
        "assistant_note": "Consultar el marco y clasificar casos", "citation": "Referencia",
        "how_to_cite": "Cómo citar este trabajo", "previous_version": "Versión 2 revisada",
        "level_names": ["La persona crea", "La IA reformula", "La IA planifica", "La persona construye", "Cocreación", "La persona supervisa"],
    },
    "ca": {
        "skip": "Ves al contingut", "brand_subtitle": "Marc d’integració de la IA",
        "navigation": "Navegació principal", "home": "Inici", "language": "Idioma",
        "current_version": "Versió vigent", "resources": "Recursos", "document": "Document",
        "read_download": "Llegir o descarregar", "download_pdf": "Descarregar PDF",
        "summary_image": "Infografia resum", "blog_article": "Article a Bilateria",
        "levels": "Accés als nivells", "full_framework": "Text complet",
        "more_resources": "Altres formats", "podcast": "Pòdcast", "podcast_note": "34 minuts · castellà",
        "video": "Vídeo", "video_note": "Explicació visual · castellà", "assistant": "Assistent MIAE",
        "assistant_note": "Consultar el marc i classificar casos", "citation": "Referència",
        "how_to_cite": "Com citar aquest treball", "previous_version": "Versió 2 revisada",
        "level_names": ["La persona crea", "La IA reformula", "La IA planifica", "La persona construeix", "Cocreació", "La persona supervisa"],
    },
    "eu": {
        "skip": "Edukira joan", "brand_subtitle": "IA integratzeko esparrua",
        "navigation": "Nabigazio nagusia", "home": "Hasiera", "language": "Hizkuntza",
        "current_version": "Uneko bertsioa", "resources": "Baliabideak", "document": "Dokumentua",
        "read_download": "Irakurri edo deskargatu", "download_pdf": "PDFa deskargatu",
        "summary_image": "Laburpen-infografia", "blog_article": "Bilateriako artikulua",
        "levels": "Mailetarako sarbidea", "full_framework": "Testu osoa",
        "more_resources": "Beste formatu batzuk", "podcast": "Podcasta", "podcast_note": "34 minutu · gaztelaniaz",
        "video": "Bideoa", "video_note": "Azalpen bisuala · gaztelaniaz", "assistant": "MIAE laguntzailea",
        "assistant_note": "Esparrua kontsultatu eta kasuak sailkatu", "citation": "Erreferentzia",
        "how_to_cite": "Lan hau nola aipatu", "previous_version": "2. bertsio berrikusia",
        "level_names": ["Pertsonak sortzen du", "IAk birformulatzen du", "IAk planifikatzen du", "Pertsonak eraikitzen du", "Elkarrekin sortzea", "Pertsonak gainbegiratzen du"],
    },
    "gl": {
        "skip": "Ir ao contido", "brand_subtitle": "Marco de integración da IA",
        "navigation": "Navegación principal", "home": "Inicio", "language": "Idioma",
        "current_version": "Versión vixente", "resources": "Recursos", "document": "Documento",
        "read_download": "Ler ou descargar", "download_pdf": "Descargar PDF",
        "summary_image": "Infografía resumo", "blog_article": "Artigo en Bilateria",
        "levels": "Acceso aos niveis", "full_framework": "Texto completo",
        "more_resources": "Outros formatos", "podcast": "Pódcast", "podcast_note": "34 minutos · castelán",
        "video": "Vídeo", "video_note": "Explicación visual · castelán", "assistant": "Asistente MIAE",
        "assistant_note": "Consultar o marco e clasificar casos", "citation": "Referencia",
        "how_to_cite": "Como citar este traballo", "previous_version": "Versión 2 revisada",
        "level_names": ["A persoa crea", "A IA reformula", "A IA planifica", "A persoa constrúe", "Cocreación", "A persoa supervisa"],
    },
    "en": {
        "skip": "Skip to content", "brand_subtitle": "AI integration framework",
        "navigation": "Main navigation", "home": "Home", "language": "Language",
        "current_version": "Current version", "resources": "Resources", "document": "Document",
        "read_download": "Read or download", "download_pdf": "Download PDF",
        "summary_image": "Summary infographic", "blog_article": "Article on Bilateria",
        "levels": "Go to levels", "full_framework": "Full text",
        "more_resources": "Other formats", "podcast": "Podcast", "podcast_note": "34 minutes · Spanish",
        "video": "Video", "video_note": "Visual explanation · Spanish", "assistant": "MIAE assistant",
        "assistant_note": "Explore the framework and classify cases", "citation": "Reference",
        "how_to_cite": "How to cite this work", "previous_version": "Revised version 2",
        "level_names": ["The person creates", "AI reformulates", "AI plans", "The person builds", "Co-creation", "The person supervises"],
    },
}

for lang, labels in json.loads((ROOT / "data" / "home-ui.json").read_text()).items():
    UI[lang].update(labels)

DESCRIPTIONS = {
    "es": "Marco para describir cómo se reparte el trabajo entre la persona y la IA generativa en las tareas educativas.",
    "ca": "Marc per descriure com es reparteix el treball entre la persona i la IA generativa en les tasques educatives.",
    "eu": "Hezkuntza-zereginetan pertsonaren eta IA sortzailearen arteko lan-banaketa deskribatzeko esparrua.",
    "gl": "Marco para describir como se reparte o traballo entre a persoa e a IA xerativa nas tarefas educativas.",
    "en": "A framework for describing how work is shared between people and generative AI in educational tasks.",
}

GUIDES = {lang: json.loads((ROOT / "data" / "guide" / f"{lang}.json").read_text()) for lang in LANGUAGES}

env = Environment(undefined=StrictUndefined, loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))

def heading_ids(html: str) -> str:
    def add_id(match: re.Match) -> str:
        inner = match.group(1)
        plain = re.sub(r"<[^>]+>", "", inner)
        number = re.search(r"(?:Nivel|Nivell|Level)\s+([0-5])|([0-5])\.\s*maila", plain, re.I)
        if not number:
            return match.group(0)
        level = number.group(1) or number.group(2)
        return f'<h3 id="nivel-{level}">{inner}</h3>'
    html = re.sub(r"<h3>(.*?)</h3>", add_id, html)
    # Stable anchors across translations; the first h3 is the classification section.
    html = re.sub(r"<h3>", '<h3 id="clasificar">', html, count=1)
    section_ids = iter(["origen", "escala", "resumen", "descripcion", "referencias"])
    return re.sub(r"<h2>", lambda _: f'<h2 id="{next(section_ids)}">', html)

def build_page(lang: str) -> str:
    source = ROOT / "content" / "v2.1" / f"{lang}.md"
    text = source.read_text(encoding="utf-8")
    html_content = markdown.markdown(text, extensions=["extra", "sane_lists"])
    html_content = heading_ids(html_content)
    title = re.sub(r"^#\s+", "", text.splitlines()[0])
    return env.get_template("page.html").render(
        lang=lang, page_title=f"{title} · MIAE", description=DESCRIPTIONS[lang],
        canonical=f"{BASE_URL}/v2.1/{lang}/", base_url=BASE_URL, root="../../",
        languages=LANGUAGES, ui=UI[lang], guide=GUIDES[lang], content=html_content,
        license_lang=lang if lang in {"es", "ca"} else "en", range=range,
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", action="store_true", help="Generate the five downloadable PDF editions")
    args = parser.parse_args()
    def build_home(lang, root_path, automatic=False):
        return env.get_template("home.html").render(
            lang=lang, ui=UI[lang], guide=GUIDES[lang], description=DESCRIPTIONS[lang],
            languages=LANGUAGES, range=range, root=root_path,
            base_url=BASE_URL, automatic=automatic,
            license_lang=lang if lang in {"es", "ca"} else "en",
        )
    (ROOT / "index.html").write_text(build_home("es", "./", True), encoding="utf-8")
    for lang in LANGUAGES:
        home_dir = ROOT / lang
        home_dir.mkdir(exist_ok=True)
        (home_dir / "index.html").write_text(build_home(lang, "../"), encoding="utf-8")
    available = []
    for lang in LANGUAGES:
        if not (ROOT / "content" / "v2.1" / f"{lang}.md").exists():
            continue
        available.append(lang)
        output_dir = ROOT / "v2.1" / lang
        output_dir.mkdir(parents=True, exist_ok=True)
        page = build_page(lang)
        (output_dir / "index.html").write_text(page, encoding="utf-8")
        if args.pdf:
            pdf_dir = ROOT / "output" / "pdf"
            pdf_dir.mkdir(parents=True, exist_ok=True)
            HTML(filename=str(output_dir / "index.html")).write_pdf(
                pdf_dir / f"miae-v2.1-{lang}.pdf"
            )
    (ROOT / "v2.1" / "index.html").write_text(
        env.get_template("entry.html").render(languages=LANGUAGES), encoding="utf-8"
    )
    suffix = " and PDF editions" if args.pdf else ""
    print(f"Generated home and {len(available)} language page(s){suffix}: {', '.join(available)}")

if __name__ == "__main__":
    main()
