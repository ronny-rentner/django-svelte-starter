# Current Work Handoff

**Status: transient handoff, not canonical project documentation**

Snapshot date: 2026-08-01

This file records the state of the current starter and hosting work for another
model/session. Hosting is unfinished and unverified. `readme.md` remains the
canonical project documentation; do not convert the material below into settled
documentation until both hosting modes work end to end.

## Executive Summary

The main goal is to launch three new sites as soon as possible and make
`django-svelte-starter` ready to serve as their actual starting point. The starter
can continue improving while those sites are built; it does not need to become a
perfect framework before site 1 starts.

The immediate task became production hosting. The intended layout is:

```text
~/Projects/sites/
├── host/          shared host infrastructure
├── site-one/      a site cloned from django-svelte-starter
├── site-two/
└── site-three/
```

The shared host is intended to own nginx, TLS certificates, PostgreSQL, backups,
and the explicit inventory of hosted sites. Each site remains an independent
project cloned from the starter and owns its Django/Svelte application,
configuration, migrations, initial database dump, and application data.

The work is not complete. The central nginx extraction is partly implemented,
but the central PostgreSQL image is currently broken, the starter still has no
Docker deployment files, no site has been registered, and nothing has been built
or started.

## Main Product Goal

The user explicitly defined the real priority:

- Launch three new sites quickly.
- Bring the starter into a state suitable for beginning site 1.
- Learn from those three real sites and feed useful improvements back into the
  starter.
- Do not spend disproportionate time polishing starter homepage copy or demo
  content before deployment is usable.
- Clarify and implement live hosting before the first launch.

This means every proposed abstraction should be judged by whether it helps clone,
configure, deploy, and operate several real sites. Avoid building speculative
framework machinery.

## Repository Roles

### `django-svelte-starter`

This is the extraction target and the reusable site template. It is not a control
repository for Relonee and not a throwaway demo. New sites are expected to begin
as copies/clones of this project.

The starter already owns:

- the site Django project and site models/endpoints;
- the site Svelte pages and components;
- the current `dm` launcher and its Python CLI;
- development/build commands;
- the integration with `djultra` and `svUltra`.

Site-side deployment belongs here. If the starter lacks a deployment feature, the
first choice is to implement it in the starter using its existing architecture.
Relonee may supply a proven file or approach when that is genuinely the cleanest
extraction, but Relonee is a reference rather than the new source of truth.

### Relonee

Relonee is the original product and evidence for successful implementation
choices. Its deployment files were inspected because the user explicitly required
the new setup to preserve the important parts of the proven stack.

Relevant source paths:

- `/home/ronny/Projects/Relonee/docker/docker-compose.yml`
- `/home/ronny/Projects/Relonee/docker/django/Dockerfile.django`
- `/home/ronny/Projects/Relonee/docker/django/entrypoint.sh`
- `/home/ronny/Projects/Relonee/docker/nginx/Dockerfile.nginx`
- `/home/ronny/Projects/Relonee/docker/nginx/templates/proxy.conf.template`
- `/home/ronny/Projects/Relonee/docker/postgres/Dockerfile.postgres`
- `/home/ronny/Projects/Relonee/docker/postgres/init-db.sh`
- `/home/ronny/Projects/Relonee/docker/postgres/init.sql.gz`
- `/home/ronny/Projects/Relonee/dm`
- `/home/ronny/Projects/Relonee/Relonee/core/management/cli.py`

Do not copy Relonee product data, domains, service names, or application-specific
helpers into the starter merely because they exist there.

### `~/Projects/sites/host`

This is the separate shared-infrastructure directory created during this work.
It is not currently a Git repository. It should stay focused on host-level
infrastructure and site registration, not become another copy of the starter or
Relonee application CLI.

## Explicit Decisions And Corrections

### Starter First

The user explicitly corrected the implementation direction:

- Use the starter as the basis for each new site.
- Only copy something from Relonee into the starter when the starter is incomplete
  and copying/adapting the proven piece is the best judgment call.
- Fix missing or broken starter behavior directly when that is simpler.
- Do not build host management around Relonee's obsolete `make` helper.
- Do not copy Relonee's application-specific `dm` into the host.
- The starter already contains the current `dm` and Docker command support; use and
  extend that path for site deployment.

### Host Placement

