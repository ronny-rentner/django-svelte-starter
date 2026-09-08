# django-svelte-starter

# ⚠️ THIS README HAS THE WRONG STYLE. IT IS BEING REWRITTEN. ⚠️

**Most of this file reads as a decision log and a narrative of how things came to be.
That is the wrong style for a starter's readme. Do not add text in that style.**

**The target style:** a reference for someone who takes this starter and builds a site
with it.

- Say what exists and how to use it.
- Instruct, do not narrate. No history, no comparison with other projects, no
  justifications.
- Basics first. One topic per section. Commands in code blocks.

**Rewritten so far:** "Configuration", "Live hosting". Until a section is rewritten, its
facts are settled and its wording is not.

---

## Project Lineage

This repository is a starter-shell extraction from `Relonee`, not a greenfield app.

The broader extraction work is split across three directions:

- `Relonee` remains the original product source.
- `djultra` is the Django/backend spin-off.
- `svUltra` is the Svelte/frontend spin-off.

`djultra` is a shared library that adds common bells and whistles to Django (base models, serializers, the email service, a dev server); `svUltra` does the same for Svelte. The models and endpoints each site defines — `Person`, `ContactMessage`, the login and contact views — live in the site itself (here, the starter), not in the libraries.

The frontend is built on `svUltra`: it was scaffolded from the svUltra kit demo and pulls its components, actions, stores, and router from the `@kit` alias (`svultra/kit`). The site-specific layer on top — pages, layout, API helpers — is the starter's own.

## Django/Svelte Build Notes

Run the two development servers together during normal development:

```sh
./dm run back
./dm run front
```

Django serves the HTML shell through djultra's `index` view, which pushes the frontend config (API URL, reCAPTCHA key, CSP nonce) into the page. djultra ships a default `index.html`; the starter overrides it with `backend/core/templates/index.html` (searched first because `core` precedes `djultra` in `INSTALLED_APPS`). That template uses `django-vite` to load `frontend/src/main.js` in dev mode and the built Svelte bundle from `static/frontend/manifest.json` after a frontend build.

Build production assets with:

```sh
./dm build
```

This runs the Svelte build first, then collects Django static files. Use `./dm build front` for only the Vite build or `./dm build static` for only Django `collectstatic`.

The frontend build writes bundled assets and the Vite manifest to `static/frontend/`. Before it, svUltra's `prebuild` script stamps the untracked `frontend/src/build-info.json` with a build number and time, which the footer shows.

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

## Configuration

Settings live in three files:

| File | Holds | Committed | A change takes effect |
| ---- | ----- | --------- | --------------------- |
| `backend/config/settings.py` | every setting, as plain Django settings, including the mail relay's host and port | yes | with the code |
| `docker/prod_django.ini` | what differs per installation: `DEBUG`, `ALLOWED_HOSTS`, the `FRONTEND_*` URLs, `DEFAULT_FROM_EMAIL` | yes, copied into the image | after an image rebuild |
| `docker/prod.env` | secrets: database credentials, `SECRET_KEY`, API keys, the mail relay login | no | after `up -d` |

A setting written as `config('NAME', default=…)` in settings.py takes its value from the
environment variable `NAME`, else from `NAME = value` in the ini, else from the default.
Values are cast to the type of the default; lists are comma-separated. A plain assignment
cannot be overridden. `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_PORT` are read
from the environment only.

Secrets go into `prod.env` and nowhere else. `docker/certbot/`, the site's Let's Encrypt
account and keys, is ignored as well.

## Live hosting

The host keeps the sites and the two shared services under `~/Projects/sites`, a
repository of its own:

```text
~/Projects/sites/
├── database/     PostgreSQL 17, one server for all sites
├── proxy/        nginx on 80 and 443, one reverse proxy for all sites
└── <site>/       a site, cloned from its own repository
```

### Shared services

Each is a Compose project, run from its directory. Bring it up once; it restarts on its
own after a reboot, until `down`. A site's `up -d` joins the networks and needs both
services running. The database one reads `prod.env` (copy `prod.env.example`, set the
superuser password); the proxy has no env file.

```sh
cd ~/Projects/sites/database
docker compose --env-file prod.env up -d     # likewise: down, exec -T postgres psql

cd ~/Projects/sites/proxy
docker compose up -d
```

The database files are in `database/data/`.

Each service provides a Docker network named after its directory, `database_network` and
`proxy_network`. A site's container joins both. On `proxy_network` its alias is its
`COMPOSE_PROJECT_NAME` from `docker/prod.env`; nginx proxies to that alias on port 8000.

### Adding a site

`new_site.md`, chapter 7, has the full steps. On the host, from the site's directory:

```sh
export ENV=prod                         # once per session; dm and the scripts read it
../database/register-site ../<site>     # the site's role and database, from docker/prod.env
./dm docker compose build
./dm docker compose up -d               # loads docker/init.sql.gz, migrates, serves
../proxy/issue-cert ../<site>           # the site's certificate
../proxy/register-site ../<site>        # the site's nginx config
```

