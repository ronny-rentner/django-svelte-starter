# Creating a new site from this starter

**Status: in progress. Correct this guide while following it.**

The starter is self-contained and meant to be copied whole. A new site is a full copy with
its own git repository, its own database.

Placeholders below: `<site>` is the directory and database name (lowercase, e.g.
`example`), `<Site>` is the display name, `<domain>` is the public domain.

## 1. Copy the starter

```sh
git clone git@github.com:ronny-rentner/django-svelte-starter.git ~/Projects/sites/<site>
cd ~/Projects/sites/<site>
rm -rf .git
git init && git add -A && git commit -m "Initial commit from django-svelte-starter"
```

## 2. Remove the starter's own material

The copy keeps `readme.md` and `AGENTS.md`: they describe the site as much as the starter.
What describes only the starter goes:

1. Delete `new_site.md` and `starter_todo.md`.
2. In `AGENTS.md`, delete the section "Starter extraction".

## 3. Configure the site

In `backend/config/settings.py`:

1. `DATABASES` — replace `dss` with `<site>` as the database name, user and password. It is
   the local development database's; a real password never goes into `settings.py`. Step 5
   creates the database itself.
2. `ALLOWED_HOSTS` — replace `example.com` with `<domain>`.
3. `EMAIL_HOST` — the site's mail relay. Its login goes into `docker/prod.env` in step 8.

## 4. Rebrand

1. `backend/core/templates/index.html` — the `<title>`.
2. `frontend/index.html` — the `<title>`.
3. `frontend/src/pages/Home.svelte` — `title` and `description` in `meta()`.
4. `frontend/src/components/layout/Footer.svelte` — the copyright holder, the "Crafted
   with" line and the social links.
5. `frontend/src/assets/` — `logo.svg`, `logo-dark.svg` and `favicon.svg`.
6. `frontend/src/styles/app.css` — `--pico-primary`, `--pico-secondary` and the site font;
   the readme's "Styling" section describes both.
7. `frontend/src/markdown/Imprint.md` — the site's details in place of the example values.
8. `frontend/src/markdown/Privacy.md` — a privacy policy for the site. The starter's is a
   generated template with placeholders; the generator is linked at its end.
9. `frontend/src/markdown/Terms.md` — the site's terms. The starter ships the heading only.
10. `cli/startdev.desktop` — `Name=` and the path in `Exec=`.

## 5. Set up the environment

Create the role and the database:

```sh
sudo -u postgres psql -p 5433 <<'SQL'
CREATE USER "<site>" WITH PASSWORD '<password>';
CREATE DATABASE "<site>" OWNER "<site>";
SQL
```

Then install the dependencies and set up the database:

```sh
python3 -m venv backend/venv
backend/venv/bin/pip install --group backend/pyproject.toml:main
npm --prefix frontend install
./dm django-admin migrate
./dm django-admin createsuperuser
```

## 6. Run and check

```sh
./dm run back      # Django, the task worker and the fastmanage daemon
./dm run front     # Vite on port 5173
```

1. At `http://localhost:5173`, the home page renders with the new brand, and the
   **Contact** modal submits and the message appears in `/admin/`.
2. The contact endpoint alone, without the modal:

   ```sh
   curl -X POST http://localhost:8000/api/contact/ -H 'Content-Type: application/json' \
     -d '{"name":"Check","email":"check@example.com","message":"Setup check","recaptcha":"test"}'
   ```

   It answers `{"detail":"Your message has been sent!"}`, and the record is stored:

   ```sh
   ./dm django-admin shell -c "from core.models import ContactMessage; print(ContactMessage.objects.values().last())"
   ```

3. At `http://localhost:8000/admin/`, the superuser from step 5 signs in.
4. `./dm build` completes and writes `static/frontend/manifest.json`.
5. No starter name is left:

   ```sh
   grep -rn "dss\|django-svelte-starter" backend cli docker frontend/src --exclude=*.md --exclude-dir=node_modules
   ```

   It finds nothing once steps 3 and 4 are done. `frontend/package.json` keeps its name.

## 7. Commit

```sh
git add -A && git commit -m "Rename to <Site>"
git remote add origin <url> && git push -u origin main
```

## 8. Going live

The live host runs the shared services from `~/Projects/sites`: `database` (PostgreSQL)
and `proxy` (nginx). Both are already running there; this chapter adds one site to them.

### Deployment files

Prepare them in the site, and commit them:

1. `docker/prod_django.ini` — `ALLOWED_HOSTS` and the three `FRONTEND_*` URLs, for
   `<domain>` and every alias the site answers to, such as `www.<domain>`. The proxy serves
   exactly these names, minus any bare IP addresses. `DEFAULT_FROM_EMAIL` — the sender of
   the site's mails.
2. `docker/init.sql.gz` — the site's initial database state:

   ```sh
   ./dm django-admin dump_db --dump-file docker/init.sql
   gzip -9 docker/init.sql
   ```

### On the host

As the deploying user:

```sh
export ENV=prod                              # once per session; dm and the scripts read it
git clone <url> ~/Projects/sites/<site>
cd ~/Projects/sites/<site>
```

### Secrets

`docker/prod.env` holds the secrets. It is in `.gitignore` and must not be committed. To set
it up in the clone:

1. Copy `docker/prod.env.example` to `docker/prod.env`.
2. Replace all values.

### Deploy

In the clone:

```sh
python3 -m venv backend/venv
backend/venv/bin/pip install --group backend/pyproject.toml:main
npm --prefix frontend install
./dm build                                   # static/frontend and static/collected
../database/register-site ../<site>          # the site's role and database
./dm docker deploy                           # builds the image and starts it: loads init.sql.gz, migrates, serves
../proxy/issue-cert ../<site>                # the site's Let's Encrypt certificate, copied to the proxy
../proxy/register-site ../<site>             # writes the nginx config, reloads
```

The order matters: the site's nginx config references its certificate and resolves the
container's alias when it loads, so the certificate and the container must exist first.
`issue-cert` needs `<domain>` and `www.<domain>` to resolve to the host, and port 80
reachable from the internet.

**To verify on the next site:** `issue-cert` with the deploy hook has not run for a new
site yet. After it, `proxy/certs/<site>/` must hold `fullchain.pem` and `privkey.pem`, and
`register-site` must pass `nginx -t`. Remove this note once observed.

Renewal is `../proxy/update-cert ../<site>`, run when due; scheduling it is still open.

## Temporary notes

A site installs `svUltra` and `djultra` from GitHub, which is what a live host does.
While they are still being changed alongside the sites, point a development checkout at
the local copies instead — and keep both changes out of the site's commits:

- `frontend/package.json` — `"svultra": "file:../../../js/svUltra"`, one level deeper
  than the starter's path, because a site lives one directory further down.
- After installing the backend dependencies:
  `backend/venv/bin/pip install -e ~/Projects/py/djultra`.
