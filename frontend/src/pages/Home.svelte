<script>
  import { Card, Icon, IconWithLabel, Main } from '@kit/components';
  import browserIcon from '@iconify-icons/ph/browser-duotone';
  import databaseIcon from '@iconify-icons/ph/database-duotone';
  import rocketIcon from '@iconify-icons/ph/rocket-launch-duotone';
  import stackIcon from '@iconify-icons/ph/stack-duotone';
  import codeIcon from '@iconify-icons/ph/code-duotone';
  import packageIcon from '@iconify-icons/ph/package-duotone';

  let { meta, ...rest } = $props();
  meta({
    title: 'Django Svelte Starter',
    description: 'A ready-to-run Django and Svelte starter with the shell, API, routing, auth, and build path already connected.'
  });
</script>

<Main {...rest}>
  <section>
    <hgroup>
      <p><Icon icon={rocketIcon} size="3rem" /></p>
      <h1>Start from a real app foundation.</h1>
      <p>
        An opinionated Django/Svelte starter with the pieces real apps need from
        day one: auth, contact forms, reCAPTCHA, routing, API helpers, config
        injection, dev servers, production builds, and UI conventions already wired.
      </p>
    </hgroup>

    <p>
      It is not an empty scaffold. It already has the page shell, frontend routing,
      API calls, login flow, contact form, reCAPTCHA wiring, development servers,
      and production build path connected.
    </p>

    <p>
      <a href="/guide" role="button">Read the guide</a>
      <a href="/faq" role="button" class="secondary outline">View the FAQ</a>
    </p>
  </section>

  <section>
    <h2>What you start with</h2>

    <div class="grid">
      <Card>
        <IconWithLabel slot="header" icon={databaseIcon}>Django API and admin</IconWithLabel>
        Django provides the API and admin dashboard. Auto admin, auto API,
        sessions, email, and database-backed models are already wired.
      </Card>

      <Card>
        <IconWithLabel slot="header" icon={browserIcon}>Svelte app</IconWithLabel>
        Pages live in <code>frontend/src/pages</code>, navigation happens without
        full page reloads, and Vite builds the frontend into
        <code>static/frontend</code>.
      </Card>

      <Card>
        <IconWithLabel slot="header" icon={stackIcon}>Shared frontend kit</IconWithLabel>
        svUltra provides the router, stores, actions, dialogs, toasts, markdown
        support, loading UI, and component conventions through the
        <code>@kit</code> alias.
      </Card>
    </div>
  </section>

  <section>
    <h2>Working boundaries</h2>

    <markdown>
      The starter includes working examples of the app boundaries:

      - **Sign-in** — passwordless email links, token login, session auth, and signed-in user state.
      - **Contact** — a modal form that posts to Django and saves `ContactMessage` records.
      - **reCAPTCHA** — site keys injected by Django and tokens verified by the backend.
      - **Routing** — Svelte routes generated from `frontend/src/pages`, with Django fallback routing for direct visits.
      - **Content** — markdown-backed pages for long-form copy.
      - **Builds** — Vite output and Django static collection through `./dm build`.
    </markdown>
  </section>

  <section>
    <h2>What is already working</h2>

    <markdown>
      TODO

      - Placeholder
      - Placeholder
    </markdown>
  </section>

  <section>
    <h2>Where project code goes</h2>

    <div class="grid">
      <Card>
        <IconWithLabel slot="header" icon={databaseIcon}>Backend</IconWithLabel>
        Put site models, views, URLs, serializers, tests, and migrations in
        <code>backend/core</code>.
      </Card>

      <Card>
        <IconWithLabel slot="header" icon={codeIcon}>Frontend</IconWithLabel>
        Put routed pages in <code>frontend/src/pages</code> and site-specific UI
        in <code>frontend/src/components</code>.
      </Card>

      <Card>
        <IconWithLabel slot="header" icon={packageIcon}>Shared libraries</IconWithLabel>
        Shared Django behavior belongs in <code>djultra</code>; shared Svelte
        behavior belongs in <code>svUltra</code>. The starter keeps the project
        decisions.
      </Card>
    </div>
  </section>
</Main>
