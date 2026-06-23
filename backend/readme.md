# Running backend commands

Backend tasks run through `./dm` ("django-manage"), the project's management
utility in the repo root. It wraps `django-admin` (the underlying `manage.py`
lives in `cli/`) and does more — running the dev servers, builds, and so on. It
executes inside `backend/venv` automatically, so the venv needs no manual
activation:

```sh
./dm django-admin check
./dm django-admin migrate
./dm django-admin createsuperuser
```

To run `django-admin` on its own, activate the venv with `smartactivate`
(activates `backend/venv` and puts `backend/` on `PYTHONPATH`), then point it at
the settings module:

```sh
source backend/venv/bin/smartactivate
DJANGO_SETTINGS_MODULE=config.settings django-admin check
```

# Development server

```sh
./dm run        # Django dev server + task worker + fastmanage daemon
./dm run front  # Vite frontend dev server
```

`./dm run` brings up the whole local backend in one command: the Django dev
server, a background `django-tasks` worker, and the fastmanage daemon. They run
as named processes (`django-dev-server`, `django-tasks-db-worker`,
`django-fastmanage-daemon`). The server auto-reloads on code changes — recreating
the worker and daemon cleanly on each reload, with no leftover processes — and
they all shut down together when you stop it.

## Instant management commands

With the dev server running, every `./dm django-admin <command>` is fast. Rather
than booting a fresh Python process and re-importing all of Django on each call,
the command runs inside the daemon's already-warm process — so `migrate`,
`shell`, `check` and friends feel instant. There is nothing to switch on: when
the daemon is up commands are fast, and when it is not they run normally.

See djultra's readme for how fastmanage works under the hood.

# Database initialization

```
CREATE DATABASE dss;
CREATE USER dss WITH PASSWORD 'dss';
GRANT ALL PRIVILEGES ON DATABASE dss TO dss;
ALTER ROLE dss SET timezone TO 'UTC';
```

# Create admin super-user

```
./dm django-admin createsuperuser
```
