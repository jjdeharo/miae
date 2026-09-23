#!/usr/bin/env python3
"""Builds the MIAE website from content/ and data/.

Pages per language: home (/<lang>/), classification sheet (/<lang>/ficha/), quick reference
(/<lang>/guia/) and the full framework (/v2.1/<lang>/), plus the neutral entry points (/ and
/v2.1/). With --pdf it also prints the downloadable PDFs into output/pdf/. See docs/adr/0001.
"""
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

# Interface texts per language. The home page ones come from data/home-ui.json and are merged below.
UI = {
    "es": {
        "share_level": "Copiar el enlace a este nivel", "link_copied": "Enlace copiado", "close": "Cerrar", "go_to_level": "Ir a la descripción del nivel", "level_word": "Nivel",
        "skip": "Saltar al contenido", "brand_subtitle": "Marco de integración de la IA",
        "navigation": "Navegación principal", "home": "Inicio", "language": "Idioma",
        "current_version": "Versión vigente", "resources": "Recursos", "document": "Documento",
        "read_download": "Leer o descargar", "download_pdf": "Descargar PDF",
        "zoom": "Zoom", "zoom_out": "Reducir", "zoom_in": "Ampliar", "zoom_reset": "Restablecer el zoom",
        "summary_image": "Infografía resumen", "blog_article": "Artículo en Bilateria",
        "levels": "Acceso a los niveles", "full_framework": "Texto completo",
        "more_resources": "Otros formatos", "podcast": "Pódcast", "podcast_note": "34 minutos · español",
        "video": "Vídeo", "video_note": "Explicación visual · español", "assistant": "Asistente MIAE",
        "assistant_note": "Consultar el marco y clasificar casos", "citation": "Referencia",
        "how_to_cite": "Cómo citar este trabajo", "previous_version": "Versión 2 revisada", "ai_use": "Elaborado con IA, nivel 4 del MIAE: el autor ha dirigido y revisado el contenido",
        "level_names": ["La persona crea", "La IA reformula", "La IA planifica", "La persona construye", "Cocreación", "La persona supervisa"],
    },
    "ca": {
        "share_level": "Copiar l’enllaç a aquest nivell", "link_copied": "Enllaç copiat", "close": "Tancar", "go_to_level": "Anar a la descripció del nivell", "level_word": "Nivell",
        "skip": "Ves al contingut", "brand_subtitle": "Marc d’integració de la IA",
        "navigation": "Navegació principal", "home": "Inici", "language": "Idioma",
        "current_version": "Versió vigent", "resources": "Recursos", "document": "Document",
        "read_download": "Llegir o descarregar", "download_pdf": "Descarregar PDF",
        "zoom": "Zoom", "zoom_out": "Reduir", "zoom_in": "Ampliar", "zoom_reset": "Restablir el zoom",
        "summary_image": "Infografia resum", "blog_article": "Article a Bilateria",
        "levels": "Accés als nivells", "full_framework": "Text complet",
        "more_resources": "Altres formats", "podcast": "Pòdcast", "podcast_note": "34 minuts · castellà",
        "video": "Vídeo", "video_note": "Explicació visual · castellà", "assistant": "Assistent MIAE",
        "assistant_note": "Consultar el marc i classificar casos", "citation": "Referència",
        "how_to_cite": "Com citar aquest treball", "previous_version": "Versió 2 revisada", "ai_use": "Elaborat amb IA, nivell 4 del MIAE: l'autor n'ha dirigit i revisat el contingut",
        "level_names": ["La persona crea", "La IA reformula", "La IA planifica", "La persona construeix", "Cocreació", "La persona supervisa"],
    },
    "eu": {
        "share_level": "Maila honetarako esteka kopiatu", "link_copied": "Esteka kopiatu da", "close": "Itxi", "go_to_level": "Mailaren deskribapenera joan", "level_word": "Maila",
        "skip": "Edukira joan", "brand_subtitle": "IA integratzeko esparrua",
        "navigation": "Nabigazio nagusia", "home": "Hasiera", "language": "Hizkuntza",
        "current_version": "Uneko bertsioa", "resources": "Baliabideak", "document": "Dokumentua",
        "read_download": "Irakurri edo deskargatu", "download_pdf": "PDFa deskargatu",
        "zoom": "Zooma", "zoom_out": "Txikitu", "zoom_in": "Handitu", "zoom_reset": "Zooma berrezarri",
        "summary_image": "Laburpen-infografia", "blog_article": "Bilateriako artikulua",
        "levels": "Mailetarako sarbidea", "full_framework": "Testu osoa",
        "more_resources": "Beste formatu batzuk", "podcast": "Podcasta", "podcast_note": "34 minutu · gaztelaniaz",
        "video": "Bideoa", "video_note": "Azalpen bisuala · gaztelaniaz", "assistant": "MIAE laguntzailea",
        "assistant_note": "Esparrua kontsultatu eta kasuak sailkatu", "citation": "Erreferentzia",
        "how_to_cite": "Lan hau nola aipatu", "previous_version": "2. bertsio berrikusia", "ai_use": "IArekin landua, MIAEren 4. maila: egileak edukia zuzendu eta berrikusi du",
        "level_names": ["Pertsonak sortzen du", "IAk birformulatzen du", "IAk planifikatzen du", "Pertsonak eraikitzen du", "Elkarrekin sortzea", "Pertsonak gainbegiratzen du"],
    },
    "gl": {
        "share_level": "Copiar a ligazón a este nivel", "link_copied": "Ligazón copiada", "close": "Pechar", "go_to_level": "Ir á descrición do nivel", "level_word": "Nivel",
        "skip": "Ir ao contido", "brand_subtitle": "Marco de integración da IA",
        "navigation": "Navegación principal", "home": "Inicio", "language": "Idioma",
        "current_version": "Versión vixente", "resources": "Recursos", "document": "Documento",
        "read_download": "Ler ou descargar", "download_pdf": "Descargar PDF",
        "zoom": "Zoom", "zoom_out": "Reducir", "zoom_in": "Ampliar", "zoom_reset": "Restablecer o zoom",
        "summary_image": "Infografía resumo", "blog_article": "Artigo en Bilateria",
        "levels": "Acceso aos niveis", "full_framework": "Texto completo",
        "more_resources": "Outros formatos", "podcast": "Pódcast", "podcast_note": "34 minutos · castelán",
        "video": "Vídeo", "video_note": "Explicación visual · castelán", "assistant": "Asistente MIAE",
        "assistant_note": "Consultar o marco e clasificar casos", "citation": "Referencia",
        "how_to_cite": "Como citar este traballo", "previous_version": "Versión 2 revisada", "ai_use": "Elaborado con IA, nivel 4 do MIAE: o autor dirixiu e revisou o contido",
        "level_names": ["A persoa crea", "A IA reformula", "A IA planifica", "A persoa constrúe", "Cocreación", "A persoa supervisa"],
    },
    "en": {
        "share_level": "Copy the link to this level", "link_copied": "Link copied", "close": "Close", "go_to_level": "Go to the level description", "level_word": "Level",
        "skip": "Skip to content", "brand_subtitle": "AI integration framework",
        "navigation": "Main navigation", "home": "Home", "language": "Language",
        "current_version": "Current version", "resources": "Resources", "document": "Document",
        "read_download": "Read or download", "download_pdf": "Download PDF",
        "zoom": "Zoom", "zoom_out": "Zoom out", "zoom_in": "Zoom in", "zoom_reset": "Reset zoom",
        "summary_image": "Summary infographic", "blog_article": "Article on Bilateria",
        "levels": "Go to levels", "full_framework": "Full text",
        "more_resources": "Other formats", "podcast": "Podcast", "podcast_note": "34 minutes · Spanish",
        "video": "Video", "video_note": "Visual explanation · Spanish", "assistant": "MIAE assistant",
        "assistant_note": "Explore the framework and classify cases", "citation": "Reference",
        "how_to_cite": "How to cite this work", "previous_version": "Revised version 2", "ai_use": "Made with AI, MIAE level 4: the author directed and reviewed the content",
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

SHARE_ICON = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
    '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>'
)

LEVEL_TITLE = re.compile(r"^(?:(?:Nivel|Nivell|Level)\s+([0-5])|([0-5])\.\s*maila)\s*[–.\-:]\s*(.+)$", re.I)

def level_summaries(lang: str) -> list:
    """The six one-paragraph summaries, taken from the 'summary of levels' section of the source."""
    text = (ROOT / "content" / "v2.1" / f"{lang}.md").read_text(encoding="utf-8")
    sections = re.split(r"^## ", text, flags=re.M)
    summary = sections[3]  # title, origin, scale, summary, description, references
    levels = []
    for match in re.finditer(r"^\*\*(.+?)\*\*:\s*(.+)$", summary, re.M):
        title = LEVEL_TITLE.match(match.group(1))
        if not title:
            continue
        number = int(title.group(1) or title.group(2))
        description = markdown.markdown(match.group(2).strip()).removeprefix("<p>").removesuffix("</p>")
        levels.append({"number": number, "title": title.group(3).strip(), "html": description})
    assert [level["number"] for level in levels] == list(range(6)), f"{lang}: six level summaries expected"
    return levels

GUIDES = {lang: json.loads((ROOT / "data" / "guide" / f"{lang}.json").read_text()) for lang in LANGUAGES}
QUICKREF = {lang: json.loads((ROOT / "data" / "quickref" / f"{lang}.json").read_text()) for lang in LANGUAGES}
LEVELS = {lang: level_summaries(lang) for lang in LANGUAGES}

env = Environment(undefined=StrictUndefined, loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))

