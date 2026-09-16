# Creating a new site

The values and decisions for `setup.md` on this side: where sites live, and the host they
run on.

**Status: in progress. Correct this file while following it.**

## Values for setup.md

- Step 1 — `<starter-url>` is `git@github.com:ronny-rentner/django-svelte-starter.git`;
  `<site>` is `~/Projects/sites/<site>`.
- Step 8 — the host is `<host>`; the site is cloned to `~/Projects/sites/<site>` there.

## The host

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

Step 8 of `setup.md`, with the host's scripts around it. On the host, in the site's clone,
after the secrets are set up:

```sh
export ENV=prod                              # once per session; dm and the scripts read it
python3 -m venv backend/venv
backend/venv/bin/pip install --group backend/pyproject.toml:main
npm --prefix frontend install
./dm build                                   # static/frontend and static/collected
../database/register-site ../<site>          # the site's role and database, from docker/prod.env
./dm docker deploy                           # builds the image and starts it: loads init.sql.gz, migrates, serves
../proxy/issue-cert ../<site>                # the site's Let's Encrypt certificate, copied to the proxy
../proxy/register-site ../<site>             # writes the nginx config, reloads
```

The order matters: the site's nginx config references its certificate and resolves the
container's alias when it loads, so the certificate and the container must exist first.
`issue-cert` needs `<domain>` and `www.<domain>` to resolve to the host, and port 80
reachable from the internet.

### Certificates

- `proxy/issue-cert <site-dir>` issues the certificate for the site's domain and its
  subdomains listed in `ALLOWED_HOSTS`, under the site's own Let's Encrypt account
  `mail@<site>`, registered on first use. Account and certificate live in the site's
  `docker/certbot/`. `fullchain.pem` and `privkey.pem` are copied to `proxy/certs/<site>/`,
  the only certificate material the proxy holds.
- `proxy/register-site <site-dir>` writes `proxy/sites/<site>.conf` for the site's
  `ALLOWED_HOSTS` without bare IP addresses and reloads nginx. It comes after `issue-cert`:
  the config references the certificate.
- `proxy/update-cert <site-dir>` renews the certificate within 30 days of expiry, refreshes
  the proxy's copy and reloads nginx. Run it daily.

**Open:** scheduling `update-cert`.

### Updating a site

On the host, in the site's directory:

```sh
export ENV=prod
./dm pull                               # git pull, then pip and npm install; `./dm pull <rev>` for a revision
./dm build                              # frontend and static files, built on the host
./dm docker deploy                      # image, then up -d
```

An older revision is deployed the same way, with `./dm pull <rev>` as the first step.
Nothing is version-pinned, so each `deploy` builds with the current release of every
dependency; `./dm docker build --no-cache django` also refreshes the base image.

### Backups

It is advisable to have backups. Everything worth keeping is on the host's file system: the
database files, the sites' uploads, and their uncommitted secrets and certificates. The
easiest way is to copy the whole `sites` tree somewhere regularly.

## Temporary notes

A site installs `svUltra` and `djultra` from GitHub, which is what a live host does.
While they are still being changed alongside the sites, point a development checkout at
the local copies instead — and keep both changes out of the site's commits:

- `frontend/package.json` — `"svultra": "file:../../../js/svUltra"`, one level deeper
  than the starter's path, because a site lives one directory further down.
- After installing the backend dependencies:
  `backend/venv/bin/pip install -e ~/Projects/py/djultra`.
