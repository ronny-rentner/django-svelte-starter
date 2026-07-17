# Starter Extraction TODO

## Before Site 1

- Trim inherited YouTube transcript functionality from the default starter unless the first site needs it. It currently ships as `backend/core/models/youtube.py`, committed migrations, and `pytubefix` / `youtube-transcript-api` dependencies.
- Add a fresh-clone bootstrap path: how to create `backend/venv`, install backend/frontend dependencies, create the local database, and provide the first config values.
- Clarify deployment/live hosting before site 1: target host, reverse proxy layout, domain/TLS, process manager, static/media serving, database, backups, email delivery, reCAPTCHA keys, deploy command, rollback path, and which config values differ between dev and live.
- Add a per-site configuration template for launch-critical values: `SECRET_KEY`, `DEBUG`, database settings, frontend URLs, allowed hosts, reCAPTCHA keys, and email settings.
- Remove local-machine defaults before cloning a real site: personal `ALLOWED_HOSTS`, the absolute path in `cli/startdev.desktop`, `dss` package/database names, and placeholder brand/legal text.
- Quiet development/demo noise that would distract site work: frontend request/debug logs, layout pageConfig logging, placeholder footer/social links, and demo-only `About` / `Landing` page content.

## Copy or Adapt Later From Relonee

- Extract the backend-agnostic API wrapper from Relonee `frontend/src/api/api.js` (apiRequest with per-endpoint AbortControllers, CSRF header from the cookie, recaptcha integration) into svUltra; the starter and Relonee then import it and keep only their own endpoint functions. svUltra's readme "Wiring your backend" section documents this design.

- Frontend dependency refresh: backend venv packages were refreshed to current PyPI releases, including Django 6 and the `django-tasks-db` split. Frontend package updates remain; current build warnings include old Browserslist data and Svelte warnings from older component code. Svelte updates need extra care because `frontend/svelte.config.js` uses advanced preprocessors that rewrite syntax and allow non-plain-Svelte expressions.
- svUltra demo history: previous demo work stalled because LLM-generated demos did not communicate the library well enough; judge the next pass by whether it clearly proves the README claims instead of by generic cleanup.
- Document/download API: `DocumentDownloadView`, `DocumentList`, file permissions, document serializer context, and media path behavior.
- Upload/extraction API: `DocumentUpload`, document AI settings, `Degree` extraction flow, and anonymous upload behavior.
- External integrations: `DocusealWebhookView`, `AnabinAiSearch`, `VidexFormChatView`, and their model/service dependencies only for projects that need them.
- Copied templates from Relonee need adaptation before production use: `emails/*` and admin overrides. The frontend shell is copied and minimally adapted for starter routing.
- Static source assets from Relonee `static/src` may be useful later for admin styling, favicon, and email/logo assets.
