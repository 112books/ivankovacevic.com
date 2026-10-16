# ACCESSOS — ivankovacevic.com

> Aquest fitxer NO conté secrets. Tokens i contrasenyes es guarden fora del repositori.

## CMS (Decap CMS)
- URL: https://ivankovacevic.com/cms/
- Login: compte de GitHub amb permís d'escriptura al repositori 112books/ivankovacevic.com.
- OAuth: https://cms-oauth-bratia-y855.vercel.app (backend GitHub, branca main).
- Flux editorial: publish_mode = editorial_workflow (esborranys + aprovació).
- Idioma de la interfície: ES.
- Editable: configuració (contacte, xarxes), pàgines, projectes, discografia, agenda, etc.
- Els canvis es comitegen a GitHub i despleguen a staging; per a producció cal ./sync-web.sh publish.

## Estadístiques (GoatCounter)
- Panell privat complet: https://ivankovacevic.goatcounter.com (compte de GoatCounter).
- Dashboard intern: https://ivankovacevic.com/ca/admin/ i /ca/admin/insights/
  - NO demana cap token: mostra dades agregades i públiques de static/data/analytics.json
    (actualitzat cada hora pel workflow fetch-analytics.yml).
  - El secret de GitHub GOATCOUNTER_TOKEN només l'usa el workflow; el navegador no pot llegir
    secrets de GitHub, per això el panell no el necessita.
- Token API (per al workflow o per a ús manual): https://ivankovacevic.goatcounter.com/user/api-token
  No posar-lo al repositori ni al xat.

## Desplegament
- Staging (automàtic): push a main -> GitHub Actions pages.yml.
- Producció: ./sync-web.sh publish (build producció + Pagefind + rsync SSH + IndexNow).
- Servidor: linuxbcn.com, usuari ivankovacevic, docroot ~/www, clau ~/.ssh/ivankovacevic_deploy.
- Backup WordPress: /Users/joan/Documents/Obsidian/-backups/ivankovacevic.com-WP-20261015/.
