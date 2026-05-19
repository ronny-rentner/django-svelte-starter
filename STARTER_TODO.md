# Starter Extraction TODO

## Copy or Adapt Later From Relonee

- Frontend dependency refresh: backend venv packages were refreshed to current PyPI releases, including Django 6 and the `django-tasks-db` split. Frontend package updates remain; current build warnings include old Browserslist data and Svelte warnings from older component code. Svelte updates need extra care because `frontend/svelte.config.js` uses advanced preprocessors that rewrite syntax and allow non-plain-Svelte expressions.
- CLI development orchestration: make `./dm run all` start backend and frontend together instead of running the backend command first and blocking the frontend command.
- Contact form flow: `ContactMessageThrottle`, `ContactMessageView`, `ContactMessageSerializer`, recaptcha verification, and frontend contact submission wiring.
- Sign-in request flow: `SigninRequestView`, `Person.send_signin_email()`, sign-in email template adaptation, recaptcha verification, and token email links.
- Token auth support dependencies: custom token authentication backend/model behavior used by `TokenLoginView2`; the API view and route are copied, but authentication still needs a backend implementation.
- User/person API shape: decide whether to copy `PersonView`, `PersonAcceptTermsView`, ownership permissions, and related serializers after starter user/account models exist.
- Document/download API: `DocumentDownloadView`, `DocumentList`, file permissions, document serializer context, and media path behavior.
- Upload/extraction API: `DocumentUpload`, document AI settings, `Degree` extraction flow, and anonymous upload behavior.
- External integrations: `DocusealWebhookView`, `AnabinAiSearch`, `VidexFormChatView`, and their model/service dependencies only for projects that need them.
- Copied templates from Relonee need adaptation before production use: `emails/*` and admin overrides. The frontend shell is copied and minimally adapted for starter routing.
- Static source assets from Relonee `static/src` may be useful later for admin styling, favicon, and email/logo assets.
- Fastmanage exit status follow-up: daemon-side status sending and client exit-code propagation are implemented, function-tested, and smoke-checked through the real daemon socket.