The chosen filesystem layout is `~/Projects/sites/host` for shared services, with
future site repositories as siblings under `~/Projects/sites/`.

The shared-host direction exists because running ten independent nginx reverse
proxies and ten independent PostgreSQL containers on one machine is unnecessary.
The shared services must still support a dedicated server containing only one
site.

### Two Hosting Modes

The user explicitly requires two usable modes:

1. A copied starter is the only site on a host and needs nginx, TLS, and PostgreSQL.
2. A copied starter is one of several sites and must use central nginx and central
   PostgreSQL instead of starting another copy of those services.

The exact Compose-file/profile design has not been decided or implemented. Do not
silently collapse the requirement to one mode. A plausible direction is a common
site service plus standalone and shared overlays, but this remains an open design
decision that must be tested against the existing `dm` command construction.

### Site-Owned `init.sql.gz`

This is the most important database correction from the session.

The user explicitly stated that `init.sql.gz` in the starter serves the same
purpose as `init.sql.gz` in Relonee. It is the prepared initial database state for
that site, not an obsolete Relonee-only migration artifact and not something to
replace automatically with an empty database plus migrations.

Required invariant:

- In standalone mode, the site's PostgreSQL image imports the site's
  `docker/postgres/init.sql.gz` when its volume is first initialized.
- In shared mode, provisioning a new central database must import that same
  site-owned dump into the newly created database.
- Django migrations then move that imported state forward.
- A new site cloned from the starter begins with the starter's dump; as that site
  develops, it may acquire its own initial/current dump.

Relonee's actual 49 MB database dump must not be used as the starter's dump. It was
temporarily copied into the host and then deleted after the user rejected that
approach. The starter needs its own database dump.

The exact source/content of the starter dump has not been verified. An attempted
read-only query of the local `dss` PostgreSQL database on port 5433 did not run
inside the sandbox, and the escalated retry was aborted. Do not claim that the
local database is suitable until its contents have been inspected for product or
personal data.

### Central Settings, Minimal Site Proxy Files

The user explicitly rejected per-site nginx files that repeat settings. Keep as
many settings as possible in central snippets. A per-site proxy configuration
should contain only values that genuinely differ, such as:

- the unique Docker network alias/upstream;
- domain names;
- certificate name/path;
- the actual proxy target;
- an explicitly chosen canonical-domain redirect, if the site wants one.

The per-site file is a proxy configuration, so the template is named
`proxy.conf.template`, not `site.conf.template`.

### Tooling And File Operations

The user prefers copying proven files with `cp` and then patching them in place.
When only a coherent range from a large source file is needed, the user explicitly
suggested extracting those lines with `sed` into the destination instead of
copying hundreds of irrelevant lines and creating a massive deletion patch.

Do not copy the obsolete Relonee `make` helper. It predates `dm` and contains
Relonee-specific commands, database volume names, domains, DocuSeal commands, and
other unrelated operations.

## Frontend And Homepage Decisions Already Learned

Although hosting is now the priority, earlier session work established page-style
rules that should not be rediscovered.

- A homepage is a real visitor-facing page, not a component showcase.
- The main headline belongs directly in the page/hero, not inside a card.
- Start from what the page must communicate or let the visitor do.
- PicoCSS is the semantic baseline. Check Pico's supported structures before
  proposing custom wrappers or random elements.
- Use semantic `main`, `section`, `hgroup`, headings, paragraphs, lists, `article`,
  `header`, `footer`, forms, and Pico variables/classes first.
- `Card` is appropriate for genuinely contained/repeated items; it maps to an
  `article` and its header slot is rendered as a real card header. Do not speculate
  about component markup without checking it.
- `IconWithLabel` is the settled component name. A proposed `Label` alias with an
  icon prop was rejected.
- Inline `<markdown>` is appropriate inside a complex page when it removes prose
  boilerplate without hiding the overall page layout.
- A separate `Home.md` would be the correct filename if the homepage became a
  standalone markdown document, but the current homepage intentionally uses
  inline markdown and there is no `frontend/src/markdown/Home.md`.
- Custom CSS is allowed only for a concrete content/layout reason. Random padding,
  margins, widths, and styling for the sake of styling were explicitly rejected.
- Do not make svUltra or internal extraction history the subject of visitor copy.
- Do not describe Django routes as "the API". Django provides the API and admin
  dashboard; automatic API/admin behavior matters more than the HTML shell.
