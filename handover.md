# Handover, 2026-09-16

Session on django-svelte-starter (`~/Projects/django-svelte-starter`), the second site aylinschaer.de
(`~/Projects/sites/aylinschaer.de`) and the shared repos djultra, svUltra, ultraclick and `~/Projects/sites`.
Host is yuki, sites live in `~/Projects/sites/<domain>` there, deploy is
`ssh yuki 'export ENV=prod && cd ~/Projects/sites/<site> && ./dm pull && ./dm build && ./dm docker deploy'`.

## What was done

### aylinschaer.de, all committed, pushed and live (last commit `550ed8f`)

- Home page: portrait (`aylin-schaer-portrait.webp`, cropped to the figure, 612×1335) and text as a centred pair,
  `grid-template-columns: auto minmax(0, 40rem)`, portrait 22rem wide with a 1rem top margin and a 2px
  `rgb(0 0 0 / 0.15)` ground line; the text column has `padding-bottom: 8rem` (0 on mobile) so the headline sits
  near her face. `RotatingHeadline.svelte`: all lines stacked in one grid cell at opacity 0/1 with a CSS transition,
  `align-self: end`, `padding-bottom: 0.15em` so the gradient covers descenders; the quotes experiment was dropped.
- About page: portrait `aylin-schaer-about.webp` on an offset slab in the site gradient, 1rem rounded corners,
  Pico shadow; bio table (`striped`, 1px black frame, Pico radius via `border-collapse: separate`, Oswald `Bio`
  header, emoji labels, top-aligned). Three education rows are `[Degree, university]` placeholders with LinkedIn's
  years (2010–2013, 2011–2012, 2007–2009); the About text is still the starter's example paragraph.
- `app.css`: `--pico-secondary: #0F7F71` (guide's green) for buttons and footer links; `--site-gradient-headline`,
  same as `--site-gradient` in light, lifted `hsl(172 79% 45%) → hsl(345 83% 60%)` in dark;
  `--pico-table-row-stripped-background-color` is 8% site red mixed into the table background (light theme).
  Note: `--pico-table-alt-background-color` in `app.css` is not a Pico variable, nothing reads it.
- Certificate: `../proxy/issue-cert .` and `../proxy/register-site .` ran on yuki, Let's Encrypt cert valid until
  2026-12-14, https://aylinschaer.de and www verify. The "To verify on the next site" note is gone from
  `new_site.md`. Still open: scheduling `proxy/update-cert` (todo).

### Starter, UNCOMMITTED in `~/Projects/django-svelte-starter`

- `new_site.md`: the verification note removed.
- `setup.md`: shell check import fixed to `backend.core.models`.
- `starter_todo.md`: four items removed (verification note, `register-site` message, `dm` error output, shell check).
- `cli/cli.py`:
  - `services()` wraps the JSON fetch in `try/except SystemExit` and prints
    `Listing the services failed with exit code N` before re-raising (verified: `ENV=nonexistent ./dm docker services`).
  - `MainGroup.__init__` sets `VIRTUAL_ENV` and prepends `sys.prefix/bin` to `PATH` so subcommands run in dm's venv.
    NOT yet verified; the planned check was `./dm updates show pip` against `backend/venv/bin/pip list --outdated`.
  - `pull` now is the git step followed by `ctx.invoke("updates.install", target="all")` (the user made the string
    form work in ultraclick, `acff5b9`); the three package lines are gone. The user reports `dm pull` works.
- `docker/django/Dockerfile.django`: `FROM python:3-slim` (was 3.12, copied from Relonee; host runs 3.13);
  pip installs with `--upgrade` and a BuildKit cache mount `--mount=type=cache,id=pip,target=/root/.cache/pip`
  instead of `--no-cache-dir`. The user is unsure about depending on BuildKit (it is Docker's default on yuki,
  26.1.5, no env var needed). Undecided: the layer only reruns when Docker rebuilds it, so without `--no-cache`
  nothing upgrades; the user said "no changes to deploy, only build", not resolved.
- `frontend/.npmrc`: `allow-git=root` added by the user (npm 12 `EALLOWGIT` workaround).
- `AGENTS.md`'s `./dm run all` stays (user decision), the todo line for it was not removed; check.

### Other repos

- `~/Projects/sites/database/register-site`: UNCOMMITTED, prints the site directory's name (`name=$(basename
  "$(realpath "$site_dir")")` before the `cd`) instead of the argument. Syntax-checked, not run.
- ultraclick `~/Projects/py/ultraclick`: `demo.py` has an uncommitted 6-line change by the user; `acff5b9` and
  `b2a6add` (0.2.7.dev1) are the user's commits. Nothing was changed in ultraclick by me; the earlier proposal to
  change its JSON branch was rejected: the contract stays.
- svUltra: `todo.md` note about `Main` having no full-width mode was committed (`65765ed`).
- carbon.berlin: untouched this session. It still has `backend/core/templates/index.html`, has no `starter` git
  remote, and needs the starter merged (docs, `FRONTEND_CONFIG`, login switch) and a rebuild that picks up the
  current djultra; that was deferred until the package-upgrade item is settled.

## Findings not yet in `starter_todo.md`

- Tests: `backend/core/tests.py` is Django's empty stub, 0 tests. `./dm django-admin test core` (the label in
  `AGENTS.md`) fails with `No module named 'core'`; `test backend.core` fails in unittest discovery
  (`TypeError: expected str … not NoneType`) because `backend/` has no `__init__.py`. Needs a decision.
- `dm --help` lists `group2` ("Subcommands for group2"), a demo leftover in `cli.py` (`GroupTwo`, `GroupDeep`).
- `updates` calls bare `pip` (lines ~755, 761, 776); with the venv `PATH` change it resolves to the venv's pip.

## Open tasks, in the order agreed

1. Verify the venv `PATH` change and the Dockerfile, decide the `--no-cache` question, then commit the starter
   (one commit), `sites/database/register-site`, and ultraclick's `demo.py` (user's).
2. Restart the dev servers after the user's package updates (only aylinschaer.de's Vite was running, no Django
   dev server); run what tests exist once the label question is settled.
3. Merge the starter into carbon.berlin, delete its template copy, rebuild on yuki.
4. Continue `starter_todo.md` item by item, presenting each before fixing: remaining small fixes
   (`staticfiles.W004`), then the guide pass over `setup.md`/`new_site.md`/`AGENTS.md`, then the design items
   (one domain variable, `prod.env`/`prod_django.ini` rework, `dm` loading `prod.env` under `ENV=prod`,
   `config()` for `DATABASES`, self-signed cert out of the box, certbot layout, cache headers for unhashed
   assets, Vite font hot reload, django-tasks worker).
5. Schedule `proxy/update-cert` on yuki before 2026-11-06 (carbon.berlin's renewal window).

## Working rules learned this session (beyond `~/.claude/CLAUDE.md`)

- Present each todo item first, then fix it; one item at a time.
- Do not change a library's contract (ultraclick) to suit a caller; fix the caller. Read the source before proposing.
- Follow the file's local style (`ctx.invoke(self.<command>, …)`, `click.run([...], headline=...)`); write the
  target state in one edit, do not remove lines one by one.
- No commits without being told; no tiny commits; commit messages are one line, no links, no attribution.
- Use own browser tabs (`browser_manage_tabs open`, close after); the theme toggle persists in the browser, toggle
  it back.
- Redirect long command output to the scratchpad and read the file; never pipe through `head`/`tail`/`grep`.
