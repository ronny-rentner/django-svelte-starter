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
- `ALLOWED_HOSTS` — add `<domain>`, keeping `localhost` and `127.0.0.1`.

## 3. Rebrand

Replace the starter's name in the logger key in `backend/config/settings.py`, the package
name in `backend/pyproject.toml`, the page titles in `backend/core/templates/index.html` and
`frontend/index.html`, and the launcher name and absolute path in `cli/startdev.desktop`:

```sh
grep -rn "django-svelte-starter\|Django Svelte Starter" . --exclude-dir={.git,node_modules,venv}
```

Leave `frontend/package.json` untouched — the build manages its `version`.

Then the site's own content and assets:

- `frontend/src/pages/Home.svelte`, `FAQ.svelte`, `About.svelte`, `Landing.svelte`
- `frontend/src/components/layout/Footer.svelte` — social links, the `/imprint`, `/terms`
  and `/privacy` links, the copyright line
- `backend/config/templates/emails/footer.html` — the imprint placeholder
- `frontend/src/assets/favicon.svg`

Then the docs: rewrite `readme.md` for the site, replace `starter_todo.md` with the site's
own list, and delete this guide.

## 4. Set up the environment

```sh
python3 -m venv backend/venv
backend/venv/bin/pip install -r backend/packages.txt
npm --prefix frontend install
psql -h localhost -p 5433 -U postgres -c "CREATE USER <site> WITH PASSWORD '<password>';"
psql -h localhost -p 5433 -U postgres -c "CREATE DATABASE <site> OWNER <site>;"
psql -h localhost -p 5433 -U postgres -c "ALTER ROLE <site> SET timezone TO 'UTC';"
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
- the **Contact** modal submits and the message appears in `/admin/`;
- **Sign in** with the superuser's email prints a `/signin?token=…` link to the backend
  console; following it signs in, and the subject reads `Sign in to <Site>`.

Then `./dm build` completes and writes `static/frontend/manifest.json`.

Finally:

```sh
grep -rn "dss\|django-svelte-starter" . --exclude-dir={.git,node_modules,venv}
```

Only `frontend/package.json` and the migration filenames should match.

## 6. Commit

```sh
git add -A && git commit -m "Rename to <Site>"
git remote add origin <url> && git push -u origin main
```

## 7. Going live

Not covered here; the site is a working development checkout at this point. `readme.md`'s
hosting section records the current plan, which is not yet verified.
