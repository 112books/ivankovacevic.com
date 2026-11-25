# PENDENTS — ivankovacevic.com

Web oficial del contrabaixista Ivan Kovačević. Actualitzat 2026-10-20.

## Fet
- Scaffold complet multi-idioma (EN/CA/ES/SR), disseny C (dark folk), CMS Decap.
- Automatització: `data/sources.yaml` + `scripts/sync-agenda.py` (iCal + **Bandsintown**) i
  `scripts/sync-videos.py` (canals + **destacats garantits**). Workflows nocturns.
  Notícies **eliminades** del projecte.
- Contingut: biografia (4 idiomes), 9 projectes (4 idiomes), discografia (25 entrades × 4),
  premsa (4 idiomes), legal (4 idiomes, amb GoatCounter i tercers).
- Pàgines legals reescrites; homepage arreglada (marquee eliminat, h1 sr-only, títol localitzat).
- Mitjans WP conservats a `media-archive/wp-uploads/` (50 fitxers; **no publicats**).
- **D'Addario**: pàgina pròpia als 4 idiomes (**noindex**, fora del sitemap), sense enllaç al peu.
  El bloc `params.sponsors` del peu queda desactivat per si torna a ser espònsor.
- **Icones de navegació**: contacte → sobre; premsa → diari.
- **Agenda**: afegit Bandsintown (Barcelona Big Blues Band, BGKO, Bratia). Bratia via Google iCal.
- **Enllaços de plataforma per projecte**: `data/project-links.yaml` (Spotify/Apple/Bandcamp/YouTube/
  Bandsintown/web) renderitzats a `layouts/projects/single.html`.
- **Gigs**: es mostra el projecte/banda (`X-PERFORMER`) a la llista i al detall.
- **Cercador arreglat**: la ruta del bundle de Pagefind era absoluta (`/pagefind/…`) i trencava sota
  subpath (staging/local); ara usa `relURL`. Pàgina de cerca exclosa de l'índex.
- **Accessibilitat**: el menú mòbil tancat i la nav compacta oculta ja no són enfocables (`visibility`).
- **Responsive**: tret el scroll horitzontal de la pàgina de gigs (`overflow-wrap` a la descripció).
- **Nav compacta mòbil**: logo ocult ≤480px i icones redistribuïdes (`space-evenly`).
- **Gigs**: fons vertical propi (`static/images/wp/gigs-bg.jpg`) sobre el degradat fosc.
- **Discografia — línia temporal**: per any (nou→vell) amb traçat de la línia en scroll, any
  «sticky» i revelat d'entrades (CSS + `static/js/timeline.js`, respecta `prefers-reduced-motion`);
  anys omplerts de 14 entrades, 11 al grup «Any desconegut».
- **Fotografies**: 53 galeries/cròniques del blog de Joan Linux a `data/galleries.yaml`,
  amb portada autoallotjada a `static/images/galleries/` (`scripts/fetch-gallery-covers.py`,
  800 px JPEG), ordenades de més nova a més vella, amb CTA i18n propi (`view_chronicle`) i
  fallback de títol. Les portades **no** s'enllacen en calent: blog.pocallum.cat envia
  `Cross-Origin-Resource-Policy: same-site` i el navegador bloquejava les miniatures
  (`ERR_BLOCKED_BY_RESPONSE.NotSameSite`). El workflow nocturn `fetch-galleries.yml` ara
  executa l'script (abans hi tornava a posar URLs externes cada nit).
- **Fonts**: `static/css/fonts.css` i `fonts-c.css` tenien `/ivankovacevic.com/fonts/…`
  hardcodejat — funcionava a staging però donava **404 a producció** (es perdien Oswald i
  Source Serif 4). Ara `../fonts/`, que resol bé als dos entorns.
- **Repàs complet (2026-10-20)**: 302 enllaços interns i 113 imatges (0 errors), 17 pàgines
  auditades al navegador (0 imatges trencades, 0 errors de consola, 0 respostes 4xx), galeria
  a 390 px sense scroll horitzontal, sitemap/robots/llms/RSS, 404 i les 47 redireccions 301
  antigues verificades.
- **Discografia**: BGKO (`Imbarca`, `Europa cierra la frontera`, `Nova Era`, `7`), anys de Bernat
  Font Trio verificats (2011-2014), Lazy Jumpers, The Nu Niles i EPS de B4 (2021/2025); enllaços
  Apple Music verificats via API d'iTunes; JSON-LD `MusicGroup`/`MusicAlbum`.
- **Vídeos**: dates reals de YouTube (105/105) i ordre global més nou→més vell (`videos.json`,
  `sync-videos.py`, `videos.js`).
