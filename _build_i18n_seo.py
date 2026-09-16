# -*- coding: utf-8 -*-
"""Build English /en/ pages, wire the flag switcher, and add BG-market SEO."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://kehayovsolar.bg"
OG_IMG = f"{SITE}/images/img/16.jpg"
LOGO = f"{SITE}/images/Logo.png"

PAGES = [
    "index.html",
    "about.html",
    "services.html",
    "packages.html",
    "projects.html",
    "contact.html",
    "privacy.html",
    "terms.html",
    "service-grid.html",
    "service-hybrid.html",
    "service-offgrid.html",
    "service-storage.html",
]

SEO = {
    "index.html": {
        "title_bg": "Фотоволтаични системи за дом и бизнес в България | Kehayov Solar",
        "desc_bg": "Проектиране, доставка и монтаж на фотоволтаични системи в цяла България. JinkoSolar панели и Deye инвертори. Оферта след оглед — база гр. Рудозем.",
        "title_en": "Solar PV systems for homes and businesses in Bulgaria | Kehayov Solar",
        "desc_en": "Design, supply and installation of photovoltaic systems across Bulgaria. JinkoSolar panels and Deye inverters. Quote after a site visit — based in Rudozem.",
        "kw": "фотоволтаични системи, соларни панели, монтаж на соларни панели, хибридна система, Deye, JinkoSolar, соларна оферта България, Рудозем",
        "kw_en": "photovoltaic systems Bulgaria, solar panels installation Bulgaria, hybrid solar, Deye, JinkoSolar, solar quote Bulgaria, Rudozem",
    },
    "about.html": {
        "title_bg": "За нас | Соларна фирма от Рудозем | Kehayov Solar",
        "desc_bg": "Kehayov Solar проектира и монтира фотоволтаични системи за дома и бизнеса. Работим от гр. Рудозем и обслужваме клиенти в цяла България.",
        "title_en": "About us | Solar company from Rudozem | Kehayov Solar",
        "desc_en": "Kehayov Solar designs and installs photovoltaic systems for homes and businesses. Based in Rudozem, we work with clients across Bulgaria.",
        "kw": "Kehayov Solar, соларна фирма Рудозем, монтаж фотоволтаици България",
        "kw_en": "Kehayov Solar, solar company Rudozem, photovoltaic installation Bulgaria",
    },
    "services.html": {
        "title_bg": "Услуги | Мрежови, хибридни и автономни ФЕЦ | Kehayov Solar",
        "desc_bg": "Мрежови, хибридни и автономни фотоволтаични системи плюс съхранение (BESS). Конфигурацията се уточнява след оглед на обекта.",
        "title_en": "Services | Grid, hybrid and off-grid solar | Kehayov Solar",
        "desc_en": "Grid-tied, hybrid and off-grid photovoltaic systems plus battery storage (BESS). The configuration is confirmed after a site visit.",
        "kw": "мрежова фотоволтаична система, хибридна система, автономна система, BESS, соларни услуги България",
        "kw_en": "grid-tied solar Bulgaria, hybrid PV, off-grid solar, BESS, solar services Bulgaria",
    },
    "packages.html": {
        "title_bg": "Соларни пакети 5, 10 и 20 kW | Kehayov Solar",
        "desc_bg": "Ориентировъчни системи 5, 10 и 20 kW с JinkoSolar панели и Deye инвертор. Точният състав и цената — след оглед. Работим в цяла България.",
        "title_en": "Solar packages 5, 10 and 20 kW | Kehayov Solar",
        "desc_en": "Typical 5, 10 and 20 kW systems with JinkoSolar panels and a Deye inverter. Final scope and price after a site visit. We work across Bulgaria.",
        "kw": "соларен пакет 5 kW, 10 kW, 20 kW, цена фотоволтаична система, оферта соларни панели",
        "kw_en": "solar package 5 kW, 10 kW, 20 kW, photovoltaic system quote Bulgaria",
    },
    "projects.html": {
        "title_bg": "Реализирани фотоволтаични проекти | Kehayov Solar",
        "desc_bg": "Над 50 реализирани проекта — снимки от реални монтажи за дома и бизнеса в цяла България.",
        "title_en": "Completed photovoltaic projects | Kehayov Solar",
        "desc_en": "50+ completed installations — photos from real home and business solar projects across Bulgaria.",
        "kw": "реализирани соларни проекти, монтаж соларни панели снимки, фотоволтаици България",
        "kw_en": "completed solar projects Bulgaria, solar panel installation photos",
    },
    "contact.html": {
        "title_bg": "Контакт и оферта за фотоволтаична система | Kehayov Solar",
        "desc_bg": "Поискайте оферта или запазете консултация. Телефон +359 87 848 9013, имейл hiki7787@gmail.com. База: гр. Рудозем, клиенти в цяла България.",
        "title_en": "Contact and solar quote | Kehayov Solar",
        "desc_en": "Request a quote or book a consultation. Phone +359 87 848 9013, email hiki7787@gmail.com. Based in Rudozem, clients across Bulgaria.",
        "kw": "оферта соларна система, консултация фотоволтаици, контакт Kehayov Solar Рудозем",
        "kw_en": "solar quote Bulgaria, photovoltaic consultation, Kehayov Solar Rudozem contact",
    },
    "privacy.html": {
        "title_bg": "Политика за поверителност | Kehayov Solar",
        "desc_bg": "Как Kehayov Solar обработва лични данни по GDPR и ЗЗЛД — цели, срокове и вашите права.",
        "title_en": "Privacy policy | Kehayov Solar",
        "desc_en": "How Kehayov Solar processes personal data under the GDPR — purposes, retention and your rights.",
        "kw": "политика за поверителност, GDPR, лични данни",
        "kw_en": "privacy policy, GDPR, personal data Kehayov Solar",
    },
    "terms.html": {
        "title_bg": "Общи условия | Kehayov Solar",
        "desc_bg": "Правила за ползване на сайта, запитвания и преддоговорни отношения с Kehayov Solar.",
        "title_en": "Terms of use | Kehayov Solar",
        "desc_en": "Rules for using the website, enquiries and pre-contract communication with Kehayov Solar.",
        "kw": "общи условия, запитване, оферта",
        "kw_en": "terms of use, enquiry, solar quote Bulgaria",
    },
    "service-grid.html": {
        "title_bg": "Мрежови фотоволтаични системи | Kehayov Solar",
        "desc_bg": "Мрежова ФЕЦ със връзка към електроразпределителната мрежа. Собствено производство без задължителна батерия. Оферта след оглед.",
        "title_en": "Grid-tied photovoltaic systems | Kehayov Solar",
        "desc_en": "Grid-tied solar that produces power by day and uses the grid when needed. A battery is optional. Quote after a site visit.",
        "kw": "мрежова фотоволтаична система, on-grid, соларна система с мрежа",
        "kw_en": "grid-tied photovoltaic system Bulgaria, on-grid solar installation",
    },
    "service-hybrid.html": {
        "title_bg": "Хибридни фотоволтаични системи | Kehayov Solar",
        "desc_bg": "Хибридна система с Deye инвертор и опция за батерия — повече контрол върху собствената енергия. Работим в цяла България.",
        "title_en": "Hybrid photovoltaic systems | Kehayov Solar",
        "desc_en": "Hybrid solar with a Deye inverter and optional battery — more control over your own energy. We work across Bulgaria.",
        "kw": "хибридна фотоволтаична система, Deye инвертор, соларна батерия",
        "kw_en": "hybrid photovoltaic system Bulgaria, Deye inverter, solar battery",
    },
    "service-offgrid.html": {
        "title_bg": "Автономни фотоволтаични системи | Kehayov Solar",
        "desc_bg": "Автономна (off-grid) система когато няма надеждна мрежа или целта е независимост. Оразмеряване след оглед.",
        "title_en": "Off-grid photovoltaic systems | Kehayov Solar",
        "desc_en": "Off-grid solar when the grid is missing or independence is the goal. Sized after a site visit.",
        "kw": "автономна фотоволтаична система, off-grid, соларна система без мрежа",
        "kw_en": "off-grid photovoltaic system Bulgaria, autonomous solar",
    },
    "service-storage.html": {
        "title_bg": "Системи за съхранение на енергия (BESS) | Kehayov Solar",
        "desc_bg": "Deye батерии към нова или съществуваща фотоволтаична система. Съхранение само когато има смисъл за обекта.",
        "title_en": "Battery energy storage systems (BESS) | Kehayov Solar",
        "desc_en": "Deye batteries for a new or existing PV system. Storage only when it makes sense for the site.",
        "kw": "BESS, соларна батерия, Deye батерия, съхранение на енергия",
        "kw_en": "BESS Bulgaria, solar battery, Deye battery, energy storage",
    },
}


def local_business(lang: str) -> dict:
    is_bg = lang == "bg"
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{SITE}/#business",
        "name": "Kehayov Solar",
        "url": SITE,
        "logo": LOGO,
        "image": OG_IMG,
        "telephone": "+359878489013",
        "email": "hiki7787@gmail.com",
        "priceRange": "$$",
        "description": SEO["index.html"]["desc_bg" if is_bg else "desc_en"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Рудозем" if is_bg else "Rudozem",
            "addressRegion": "Смолян" if is_bg else "Smolyan",
            "addressCountry": "BG",
        },
        "areaServed": {"@type": "Country", "name": "България" if is_bg else "Bulgaria"},
        "geo": {"@type": "GeoCoordinates", "latitude": 41.487, "longitude": 24.849},
        "knowsLanguage": ["bg", "en"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Фотоволтаични системи" if is_bg else "Photovoltaic systems",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Мрежови фотоволтаични системи" if is_bg else "Grid-tied photovoltaic systems"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Хибридни фотоволтаични системи" if is_bg else "Hybrid photovoltaic systems"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Автономни фотоволтаични системи" if is_bg else "Off-grid photovoltaic systems"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Системи за съхранение на енергия (BESS)" if is_bg else "Battery energy storage systems (BESS)"}},
            ],
        },
    }


def seo_head(page: str, lang: str) -> str:
    meta = SEO[page]
    if lang == "bg":
        title, desc, keywords = meta["title_bg"], meta["desc_bg"], meta["kw"]
        canonical = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
        locale, locale_alt = "bg_BG", "en_GB"
        prefix = ""
    else:
        title, desc, keywords = meta["title_en"], meta["desc_en"], meta["kw_en"]
        canonical = f"{SITE}/en/{page}"
        locale, locale_alt = "en_GB", "bg_BG"
        prefix = "../"

    bg_url = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
    en_url = f"{SITE}/en/{page}"
    og_type = "website" if page == "index.html" else "article"
    schema = json.dumps(local_business(lang), ensure_ascii=False, indent=2)
    return f"""<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="Kehayov Solar">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="BG-22">
