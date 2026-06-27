# django-svelte-starter

## Project Lineage

This repository is a starter-shell extraction from `Relonee`, not a greenfield app.

The broader extraction work is split across three directions:

- `Relonee` remains the original product source.
- `djultra` is the Django/backend spin-off.
- `svUltra` is the Svelte/frontend spin-off.

The current frontend here has not been replaced with `svUltra`.

That was intentional: the plan was to first get the `svUltra` demo right with a few basic widgets that prove the value clearly on their own. Until that demo is convincing enough to justify integration, this starter keeps the copied/adapted frontend shell instead of forcing an early `svUltra` migration.

## Django/Svelte Build Notes

Run the two development servers together during normal development:

```sh
./dm run back
./dm run front
```

Django serves the HTML shell from `backend/core/templates/index.html`. That template uses `django-vite` to load `frontend/src/main.js` in dev mode and the built Svelte bundle from `static/frontend/manifest.json` after a frontend build.

Build production assets with:

```sh
./dm build
```

This runs the Svelte build first, then collects Django static files. Use `./dm build front` for only the Vite build or `./dm build static` for only Django `collectstatic`.

The frontend build writes bundled assets and the Vite manifest to `static/frontend/`. The `postbuild` script also updates generated build metadata in `frontend/src/build-info.json` and bumps the version field in `frontend/package.json`.

`static/src/` is Django static source for files that are not produced by Vite, such as admin CSS, favicons, email logos, and similar assets. The raw underlying commands are:

```sh
cd frontend && npm run build
./dm django-admin collectstatic --noinput
```

## How the frontend and API are served

In development, Django serves the API and the HTML shell on port 8000, and Vite
serves the Svelte app with hot-reload on port 5173. The page and the API can be
different origins — the Vite page on `:5173` calling the API on `:8000`, or Django
reached under a host alias (e.g. `127.0.0.1` vs `localhost`) that differs from the
API URL.

In production, a reverse proxy (nginx, in Docker or whatever you run) serves the
built SPA and forwards `/api` to Django, normally all under one real domain — so
the page and API share an origin. There is no Vite; the dev ports are gone.

Three settings encode these URLs, set per environment:

- `FRONTEND_URL` — where the SPA is served (`http://localhost:5173` in dev, the
  real site origin in prod).
- `FRONTEND_API_URL` — the API base the SPA calls (`http://localhost:8000/api`).
- `FRONTEND_URL_EMAILS` — the app's public base URL used in email links.

When the page and API differ in origin, cross-origin access is gated by
`CORS_ALLOWED_ORIGINS` and the CSP `connect-src`; their comments in `settings.py`
explain how to allow extra hosts such as LAN IPs.

## reCAPTCHA

The contact form and the sign-in request are protected by reCAPTCHA v3. The
frontend loads the widget with `RECAPTCHA_SITE_KEY` and sends a token with each
submission; the backend verifies that token with Google using
`RECAPTCHA_SECRET_KEY`.

Both keys default to Google's universal test keys, which always validate (the
widget shows a "for testing only" banner) — so the forms work out of the box with
no setup. For production, set real keys via environment variables (or the
`CONFIG_FILE`):

```sh
RECAPTCHA_SITE_KEY=...      # public, used by the widget
RECAPTCHA_SECRET_KEY=...    # private, used for server-side verification
```

## Backend management

Run the backend with `./dm run` — it starts the Django dev server together with a
`django-tasks` worker and the fastmanage daemon, so management commands such as
`./dm django-admin migrate` and `./dm django-admin createsuperuser` run in a warm
process and feel instant. See `backend/readme.md` for the backend command
reference and djultra's readme for the fastmanage internals.
