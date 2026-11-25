# ivankovacevic.com — instruccions del projecte

Web oficial del contrabaixista **Ivan Kovačević**. Hugo estàtic multilingüe, CMS Decap,
estadístiques GoatCounter. Migrat des de WordPress (2026-10-14).

## Entorns

| Entorn | URL |
|---|---|
| Local | `http://localhost:1313/ivankovacevic.com/` |
| Staging (GitHub Pages, noindex) | `https://112books.github.io/ivankovacevic.com/` |
| Producció | `https://ivankovacevic.com/` (servidor LinuxBCN) |

## Stack

- Hugo extended 0.166.0 · Pagefind 1.5.2 · Node · Python 3
- Idiomes: **EN** (principal, weight 1) · **CA** (2) · **ES** (3) · **SR** (`sr-Latn`, 4)
- `defaultContentLanguage = "en"`, `defaultContentLanguageInSubdir = true`

## Comandes

```bash
hugo server --environment local     # desenvolupament
hugo --minify --environment production   # build producció
rm -rf public && hugo --minify --environment staging && npx pagefind --site public
./sync-web.sh publish               # desplegament producció (SSH)
python3 scripts/make-og-images.py          # miniatures socials 1200×630 (després de canviar portades/fotos)
python3 scripts/make-og-images.py --check  # comprova que estiguin al dia (ho fa el CI)
```

## Estructura de configuració

- `hugo.toml` — base comuna (idiomes, menús, params, markup)
- `config/local/hugo.toml` · `config/staging/hugo.toml` · `config/production/hugo.toml`

## Convencions

- Seccions amb **directoris traduïts** + `type:` explícit al `_index.md` + `cascade: type:`
  perquè els fills hereten el tipus. **No** usar `permalinks` (genera `/es/es/`).
- Menús: iterar sempre `site.Menus.main` (mai URLs hardcoded), per respectar els slugs per idioma.
- Enllaços interns: `relURL`/`absURL` o `.RelPermalink`. Mai rutes absolutes escrites a mà.
- Imatges de contingut: `static/images/...`; les importades del WP a `static/images/wp/`;
  les portades de galeria, a `static/images/galleries/` (`scripts/fetch-gallery-covers.py`).
  **Mai** enllaçar imatges en calent des de `blog.pocallum.cat`: respon amb
  `Cross-Origin-Resource-Policy: same-site` i el navegador les bloqueja.
- Imatges per compartir: `scripts/make-og-images.py` genera variants 1200×630 a
  `static/images/og/` i `data/og-images.json` (llegit per `partials/seo.html`). Telegram,
  WhatsApp i Facebook descarten imatges de més de 5 MB: **regenera les variants** quan afegeixis
  o canviïs una portada/foto. L'arrel `/` redirigeix amb `layouts/alias.html`, que ha de dur
  igualment les etiquetes OpenGraph (els crawlers no segueixen `meta refresh`).
- Sense secrets al repositori. Cap credencial als `.md`.
- Commits petits, convenció `feat:` / `fix:` / `chore:` / `docs:`. **Mai** `push --force`.
- `rm -rf public` abans d'un build de producció.

## Regles de disseny

- **No canviar res de disseny (colors, tipografia, marges, layout) sense aprovació explícita de Joan.**

## Control horari

Sessions a `.taques/ivankovacevic.com/.sessions.jsonl` (skill `gestor-hores`). Append-only.

## Referències

- Pla de migració: `PLA-MIGRACIO.md`
- Pendents: `PENDENTS.md`
