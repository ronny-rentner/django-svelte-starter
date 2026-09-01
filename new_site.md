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
- `LOGGING` — replace the `django-svelte-starter` logger key with `<site>`.

## 3. Rebrand

- `backend/core/templates/index.html` — the `<title>`
- `frontend/index.html` — the `<title>`
- `frontend/src/pages/Home.svelte` — the `title` in `pageConfig`
- `backend/pyproject.toml` — `name = "dss-backend"`
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
backend/venv/bin/pip install -e backend
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

## Temporary notes

`svUltra` and `djultra` are still being changed alongside the sites, so a site runs against
the local checkouts rather than the published packages. Two path changes are needed in
chapter 4, and both disappear once the libraries are pulled from GitHub:

- `frontend/package.json` — the `svultra` path needs one more level than the starter's,
  `file:../../../js/svUltra`, because a site lives one directory deeper.
- After installing the backend dependencies:
  `backend/venv/bin/pip install -e ~/Projects/py/djultra`.