- Do not invent product terms such as `djultra` in visitor-facing copy.
- The starter homepage remains low priority compared with making the starter
  deployable.

These rules are recorded in the `Frontend Page Style` section of `AGENTS.md`.

## Current Starter State

### Git State

At the snapshot, `main` is three commits ahead of `origin/main`:

```text
7208921 Add Admin config for Person/ContactMessage; document admin convention and hosting plan; stub Home working section
02087ce Queue API wrapper extraction from Relonee into svUltra
d0554a5 Rebuild Home as starter landing page; document sign-in and page-style guidance; prune done todos
```

Current dirty files:

```text
M  AGENTS.md
M  frontend/package.json
M  frontend/src/App.svelte
M  frontend/src/api/api.js
M  frontend/src/build-info.json
M  frontend/src/components/ContactForm.svelte
M  frontend/src/components/LoginForm.svelte
M  readme.md
M  starter_todo.md
?? screenshots/
```

These changes must be preserved. Do not reset, restore, stash, or overwrite them.
Some are from earlier frontend/API extraction work and are unrelated to unfinished
hosting.

### Existing Hosting Documentation

`readme.md` currently has a `Live hosting plan (in progress)` section. It records:

- production uses one real origin behind a reverse proxy;
- shared deployment work lives under `~/Projects/sites/host`;
- future sites live beside `host` under `~/Projects/sites/`;
- the concrete first-site setup is still unfinished;
- TLS, process management, PostgreSQL, static/media, backups, email, reCAPTCHA,
  deployment, rollback, and environment-specific configuration still need a
  verified path.

The user explicitly instructed: do not update hosting documentation incrementally.
Finish and verify hosting, then update the docs once with the real outcome.

`starter_todo.md` still contains the live-hosting task. Do not remove it until the
verified outcome is documented in `readme.md`.

### Existing `dm`

The starter's `dm` is the current site command entry point:

- `/home/ronny/Projects/django-svelte-starter/dm`
- it launches `/home/ronny/Projects/django-svelte-starter/cli/cli.py` through
  `backend/venv/bin/python`;
- the CLI already contains `DockerCommand`;
- its Docker Compose command currently expects
  `./docker/docker-compose.yml` and `./docker/<ENV>.env`;
- it supports forwarding arbitrary Compose arguments through
  `./dm ... docker compose ...` and has a Docker build path.

The site deployment design must fit this existing command path or improve it
directly. Do not create a parallel site helper.

### Starter Docker State

`/home/ronny/Projects/django-svelte-starter/docker/` exists but is completely
empty. No site Dockerfile, Compose file, environment template, nginx config,
PostgreSQL image, entrypoint, media/static volume setup, or database dump has been
added.

Consequently, neither standalone nor shared hosting is implemented in the
starter.

### Known Clean-Build Dependency Problems

These were discovered while inspecting what a Django site image would need:

- `backend/packages.txt` does not install `djultra`. The local venv currently sees
  it as an editable package from `/home/ronny/Projects/py/djultra`.
- Relonee installs `djultra` from its GitHub repository in `packages.txt`; whether
  the starter should do the same must be decided and tested.
- `frontend/package.json` currently declares
  `"svultra": "file:../../js/svUltra"`. That works in Ronny's local Projects
  layout but is not self-contained for an arbitrary production build context.
- `static/frontend/` is generated and ignored by Git. A production image must
  either build the frontend or receive a verified host-built frontend bundle.
- No frontend lockfile was found in `frontend/`.

A Docker image that merely copies Relonee's Django Dockerfile will not be a clean
starter deployment until these dependencies and build artifacts are handled.

### Current Homepage

The homepage is `/frontend/src/pages/Home.svelte`. It contains:

- a direct hero headline and copy;
- Pico-style sections;
- `Card` and `IconWithLabel` feature items;
- inline `<markdown>` for prose/list sections;
- an intentionally unfinished `What is already working` section containing
  `TODO` and two placeholders.

There is no `frontend/src/markdown/Home.md`; `frontend/src/markdown/` currently
contains only `guide.md`.

The user explicitly deprioritized further starter-content detail work.

## Current Shared Host State

All host files are outside the starter Git repository under:

```text
/home/ronny/Projects/sites/host
```

The directory is not currently version-controlled and has no `.gitignore`, README,
environment file, or secret-management setup.

