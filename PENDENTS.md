# PENDENTS — ivankovacevic.com

Backlog viu. Estat a 2026-10-14.

## Fet recentment
- [x] Repositori GitHub `112books/ivankovacevic.com` creat + push inicial.
- [x] `pages.yml` (GitHub Pages, staging) + Pages activat. Staging: https://112books.github.io/ivankovacevic.com/
- [x] Disseny C (folk fosc) aplicat: fonts locals (Oswald + Source Serif 4), paleta terracota/fosc càlid, animacions reveal + marquee.
- [x] Pàgines legals EN/CA/SR (avis, privacitat, cookies). ES ja existia.
- [x] i18n SR complet (56 claus).
- [x] Infraestructura d'agregació multi-font: `data/sources.yaml` + `scripts/sync-agenda.py`,
      `scripts/sync-videos.py`, `scripts/sync-news.py`. Workflows `fetch-concerts`,
      `fetch-videos`, `fetch-news` (nou) llegeixen la configuració.

## Automatització de contingut (model aprovat)
Font de veritat única: **`data/sources.yaml`**. Afegir un projecte = afegir una entrada.

- **Agenda (`gigs`)**: llista de calendars iCal (Google Calendar públic `.ics`) de cada
  projecte on toca. El workflow nocturn els fusiona en un sol VCALENDAR
  (`static/data/concerts.txt` per al JS) i en `data/concerts-schema.json` (JSON-LD).
  Cada event porta el nom del projecte com a artista.
- **Vídeos (`videos`)**: llista de canals de YouTube (projectes + propi). `sync-videos.py`
  baixa amb yt-dlp, etiqueta cada vídeo amb el canal d'origen i fusiona.
- **Notícies (`news`)**: llista de feeds RSS/Atom (Google Alerts, blogs de projectes, premsa).
  `sync-news.py` agrega mencions a `static/data/news.json`.
- **Fotografies**: **selecció manual** (decisió de Joan). No s'automatitza.

### Cal omplir `data/sources.yaml` amb:
- [ ] Llista de **projectes** d'Ivan i, per a cadascun: calendari iCal, canal de YouTube, RSS/xarxes.
- [ ] **Google Alerts** per «Ivan Kovačević» i variants → RSS.
- [ ] Confirmar si hi ha xarxes pròpies (Instagram/Facebook) a agregar.

## Tasques manuals (Joan)
- [ ] **GoatCounter**: crear `ivankovacevic.goatcounter.com` + token API.
- [ ] **GitHub**: afegir Ivan com a col·laborador (`write`) i donar-li accés al CMS.
- [ ] **Google Fotos**: àlbums compartits per a la selecció de fotografies.
- [ ] **Producció**: host, usuari SSH i docroot del servidor de LinuxBCN.

## Contingut pendent
- [ ] **Traduccions CA i SR** dels projectes, notícies i discografia (seccions + biografia fetes).
- [ ] **SR**: revisió per part de l'Ivan abans de publicar (marcar `draft: false`).
- [ ] **Discografia**: dades reals (bandes, àlbums, any, portades). Actualment 1 disc de mostra.
- [ ] **Projectes**: afegir `name`, `role`, `photo`, `description` a cada fitxa.
- [ ] **Notícies**: migrar/escriure contingut editorial (D'Addario, Ruta 66...).
- [ ] Netejar imatges de Bratia restants a `static/images/` (gallery/, error/, contact/, sponsor/).

## Tècnic pendent
- [ ] Secció `/admin/` (dashboard GoatCounter) — recrear contingut.
- [ ] `og:image` real (substituir `images/wp/foto-background.png`).
- [ ] CSP `connect-src` encara apunta a l'OAuth `cms-oauth-bratia` (reutilitzat).
- [ ] Redirects: completar amb la llista del `wp-sitemap.xml` antic.
- [ ] Etiqueta de canal per vídeo a les targetes de `videos/list.html` (dades ja hi són).

## Decisions obertes
- Àmbit d'edició de l'Ivan al CMS (ES/EN; CA/SR per traducció?).
- Nom del projecte a `data/sources.yaml` per a Bratia → confirmar nomenclatura.
