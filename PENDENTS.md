# PENDENTS — ivankovacevic.com

Web oficial del contrabaixista Ivan Kovačević. Actualitzat 2026-10-15.

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
- **Fotografies**: 47 cròniques del blog de Joan Linux afegides a `data/galleries.yaml`,
  amb portada pròpia a `static/images/wp/photos/`, ordenades de més nova a més vella, amb CTA
  i18n propi (`view_chronicle`) i fallback de títol.
- **Discografia**: BGKO (`Imbarca`, `Europa cierra la frontera`, `Nova Era`, `7`), anys de Bernat
  Font Trio verificats (2011-2014), Lazy Jumpers, The Nu Niles i EPS de B4 (2021/2025); enllaços
  Apple Music verificats via API d'iTunes; JSON-LD `MusicGroup`/`MusicAlbum`.
- **Vídeos**: dates reals de YouTube (105/105) i ordre global més nou→més vell (`videos.json`,
  `sync-videos.py`, `videos.js`).
- **SEO/GEO**: `static/robots.txt` nou (bots d'IA permesos), `static/llms.txt` corregit i
  redireccions 301 de l'antic WordPress ampliades a `static/.htaccess`. Pla a `PLA-SEO.md`.
- **SEO**: el `SearchAction` de la home ara usa l'URL de cerca localitzat (cerca/buscar/pretraga).

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
- [ ] **Projectes**: afegir enllaços de plataforma per a la resta de projectes
      (Down Home, Lazy Jumpers, The Nu Niles, BBBB) a `data/project-links.yaml`.
- [ ] **Discografia/projectes**: `year` d'inici de cada projecte (BGKO 2012, Bernat Font 2009,
      Los Mambo Jambo 2008/2009, Lazy Jumpers 2003, The Nu Niles 1996).
- [ ] **Traduccions CA/ES/SR** de la discografia (actualment buides o parcials).
- [ ] **SR**: revisió per part de l'Ivan abans de publicar (`draft: false`).

### Disseny (cal aprovació de Joan)
- [ ] Revisió visual d'Ivan del disseny C (dark folk) en conjunt.

### Tècnic
- [ ] Secció `/admin/` (dashboard GoatCounter) — recrear contingut.
- [ ] `og:image` real (substituir `images/wp/foto-background.png`).
- [ ] CSP `connect-src` encara apunta a l'OAuth `cms-oauth-bratia` (reutilitzat).
- [ ] Redirects: completar amb la llista del `wp-sitemap.xml` antic.
- [ ] Etiqueta de canal per vídeo a les targetes de `videos/list.html`.
- [ ] Renombrar workflow `fetch-concerts.yml` (ara «iCal» → «iCal + Bandsintown»).

### SEO
> Pla complet (redireccions, GEO/IA, sitemaps) a `PLA-SEO.md`.
- [ ] **Metes**: `title` i `meta description` únics i de longitud correcta per pàgina i idioma.
- [ ] **Canonical + hreflang**: revisar canonical i `hreflang` (incloent `x-default`) a les 4 llengües.
- [ ] **Open Graph / Twitter**: `og:image` real per pàgina (ara `images/wp/foto-background.png`);
      `og:title`/`description`/`image`/`url` i `twitter:card`.
- [ ] **Dades estructurades (JSON-LD)**: `Person` (Ivan), `MusicGroup` (bandes), `MusicAlbum`
      (discografia), `MusicEvent` (agenda), `Organization`, `WebSite`+`SearchAction`.
- [ ] **Redirects**: completar la llista del `wp-sitemap.xml` antic (301 → noves rutes per idioma).
- [ ] **Sitemap**: dividir/actualitzar i enviar a Google Search Console + Bing; vigilar `noindex`.
- [ ] **RSS/feed**: decidir si cal (ara no hi ha news).

### SEO per IA (GEO)
- [ ] **`llms.txt`** (i opcionalment `llms-full.txt`) amb resum del lloc i enllaços clau.
- [ ] **Política per a bots d'IA** a `robots.txt`: permetre/bloquejar explícitament
      (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot…).
- [ ] **Entitats clares**: JSON-LD coherent Ivan ↔ bandes ↔ discos ↔ concerts (desambiguació).
- [ ] **Contingut citable**: resum biogràfic, fitxes de disc amb any/formats i dades en text
      (no només imatge), perquè siguin fàcilment extractables.
- [ ] **Renderitzat sense JS**: comprovar que les pàgines clau tinguin contingut en HTML
      (agenda i discografia carreguen via JS; valorar `noscript`/SSR parcial).

### Manual (Joan)
- [ ] Host, usuari SSH i docroot de producció (LinuxBCN).
- [ ] Ruta de fotografies a Google Photos per a la selecció.

## Decisions obertes / a confirmar
- Àmbit d'edició de l'Ivan al CMS (ES/EN; CA/SR per traducció?).
