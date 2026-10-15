# AUDITORIA DE SEGURETAT — producció (2026-10-15)

Abast: https://ivankovacevic.com (Hugo estàtic, Apache+proxy a LinuxBCN).

## Correcte
- TLS: Let's Encrypt, vàlid 2026-09-22 -> 2026-12-21, SAN ivankovacevic.com i www.
- Protocols: TLS 1.0/1.1 desactivats; TLS 1.2 i 1.3 actius.
- Capçaleres: HSTS preload, CSP, X-Frame-Options SAMEORIGIN, X-Content-Type-Options nosniff,
  Referrer-Policy, Permissions-Policy i COOP.
- Sense X-Powered-By ni versió d'Apache (Server: HTTPd).
- WordPress: /wp-admin, /wp-login.php, /xmlrpc.php, /wp-json, /wp-cron.php, /wp-includes i
  /wp-content -> 410; no queden fitxers WP al docroot.
- Sense llistat de directoris; .git, .env i .DS_Store bloquejats (403).
- Sense cookies de sessió i sense contingut mixt (http://) a les pàgines.
- TRACE -> 405; backups (*.sql.gz, *.zip) fora del docroot.
- /admin/ i /cms/ amb meta robots noindex, nofollow i exclosos a robots.txt.

## Pendent / recomanat (cal panell de hosting o permisos de servidor)
- [ ] Forçar 301 http:// -> https://: ara http://ivankovacevic.com/ respon 200. El proxy no
      exposa X-Forwarded-Proto a Apache (Listen 127.0.0.1:8080) i no podem verificar mod_rewrite;
      cal activar "Force HTTPS" al panell (Plesk/Dinaserver) o al vhost.
- [ ] Canonicalitzar www.ivankovacevic.com -> ivankovacevic.com (301). Ara respon 200.
- [ ] CSP: style-src 'unsafe-inline' (necessari pel disseny) i img-src https: (portades externes).
- [ ] /cms/config.yml és públic (només repo i URL OAuth, sense secrets); opcional bloquejar.

## Verificació
- curl -I https://ivankovacevic.com/
- openssl s_client -connect ivankovacevic.com:443 -servername ivankovacevic.com
- Rich Results Test (schema.org), Google Search Console i Bing Webmaster.
