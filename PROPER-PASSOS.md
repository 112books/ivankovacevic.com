# QUÈ HE DE FER JO (Joan) — ivankovacevic.com

> Actualitzat 2026-10-16. La resta de feina tècnica ja està feta i publicada.

## 1. Panell de hosting (LinuxBCN / Dinaserver-Plesk) — 5 min
- [ ] Canonicalitzar www -> sense www: que https://www.ivankovacevic.com/ faci 301 a https://ivankovacevic.com/.
  - A Plesk: Domains -> ivankovacevic.com -> Hosting & DNS -> Preferred domain (o Redirect www to non-www).
  - Comprovar: curl -sI https://www.ivankovacevic.com/  -> ha de donar 301.
- [x] Force HTTPS activat (2026-10-16).

## 2. Google Search Console — FET
- [x] Propietat del domini ivankovacevic.com verificada.
- [x] Sitemap https://ivankovacevic.com/sitemap.xml enviat (2026-10-16).
- [ ] Opcional: Inspecció d'URL -> demanar indexació de /en/, /ca/, /es/, /sr/, /en/discography/, /ca/fotografies/, /en/concerts/.

## 3. Bing Webmaster Tools — FET
- [x] Sitemap https://ivankovacevic.com/sitemap.xml enviat (2026-10-16).
- (El desplegament també notifica IndexNow automàticament.)

## 4. Contingut que ha de validar l'Ivan
- [ ] Revisió de les traduccions SR de la discografia (ja estan fetes; només cal el seu OK).
- [ ] Revisió visual del disseny C (dark folk) en conjunt.
- [ ] Confirmar el retir de Bernat Font (es manté el projecte a la memòria).
- [ ] Decidir l'àmbit d'edició de l'Ivan al CMS: ES/EN directament; CA/SR per traducció?

## 5. Decisions de discografia (Joan)
- [ ] Spotify: cal una API key de Spotify o enllaços manuals per disc. Apple ja està omplert.
- [ ] 4 portades: lj-somebody-tell-that-woman, nn-haircut-boogie, nn-el-tren-de-la-costa,
      nn-el-crujir-de-tus-rodillas (originals o deixar-les sense).
- [ ] 4 anys: b4-dani-nello-presents, b4-mike-sanchez, lmj-el-jaguar, lmj-mambo-7-baile.
- [ ] Confirmar si lmj-mambo-jambo (àlbum 2012 a Apple) és una entrada nova o és lmj-sonido-jambofonico.
- [ ] Confirmar l'any del debut bgko-cd.
- [ ] b4-mike-sanchez: EP 2025 o single antic?

## 6. Opcionals / més endavant
- [ ] Ruta de Google Photos per a la selecció de fotografies.
- [ ] Línia temporal de projectes (és disseny; cal el teu OK).
- [ ] Etiqueta de canal als vídeos (abans cal decidir com etiquetar els projectes: sources.yaml té 8 entrades al mateix canal).

## 7. Preus d'entrada (per a l'agenda)
- [ ] Passar els imports dels propers concerts per omplir `data/concert-prices.yaml`
      (clau `YYYY-MM-DD-lloc`, camps `price`/`validFrom`) i que el JSON-LD `MusicEvent`
      torni a dur `offers` vàlides.

## Comprovacions ràpides
- curl -sI https://www.ivankovacevic.com/        (ha de ser 301)
- curl -sI http://ivankovacevic.com/             (ha de ser 301)
- curl -s  https://ivankovacevic.com/robots.txt
- curl -s  https://ivankovacevic.com/sitemap.xml | head
- curl -s  https://ivankovacevic.com/en/concerts/ | grep -c '"offers"'   (0 = sense preus; vegeu data/concert-prices.yaml)
