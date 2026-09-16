# Setting up a site

From the starter to a running site, step by step. Placeholders: `<site>` is the directory
and database name (lowercase, e.g. `example`), `<Site>` the display name, `<domain>` the
public domain.

## 1. Copy the starter

```sh
git clone <starter-url> <site>
cd <site>
rm -rf .git
git init && git add -A && git commit -m "Initial commit from django-svelte-starter"
```

## 2. Remove the starter's own material

1. Delete `new_site.md`, `development.md` and `starter_todo.md`.
2. In `AGENTS.md`, delete the section "Starter extraction".

## 3. Configure the site

In `backend/config/settings.py`:

1. `DATABASES` — replace `dss` with `<site>` as the database name and user. For local
   development, the password can be the site name.
2. `ALLOWED_HOSTS` — replace `example.com` with `<domain>`.
3. `EMAIL_HOST` — the site's mail relay. Its login goes into `docker/prod.env` in step 8.
4. `PROJECT_NAME` — replace `django-svelte-starter` with the site's name as a string.

## 4. Rebrand

1. `frontend/index.html` — the `<title>`.
2. `frontend/src/pages/Home.svelte` — `title` and `description` in `meta()`.
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

Python 3, Node.js, git and PostgreSQL on port 5433 are installed. Create the role and the
database:

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
   ./dm django-admin shell -c "from backend.core.models import ContactMessage; print(ContactMessage.objects.values().last())"
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

## 8. Deploy

The site runs as a Docker container. By default, the container is reached through the
Docker network `proxy_network` under its `COMPOSE_PROJECT_NAME` on port 8000, where a
reverse proxy serves `<domain>`; the database is a PostgreSQL server reached as `postgres`
on `database_network`, holding the role and database named in `docker/prod.env`. Both
networks exist before the container starts. If you want to run without a proxy, you can
publish the port with a `ports:` entry in `docker/docker-compose.yml`.

### Deployment files

Prepare them in the site, and commit them:

1. `docker/prod_django.ini` — `ALLOWED_HOSTS` and the three `FRONTEND_*` URLs, for
   `<domain>` and every alias the site answers to, such as `www.<domain>`.
   `DEFAULT_FROM_EMAIL` — the sender of the site's mails.
2. `docker/init.sql.gz` — the site's initial database state:

   ```sh
   ./dm django-admin dump_db --dump-file docker/init.sql
   gzip -9 docker/init.sql
   ```

### On the host

As the deploying user:

```sh
export ENV=prod                              # once per session; dm reads it
git clone <url> <site>
cd <site>
```

### Secrets

`docker/prod.env` holds the secrets. It is in `.gitignore` and must not be committed. To set
it up in the clone:

1. Copy `docker/prod.env.example` to `docker/prod.env`.
2. Replace all values.

### Start

In the clone:

```sh
python3 -m venv backend/venv
backend/venv/bin/pip install --group backend/pyproject.toml:main
npm --prefix frontend install
./dm build                                   # static/frontend and static/collected
./dm docker deploy                           # builds the image and starts it
```

The container waits for the database, loads `docker/init.sql.gz` into it when it is empty,
runs the migrations, starts the task worker and serves on port 8000. The reverse proxy then
serves `<domain>`.
