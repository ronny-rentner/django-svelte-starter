# Starter Extraction TODO

## Doc gaps found while rolling out site 2

- `setup.md` step 7 pushes to `<url>` but never creates the repository. `new_site.md` needs the local decision: a private GitHub repository under `ronny-rentner`, created before step 7.
- `setup.md` step 1 removes the git history. Keep it: `git remote rename origin starter`, so a starter update is `git pull starter main`. All git operations go into this one step: the clone, the `starter` remote, creating the site's repository, adding it as `origin`. Step 7 keeps only the commit and push.
- `AGENTS.md` must say that the agent runs all commands and edits of a setup itself. Where a command really needs the user, such as `sudo`, the agent gives the exact command to paste.
- `setup.md` step 6 assumes ports 8000 and 5173 are free. With another site's dev servers running, say what to do: stop them, or run the new site's on other ports.
- Bug, djultra: `./dm run back` with django-tasks 0.12.0 fails to start the task worker, `Worker.__init__() missing 1 required keyword-only argument: 'excluded_queue_names'` in `djultra/management/commands/dev.py:54`. The dev server itself runs on; nothing processes tasks.
- `./dm run back` and `./dm django-admin` warn `staticfiles.W004: static/frontend does not exist` until the first `./dm build`. Silence it or say so in `setup.md`.
- `setup.md` step 6 greps the site for the starter's names. Remove it: the grep is the maintainer's tool for finding the spots when writing steps 3 and 4, noted in `development.md`; the guide lists the spots.
- `setup.md` step 6, the shell check `from core.models import ContactMessage` fails with `ModuleNotFoundError: No module named 'core'`; the app is `backend.core`. The command in the guide is wrong.
- A login on `/admin/login/` opened directly, without `next`, ends on Django's default `LOGIN_REDIRECT_URL`, `/accounts/profile/`, which the app answers with its 404 page. Via `/admin/`, as `setup.md` says, it does not happen.
- `backend/core/templates/index.html` hardcodes the `<title>`.
- `backend/core/templates/index.html` duplicates djultra's `templates/index.html`. The only differences are the theme backgrounds, the `data-theme` bootstrap script and the favicon link, none of them site-specific.
- `frontend/index.html` hardcodes the `<title>`.
- `new_site.md` needs the values for `setup.md` step 8, `prod_django.ini`: the LAN alias `<site>.yuki` in `ALLOWED_HOSTS`, as carbon.berlin has, and the sender `info@<domain>`.
- The domain is hardcoded again and again: `ALLOWED_HOSTS` in `settings.py`, `ALLOWED_HOSTS`, the three `FRONTEND_*` URLs and `DEFAULT_FROM_EMAIL` in `prod_django.ini`, the titles, the footer, the database name. Put it in one variable and derive the rest from it throughout the app.
- `setup.md` and `new_site.md` never mention DNS. `<domain>` and `www.<domain>` must resolve to the host before the certificate and the proxy; on site 2 they resolved to nothing.
- `setup.md` step 8 says "Replace all values" for `prod.env`. It should say: update what you have, delay the rest to later when not essential.
- `docker/prod_django.ini` and `docker/prod.env.example` are badly created: bad comments, bad ideas. Relonee's files are much better and were not copied correctly. Both need to be reworked from Relonee's.
- `new_site.md` and `setup.md` use relative paths everywhere (`../database/register-site ../<site>`, `cd <site>`) without saying which directory a command runs in. State the working directory once at the beginning, keep it the same throughout, and stop the `cd` all over the place. With the site's directory as the working directory, the host scripts take `.`: `../database/register-site .`, `../proxy/issue-cert .`, `../proxy/register-site .`, `../proxy/update-cert .`.
- `docker/certbot/` mirrors the certbot container's absolute paths: `etc/letsencrypt/live/<site>/` and `var/lib/letsencrypt/`, from `issue-cert`'s mounts. A strange, deep layout for two files; rework it, with the self-signed pair in the same structure as the issued one. The proxy's `var/www/html` is the same pattern, and worse: named after `/var/www/html` and then mounted at `/usr/share/nginx/html`.
- `sites/proxy/register-site` and `sites/proxy/issue-cert` each parse `prod_django.ini` with their own inline Python. One reader for the ini, not one per script.
- Bug, `sites/database/register-site`: its final message prints the argument as the site name, "Site '.' has database 'aylinschaer.de' …", instead of the site directory's name.
- `COMPOSE_PROJECT_NAME` must consist of lowercase alphanumerics, hyphens and underscores; a domain with a dot such as `aylinschaer.de` is rejected: `invalid project name "aylinschaer.de"`. carbon.berlin uses `carbon-berlin`, the domain with the dot as a hyphen. `new_site.md` needs that convention.
- Bug, `dm`: when a command it runs fails, its error output is not shown. `./dm docker deploy` ended with "exited with code 15" and nothing else; the compose error above was only visible by running the command directly.
- `setup.md` step 8 has no check after `./dm docker deploy`, unlike step 6 after the local run: nothing says how to see that the container loaded the database, migrated and answers on port 8000.
- Without DNS, `issue-cert` cannot run, and without its certificate the proxy's `register-site` cannot write a valid config: a site is unreachable until DNS is set up. Nothing delivers a self-signed certificate for the time before, so the site works out of the box, with a browser warning.
- `setup.md` needs a headline for what can be set up after launch: reCAPTCHA keys, the SMTP account, tracking, proper SSL certificates, proper DNS.
- `prod.env` sets `CONFIG_FILE=./docker/prod_django.ini`, and the container gets it through Compose. `dm` itself only passes the env file to Compose (`cli.py:665`) and never loads it into its own environment, so on the host `./dm build` and every `./dm django-admin` run with `CONFIG_FILE` unset: `settings.py` falls back to `/dev/null`, `DEBUG` to `True`, `ALLOWED_HOSTS` to the development list. With `ENV=prod`, `dm` has to load `docker/prod.env` for its own process too.
- Once the site has its own commits, a plain `git pull starter main` fails with "Need to specify how to reconcile divergent branches". We want a merge here, so we don't have to force push. Add `git config pull.rebase false` to step 1, so that `git pull starter main` merges.
- `new_site.md` needs the value for `setup.md` step 3: `EMAIL_HOST` is `mail-eu.smtp2go.com` for all sites.
- `setup.md` says `<site>` is lowercase like `example`; carbon.berlin uses the domain as directory, database and role name. `new_site.md` needs the local decision: `<site>` is the domain.
- `setup.md` step 2 must not edit `AGENTS.md`. The rollout only deletes and replaces files, at the end, once the site runs. A site gets its own short `AGENTS.md`, still to be written, with the rules for working on a site and no copy of the readme. The last step deletes `new_site.md`, `development.md`, `starter_todo.md` and puts that file in place.
- `AGENTS.md` lists `./dm run all`, which was never fully implemented.
- `setup.md` step 4 mixes the name spots with the owner's content. Setup sets only the name: the three titles, the footer's copyright holder, `startdev.desktop`. The owner's content — `Home.svelte`, the social links and the "Crafted with" line, logo and favicon, colours and font, the legal texts — is not a setup step.
- The site name is typed three times: `backend/core/templates/index.html` `<title>`, `frontend/index.html` `<title>`, `Home.svelte` `meta()`. `settings.py` has `PROJECT_NAME`, which names the admin, and the email header gets `project_name`. Give the titles the same source, so the rebrand sets one value; `setup.md` step 4 then loses three items.
- `settings.py` reads `DATABASES` with `os.environ.get`, copied from Relonee before `config()` existed. Refactor it to `config('DB_NAME', default='dss')` and so on, so the ini can set them too; the readme's Configuration section then drops the "environment only" exception.