- **SEO/GEO**: `layouts/robots.txt` ampliat (bots d'IA permesos), `static/llms.txt` corregit,
  `llms-full.txt` generat, `og:image` per pàgina, `<noscript>` a l'agenda i redireccions 301 de
  l'antic WordPress (122 URLs) a `static/.htaccess`. Pla a `PLA-SEO.md`.
- **Disseny (aprovat per Joan)**: fons de cerca (`search-bg.jpg`), banner a tot l'ample a projectes
  (`projects-hero.jpg`) i fons atenuat a les pàgines legals (`legal-bg.jpg`).
- **Crèdits i panell**: fotos de Joan Linux (@pocallum) al peu (excepte signades i portades);
  `/ca/admin/` i `/ca/admin/insights/` operatius; accés a CMS i estadístiques a `ACCES.md`.
- **Seguretat**: auditoria de producció (`SEGURETAT.md`); restes WP (`wp-content`) eliminades i
  bloquejades amb 410; IndexNow afegit al desplegament.
- **SEO/GEO**: JSON-LD MusicEvent: `offers` només s'emet quan es coneix el preu (Google exigeix
  `price`, `priceCurrency` i `validFrom`); preus manuals a `data/concert-prices.yaml`.
- **Analytics**: dashboard /ca/admin/insights/ amb pestanyes (resum per dia/setmana/mes/trimestre/any + idiomes; pàgines i seccions; navegadors/SO/dispositius) i data d'inici del seguiment.
- **PRODUCCIÓ migrada a Hugo** (2026-10-15): `./sync-web.sh publish` completat (86,5 MB, rsync);
  301 antics verificats, `robots.txt`/`llms.txt`/`llms-full.txt`/`sitemap.xml` en línia.
- **SEO**: el `SearchAction` de la home ara usa l'URL de cerca localitzat (cerca/buscar/pretraga).
- **Miniatures socials (2026-11-25)**: en compartir `https://ivankovacevic.com` per Telegram/WhatsApp
  no hi havia cap imatge perquè l'arrel és una pàgina de redirecció de Hugo (`meta refresh`) sense
  etiquetes OpenGraph; els crawlers **no segueixen** `meta refresh`. Ara `layouts/alias.html`
  genera l'arrel amb `og:image`, `twitter:card` i canonical cap a `/en/`.
  A més, `scripts/make-og-images.py` crea variants 1200×630 a `static/images/og/` (48 imatges:
  abans n'hi havia de 7-11 MB, per sobre del límit de 5 MB de Telegram/Facebook) i
  `data/og-images.json`, que `seo.html` usa per emetre `og:image:width/height/type`.
- **SEO/AI-SEO (2026-11-25)**: `llms.txt` i `generate-llms.py` apuntaven a `/en/gigs/` (404;
  la secció és `/en/concerts/`). 12 `description` amb cometes mal escapades (`7\\\"` → `7"`).
  404 amb `noindex`, un sol `<h1>` per idioma i `lang` correcte.
- **Etiquetes d'idioma (2026-11-25)**: `locale` a `hugo.toml` (`en-GB`, `ca-ES`, `es-ES`,
  **`sr-Latn`**) i `<html lang>`, `hreflang` (cap i sitemap), `<language>` de l'RSS i selector
  d'idiomes emesos amb `.Language.Locale` en lloc de `.Language.Lang`.
  Nota: `languageCode`/`.Language.LanguageCode` estan **deprecats** des de Hugo 0.158; cal
  `locale`/`.Language.Locale` (amb 0.166 el build ja no emet cap avís).
- **Metes (2026-11-25)**: cap `description` per sobre de 160 caràcters (les 3 de la pàgina legal
  venien del text de reserva de l'idioma, escurçat a `hugo.toml`; les altres 4 del recompte
  anterior eren fals positiu per comptar `&amp;`).
- **CI (2026-11-25)**: `build.yml` executa `make-og-images.py --check` i falla si una portada nova
  no té la variant 1200×630 o si `data/og-images.json` queda desfasat.

## Pendent

### Contingut
- [ ] **Discografia**: anys pendents (4): `b4-dani-nello-presents`, `b4-mike-sanchez`,
      `lmj-el-jaguar`, `lmj-mambo-7-baile` (queden a «Any desconegut»).
- [ ] **Discografia**: portades pendents (4): `lj-somebody-tell-that-woman`, `nn-haircut-boogie`,
      `nn-el-tren-de-la-costa`, `nn-el-crujir-de-tus-rodillas`.
- [ ] **Discografia**: enllaços `spotify` (i youtube/smartlink) pendents; Apple Music ja està
      omplert on existeix. Odesli demana API key i MusicBrainz no és fiable per a aquests segells.
- [ ] **Discografia**: confirmar si `lmj-mambo-jambo` (àlbum homònim 2012 a Apple) és una entrada
      nova o la mateixa que `lmj-sonido-jambofonico`, i l'any de `bgko-cd` (debut).
