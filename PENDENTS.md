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
- **SEO**: el `SearchAction` de la home ara usa l'URL de cerca localitzat (cerca/buscar/pretraga).

## Pendent

### Contingut
- [ ] **Discografia**: omplir `year:` de les 25 entrades (recerca feta, queden 4-5 dubtes:
      senzills de Los Mambo Jambo «El Jaguar», «Mambo 7/Baile»; àlbums B4/BBBB).
- [ ] **Discografia**: implementar línia temporal vertical per any (nou→vell) a
      `layouts/discography/list.html`.
- [ ] **Projectes**: línia temporal per any d'inici a `layouts/projects/list.html`.
- [ ] **Projectes**: afegir enllaços de plataforma per a la resta de projectes
      (Down Home, Lazy Jumpers, The Nu Niles, BBBB) a `data/project-links.yaml`.
- [ ] **Discografia/projectes**: `year` d'inici de cada projecte (BGKO 2012, Bernat Font 2009,
      Los Mambo Jambo 2008/2009, Lazy Jumpers 2003, The Nu Niles 1996).
- [ ] **Traduccions CA/ES/SR** de la discografia (actualment buides o parcials).
- [ ] **SR**: revisió per part de l'Ivan abans de publicar (`draft: false`).

### Disseny (cal aprovació de Joan)
- [ ] **Nav compacta en mòbil**: amb la barra visible (en scroll), les 3 últimes icones queden fora
      de pantalla (390px). Opcions: amagar el logo compacte en mòbil (≤480px) o reduir mida d'icones.
- [ ] **Discografia — línia temporal animada en scroll**: un cop hi hagi els anys, animar la línia
      temporal segons l'scroll (entrada d'entrades, traçat de la línia, etc.).

### Tècnic
- [ ] Secció `/admin/` (dashboard GoatCounter) — recrear contingut.
- [ ] `og:image` real (substituir `images/wp/foto-background.png`).
- [ ] CSP `connect-src` encara apunta a l'OAuth `cms-oauth-bratia` (reutilitzat).
- [ ] Redirects: completar amb la llista del `wp-sitemap.xml` antic.
- [ ] Etiqueta de canal per vídeo a les targetes de `videos/list.html`.
- [ ] Renombrar workflow `fetch-concerts.yml` (ara «iCal» → «iCal + Bandsintown»).

### Manual (Joan)
- [ ] Host, usuari SSH i docroot de producció (LinuxBCN).
- [ ] Ruta de fotografies a Google Photos per a la selecció.

## Decisions obertes / a confirmar
- Àmbit d'edició de l'Ivan al CMS (ES/EN; CA/SR per traducció?).