<meta name="geo.placename" content="Rudozem">
<meta name="geo.position" content="41.487;24.849">
<meta name="ICBM" content="41.487, 24.849">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="bg" href="{bg_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{bg_url}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{locale_alt}">
<meta property="og:site_name" content="Kehayov Solar">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:image:alt" content="Photovoltaic installation by Kehayov Solar">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
<link rel="shortcut icon" href="{prefix}images/Logo.png">
<link rel="icon" type="image/png" href="{prefix}images/Logo.png">
<link rel="apple-touch-icon" href="{prefix}images/Logo.png">
<script type="application/ld+json">
{schema}
</script>"""


HEAD_RE = re.compile(
    r'<html lang="[a-z]{2}">\s*<head>[\s\S]*?(?=<link href="(?:\.\./)?css/style\.css")',
)


def inject_seo(html: str, page: str, lang: str) -> str:
    head = seo_head(page, lang)
    new, n = HEAD_RE.subn(head + "\n", html, count=1)
    if n != 1:
        raise RuntimeError(f"SEO head inject failed for {page} ({lang})")
    return new


def wire_bg_lang(html: str, page: str) -> str:
    html = html.replace(
        '<a href="#" hreflang="en" lang="en">',
        f'<a href="en/{page}" hreflang="en" lang="en">',
    )
    return html


def wire_en_lang(html: str, page: str) -> str:
    html = html.replace(
        f'<a class="is-active" href="{page}" hreflang="bg" lang="bg" aria-current="true">',
        f'<a href="../{page}" hreflang="bg" lang="bg">',
    )
    html = html.replace(
        f'<a href="en/{page}" hreflang="en" lang="en">',
        f'<a class="is-active" href="{page}" hreflang="en" lang="en" aria-current="true">',
    )
    html = re.sub(
        r'(<summary[^>]*>[\s\S]*?src=")([^"]*image-icons/)bg\.svg(")',
        r"\1\2uk.svg\3",
        html,
        count=2,
    )
    html = html.replace('alt="Bulgarian"', 'alt="English"')
    html = html.replace('alt="Български"', 'alt="English"')
    return html


def rewrite_en_assets(html: str) -> str:
    for attr in ("href", "src", "data-videomp4"):
        html = re.sub(
            rf'({attr}=")(?!https?:|mailto:|tel:|#|en/)((?:css|js|images)/)',
            rf"\1../\2",
            html,
        )
    html = html.replace('action="mail.php"', 'action="../mail.php"')
    html = html.replace("url('images/", "url('../images/")
    html = html.replace('url("images/', 'url("../images/')
    return html


# Longest phrases first. Keep brand names.
PAIRS = [
]


def load_pairs() -> list[tuple[str, str]]:
    raw = (ROOT / "_i18n_pairs.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    items = [(k, v) for k, v in data.items() if k != v]
    items.sort(key=lambda kv: len(kv[0]), reverse=True)
    return items


def translate(html: str, pairs: list[tuple[str, str]]) -> str:
    for bg, en in pairs:
        if bg in html:
            html = html.replace(bg, en)
    return html


def leftover_cyrillic(html: str) -> list[str]:
    return sorted(set(re.findall(r"[А-Яа-яЁёІіЇїЄєҐґ][^<>]{0,80}", html)))


def append_faq_schema(html: str) -> str:
    html = re.sub(
        r'\n<script type="application/ld\+json">\n\{\n  "@context": "https://schema.org",\n  "@type": "FAQPage"[\s\S]*?</script>',
        "",
        html,
    )
    pairs = re.findall(
        r'kehayov-faq__question">([^<]+)</summary>\s*'
        r'<div class="kehayov-faq__answer">\s*<p>([^<]+)</p>',
        html,
    )
    if not pairs:
        return html
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q.strip(),
                "acceptedAnswer": {"@type": "Answer", "text": a.strip()},
            }
            for q, a in pairs
        ],
    }
    block = (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )
    return html.replace("</head>", block + "</head>", 1)


def write_sitemap() -> None:
    urls = []
    for page in PAGES:
        bg = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
        en = f"{SITE}/en/{page}"
        urls.append((bg, en, "weekly" if page == "index.html" else "monthly", "1.0" if page == "index.html" else "0.8"))
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for bg, en, freq, prio in urls:
        parts += [
            "  <url>",
            f"    <loc>{bg}</loc>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            f'    <xhtml:link rel="alternate" hreflang="bg" href="{bg}"/>',
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{bg}"/>',
            "  </url>",
            "  <url>",
            f"    <loc>{en}</loc>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>0.6</priority>",
            f'    <xhtml:link rel="alternate" hreflang="bg" href="{bg}"/>',
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{bg}"/>',
            "  </url>",
        ]
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://kehayovsolar.bg/sitemap.xml\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    pairs = load_pairs()
    en_dir = ROOT / "en"
    en_dir.mkdir(exist_ok=True)
    leftovers = {}
    for page in PAGES:
        src = ROOT / page
        html = src.read_text(encoding="utf-8")
        html = inject_seo(html, page, "bg")
        html = wire_bg_lang(html, page)
        src.write_text(append_faq_schema(html), encoding="utf-8", newline="\n")

        en = rewrite_en_assets(html)
        en = translate(en, pairs)
        en = inject_seo(en, page, "en")
        en = wire_en_lang(en, page)
        en = append_faq_schema(en)
        (en_dir / page).write_text(en, encoding="utf-8", newline="\n")
        left = leftover_cyrillic(en)
        if left:
            leftovers[page] = left[:40]
        print("OK", page, "leftover", len(left))
    write_sitemap()
    (ROOT / "_i18n_leftover.json").write_text(
        json.dumps(leftovers, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("sitemap + robots written")


if __name__ == "__main__":
    main()
