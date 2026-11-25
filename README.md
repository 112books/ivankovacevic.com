# ivankovacevic.com

Web oficial del contrabaixista **Ivan Kovačević** — Hugo (multilingüe EN/CA/ES/SR),
CMS Decap, estadístiques GoatCounter. Migrat des de WordPress.

## Requisits
- Hugo extended 0.166.0+
- Node.js (per a Pagefind)
- Python 3 (scripts d'importació/manteniment)

## Desenvolupament local
```bash
hugo server --environment local
# http://localhost:1313/ivankovacevic.com/
```

## Build de producció
```bash
rm -rf public
hugo --minify --environment production
npx pagefind --site public
```

## Miniatures socials (Telegram, WhatsApp, Facebook, X, LinkedIn)
Les imatges de previsualització es generen a partir del front matter
(`og_image` > `cover` > `photo` > `images/og-image.jpg`):

```bash
python3 scripts/make-og-images.py          # regenera static/images/og/ + data/og-images.json
python3 scripts/make-og-images.py --check  # exit 1 si estan desfasades (ho fa el CI)
```

Cal executar-lo **després d'afegir o canviar una portada o foto**: els crawlers
socials descarten imatges de més de 5 MB i retallen a ~1.91:1 (1200×630).
L'arrel `/` és una redirecció de Hugo i, com que els crawlers no segueixen
`meta refresh`, `layouts/alias.html` hi duu les etiquetes OpenGraph.

## Desplegament
```bash
./sync-web.sh publish   # via rsync SSH al servidor de LinuxBCN
```

## Estructura
- `content/<lang>/` — contingut per idioma (seccions amb directoris traduïts)
- `layouts/` — plantilles Hugo
- `data/` — dades (contacte, xarxes, discografia)
- `config/` — configuració per entorn (local / staging / production)
- `scripts/` — importació WP, processament de concerts/vídeos, portades de galeria
  (`fetch-gallery-covers.py`) i miniatures socials (`make-og-images.py`)
- `.github/workflows/` — CI i feines nocturnes (concerts, vídeos, analytics)

Consulta `PLA-MIGRACIO.md` (pla complet) i `PENDENTS.md` (backlog viu).