### Current Tree

```text
host/
├── make
└── docker/
    ├── docker-compose.yml
    ├── nginx/
    │   ├── Dockerfile.nginx
    │   ├── templates/proxy.conf.template
    │   ├── sites/proxy.conf.template
    │   ├── snippets/acme.conf
    │   ├── snippets/proxy.conf
    │   ├── snippets/server.conf
    │   ├── snippets/ssl.conf
    │   └── var/www/html/
    └── postgres/
        ├── Dockerfile.postgres
        ├── init-db.sh
        ├── backups/
        └── sites/
```

There is no `host.env`, no `init.sql.gz`, no real site `*.conf`, no certificate
directory, and no host `dm`.

### Compose File

`/home/ronny/Projects/sites/host/docker/docker-compose.yml` currently defines:

- `nginx`, publishing host ports 80 and 443;
- `certbot` behind a `tools` profile;
- `postgres` with a named `postgres_data` volume;
- named Docker networks `sites_proxy` and `sites_postgres`;
- PostgreSQL tuning copied from Relonee:
  `shared_buffers=256MB`, `work_mem=128MB`, and `shm_size=256mb`;
- PostgreSQL host-side backup directory mounted at `/backups`;
- PostgreSQL network alias `postgres`;
- a healthcheck using container `POSTGRES_USER`/`POSTGRES_DB`.

The Compose file requires `./host.env`, which does not exist. It has never passed
`docker compose config`.

No site service currently joins either shared network.

### Nginx Work That Landed

The nginx configuration was extracted from Relonee and substantially reduced.

`Dockerfile.nginx` now:

- uses `nginx:mainline`;
- removes the official image's default `conf.d/default.conf`;
- copies central templates and snippets;
- creates certificate and `sites-enabled` directories.

The commented experimental apt/Brotli/Certbot installation block from Relonee was
removed. The user initially questioned that removal, then confirmed those lines
were only comments and said to continue.

The rendered central template:

```text
docker/nginx/templates/proxy.conf.template
```

- includes `/etc/nginx/sites-enabled/*.conf`;
- provides a port-80 default server;
- serves ACME challenges through the central snippet;
- returns 404 for unmatched requests;
- allows nginx to start before a site or certificate is registered, assuming the
  rest of the image/config is valid.

Central snippets preserve Relonee's actual settings:

- `server.conf`: 50 MB client body limit and gzip settings;
- `ssl.conf`: TLS 1.2/1.3 and copied cipher settings;
- `proxy.conf`: forwarded headers, redirect behavior, retry conditions, and
  connect/read/send timeouts;
- `acme.conf`: Certbot webroot challenge location.

The per-site template is:

```text
docker/nginx/sites/proxy.conf.template
```

It contains placeholders:

- `SITE_UPSTREAM`
- `SITE_DOMAINS`
- `SITE_CERTIFICATE`

It includes central settings instead of repeating them. It currently preserves
the requested host when redirecting HTTP to HTTPS; no canonical-domain policy has
been chosen.

No nginx configuration has been rendered, built, or checked with `nginx -t`.
Potential syntax/runtime issues remain untested.

### PostgreSQL Work Is Currently Broken

The current host PostgreSQL Dockerfile still contains:

```dockerfile
COPY ./init.sql.gz /docker-entrypoint-initdb.d/init.sql.gz
```

but `/home/ronny/Projects/sites/host/docker/postgres/init.sql.gz` does not exist.
Therefore the host PostgreSQL image cannot build in its current state.

This mismatch exists because:

1. The Relonee Dockerfile and `init-db.sh` were copied into the host.
2. The `COPY init.sql.gz` line was initially removed after the file appeared
   absent from an `rg --files` result. That reasoning was wrong because ignored
   files can be omitted and, more importantly, necessity should be judged by the
   required behavior rather than current presence.
3. Relonee's actual 49 MB dump was then found and copied into the host.
4. The user correctly rejected copying Relonee's database for the starter.
5. The copied dump was deleted successfully.
6. A later patch intended to remove the dump from the generic host image was
   interrupted and established no change.

The current `init-db.sh` is still the Relonee version. It checks only the bootstrap
`POSTGRES_USER` and `POSTGRES_DB`, both of which the official PostgreSQL entrypoint
already creates. It does not provision later sites and its SQL-load commands are
commented out.