def share_link(lang: str, level: int, tag: str = "a") -> str:
    """Share control for a level: an anchor to the shareable URL, or a button on the page it opens."""
    label = f'{UI[lang]["share_level"]} ({UI[lang]["level_word"]} {level})'
    link = f"{BASE_URL}/{lang}/?nivel={level}"
    href = f' href="{link}"' if tag == "a" else f' type="button" data-share-url="{link}"'
    return (f'<{tag} class="share-level"{href} data-share-level="{level}" data-copied="{UI[lang]["link_copied"]}" '
            f'title="{label}" aria-label="{label}">{SHARE_ICON}</{tag}>')

def heading_ids(html: str, lang: str) -> str:
    """Gives the framework's headings the same anchors in every language (#nivel-N, #origen...),
    so a link to a section works whatever the language, and adds the share control to each level."""
    def add_id(match: re.Match) -> str:
        inner = match.group(1)
        plain = re.sub(r"<[^>]+>", "", inner)
        number = re.search(r"(?:Nivel|Nivell|Level)\s+([0-5])|([0-5])\.\s*maila", plain, re.I)
        if not number:
            return match.group(0)
        level = number.group(1) or number.group(2)
        return f'<h3 id="nivel-{level}"><span>{inner}</span>{share_link(lang, int(level))}</h3>'
    html = re.sub(r"<h3>(.*?)</h3>", add_id, html)
    # Stable anchors across translations; the first h3 is the classification section.
    html = re.sub(r"<h3>", '<h3 id="clasificar">', html, count=1)
    section_ids = iter(["origen", "escala", "resumen", "descripcion", "referencias"])
    return re.sub(r"<h2>", lambda _: f'<h2 id="{next(section_ids)}">', html)

