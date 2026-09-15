# Repository Guidelines

This site is built from django-svelte-starter. `readme.md` is the starter's manual — how the
site is run, built, configured and deployed — and stays as it came from the starter;
`setup.md` is the manual that set the site up. Read `readme.md` first and keep it in context.

## Working on the site

- You run every command and every edit yourself. Where a command really needs the user,
  such as `sudo`, give them the exact command to paste.
- Before changing code, read the files and the control flow around them. Write from the
  existing source of truth, keep no duplicate state, and reject patches that only cover
  the local symptom.
- Svelte files use the preprocessors in `frontend/svelte.config.js`, which rewrite syntax
  and allow what plain Svelte rejects. Read it before changing Svelte syntax or taking a
  compiler warning for an obvious fix.
- The database only moves forward by migrations. Never edit or delete a committed one.
- Secrets live in `docker/prod.env` and nowhere else. Never commit credentials.

## The starter and the libraries

Keep the site upgradable as far as reasonably possible: from the starter, from `svUltra`
and `djultra`, and from the Django and Svelte releases underneath. Breaking that is a
judgement call, never a side effect. The main way is to add — components, styles, pages,
content — in the site's own directories, and to keep the starter's ways of working: an
email goes out through Django and the existing SMTP configuration, not through something
reimplemented in the frontend.

- `svUltra` and `djultra` are installed from GitHub and are never changed from the site.
  What the site needs beyond them is written in the site.
- A kit component is configured from outside: props, attributes, component styling. A
  site-specific version is a copy in `frontend/src/components/`, changed freely; it no
  longer follows svUltra updates.
- Nothing is version-pinned; `./dm pull` updates the checkout and its dependencies.
- The starter is the `starter` remote; `git pull starter main` merges its updates.

## Pages and styling

- Build a page from its job for the visitor, not from a component to show.
- PicoCSS is the baseline: semantic HTML first, Pico's classes and variables, custom CSS
  only with a concrete local reason.
- Fixed page copy is written as headings, paragraphs and lists, not hidden in arrays and
  loops; `{#each}` is for real collections.
- A component is `script`, `style`, then markup; it accepts `children` and `...rest` and
  forwards `...rest` to its real element.

## Commits

One-line imperative subjects that say what changed.
