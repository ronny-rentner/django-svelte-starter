# django-svelte-starter

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
