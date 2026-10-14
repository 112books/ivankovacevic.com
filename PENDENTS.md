# PENDENTS — ivankovacevic.com

Backlog viu. Estat a 2026-10-14.

## Tasques manuals (Joan)
- [ ] **Google Calendar** "Ivan Kovačević – Gigs" (compte Joan/LinuxBCN), públic, iCal `.ics`.
      Compartir amb Ivan. Actualitzar `fetch-concerts.yml` (millor via `vars.CALENDAR_ICS_URL`).
- [ ] **YouTube**: confirmar canal propi (`UCG-CSJzP_90xHVhaDQj6PvA`) o crear llista de
      reproducció pública. Actualitzar `fetch-videos.yml` si cal.
- [ ] **Google Fotos**: àlbums compartits i omplir `data/galleries.yaml`.
- [ ] **GoatCounter**: crear `ivankovacevic.goatcounter.com` + token API.
- [ ] **GitHub**: afegir Ivan com a col·laborador (`write`) i donar-li accés al CMS.
- [ ] **Producció**: host, usuari SSH i docroot del servidor de LinuxBCN.

## Contingut pendent
- [ ] **Traduccions CA i SR** dels projectes, notícies, discografia i textos legals.
      Actualment CA/SR només tenen esquelet de seccions + biografia.
- [ ] **SR**: revisió per part de l'Ivan abans de publicar (marcar `draft: false`).
- [ ] **Pàgines legals**: crear EN/CA/SR (ara només ES). El peu enllaça a `/es/legal/`.
- [ ] **Discografia**: dades reals (bandes, àlbums, any, portades). Actualment 1 disc de mostra.
- [ ] **Projectes**: afegir `name`, `role`, `photo`, `description` a cada fitxa; netejar HTML cru del WP.
- [ ] **Notícies**: EN buit; ES amb 1 entrada. Migrar/escriure la resta (D'Addario, Ruta 66...).
- [ ] **Notícia D'Addario**: recuperar contingut de `/ivan-kovacevic-sobre-daddario/`.
- [ ] `data/band.yaml`, `data/galleries.yaml`, `static/data/concerts.*`, `static/data/videos.json`
      són encara placeholders de Bratia → substituir.
- [ ] Netejar imatges de Bratia restants a `static/images/` (gallery/, error/, contact/, sponsor/).

## Tècnic pendent
- [ ] `pages.yml` (GitHub Pages, staging) + activar Pages al repo.
- [ ] `build.yml`: revisar que validi el build.
- [ ] Secció `/admin/` (dashboard GoatCounter) — recrear contingut de la secció admin.
- [ ] `og:image` real (substituir `images/wp/foto-background.png`).
- [ ] Revisió de disseny (identitat visual pròpia) — **requereix aprovació de Joan**.
- [ ] Crisp: CSP `connect-src` encara apunta a l'OAuth `cms-oauth-bratia` (reutilitzat).
- [ ] Redirects: completar amb la llista del `wp-sitemap.xml` antic.

## Decisions obertes
- Disseny: paleta tipografia i animacions (direcció: balcànic + jazz elegant fosc).
- Àmbit d'edició de l'Ivan al CMS (ES/EN; CA/SR per traducció?).

## Disseny C (folk fosc)
- Implementar opció C: `static/css/styles.css` (variables, tipografies Oswald + Source Serif 4, colors terracota, paleta fosca càlida). Afegir fonts a head.
- Afegir transicions i animacions (reveal, hover botons, marquee de gires opcional a hero).
- Actualitzar marques (logotip, favicons si cal) sense trencar.
