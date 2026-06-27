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

## Frontend config

The frontend has two separate configs:

- **`window.config` — system config.** The frontend's system configuration, injected
  by the Django shell at page load: API URLs, API keys (such as the reCAPTCHA site
  key), and similar deployment values — how this deployment is wired.
- **`configStore` — user config.** The user's own configuration (such as dark mode),
  persisted in the browser's `localStorage` so it survives across visits.

  Read and write it from any component or module via the kit store:

  ```js
  import { configStore as config } from '@kit/stores';
  import { get } from 'svelte/store';

  $config.darkMode            // read reactively in a Svelte component
  get(config).darkMode        // read imperatively, outside a reactive context

  // Update by passing an object: it deep-merges into the current config and
  // persists to localStorage automatically — other keys are left untouched.
  config.update({ darkMode: true });

  // Add a new user setting the same way — just write a new key:
  config.update({ sidebarCollapsed: true });
  ```

  Changes save immediately and sync across the user's open tabs.

  Because `update` deep-merges, a nested object keeps its other keys — which is exactly
  what a UI wants: when the user flips one knob (say, a list's sort order), the rest of
  that setting (its active tags) stays put instead of being wiped out. When you *do*
  want to replace a nested object wholesale instead of merging into it, wrap it with
  `overwrite()`:

  ```js
  import { configStore as config, overwrite } from '@kit/stores';

  // stored value: { filters: { sort: 'date', tags: ['x'] } }
  config.update({ filters: { sort: 'name' } });            // merge   → { filters: { sort: 'name', tags: ['x'] } }
  config.update({ filters: overwrite({ sort: 'name' }) }); // replace → { filters: { sort: 'name' } }
  ```

## Simulating slow loading

To test the loading screens and SPA behaviour under slow page loads, set a loading delay
on `window.config`. The router then waits that many milliseconds before swapping in the
next page, so you can watch the loading overlay and how the app behaves while content is
slow to arrive.

For a quick one-off, set it from the browser console — session-only, a reload clears it:

```js
window.config.loadingDelay = 4000   // every navigation waits 4 s before the new page swaps in
```

To keep it on across reloads while you work, set the same value in `frontend/src/init.js`
(which builds up `window.config` on every load):

```js
window.config.loadingDelay = 4000;
```

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
