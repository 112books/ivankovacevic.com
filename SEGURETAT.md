# AUDITORIA DE SEGURETAT — producció (actualitzat 2026-10-16)

Abast: https://ivankovacevic.com (Hugo estàtic, Apache+proxy a LinuxBCN).

## Correcte
- TLS: Let's Encrypt, SAN ivankovacevic.com i www; TLS 1.0/1.1 desactivats, 1.2 i 1.3 actius.
- Capçaleres: HSTS preload, CSP, X-Frame-Options SAMEORIGIN, X-Content-Type-Options nosniff,
  Referrer-Policy, Permissions-Policy i COOP.
- Force HTTPS: http -> https amb 301 (activat al panell el 2026-10-16).
- WordPress: /wp-admin, /wp-login.php, /xmlrpc.php, /wp-json, /wp-cron.php, /wp-includes i
  /wp-content -> 410; no queden fitxers WP al docroot.
- Sense llistat de directoris; .git, .env i .DS_Store bloquejats (403).
- Sense cookies de sessió i sense contingut mixt; TRACE -> 405.
- /admin/ i /cms/ amb meta robots noindex, nofollow i exclosos a robots.txt.
- CSP pròpia per a /cms/ (Decap necessita 'unsafe-eval'); la resta del web sense 'unsafe-eval'.

## Pendent / recomanat
- [ ] Canonicalitzar www.ivankovacevic.com -> ivankovacevic.com (301). Ara www respon 200.
- [ ] CSP: style-src 'unsafe-inline' (necessari pel disseny) i img-src https: (portades externes).
- [ ] /cms/config.yml és públic (només repo i URL OAuth, sense secrets); opcional bloquejar.

## Verificació
- curl -I https://ivankovacevic.com/  (i http://... per comprovar el 301)
- openssl s_client -connect ivankovacevic.com:443 -servername ivankovacevic.com
- Rich Results Test (schema.org), Google Search Console i Bing Webmaster.