The empty `docker/postgres/sites/` directory is a leftover from an abandoned
speculative site-bootstrap direction. Nothing reads it.

The current shared database design therefore does not yet answer how a new site's
role/database is created or how that site's own `init.sql.gz` is imported.

### Host Helper State

`/home/ronny/Projects/sites/host/make` is an unchanged copy of Relonee's obsolete
8 KB helper. It is the wrong helper and should not be used. It contains Relonee
domains, product commands, old database volume names, and unrelated services.

Two attempts to copy a `dm` helper into `host` were interrupted. No host `dm`
exists. Do not resume either attempt:

- do not copy `make` to `dm`;
- do not copy Relonee's current application-specific `dm`/CLI into `host`;
- do not ignore the starter's existing `dm` for site-side deployment.

The old host `make` file should eventually be removed as rejected copied debris,
but only while deliberately finalizing the host command surface.

## Relonee Deployment Evidence

### Relonee Compose Shape

Relonee's Compose stack contains:

- a Django/Gunicorn service;
- an nginx reverse proxy;
- a PostgreSQL service with a named volume;
- DocuSeal and Anaprint product services;
- separate Docker networks;
- env-file-driven database settings;
- PostgreSQL health gating before Django starts.

Only the generic Django/nginx/PostgreSQL approach is relevant to the starter.
DocuSeal, Anaprint, Relonee domains, and product-specific networks must not be
copied by default.

### Relonee Nginx Settings Preserved Centrally

The host snippets currently preserve:

```nginx
client_max_body_size 50M;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers HIGH:!aNULL:!MD5;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header Host $host;
proxy_redirect off;
proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
proxy_connect_timeout 1s;
proxy_read_timeout 30s;
proxy_send_timeout 30s;
```

The gzip MIME types and compression values were also copied exactly.

### Relonee Database Dump Facts

Relonee's `init.sql.gz` is approximately 49 MB. Inspection established:

- it is a gzip-compressed plain SQL `pg_dump`;
- it was dumped from PostgreSQL 16.4 using `pg_dump` 17;
- it does not contain `CREATE DATABASE` or `CREATE ROLE` statements;
- no ownership statements were found in the inspected dump;
- it is loaded into the database selected by `POSTGRES_DB` through the official
  PostgreSQL entrypoint.

These facts describe the mechanism. The Relonee data itself is not suitable for
the starter.

### Relonee Django Image Issues To Adapt, Not Copy Blindly

Relonee's Django image:

- uses a different project layout and WSGI module;
- waits for a service named `db`;
- runs migrations and a database task worker;
- installs several product-specific system packages;
- assumes its own `packages.txt` and static build process.

The starter's WSGI module is `config.wsgi`, under `backend/`. A copied image must
be adapted to that layout and to the selected standalone/shared database hostname.

## Failed, Rejected, Or Superseded Approaches

Do not repeat these:

1. **Using Relonee's old `make` helper.** It has long been superseded by `dm` and
   is product-specific.
2. **Copying Relonee's current `dm` into the host.** The current file is only a
   launcher for Relonee's large application CLI and venv; it is not a standalone
   host utility.
3. **Treating `sites/host` as the main product.** The starter is what new sites
   will clone; site deployment must be completed there.
4. **Generating small nginx snippets by copying the entire large proxy file and
   deleting most of it.** Use `sed` extraction for coherent source ranges.
5. **Calling `init.sql.gz` unnecessary because migrations can create an empty
   schema.** The user explicitly requires the starter dump to serve the same
   prepared-initial-state purpose as Relonee's dump.
6. **Copying Relonee's actual database into the starter/host.** The mechanism is
   reusable; the product data is not.
7. **Judging required files by whether `rg --files` currently lists them.** Decide
   required behavior first, and remember ignored files may not appear.
8. **Updating hosting docs while implementation is unsettled.** Update once after
   end-to-end verification.
9. **Continuing to polish starter homepage content while deployment is blocked.**
   Hosting is the priority.
10. **Running broad system-status checks.** Inspect only runtime state required to
    configure or verify this deployment; unrelated system checks are not part of
    the task.

## Open Decisions

The next model should surface these explicitly rather than silently selecting a
large architecture:

1. **Compose layout for two modes.** Decide between overlays, profiles, or another
   minimal structure that works naturally with the starter's existing `dm`.
