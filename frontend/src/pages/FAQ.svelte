<script>
  import { Main } from '@kit/components';
  import { accordion } from '@kit/actions';

  let { meta, ...rest } = $props();
  meta({
    title: 'FAQ',
    description: 'Frequently asked questions about the django-svelte starter.'
  });
</script>

<style>
  details {
    /* Limit line length while allowing items to fill narrower screens. */
    max-width: 48rem;
    margin-bottom: calc(var(--pico-spacing) * 0.5);
    border: var(--pico-border-width) solid var(--pico-muted-border-color);
    border-radius: var(--pico-border-radius);
    background-color: var(--pico-card-background-color);

    /* Draw the focus outline over the item's border. */
    outline-offset: calc(-1 * var(--pico-outline-width));

    /* Separate question text from the enclosing border. */
    summary {
      padding: var(--pico-spacing);
    }

    /* Align answer text with the summary text. */
    > summary + * {
      padding-inline: var(--pico-spacing);
    }

    /* Keep the focus frame on the item as its answer opens and closes. */
    &:has(> summary:focus) {
      outline: var(--pico-outline-width) solid var(--pico-primary-focus);
    }

    /* The item supplies the focus frame for both summary variants. */
    > summary:focus {
      outline: none;
      box-shadow: none;
    }

    /* Emphasize plain questions and round their hover background. */
    summary:not([role="button"]) {
      /* Keep unfocused question text the same color in both states. */
      --pico-accordion-open-summary-color: var(--pico-accordion-close-summary-color);
      font-weight: bold;
      border-radius: var(--pico-border-radius);
      transition-property: color, background-color;

      &:hover, &:focus-visible {
        background-color: var(--pico-card-sectioning-background-color);
      }

      &:focus, &:focus-visible {
        color: var(--pico-color)
      }
    }
  }
</style>

<Main {...rest}>
  <h1>Frequently Asked Questions</h1>

  <details use:accordion>
    <summary>What is this starter?</summary>
    <div><markdown>
      A ready-to-run base for a website: a Django 5 backend and a Svelte 5 frontend, wired together so you start from working software instead of an empty project.

      - **Frontend** — components, file-based routing and build preprocessors from the svUltra kit.
      - **Backend** — authentication, settings, the admin and API endpoints from djultra.
      - **Glue** — django-vite, so the Svelte app runs as part of the Django site: one server in production, hot reload in development.
    </markdown></div>
  </details>

  <details use:accordion>
    <summary>How do I add a page?</summary>
    <div><markdown>
      Pages are just files — there is no central route list to maintain:

      1. Create a `.svelte` file under `frontend/src/pages/`.
      2. Its name becomes the route: `About.svelte` is served at `/about`, `Home.svelte` at `/`.
      3. Add a link to that path in the menu to show it in the nav.

      The generateRoutes plugin watches the folder and rebuilds the route table for you; matching and code-splitting are handled.
    </markdown></div>
  </details>

  <details use:accordion>
    <summary>Is this a single-page app?</summary>
    <p>Yes. The first visit loads one HTML shell plus the compiled Svelte bundle; after that, following a link doesn't fetch a new document — the router swaps the page's component in place. The URL changes and the back button works as usual, but the surrounding layout never reloads, so moving between pages is instant. New content is fetched on demand from the Django backend over a REST API — that's where the data is stored.</p>
  </details>

  <details use:accordion>
    <summary>Will search engines find my pages?</summary>
    <div><markdown>
      Yes. Google renders the page's JavaScript before indexing, so it sees the fully rendered content just like a visitor does — and each page sets its own `<title>` and meta description through `meta()`, so the right title and summary show up in the search result and the link preview.
    </markdown></div>
  </details>

  <details use:accordion>
    <summary>Won't a single-page app be slow to load?</summary>
    <div><markdown>
      No — and Svelte is the main reason. It compiles components to small, plain JavaScript with no framework runtime shipped alongside (unlike React or Vue), and the build code-splits per route. So the CSS and the shared app JavaScript load once on the first page; after that, navigating fetches only the next page's chunk — typically 2–3 kB — so it's near-instant.

      This build, gzipped:

      - CSS (Pico and the app's own): **~15 kB**
      - shared app JavaScript — the entry plus components, loaded once: **~54 kB**
      - each page's own chunk after that: this FAQ is **~2 kB**
    </markdown></div>
  </details>

  <details use:accordion>
    <summary>How does this FAQ page work?</summary>
    <div><markdown>
      Each question is an HTML `<details>` with a `<summary>` — the browser's built-in way to show and hide a block. On their own, though, they snap open and shut, which feels abrupt.

      svUltra brings a few built-in actions; one of them, `accordion`, slides an element open and closed instead. Drop it on the `<details>` and you get the smooth panels you see here:

      ```svelte
      <details use:accordion>
        <summary>Question</summary>
        <p>Answer</p>
      </details>
      ```
    </markdown></div>
  </details>

  <details use:accordion>
    <summary>How does the accordion work?</summary>
    <div><markdown>
      Clicking a summary doesn't fire the browser's instant toggle — the action intercepts it and animates instead: it measures the panel below the summary and slides its height from zero to full while fading it in, then reverses that to close.

      It animates the single element right after the summary, so a panel whose body is several blocks needs them wrapped in one element — a plain `<div>` is enough.
    </markdown></div>
  </details>
</Main>
