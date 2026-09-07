# Creating a new site from this starter

**Status: in progress — this guide has not yet been followed end to end. Correct it while
following it.**

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

## 2. Configure the site

In `backend/config/settings.py`:

- `DATABASES` — replace `dss` with `<site>` as the database name and user, and set a
  password. Step 4 creates the database itself.
- `ALLOWED_HOSTS` — replace `example.com` with `<domain>`.

## 3. Rebrand

- `backend/core/templates/index.html` — the `<title>`
- `frontend/index.html` — the `<title>`
- `frontend/src/pages/Home.svelte` — the `title` in `pageConfig`
- `cli/startdev.desktop` — `Name=` and the path in `Exec=`

## 4. Set up the environment

Create the role and the database with the password from step 2:

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

## 5. Run and check

```sh
./dm run back      # Django, the task worker and the fastmanage daemon
./dm run front     # Vite on port 5173
```

At `http://localhost:5173`:

- the home page renders with the new brand;
- the **Contact** modal submits and the message appears in `/admin/`.

The contact endpoint alone, without the modal:

```sh
curl -X POST http://localhost:8000/api/contact/ -H 'Content-Type: application/json' \
  -d '{"name":"Check","email":"check@example.com","message":"Setup check","recaptcha":"test"}'
```

It answers `{"detail":"Your message has been sent!"}`, and the record is stored:

```sh
./dm django-admin shell -c "from core.models import ContactMessage; print(ContactMessage.objects.values().last())"
```

At `http://localhost:8000/admin/`, the superuser from step 4 signs in.

Then `./dm build` completes and writes `static/frontend/manifest.json`.

Finally:

```sh
grep -rn "dss\|django-svelte-starter" backend cli frontend/src --exclude=*.md --exclude-dir=node_modules
```

It finds nothing once steps 2 and 3 are done. The docs keep their references to the
starter, and `frontend/package.json` keeps its name.

## 6. Commit

```sh
git add -A && git commit -m "Rename to <Site>"
git remote add origin <url> && git push -u origin main
```

## 7. Going live

The live host runs the shared services from `~/Projects/sites`: `database` (PostgreSQL)
and `proxy` (nginx). Both are already running there; this chapter adds one site to them.

Prepare the deployment files in the site, and commit them:

- `docker/prod_django.ini` — `ALLOWED_HOSTS` and the three `FRONTEND_*` URLs, for
  `<domain>` and every alias the site answers to. The proxy serves exactly these names,
  minus any bare IP addresses.
- `docker/init.sql.gz` — the site's initial database state:

  ```sh
  ./dm django-admin dump_db --dump-file docker/init.sql
  gzip -9 docker/init.sql
  ```

Then `docker/prod.env`, copied from `docker/prod.env.example` and filled in with a
generated `DB_PASSWORD` and `SECRET_KEY`. It is not committed, so it has to reach the
host another way:

```sh
scp docker/prod.env <host>:Projects/sites/<site>/docker/prod.env
```

On the host, as the deploying user:

```sh
git clone <url> ~/Projects/sites/<site>
cd ~/Projects/sites/<site>
python3 -m venv backend/venv
backend/venv/bin/pip install --group backend/pyproject.toml:main
npm --prefix frontend install
./dm build                                   # static/frontend and static/collected
../database/register-site ../<site>          # the site's role and database
./dm --env prod docker compose build
./dm --env prod docker compose up -d         # loads init.sql.gz, migrates, serves
../proxy/issue-cert ../<site>                # the site's Let's Encrypt certificate
../proxy/register-site ../<site>             # copies it to the proxy, writes the nginx config, reloads
```

The order matters: the site's nginx config references its certificate and resolves the
container's alias when it loads, so the certificate and the container must exist first.
`issue-cert` needs `<domain>` and `www.<domain>` to resolve to the host, and port 80
reachable from the internet.

Renewal is `../proxy/update-cert ../<site>`, run when due; scheduling it is still open.

## Temporary notes

A site installs `svUltra` and `djultra` from GitHub, which is what a live host does.
While they are still being changed alongside the sites, point a development checkout at
the local copies instead — and keep both changes out of the site's commits:

- `frontend/package.json` — `"svultra": "file:../../../js/svUltra"`, one level deeper
  than the starter's path, because a site lives one directory further down.
- After installing the backend dependencies:
  `backend/venv/bin/pip install -e ~/Projects/py/djultra`.