2. **Shared database provisioning interface.** Decide exactly how the central host
   creates a site role/database and imports the site's dump without storing a
   second copy of site secrets.
3. **Starter dump source.** Inspect the current starter database and decide what
   prepared state belongs in the starter dump. Ensure it contains no Relonee or
   personal data.
4. **Dump refresh workflow.** Decide how a site intentionally regenerates its
   `init.sql.gz`. Relonee has a Django `dump_database` command, but it uses
   `shell=True`, string-built commands, global `PGPASSWORD`, `sed`, and `grep`, and
   does not gzip the output. It should not be copied unchanged.
5. **Site Django image build.** Decide how to install `djultra`, build/include
   `svUltra` frontend assets, collect static files, run Gunicorn, run migrations,
   and start the task worker.
6. **Standalone nginx ownership.** Decide whether standalone mode embeds the same
   nginx configuration in the site or composes the host infrastructure beside it.
   The user requires a one-site host to receive nginx/TLS/PostgreSQL without
   manually inventing another deployment.
7. **Initial TLS workflow.** Define issuance order so nginx can answer ACME before
   an HTTPS site config references certificates that do not exist.
8. **Canonical domains.** Keep or redirect `www`/aliases only when each site
   explicitly chooses a canonical host.
9. **Backups and restore.** A mounted backups directory alone is not a backup
   system. Define commands/scheduling, retention, restoration, and off-host copy.
10. **Live environment templates.** Define site-specific values for Django secret,
    debug mode, hosts, URLs, DB credentials, email, reCAPTCHA, media/static, and
    network alias.
11. **Deployment and rollback.** Define build, migration, restart, health check,
    and rollback behavior before declaring hosting complete.
12. **Host repository lifecycle.** Decide when to initialize Git, what to ignore,
    and where untracked secrets/certificates/backups live.

## Recommended Next Sequence

This is a handoff recommendation, not a settled design:

1. Stop editing the central PostgreSQL image until the two-mode database flow is
   written down concretely in terms of files and commands.
2. Design the smallest Compose arrangement that gives the starter a site service
   plus standalone and shared modes through existing `dm`.
3. Copy/adapt Relonee's Django and PostgreSQL deployment files into the starter
   only where the starter is demonstrably missing them.
4. Put the required site-owned `init.sql.gz` path in the starter's PostgreSQL
   context.
5. Inspect the starter's current database safely and generate a starter-specific
   dump using a robust, non-shell-injection-prone command.
6. Implement shared-host database provisioning that imports that same dump into a
   newly created site database.
7. Finish the central host environment, remove the obsolete host `make`, and
   remove or repurpose the unused `postgres/sites` directory.
8. Build and validate the host Compose configuration.
9. Validate nginx with no sites, then with one real test registration.
10. Validate standalone site initialization from the dump.
11. Validate shared site initialization from the same dump and connectivity over
    `sites_postgres` and `sites_proxy`.
12. Verify migrations, task worker, Gunicorn, static frontend, admin, API, media,
    TLS, certificate renewal, backups, restore, and a deployment restart.
13. Only then update `readme.md` once and remove the completed hosting item from
    `starter_todo.md`.

## Verification Not Yet Performed

None of the following has been run successfully for the new hosting setup:

- `docker compose config`
- nginx image build
- PostgreSQL image build
- site Django image build
- container startup
- `nginx -t`
- PostgreSQL health check
- database import
- Django migrations in Docker
- task worker in Docker
- Gunicorn request
- shared-network DNS/connectivity
- HTTP request through nginx
- TLS issuance or renewal
- backup or restore
- standalone mode
- shared mode

Do not describe the setup as working until these checks pass.

## Definition Of Done For Hosting

Hosting is complete only when a fresh site clone can be configured and launched
through documented commands in both required modes:

- its own prepared `init.sql.gz` initializes the correct database;
- Django connects, migrates, runs its worker, and serves through Gunicorn;
- the built Svelte frontend and Django static/media behavior work;
- nginx reaches the correct site by domain;
- TLS can be issued and renewed;
- central PostgreSQL isolates sites by database/user;
- backups are created and a restore is demonstrated;
- a deploy/restart and rollback path are explicit;
- secrets and generated state are not committed;
- the final verified decisions are recorded once in `readme.md`.
