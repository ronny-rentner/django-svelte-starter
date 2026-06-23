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

## Backend management

Run the backend with `./dm run` — it starts the Django dev server together with a
`django-tasks` worker and the fastmanage daemon, so management commands such as
`./dm django-admin migrate` and `./dm django-admin createsuperuser` run in a warm
process and feel instant. See `backend/readme.md` for the backend command
reference and djultra's readme for the fastmanage internals.
