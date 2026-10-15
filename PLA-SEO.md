# PLA SEO i GEO — ivankovacevic.com

> Objectiu: preservar l'autoritat de l'antic WordPress en la migració a Hugo i maximitzar
> la visibilitat d'Ivan Kovačević i dels seus projectes a cercadors i sistemes d'IA.
> Data: 2026-10-15. Estat: en curs.

## 1. Estat actual

Ja implementat:
- `layouts/partials/seo.html`: `meta description`, canonical, hreflang recíproc + `x-default`,
  Open Graph, Twitter Card i JSON-LD `Person` (enriquit), `BreadcrumbList`,
  `WebSite`+`SearchAction` i `MusicEvent` (agenda).
- Afegit en aquesta tanda: JSON-LD `MusicGroup` (pàgines de projecte) i `MusicAlbum` (fitxes de disc).
- `static/llms.txt` (resum per a IA) — corregit (secció News eliminada; afegida Press).
- `static/robots.txt` **nou**: indexació oberta, `/admin/` i `/daddario/` exclosos,
  bots d'IA permesos explícitament, sitemap declarat.
- `static/.htaccess`: redireccions 301 de l'antic WordPress ampliades, 410 per endpoints WP,
  i capçaleres de seguretat (HSTS, CSP, X-Frame-Options, COOP…).
- Sitemap: `/sitemap.xml` (índex) + `/en|ca|es|sr/sitemap.xml`. L'arrel `/` redirigeix a `/en/`.

## 2. Redireccions 301 (WordPress → Hugo)

Estratègia: **producció és Apache** (LinuxBCN) → `static/.htaccess` amb `RedirectMatch 301`.
Staging (GitHub Pages) és `noindex` i no llegeix `.htaccess`; no cal reproduir-ho allà.

| Origen antic | Destí nou |
|---|---|
| `/discografia/` | `/es/discografia/` |
| `/videos/`, `/contacto/`, `/ivan-kovacevic-biografia/` | `/es/videos/`, `/es/contacto/`, `/es/biografia/` |
| `/aviso-legal/`, `/politica-de-privacidad/`, `/politica-de-cookies/` | `/es/legal/…` |
| `/proximos-conciretos/`, `/proximos-conciertos/` | `/es/conciertos/` |
| `/event/*`, `/events/`, `/events/category/*` | `/es/conciertos/` |
| `/category/proyectos/*`, `/category/slide-es/` | `/es/proyectos/` |
| `/en/category/projects/*`, `/en/category/slide/` | `/en/projects/` |
| `/tag/*`, `/category/noticias/`, `/category/en-los-medios/` | `/es/prensa/` |
| Posts `/2018/05/0[79]/*` i `/2021/04/21/bratia/` | projectes / premsa corresponents |
| `/sitemap_index.xml`, `/wp-sitemap.xml` | `/sitemap.xml` |
| `/feed/`, `/comments/feed/` | `/es/` |
| `/wp-admin/*`, `/wp-login.php`, `/xmlrpc.php`, `/wp-json/*`, `/wp-cron.php`, `/wp-includes/*`, `/author/*` | **410 Gone** |

Pendent de decidir: `/wp-content/uploads/*` (imatges antigues). Ara fan 404. Opcions:
(a) deixar 404; (b) captura 301 a l'apartat corresponent si aporta backlinks. Cal la llista de
fitxers del `wp-sitemap`/DB per mapar-les.

## 3. SEO on-page (pendent)

- [ ] `title` i `meta description` únics i amb longitud correcta per pàgina i idioma (auditar les 4 llengües).
- [ ] `og:image` real i específic per pàgina (ara s'usa el global `images/wp/foto-background.png`).
- [ ] Confirmar `canonicalBaseURL` a `config/production/hugo.toml` (canonical absolut a `ivankovacevic.com`).
- [ ] Decidir si cal RSS/feed (ara no hi ha secció de notícies).
- [ ] Revisar que el 404 personalitzat es desplega correctament (`pages.yml` copia `en/404.html` → `404.html`).

## 4. GEO — alimentar les IA

- [ ] `llms.txt` (fet) + `llms-full.txt` amb l'índex complet (discografia amb any/tipus/format,
      projectes, biografia) en text pla i enllaços canònics.
- [x] `robots.txt` amb política explícita per a GPTBot, ClaudeBot, PerplexityBot,
      Google-Extended, Applebot-Extended, CCBot, etc. (permesos).
- [ ] Contingut citable: cada fitxa de disc ja porta any i tipus en text; valorar afegir formats
      (CD/EP/7") i formació perquè les IA puguin extreure dades sense imatge.
- [ ] Entitats coherents: reutilitzar `@id` de `Person` a `MusicAlbum`/`MusicGroup` i
      mantenir `sameAs` amb els perfils oficials.
- [ ] Renderitzat sense JS: discografia i projectes ja són HTML; l'agenda i els vídeos depenen de
      `concerts.json`/`videos.json` → afegir `<noscript>` o SSR parcial de l'agenda.

## 5. Sitemaps i alta a cercadors (Joan, amb accés als comptes)

1. **Google Search Console**: afegir la propietat de domini `ivankovacevic.com` (verificació DNS TXT).
   Enviar `https://ivankovacevic.com/sitemap.xml`.
2. **Bing Webmaster Tools**: importar des de GSC o verificar; enviar el mateix sitemap.
3. **Comprovacions**: `robots.txt` i sitemap accessibles; revisar «Cobertura» per 404/301 inesperats.
4. Mantenir el WordPress en producció fins que els 301 estiguin desplegats i verificats.
5. Sol·licitar reindexació de les URLs clau (home, biografia, discografia, projectes, agenda).

## 6. Verificació

- [ ] `curl -I` de les URLs antigues clau → 301 correctes.
- [ ] `curl -I` dels endpoints WP → 410.
- [ ] Rich Results Test de Google per Person/MusicGroup/MusicAlbum/MusicEvent/Breadcrumb.
- [ ] hreflang recíproc a les 4 llengües (x-default = EN).
- [ ] Sitemap sense errors a GSC i Bing.
- [ ] Core Web Vitals / PageSpeed.
- [ ] `llms.txt` i `llms-full.txt` vàlids i accessibles.

## 7. Ordre d'execució

1. Redireccions 301 + `robots.txt` + `llms.txt` (fet en aquesta tanda).
2. `llms-full.txt` + `<noscript>` de l'agenda.
3. Metas i `og:image` únics per pàgina.
4. Desplegament a producció (`sync-web.sh publish`) i alta a GSC/Bing.

## 8. Inventari d'URLs antigues (font: sitemap Yoast de producció)

- `post-sitemap.xml`: 18 URLs (posts 2018/2021).
- `page-sitemap.xml`: 16 URLs (pàgines).
- `tribe_events-sitemap.xml`: 71 URLs (`/event/*`).
- `category-sitemap.xml`: 10, `post_tag-sitemap.xml`: 4, `tribe_events_cat-sitemap.xml`: 3.

Total: 122 URLs inventariades i cobertes per les regles de la secció 2.