## Before Site 1

- We cannot install a single npm package without npm enforcing `package.json`. Find a way to stop npm from doing that.
- Bug in clean-browser-mcp: `browser_scroll` tries to scroll the page when the page has to scroll `#app`. With an amount that cannot be reached (100,000 px) it never stops and blocks the browser tools.
- Bug: stopping a backgrounded MCP tool task with `TaskStop` reports success, but the command keeps running — the `browser_scroll` above kept executing in the browser extension.
- Bug in clean-browser-mcp: `browser_type` with `submit: true` sends `keyUp` for Enter, and the form does not submit. Seen on the Django admin login form: the fields stay filled, no error, same URL.
- Trim inherited YouTube transcript functionality from the default starter unless the first site needs it. It currently ships as `backend/core/models/youtube.py`, committed migrations, and `pytubefix` / `youtube-transcript-api` dependencies.
- Add a fresh-clone bootstrap path: how to create `backend/venv`, install backend/frontend dependencies, create the local database, and provide the first config values.
- On yuki, `docker volume rm database_postgres_data`: the old PostgreSQL volume, kept as fallback after the data moved to `sites/database/data/` on 2026-09-08.
- SQL dumps for backups are missing, deferred.
- Rename `build-info.json` to `buildInfo.json`, matching svUltra's `buildInfo.js` and `updateBuildInfo.js`: the two kit modules, svUltra's readme, the starter's and the sites' `.gitignore`, readme and AGENTS.md, and the file on the host.
- Schedule `proxy/update-cert` on yuki, deferred. carbon.berlin's certificate expires 2026-12-06; certbot renews from 2026-11-06, so the cron line, or a manual run, must be in place by then.
- On the next new site, verify `proxy/issue-cert`: the deploy hook copying into `proxy/certs/<site>/` has not been observed yet. The note sits in `new_site.md`, chapter 7.
- Add a per-site configuration template for launch-critical values: `SECRET_KEY`, `DEBUG`, database settings, frontend URLs, allowed hosts, reCAPTCHA keys, and email settings.
- Remove local-machine defaults before cloning a real site: personal `ALLOWED_HOSTS`, the absolute path in `cli/startdev.desktop`, `dss` package/database names, and placeholder brand/legal text.
- Quiet development/demo noise that would distract site work: frontend request/debug logs, layout pageConfig logging, placeholder footer/social links, and demo-only `About` / `Landing` page content.

## Copy or Adapt Later From Relonee


- Frontend dependency refresh: backend venv packages were refreshed to current PyPI releases, including Django 6 and the `django-tasks-db` split. Frontend package updates remain; current build warnings include old Browserslist data and Svelte warnings from older component code. Svelte updates need extra care because `frontend/svelte.config.js` uses advanced preprocessors that rewrite syntax and allow non-plain-Svelte expressions.
- svUltra demo history: previous demo work stalled because LLM-generated demos did not communicate the library well enough; judge the next pass by whether it clearly proves the README claims instead of by generic cleanup.
- Document/download API: `DocumentDownloadView`, `DocumentList`, file permissions, document serializer context, and media path behavior.
- Upload/extraction API: `DocumentUpload`, document AI settings, `Degree` extraction flow, and anonymous upload behavior.
- External integrations: `DocusealWebhookView`, `AnabinAiSearch`, `VidexFormChatView`, and their model/service dependencies only for projects that need them.
- Copied templates from Relonee need adaptation before production use: `emails/*` and admin overrides. The frontend shell is copied and minimally adapted for starter routing.
- Static source assets from Relonee `static/src` may be useful later for admin styling, favicon, and email/logo assets.
