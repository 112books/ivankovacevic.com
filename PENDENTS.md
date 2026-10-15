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
- **D'Addario**: pàgina pròpia als 4 idiomes + logo patrocinador al peu (entre menú Follow i llegals).
- **Icones de navegació**: contacte → sobre; premsa → diari.
- **Agenda**: afegit Bandsintown (Barcelona Big Blues Band, BGKO, Bratia). Bratia via Google iCal.
- **Enllaços de plataforma per projecte**: `data/project-links.yaml` (Spotify/Apple/Bandcamp/YouTube/
  Bandsintown/web) renderitzats a `layouts/projects/single.html`.

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