- [ ] **Discografia**: decidir si `b4-mike-sanchez` (Apple no el llista el 2025) és EP 2025 o single antic.
- [ ] **Projectes**: línia temporal per any d'inici a `layouts/projects/list.html`.
- [x] **Projectes**: enllaços Apple afegits a Bernat Font Trio, BBBB, The Nu Niles i
      Lazy Jumpers (data/project-links.yaml). Down Home sense enllaços verificats.
- [ ] **Discografia/projectes**: `year` d'inici de cada projecte (BGKO 2012, Bernat Font 2009,
      Los Mambo Jambo 2008/2009, Lazy Jumpers 2003, The Nu Niles 1996).
- [x] **Traduccions CA/ES/SR** de la discografia: cossos i metes localitzats (18 cossos completats).
- [ ] **SR**: revisió per part de l'Ivan abans de publicar (`draft: false`).

### Disseny (cal aprovació de Joan)
- [ ] Revisió visual d'Ivan del disseny C (dark folk) en conjunt.

### Tècnic
- [x] Secció /admin/ (dashboard GoatCounter) redissenyada amb pestanyes i estètica del lloc.
- [x] `og:image` per pàgina (portada/foto) i global `images/og-image.jpg` de reserva.
- [x] CSP connect-src -> OAuth cms-oauth-bratia (intencionat: el necessita el CMS).
- [x] Redirects: inventari complet del sitemap Yoast (122 URLs) a `static/.htaccess`.
- [ ] Etiqueta de canal per vídeo a les targetes de `videos/list.html`.
- [ ] **Portades de galeria**: les de Google Photos no exposen `og:image` (pàgina renderitzada
      amb JS), així que si es perd un fitxer de `static/images/galleries/` l'script no el pot
      regenerar sol: cal `git checkout -- static/images/galleries` o tornar-lo a baixar a mà.
- [x] Workflow d agenda renombrat a Fetch concerts (iCal + Bandsintown).

### SEO
> Pla complet (redireccions, GEO/IA, sitemaps) a `PLA-SEO.md`.
- [x] **Metes**: `description` única a discografia (49), projectes (9) i legals (3) × 4 idiomes.
- [x] **Canonical + hreflang**: canonical, hreflang recíproc i `x-default` (EN) a les 4 llengües.
- [x] **Open Graph / Twitter**: `og:image` per pàgina (portada/foto; global de reserva) + OG/Twitter.
- [x] **Dades estructurades (JSON-LD)**: `Person`, `MusicGroup`, `MusicAlbum`, `MusicEvent`,
      `BreadcrumbList`, `WebSite`+`SearchAction`.
- [ ] **Metes curtes**: 45 pàgines (índexs de secció i legals, 4 idiomes) tenen `description`
      de menys de 70 caràcters ("Galeries de fotografies.", "Actuacions en directe i vídeos."…).
      Ampliar-les a 110-155 caràcters amb text propi per idioma.
- [ ] **Dades estructurades — preus**: omplir `data/concert-prices.yaml` (clau `YYYY-MM-DD-lloc`,
      camps `price`/`priceCurrency`/`validFrom`) perquè els `MusicEvent` tornin a dur `offers`
      vàlides i Google no assenyali cap camp.
- [x] **Redirects**: 301 de l'inventari complet del sitemap Yoast (122 URLs) a `.htaccess`.
- [x] **Sitemap**: enviar a Google Search Console + Bing (requereix accés de Joan).
- [x] **RSS/feed**: decidit no fer-ne (no hi ha notícies).

### SEO per IA (GEO)
- [x] **`llms.txt`** + **`llms-full.txt`** (generat amb `scripts/generate-llms.py`, enganxat a
      `pages.yml` i `sync-web.sh`).
- [x] **Política per a bots d'IA** a `layouts/robots.txt` (GPTBot, ClaudeBot, PerplexityBot,
      Google-Extended, CCBot… permesos; staging bloquejat).
- [x] **Entitats clares**: JSON-LD coherent Ivan ↔ bandes ↔ discos ↔ concerts.
- [x] **Contingut citable**: fitxes de disc amb any/tipus/enllaços en text + `llms-full.txt`.
- [x] **Renderitzat sense JS**: `<noscript>` amb els propers concerts a l'agenda.

### Manual (Joan)
- [x] Host, usuari SSH i docroot de producció (LinuxBCN) — migració feta el 2026-10-15.
- [x] Forçar 301 http -> https (activat al panell el 2026-10-16).
- [ ] Canonicalitzar www -> sense www (pendent, panell de hosting).
- [ ] Ruta de fotografies a Google Photos per a la selecció.

## Decisions obertes / a confirmar
- Àmbit d'edició de l'Ivan al CMS (ES/EN; CA/SR per traducció?).
