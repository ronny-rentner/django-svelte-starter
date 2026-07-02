# Starter Extraction TODO

## Copy or Adapt Later From Relonee

- Frontend dependency refresh: backend venv packages were refreshed to current PyPI releases, including Django 6 and the `django-tasks-db` split. Frontend package updates remain; current build warnings include old Browserslist data and Svelte warnings from older component code. Svelte updates need extra care because `frontend/svelte.config.js` uses advanced preprocessors that rewrite syntax and allow non-plain-Svelte expressions.
- Frontend starter extraction: keep the Vite/Svelte shell, generated routes, layout, stores, API helper pattern, and Django template integration; separate or delete project-specific Relonee/Anabin/document/process/visa pages, markdown, and assets once replacement starter pages are defined.
- Frontend project prototype content: current visible shell mixes starter code with the later YouTube/finance idea (`my market mentor`, `/generate`, YouTube asset) and old Relonee marketing/legal/account content; decide the minimal neutral starter surface before broad cleanup.
- svUltra demo history: previous demo work stalled because LLM-generated demos did not communicate the library well enough; judge the next pass by whether it clearly proves the README claims instead of by generic cleanup.
- CLI development orchestration: make `./dm run all` start backend and frontend together instead of running the backend command first and blocking the frontend command.
- Document/download API: `DocumentDownloadView`, `DocumentList`, file permissions, document serializer context, and media path behavior.
- Upload/extraction API: `DocumentUpload`, document AI settings, `Degree` extraction flow, and anonymous upload behavior.
- External integrations: `DocusealWebhookView`, `AnabinAiSearch`, `VidexFormChatView`, and their model/service dependencies only for projects that need them.
- Copied templates from Relonee need adaptation before production use: `emails/*` and admin overrides. The frontend shell is copied and minimally adapted for starter routing.
- Static source assets from Relonee `static/src` may be useful later for admin styling, favicon, and email/logo assets.
- Fastmanage exit status follow-up: daemon-side status sending and client exit-code propagation are implemented, function-tested, and smoke-checked through the real daemon socket.
