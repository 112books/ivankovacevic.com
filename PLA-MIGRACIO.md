# Pla de migració — ivankovacevic.com (WordPress → Hugo)

> Pla d'execució pas a pas per a un agent d'IA (Claude Code o similar).
> Base: projecte `../bratiamusic` (Hugo multilingüe, Decap CMS, GoatCounter).
> Creat: 2026-10-14. Marca [x] cada pas quan estigui fet.

## 0. Context

| Entorn | URL / ruta | Funció |
|---|---|---|
| Local | `/Users/joan/Documents/Obsidian/ivankovacevic.com` → `http://localhost:1313/ivankovacevic.com/` | Treball (casa i estudi) |
| Repositori | `github.com/112books/ivankovacevic.com` | Control de versions |
| Staging | `https://112books.github.io/ivankovacevic.com/` | Proves (noindex) |
| Producció | `https://ivankovacevic.com/` | Avui WordPress allotjat per LinuxBCN; es substitueix al final |

Web actual (WordPress, ES per defecte + EN amb un plugin multilingüe; plugin d'esdeveniments The Events Calendar):
- Agenda `/events/list/` · Biografía `/ivan-kovacevic-biografia/` · Discografía `/discografia/`
- Proyectos `/category/proyectos/` · Noticias `/category/noticias/` · Vídeos `/videos/`
- `/ivan-kovacevic-sobre-daddario/` · Contacto `/contacto/` · versió EN `/en/...`
- Projectes: Bratia, Bernat Font Trio, 5 Spots, Barcelona Big Blues Band, Barcelona Gipsy Klezmer Orchestra, Los Mambo Jambo; altres: Lazy Jumpers, The Nu Niles, Down Home.
- 9 vídeos YouTube, Instagram/Facebook/YouTube al peu, banner de galetes (Site Kit de Google).

## 1. Decisions (resoltes 2026-10-14)

| Tema | Decisió |
|---|---|
| Idiomes | **EN** (principal, per defecte) · **CA** · **ES** · **SR** (serbi en alfabet llatí, `sr-Latn`) |
| Repositori | **Públic** a `112books/ivankovacevic.com` → GitHub Pages gratuït. Cap secret al codi. |
| Comptes Google (Calendar, llista YouTube, àlbums Fotos) | Propietat del compte de **Joan / LinuxBCN**, compartits amb l'Ivan |
| Edició | **L'Ivan edita via CMS** → necessita compte GitHub i accés de col·laborador |
| Producció | **Servidor propi de LinuxBCN**. Host, usuari SSH i docroot: **pendents**, en Joan els donarà. No bloqueja res fins al pas 11. |
| Identitat visual | **Pròpia, diferent de Bratia**: mateixa estructura, colors i tipografia nous, logo tipogràfic provisional |

Notes que se'n deriven:
- Serbi: traducció automàtica inicial marcada com a esborrany; **l'Ivan l'ha de revisar** abans de publicar (anotar-ho a PENDENTS.md). Tipografia amb diacrítics `č ć š ž đ` (la majoria de Google Fonts llatines extended els tenen; comprovar-ho).
- Com que l'idioma per defecte passa a ser l'anglès, **totes** les URL espanyoles antigues del WP (que eren a l'arrel) han de redirigir a `/es/...` (pas 4).
- Nom amb diacrític: "Ivan Kovačević" als textos i al schema; el domini i els slugs, sense (`kovacevic`).

## 2. Crear el projecte local a partir de bratiamusic

La carpeta ja existeix amb `git init` (branca `master`, sense commits) i `.taques/`. No clonar l'historial de bratiamusic: copiar fitxers.

- [ ] Copiar sense historial ni artefactes:
  ```bash
  cd /Users/joan/Documents/Obsidian
  rsync -av \
    --exclude='.git' --exclude='.taques' --exclude='.taques-central' \
    --exclude='public' --exclude='resources' --exclude='.DS_Store' \
    --exclude='.hugo_build.lock' --exclude='PENDENTS.md' --exclude='_CLAUDE.md' \
    --exclude='static/data/analytics.json' --exclude='static/d7d7ec00a39c4c4c82b133da9aaeda28.txt' \
    --exclude='.obsidian/workspace*' \
    bratiamusic/ ivankovacevic.com/
  cd ivankovacevic.com && git branch -m master main
  ```
- [ ] Buscar i substituir totes les referències a Bratia:
  `grep -rniI "bratia" --exclude-dir=.git .` → hugo.toml, config/*, layouts/partials/seo.html (schema MusicGroup → **Person** amb `jobTitle` "Contrabaixista"), footer, i18n, static/llms.txt, humans.txt, site.webmanifest, static/cms/config.yml, sync-web.sh, workflows, .htaccess.
- [ ] `config/local/hugo.toml` → `baseURL = "http://localhost:1313/ivankovacevic.com/"`
- [ ] `config/staging/hugo.toml` → `baseURL = "https://112books.github.io/ivankovacevic.com/"`, `noindex = true`, `canonicalBaseURL = "https://ivankovacevic.com/"`
- [ ] `config/production/hugo.toml` → `baseURL = "https://ivankovacevic.com/"`; generar **nova** clau IndexNow (no reutilitzar la de Bratia).
- [ ] `hugo.toml`: `defaultContentLanguage = "en"`, `defaultContentLanguageInSubdir = true`, quatre idiomes amb `contentDir`: `content/en` (weight 1), `content/ca` (2), `content/es` (3), `content/sr` (4, `languageCode = "sr-Latn"`, `label = "Srpski"`).
- [ ] Crear `i18n/sr.toml` (copiar `i18n/en.toml` i traduir) i `content/sr/`. Comprovar que el `lang-switcher` mostra els 4 idiomes i que els hreflang surten com `en`, `ca`, `es`, `sr-Latn`.
- [ ] Al CMS, duplicar les col·leccions per a EN/CA/ES/SR (o usar el mode `i18n` de Decap amb `structure: multiple_folders`).
- [ ] Menú nou als 4 idiomes (EN: Home · Biography · Projects · Discography · Gigs · Videos · Photos · News · Contact). Slugs **traduïts** per SEO (`/es/biografia/`, `/ca/biografia/`, `/sr/biografija/`), amb `translationKey`. D'Addario va com a notícia o dins Biografia.
- [ ] Afegir **Fotografías** al menú (secció que el WP no tenia).
- [ ] Netejar contingut de Bratia a `content/`, `data/`, `static/images/` (deixar l'estructura, buidar els textos).
- [ ] Identitat visual pròpia (secció 1): nova paleta i tipografia (font lliure, Google Fonts o autoallotjada, amb llatí extended), logo tipogràfic provisional "Ivan Kovačević — double bass". Substituir totes les imatges de fons de Bratia. Regenerar favicons i `site.webmanifest`.
- [ ] Comprovar: `hugo server --environment local` sense errors ni avisos.

## 2b. Fonts externes: YouTube, Google Calendar, Google Fotos

Bratia s'alimenta de tres fonts externes via workflows nocturns. Per a l'Ivan cal crear-les o localitzar-les. Les tasques marcades **(Joan)** són manuals: l'agent no té accés als comptes de Google.

**YouTube**
- [ ] Localitzar el canal de l'Ivan: enllaç de YouTube al peu de ivankovacevic.com i a la pàgina `/videos/`. Treure'n l'ID `UC...` (a l'HTML del canal, `"channelId"` o `<link rel="canonical">`).
- [ ] Si no té canal propi (els 9 vídeos poden ser de bandes diferents): **(Joan)** crear una **llista de reproducció** pública al compte de Joan/LinuxBCN i fer servir l'URL de la llista. Si en té, millor el seu canal.
- [ ] Adaptar `.github/workflows/fetch-videos.yml`: substituir `https://www.youtube.com/channel/UCXqrXtF9DiXVmfB4X8RX6gA/videos` (Bratia) pel canal o la llista de l'Ivan; `scripts/process-youtube.py` es manté.
- [ ] Guardar l'URL a `data/social.yaml` (camp `youtube`).

**Google Calendar (agenda)**
- [ ] **(Joan)** Crear el calendari "Ivan Kovačević – Gigs" al compte Google de Joan/LinuxBCN; Configuració → *Fes-lo públic* → copiar l'**adreça pública en format iCal** (`.../public/basic.ics`).
- [ ] **(Joan)** Compartir-lo amb l'Ivan amb permís "Fer canvis als esdeveniments" si ell hi ha d'afegir concerts.
- [ ] Format de cada esdeveniment (perquè `scripts/process-concerts.py` ho llegeixi bé): títol = nom del projecte/banda + sala; *Ubicació* = adreça completa; descripció amb l'enllaç d'entrades a la primera línia. Confirmar-ho llegint el script abans de fixar-ho.
- [ ] Migrar-hi els concerts futurs del WordPress (endpoint `tribe/events/v1/events` del pas 3); els passats van a `data/concerts-archive.yaml`.
- [ ] Adaptar `.github/workflows/fetch-concerts.yml`: substituir l'URL `.ics` de Bratia per la nova. Recomanable passar-la a variable del repo (`vars.CALENDAR_ICS_URL`) en lloc de deixar-la al YAML.
- [ ] Mantenir el partial `calendar-subscribe.html` (botó "Subscriu-te a l'agenda") amb la nova URL.

**Google Fotos (galeries)**
- [ ] **(Joan)** Crear, al compte de Joan/LinuxBCN, un o més **àlbums compartits** a Google Fotos (p. ex. "Ivan Kovačević – Retrats", "– En directe"); *Compartir → Crear enllaç* (`https://photos.app.goo.gl/...`).
- [ ] Omplir `data/galleries.yaml` amb el mateix format que Bratia: `id`, `title` (es/en), `date`, `author`, `author_url`, `url`. El camp `cover` l'omple `fetch-galleries.yml` automàticament.
- [ ] Revisar `fetch-galleries.yml` (no té URLs fixes de Bratia; només llegeix `data/galleries.yaml`).
- [ ] Fotos de premsa d'alta resolució: a part, en un ZIP descarregable des de Contacte (no des de Google Fotos).

**Verificació**
- [ ] Executar els tres workflows amb `gh workflow run ...` i comprovar que generen `static/data/videos.json`, el `.ics`/`concerts-schema.json` i les portades de galeries sense errors.

## 3. Migrar continguts del WordPress

El WP exposa l'API REST; extreure-ho amb un script (`scripts/import-wp.py`), no a mà.

- [ ] Descarregar a `_import/` (no versionat, afegir a `.gitignore`):
  - Pàgines: `https://ivankovacevic.com/wp-json/wp/v2/pages?per_page=100`
  - Entrades: `.../wp-json/wp/v2/posts?per_page=100&_embed` (categories Proyectos / Noticias)
  - Categories: `.../wp-json/wp/v2/categories`
  - Mèdia: `.../wp-json/wp/v2/media?per_page=100` (paginar amb `&page=N`)
  - Esdeveniments: `.../wp-json/tribe/events/v1/events?per_page=100&start_date=2000-01-01`
  - Idioma: si l'API no separa ES/EN, provar `?lang=en`.
  - Si l'API està tancada: exportació WXR des de l'escriptori de WP (Eines → Exporta) i convertir-la.
- [ ] El contingut del WP és ES (i part EN): importar-lo a `content/es` i `content/en`. CA i SR es tradueixen a partir de l'EN/ES; marcar-los `draft: false` només després de revisió.
- [ ] Convertir HTML → Markdown (pandoc o `markdownify`), front matter Hugo: `title`, `date`, `slug`, `translationKey`, `aliases` (URL antiga), `images`.
- [ ] Mapatge de seccions:
  | WordPress | Hugo |
  |---|---|
  | Biografía | `content/{es,en}/biografia/_index.md` |
  | Discografía | `data/discography.yaml` + layout (reutilitzar `layouts/discography`), agrupat per banda |
  | Proyectos (categoria) | `content/{es,en}/proyectos/<slug>.md` (una fitxa per banda, enllaç extern) |
  | Noticias (categoria) | `content/{es,en}/noticias/<any>-<slug>.md` |
  | Vídeos | reutilitzar `layouts/videos`, alimentat pel canal/llista de YouTube del pas 2b |
| Fotografies (nova secció) | reutilitzar `layouts/photos` + `data/galleries.yaml` (pas 2b) |
  | Agenda | reutilitzar `layouts/concerts`, alimentat pel Google Calendar del pas 2b |
  | Contacto | `content/{es,en}/contacto/` + `data/contact.yaml` |
  | Legal | adaptar `content/*/legal` amb titular Ivan Kovačević; **sense banner de galetes** (GoatCounter no en fa servir) |
- [ ] Imatges: descarregar els originals de `/wp-content/uploads/` (no les miniatures `-300x200`), a `static/images/` o page bundles; convertir a WebP i redimensionar amb Hugo image processing.
- [ ] Revisar a mà textos, accents i enllaços trencats (`htmltest` o `lychee` sobre `public/`).

## 4. Redireccions de les URL antigues

Imprescindible per no perdre SEO.

- [ ] Llistat complet d'URL antigues: `https://ivankovacevic.com/wp-sitemap.xml` (o el sitemap de Site Kit/Yoast).
- [ ] Generar `static/.htaccess` amb `Redirect 301` per a cada URL que canviï, p. ex.:
  ```apache
  # L'arrel antiga era ES; ara l'arrel és EN → tot el contingut ES antic va a /es/
  Redirect 301 /ivan-kovacevic-biografia/ /es/biografia/
  Redirect 301 /events/list/ /es/agenda/
  Redirect 301 /category/proyectos/ /es/proyectos/
  Redirect 301 /category/noticias/ /es/noticias/
  Redirect 301 /en/next-shows-2/ /en/agenda/
  RedirectMatch 301 ^/wp-content/uploads/(.*)$ /images/wp/$1
  RedirectMatch 410 ^/(wp-admin|wp-login\.php|xmlrpc\.php)
  ```
- [ ] A més, `aliases` al front matter (serveix per a GitHub Pages, que ignora .htaccess).
- [ ] Reaprofitar de Bratia els headers de seguretat (HSTS, CSP...), canviant el domini GoatCounter al `connect-src`.

## 5. Repositori GitHub

- [ ] `gh repo create 112books/ivankovacevic.com --public --source=. --remote=origin`
- [ ] Revisar `.gitignore`: `public/`, `resources/`, `.hugo_build.lock`, `_import/`, `.DS_Store`, `.obsidian/workspace*`, `.env`
- [ ] Comprovar que no hi ha cap secret: `grep -rniE "token|secret|password|ssh-" --exclude-dir=.git .`
- [ ] Primer commit a `main` i push.

## 6. GitHub Pages (staging)

Bratia NO té Pages: el `build.yml` només valida. Aquí n'hi cal un de nou.

- [ ] Crear `.github/workflows/pages.yml`: checkout (`fetch-depth: 0`) → Hugo extended 0.166.0 → `hugo --minify --environment staging` → `npx pagefind --site public` → `actions/upload-pages-artifact` → `actions/deploy-pages`. Permisos: `pages: write`, `id-token: write`. Disparadors: push a `main` + `workflow_dispatch`.
- [ ] `gh api -X POST repos/112books/ivankovacevic.com/pages -f build_type=workflow`
- [ ] Verificar `https://112books.github.io/ivankovacevic.com/`: CSS, imatges, canvi d'idioma (vigilar la subruta; usar `relURL`/`absURL`, i la regla de `site.Menus` del _CLAUDE.md de Bratia).
- [ ] Verificar `<meta name="robots" content="noindex">` a staging.
- [ ] Workflows heretats de Bratia (`fetch-concerts`, `fetch-galleries`, `fetch-videos`, `fetch-analytics`): adaptar els que calguin i **esborrar** la resta. Tots amb `git pull --rebase` abans del push.

## 7. CMS (Decap)

- [ ] `static/cms/config.yml`: `repo: 112books/ivankovacevic.com`, `branch: main`, `locale: "es"`, col·leccions noves: Biografía, Proyectos, Noticias, Discografía (data), Agenda (si és data/), Vídeos, Contacto, Redes sociales. Mantenir `editorial_workflow`.
- [ ] Autenticació — reutilitzar el proveïdor existent `cms-oauth-bratia` (Vercel, `https://cms-oauth-bratia-y855.vercel.app`):
  - L'OAuth App de GitHub dona accés a tots els repos on l'usuari té permís, per tant serveix per a aquest repo.
  - Afegir `112books.github.io` i `ivankovacevic.com` a la variable `ORIGINS` de Vercel (si n'hi ha) i redesplegar.
  - Alternativa si es vol aïllar: nou desplegament `cms-oauth-ivan` amb una OAuth App nova.
- [ ] Provar el login i un canvi real a `/cms/` tant a staging com, al final, a producció.
- [ ] Demanar a l'Ivan el seu usuari de GitHub (o ajudar-lo a crear-ne un) i afegir-lo com a col·laborador amb permís `write`: `gh api -X PUT repos/112books/ivankovacevic.com/collaborators/<usuari> -f permission=push`.
- [ ] Escriure una mini guia d'ús del CMS per a l'Ivan (en anglès o castellà) a `docs/cms-guide.md`.

## 8. Estadístiques (GoatCounter + goatcounter-dashboard)

- [ ] Crear compte `ivankovacevic.goatcounter.com` (en Joan, manual) i generar token d'API.
- [ ] Al web: el partial `layouts/partials/analytics/` amb el codi de seguiment **només a `baseof.html`** i només a l'entorn `production` (no comptar staging ni local).
- [ ] Al repo `goatcounter-dashboard`:
  - [ ] Nou `config/ivankovacevic.com.yaml` copiant `config/llumatics.com.yaml`.
  - [ ] Secret `GOATCOUNTER_TOKEN_IVANKOVACEVIC` (`gh secret set`).
  - [ ] Afegir el site a `fetch-analytics.yml` i `weekly-agent.yml` (seqüencial, no en paral·lel).
  - [ ] Actualitzar la llista d'instàncies al seu CLAUDE.md.
- [ ] Al web: pàgina `/admin/` (reutilitzar `layouts/admin` de Bratia) que enllaci el CMS i el dashboard; treure el dashboard propi de Bratia (`fetch-analytics.yml`, `admin/insights`) si es fa servir el central.
- [ ] Eliminar Site Kit / Google Analytics: res de Google al web nou.

## 9. CLAUDE.md i documentació

- [ ] `CLAUDE.md` (a l'arrel), basat en `../bratiamusic/_CLAUDE.md` però curt: URLs dels 4 entorns, stack, comandes, estructura config/, desplegament, CMS, GoatCounter, regles (sense secrets al repo, `site.Menus`, `rm -rf public` abans del build, Hugo local vs CI), convencions de commit (`feat:`/`fix:`/`chore:`), secció "Control horari" igual que a goatcounter-dashboard (`.taques/` append-only).
- [ ] `PENDENTS.md` amb el backlog viu (decisions obertes, material pendent de l'Ivan).
- [ ] `README.md` breu.

## 10. Verificació abans de producció

- [ ] `hugo --minify --environment production` sense errors.
- [ ] Enllaços: `lychee public/` o `htmltest`.
- [ ] Totes les URL del sitemap antic responen 301 → 200 (script que recorri la llista).
- [ ] Lighthouse/PageSpeed a staging (mòbil): rendiment, accessibilitat, SEO.
- [ ] Schema.org (Person + MusicEvent) validat a validator.schema.org.
- [ ] hreflang ES/EN correcte, `sitemap.xml`, `robots.txt`, `llms.txt`.
- [ ] Revisió visual i de textos per part d'en Joan i de l'Ivan.

## 11. Pas a producció

Irreversible si no hi ha còpia: **no fer-ho sense l'OK explícit d'en Joan.**

- [ ] Còpia completa del WordPress actual (fitxers + base de dades) a `/Users/joan/Documents/Obsidian/-backups/ivankovacevic.com-WP-<data>/`.
- [ ] **(Joan)** Facilitar host, usuari SSH i docroot del servidor de LinuxBCN.
- [ ] Adaptar `sync-web.sh` (opció publish): aquestes dades, clau `~/.ssh/ivankovacevic_deploy` (nova, només per a aquest web). `rm -rf public` → build production → pagefind → rsync `--delete --checksum --omit-dir-times`.
- [ ] Primer desplegament a un subdirectori o subdomini de prova al mateix servidor (p. ex. `nou.ivankovacevic.com`) per comprovar `.htaccess` i headers.
- [ ] Canvi: moure el WP fora del docroot (no esborrar-lo) i publicar el Hugo.
- [ ] Comprovacions post-desplegament: `curl -sI https://ivankovacevic.com/` (HSTS, CSP), redireccions, CMS, GoatCounter rebent visites.
- [ ] Google Search Console i Bing Webmaster: enviar `sitemap.xml` nou; IndexNow.
- [ ] Al cap de 2-4 setmanes sense incidències: arxivar definitivament el WordPress.

## Notes per a l'agent

- Treballa sempre en local i fes commits petits; mai push --force.
- No posis credencials al repo ni als fitxers .md.
- Les decisions de la secció 1 ja estan preses; si en sorgeix una de nova, tria l'opció més reversible i anota-la a PENDENTS.md.
- No toquis el repo `bratiamusic`; només se'n copia.
- A `goatcounter-dashboard` i `cms-oauth-bratia` només fes els canvis que diu aquest pla.