### Certificates

- `proxy/issue-cert <site-dir>` issues the certificate for the site's domain and its
  subdomains listed in `ALLOWED_HOSTS`, under the site's own Let's Encrypt account
  `mail@<site>`, registered on first use. Account and certificate live in the site's
  `docker/certbot/`. `fullchain.pem` and `privkey.pem` are copied to `proxy/certs/<site>/`,
  the only certificate material the proxy holds.
- `proxy/register-site <site-dir>` writes `proxy/sites/<site>.conf` for the site's
  `ALLOWED_HOSTS` without bare IP addresses and reloads nginx. Run it after `issue-cert`.
- `proxy/update-cert <site-dir>` renews the certificate within 30 days of expiry, refreshes
  the proxy's copy and reloads nginx. Run it daily.

### Updating a site

On the host, in the site's directory:

```sh
export ENV=prod
git pull
npm --prefix frontend install
./dm build                              # frontend and static files, built on the host
./dm docker compose build
./dm docker compose up -d
```

Nothing is version-pinned. `./dm docker build --no-cache django` also refreshes the base
image and every dependency.

### Backups

It is advisable to have backups. Everything worth keeping is on the host's file system: the
database files, the sites' uploads, and their uncommitted secrets and certificates. The
easiest way is to copy the whole `sites` tree somewhere regularly.

**Open:** scheduling `update-cert`, deploy and rollback commands in `dm`.

## Database lifecycle (`init.sql.gz`)

Each site owns a prepared initial database state: `init.sql.gz`, a gzipped SQL
dump generated from a real Django-initialized database and committed in the site
repository. It is never written by hand.

- **Birth**: a programmer creates an empty database, runs the Django migrations,
  seeds the defaults (the dev admin account `admin`/`admin`), and dumps the
  result to `init.sql.gz`.
- **Dev**: a new programmer imports `init.sql.gz` into their PostgreSQL and runs
  `migrate`; migrations that landed after the dump move the imported state
  forward.
- **Live**: the first deployment initializes the site's production database from
  the same file; from then on only migrations change it.
- **Refresh**: live and dev databases drift away from the dump through
  migrations and real data. Regenerating `init.sql.gz` from a chosen database
  state is a deliberate team decision — it defines what a fresh developer
  environment contains. Nothing forces a refresh.

The dump imports into whatever PostgreSQL the site's environment points at: the
local non-Docker PostgreSQL in development or a Docker one in testing and
production.

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

## Frontend API calls

The site's endpoint functions live in `frontend/src/api/api.js` (imported as
`@api/api.js`): sign-in/sign-out, the auth ping, person loading, and the sign-in
and contact form submits. They are small functions built on `svultra/kit/api`
(aliased `@kit/api`), which provides the generic layer — the `apiRequest` fetch
wrapper (CSRF header, credentials, automatic aborting of superseded requests),
request cancellation, and the reCAPTCHA loader. New endpoints for a site go into
`frontend/src/api/api.js` as functions calling `apiRequest`.

## Sign-in

The starter ships passwordless, token-based sign-in. The **Sign in** button opens a
modal (`LoginForm`) that takes an email and POSTs to `/api/signin-request/` (reCAPTCHA-
guarded). If a `Person` with that email exists, the backend emails a link —
`/signin?token=<uuid>` — that hits `/api/token-login/` to establish the session. The
frontend then loads the person (`fetchUserInfo` → `/api/person/`) into `personStore`
and the nav swaps the button for a user menu with **Sign out**; `personStore` is
localStorage-backed, so a reload stays signed in.

`USER_LOGIN_ENABLED` (default `True`) gates the login API — with it off, the
`token-login` / `signin-request` / `person` routes aren't registered. It's backend-only
and doesn't touch the models or the frontend.

In dev the sign-in email prints to the backend console (Django's console email backend
while `DEBUG`), so you don't need a mail server; the `Person.signin_token` also shows in
the admin.

## Contact form

The starter ships a working contact form — a modal opened from the **Contact** link in
the nav and footer. It validates the name/email/message fields, runs reCAPTCHA, and
POSTs to `/api/contact/`. The backend (core's `ContactMessageView`) verifies the
reCAPTCHA token, rate-limits to 2 requests per minute, and saves a `ContactMessage`
record (with the sender's IP and user-agent).

## Admin

`djultra` generates Django admin classes for models that define an inner `Admin`
class. The starter uses that convention for `Person` and `ContactMessage`, keeping
their admin configuration next to the model while still letting `djultra` provide
the generated `ModelAdmin` base behavior.

## Time zones

Timestamps are stored and computed in UTC. `djultra` sets `TIME_ZONE = 'UTC'` (Django's own
default is `America/Chicago`), and `USE_TZ` is already true by default, so a site does not
set either. Convert to a local zone only when displaying a time to a user.

Override it per site with the `TIME_ZONE` environment variable or `CONFIG_FILE` if a
deployment genuinely needs a different default.

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