def build_page(lang: str) -> str:
    """The full framework in one language, from content/v2.1/<lang>.md."""
    source = ROOT / "content" / "v2.1" / f"{lang}.md"
    text = source.read_text(encoding="utf-8")
    html_content = markdown.markdown(text, extensions=["extra", "sane_lists"])
    html_content = heading_ids(html_content, lang)
    title = re.sub(r"^#\s+", "", text.splitlines()[0])
    return env.get_template("page.html").render(
        lang=lang, page_title=f"{title} · MIAE", description=DESCRIPTIONS[lang],
        canonical=f"{BASE_URL}/v2.1/{lang}/", base_url=BASE_URL, root="../../",
        languages=LANGUAGES, ui=UI[lang], guide=GUIDES[lang], content=html_content,
        license_lang=lang if lang in {"es", "ca"} else "en", range=range,
    )

def main() -> None:
    """Writes every page, and the PDFs with --pdf. Languages without a framework text are skipped."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", action="store_true", help="Generate the five downloadable PDF editions")
    args = parser.parse_args()
    def build_home(lang, root_path, automatic=False):
        return env.get_template("home.html").render(
            lang=lang, ui=UI[lang], guide=GUIDES[lang], description=DESCRIPTIONS[lang],
            languages=LANGUAGES, range=range, root=root_path, levels=LEVELS[lang],
            share_button=lambda level: share_link(lang, level, "button"),
            base_url=BASE_URL, automatic=automatic,
            license_lang=lang if lang in {"es", "ca"} else "en",
        )
    def build_quickref(lang):
        return env.get_template("quickref.html").render(
            lang=lang, ui=UI[lang], qr=QUICKREF[lang], languages=LANGUAGES,
            description=DESCRIPTIONS[lang], root="../../", base_url=BASE_URL,
        )
    def build_tools(lang):
        return env.get_template("tools.html").render(
            lang=lang, ui=UI[lang], guide=GUIDES[lang], languages=LANGUAGES,
            root="../../", base_url=BASE_URL,
            license_lang=lang if lang in {"es", "ca"} else "en",
        )
    (ROOT / "index.html").write_text(build_home("es", "./", True), encoding="utf-8")
    for lang in LANGUAGES:
        home_dir = ROOT / lang
        home_dir.mkdir(exist_ok=True)
        (home_dir / "index.html").write_text(build_home(lang, "../"), encoding="utf-8")
        tools_dir = home_dir / "ficha"
        tools_dir.mkdir(exist_ok=True)
        (tools_dir / "index.html").write_text(build_tools(lang), encoding="utf-8")
        quickref_dir = home_dir / "guia"
        quickref_dir.mkdir(exist_ok=True)
        quickref_page = quickref_dir / "index.html"
        quickref_page.write_text(build_quickref(lang), encoding="utf-8")
        if args.pdf:
            pdf_dir = ROOT / "output" / "pdf"
            pdf_dir.mkdir(parents=True, exist_ok=True)
            HTML(filename=str(quickref_page)).write_pdf(pdf_dir / f"miae-v2.1-guia-{lang}.pdf")
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
