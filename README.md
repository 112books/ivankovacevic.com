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

## Desplegament
```bash
./sync-web.sh publish   # via rsync SSH al servidor de LinuxBCN
```

## Estructura
- `content/<lang>/` — contingut per idioma (seccions amb directoris traduïts)
- `layouts/` — plantilles Hugo
- `data/` — dades (contacte, xarxes, discografia)
- `config/` — configuració per entorn (local / staging / production)
- `scripts/` — importació WP, processament de concerts/vídeos i portades de galeria
  (`fetch-gallery-covers.py`; autoallotja les imatges de `data/galleries.yaml`)
- `.github/workflows/` — CI i feines nocturnes (concerts, vídeos, analytics)

Consulta `PLA-MIGRACIO.md` (pla complet) i `PENDENTS.md` (backlog viu).
