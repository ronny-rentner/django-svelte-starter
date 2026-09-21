# Markdown content directories — implementation plan

Status: **in progress — planned, not implemented**.

This records the agreed approach and its current technical details. The overview’s use of original images remains unresolved; see section 6. Line references identify the source inspected during planning and will move after edits. Proposed files and functions are marked **new**.

## 1. Goal and boundaries

Enable svUltra and starter-based sites to efficiently handle directories of Markdown content: compile each file through the existing Markdown/Svelte pipeline, load its component on demand, and generate a catalog for pages that list the content.

svUltra supplies the shared compiler support, directory discovery and reusable components. A consuming page owns its route, page layout, title and metadata. Markdown files supply content, not complete page shells.

The first consumer is aylinschaer.de. Shared implementation goes into svUltra; site integration goes into Aylin only. Copying the integration to the starter comes later. Carbon is outside this implementation.

The existing Home page remains the definition of Aylin’s work and the site’s purpose. Publishing articles does not include rewriting Home, About or FAQ.

The intended route flow is:

```text
/article/1
  → one Article.svelte page reads the ID from currentPath
  → selects markdown/articles/1.md from a Vite import glob
  → loads that file’s compiled content component
  → sets title and description and renders the content inside the page
```

Use the existing Marked renderer and Vite/Svelte compilation. No mdsvex migration, browser-side Markdown renderer, generated .svelte page files, template multiplication or manually replicated compilation pipeline.

## 2. Configuration and framework interfaces

Repositories:

| Name | Directory |
| --- | --- |
| svUltra | `/home/ronny/Projects/js/svUltra` |
| Aylin | `/home/ronny/Projects/sites/aylinschaer.de` |
| Starter | `/home/ronny/Projects/django-svelte-starter` |

In Aylin’s `frontend/svelte.config.js:15`, add the supported Svelte extension configuration:

```js
extensions: ['.svelte', '.md'],
```

Keep the existing `svultraPreprocess()` configuration, including `markdown.path` at lines 22–24. That path continues to control `<markdown file="…">` lookup. Images inside a referenced Markdown file resolve relative to that file, not relative to the configured Markdown root.

Extend the existing call in Aylin’s `frontend/vite.config.js:93`:

```js
generateRoutesPlugin({
  markdownDirs: {
    articles: './src/markdown/articles',
  },
  routeRenames: {
    '/home': '/',
    '/404': '*',
    '/article': '/article/*',
  },
}),
```

`markdownDirs` is the new generic framework option:

- Keys name collections; values name directories relative to Vite’s project root.
- Each directory contributes its immediate `.md` files. Subdirectories, including Aylin’s `_src`, are excluded.
- Collection names do not define routes. A consuming page chooses its URL and layout.
- Multiple named directories use the same discovery mechanism.
- With no configured Markdown directories, existing route generation and its output remain unchanged.

## 3. One Markdown renderer for all input forms

### Existing entry points

In svUltra’s `src/preprocessors/markdown.js`:

| Current location | Function or definition | Responsibility |
| --- | --- | --- |
| Line 23 | `renderer` | Shared code escaping and link rendering |
| Line 65 | `accordionExtension` | Markdown FAQ syntax |
| Line 91 | `markedOptions` | Shared Marked configuration |
| Line 107 | `renderMarkdown(markdownText, useAccordion = false)` | Markdown rendering |
| Line 170 | `processMarkdownTags(content, magicString, filename, rootPath, deps)` | Find tags, obtain Markdown source and replace tags |
| Line 221 | `markdownPreprocessor(options = {})` | Public preprocessor factory |
| Line 226 | `async markup({ content, filename })` | Svelte markup-preprocessing entry point |

Extend the existing renderer instead of adding a separate `renderMarkdownModule()` implementation. All input forms must share image handling, image grouping, link rendering and code escaping.

Proposed private renderer signature:

```js
function renderMarkdown(markdownText, {
  sourceFilename,
  imports,
  useAccordion = false,
}) // → HTML/Svelte markup string
```

The renderer owns the common Marked configuration. FAQ mode adds its extension to that same rendering path. Do not retain separate implementations of normal Markdown and standalone-module image processing.

`markup()` creates one import collection for the containing component. Direct Markdown rendering, every embedded Markdown tag and FAQ answers share it. This prevents duplicate imports and conflicting generated binding names within a component.

Extend the existing tag-processing signature to accept that collection:

```js
async function processMarkdownTags(content, magicString, filename, rootPath, deps, imports)
```

Its responsibilities remain finding tags, reading referenced files, tracking file dependencies, invoking `renderMarkdown()` and replacing tags. Preserve the existing file/inline/default-filename modes and rendered-output pattern replacements.

The call chain becomes:

```text
markdownPreprocessor.markup({ content, filename })
  → create one component-wide import collection
  │
  ├─ .svelte input → processMarkdownTags(..., imports)
  │                   ├─ inline source → renderMarkdown(...)
  │                   └─ file source   → renderMarkdown(...)
  │
  └─ .md input → renderMarkdown(...)
  │
  → assemble collected imports once into the resulting component
  → return code, source map and tracked dependencies
```

Import assembly must preserve existing scripts. Add generated imports to the instance script, creating an instance script when necessary; do not turn an existing module script into an instance script or produce duplicate instance scripts.

### FAQ rendering and the current FAQ page

The starter’s current `frontend/src/pages/FAQ.svelte` writes its `<details use:accordion>` structure directly. Some answers contain inline `<markdown>` blocks. It does not use a separate FAQ Markdown file or `mode="faq"`. This feature does not require rewriting that page.

The library’s `mode="faq"` remains supported independently. Its renderer currently calls global `marked.parse(token.text)` at `markdown.js:83`, which bypasses the renderer instance’s image handling. Change the extension to tokenize its answer with `this.lexer.blockTokens(body)` and render the resulting tokens with `this.parser.parse(token.tokens)`. FAQ answer bodies then use the same image and paragraph renderers as other Markdown.

### Relative images and image groups

These rules apply to direct `.md` imports, file tags and inline Markdown:

| Input | Base directory for relative image references |
| --- | --- |
| Imported `.md` | The Markdown file’s directory |
| `<markdown file="…">` | The referenced Markdown file’s directory |
| Inline `<markdown>` | The containing `.svelte` file’s directory |

Resolve relative image files through Vite `?url` imports, including Aylin’s `.image` files. Rebase generated import paths relative to the component receiving them. Keep external and root-relative image references as URLs. Preserve alternative text and image titles.

For paragraph rendering:

- One image remains an ordinary image.
- Two or more images in one image-only paragraph become an `ImageSlider`.
- Whitespace and Markdown line breaks may separate grouped images.
- A blank line creates a separate paragraph and therefore separates image groups.
- Paragraphs containing prose and images retain ordinary Markdown rendering.

Example Markdown:

```md
A paragraph about the event.

![First photograph](9.image)
![Second photograph](9_2.image)

![Separate photograph](9_3.image)
```

Illustrative generated Svelte source for a direct `.md` import:

```svelte
<script>
  import ImageSlider from 'svultra/kit/components/ImageSlider.svelte';
  import image0 from './9.image?url';
  import image1 from './9_2.image?url';
  import image2 from './9_3.image?url';
</script>

<p>A paragraph about the event.</p>

<ImageSlider images={[
  { src: image0, alt: 'First photograph' },
  { src: image1, alt: 'Second photograph' },
]} />

<p><img src={image2} alt="Separate photograph" /></p>
```

The generated component import belongs to the component containing the rendered Markdown. An import in the parent `Article.svelte` cannot supply an identifier to a separately compiled Markdown child.

### Preprocessor ordering

`src/preprocessors/preset.js:20` defines `svultraPreprocess(options = {})`. Its current order is syntax sugar, Markdown, attribute transformation, component styles and class merging.

At `src/preprocessors/syntax-sugar.js:192`, skip raw standalone `.md` input before syntax substitutions. Inline Markdown bodies are already protected from those substitutions.

Keep the current ordering. The existing FAQ extension already generates standard Svelte `{#snippet …}` syntax after syntax sugar has run. New generated markup can use the same convention. This is an implementation choice, not a limitation of the architecture: supporting svUltra shorthand in generated Markdown output would require revisiting the ordering.

The complete compilation chain is:

```text
Vite resolves an import of markdown/articles/9.md
  → vite-plugin-svelte accepts the configured .md extension
  → svultraPreprocess()
      → syntaxSugar leaves raw .md source unchanged
      → markdownPreprocessor.markup()
          → shared renderMarkdown()
          → generated HTML/Svelte markup and collected imports
      → attributeTransformer
      → transformComponentStyles
      → classMergePreprocessor
  → vite-plugin-svelte invokes the Svelte compiler
  → Vite resolves component and asset imports
  → browser-loadable component module
```

Development uses Vite’s on-demand transformation and HMR. Production builds compile the same imported modules into lazy chunks. Marked is not shipped to the browser. No generated `.svelte` files or manual Svelte compiler calls are introduced.

## 4. Generate catalogs alongside routes

Extend `src/kit/router/generateRoutes.js:9`:

```js
export default function generateRoutesPlugin(userOptions = {})
```

Add `markdownDirs: {}` to its defaults. Reuse the existing initialization, serialized watcher queue and generated output file.

### Metadata and catalog functions

New build-time helper in `src/preprocessors/markdown.js`:

```js
export function extractMarkdownMetadata(markdownText)
// → { title, excerpt, firstImage }
```

The generator imports this helper directly. Browser code does not import it. Read Marked tokens instead of stripping rendered HTML.

Metadata rules:

- `title`: the complete first sentence of the first prose paragraph, with Markdown formatting removed and link labels retained.
- If that paragraph has no sentence-ending punctuation, use the whole paragraph.
- Preserve abbreviations present in the corpus, including `Dr.`, `e.g.` and `z. B.`, when identifying sentence boundaries.
- `excerpt`: following prose, limited to 200 characters at a word boundary, with an ellipsis when shortened.
- `firstImage`: the first image’s `{ src, alt }`, or `null`.
- Deriving metadata does not remove or rewrite the article’s opening text.

New internal generator function:

```js
async function generateMarkdownCatalog(dir)
// → Promise<Array<{ id, title, excerpt, firstImage }>>
```

`id` is the filename without `.md`, preserved as a string. Catalog output uses stable filename ordering. Aylin separately interprets numeric IDs as chronological ordering; the framework does not infer publication dates.

### Generator call chain

```text
configResolved(config)                         existing line 28
  → resolve pagesDir and configured markdownDirs
  → generateAndWriteRoutes()                   existing line 87
      → generateRoutes(...)                    existing line 113
      → applyRouteRenames(...)                 existing line 152
      → generateMarkdownCatalog(dir)           new, per configured directory
          → read .md files
          → extractMarkdownMetadata(source)
      → serialize routes, catalog data and image URL imports
      → write generatedRoutes.svelte.js only when output changed
```

Keep the existing `routes` export. Add `markdownCatalogs` when Markdown directories are configured. Example output with illustrative article text:

```js
import image0 from './markdown/articles/1.image?url';

export const routes = {
  '/articles': () => import('./pages/Articles.svelte'),
  '/article/*': () => import('./pages/Article.svelte'),
  // Existing routes remain here.
};

export const markdownCatalogs = {
  articles: [
    {
      id: '1',
      title: 'Finance starts with people.',
      excerpt: 'A useful finance process starts with a shared understanding.',
      firstImage: { src: image0, alt: 'Workshop participants' },
    },
  ],
};
```

The image import asks Vite to include the original asset and supply its served URL, respecting the configured `/static` base and asset output paths. `?url` is a Vite import instruction, not a public cache-busting query parameter. Importing the URL does not itself download the image in the browser; displaying an `<img>` with that URL does.

This is the **original image**, not a generated thumbnail. The overview image-size concern is unresolved below.

Catalogs contain metadata and image URLs, not full bodies or eager imports of compiled Markdown components.

Extend `configureServer(server)` at line 36 to watch the configured Markdown directories through the existing event queue. Additions, removals and metadata changes update the catalog. Body-only changes continue through Svelte HMR without rewriting an unchanged catalog. Preserve visible error reporting and the existing watcher recovery behavior.

## 5. Routing and page ownership

### Existing wildcard behavior and the required correction

`src/kit/router/Router.svelte:86` resolves routes. Lines 93–104 already match both `/article/1` and `/article/2` to `/article/*`.

The defect is in `updateComponent()` at line 109: `currentPath.set(path)` and `_currentPath = path`, currently at lines 128–129, run only when the selected page loader changes at line 117.

Consequences for the proposed Article page:

- Directly opening `/article/1` works: the loader changes and the path is published.
- Following a link from `/article/1` to `/article/2` changes the browser URL but selects the same `Article.svelte` loader. The path publication is skipped, leaving `currentPath` at `/article/1`.
- A subsequent navigation back to `/article/1` is also incorrectly skipped because the internal pathname is stale.

Move the two path assignments before the loader comparison. Track whether the path changed; for a changed path using the same loader, await the already imported `tick()` and call `window.scrollTo(0, 0)`.

Keep wildcard matching, public router signatures and different-component loading behavior. The fix publishes URL changes independently of component changes; it does not remount Article for each ID or add a route-parameter API.

Relevant existing router interfaces:

| Location in Router.svelte | Interface |
| --- | --- |
| Line 10 | `meta({ title, description } = {})` |
| Lines 37–39 | `currentComponent`, `isLoading`, `currentPath` stores |
| Line 63 | `navigate(path)` |
| Line 173 | Router props `{ routes, Layout = DefaultLayout }` |

These are already exported through `src/kit/router/index.js`.

### New Aylin page: `frontend/src/pages/Article.svelte`

The page owns `Main`, its heading, title/description, article loading and an “All articles” link to `/articles`.

Use the agreed Vite glob:

```js
const articleModules = import.meta.glob('../markdown/articles/*.md');
```

Read the ID from the existing `currentPath` store and find its catalog entry. For `/article/1`, select:

```js
articleModules['../markdown/articles/1.md']
```

Use reactive derivation and Svelte’s `{#await}` block. Render the resolved module’s default export as the content component. An obsolete import promise must not replace the currently selected article; use the await block’s existing behavior rather than adding request counters.

Call the supplied `meta({ title, description })` with the catalog title and excerpt. Provide loading, unknown-article and import-error states. An unknown ID must not silently show another article.

Runtime chain:

```text
/article/1
  → Router resolves /article/*
  → Article.svelte
      → currentPath supplies the ID
      → markdownCatalogs.articles supplies metadata
      → selected articleModules import loads the compiled content
      → await block receives the component
      → Main + heading + content component
```

## 6. Overview, images and slider

### New Aylin page: `frontend/src/pages/Articles.svelte`

The current plan is to list all 162 articles, sorted by numeric ID ascending: `1` is newest. Keep filenames and their gaps; do not renumber the corpus.

Each entry displays its title link, excerpt and first image when present. Use Pico-based markup and a locally wrapping grid. Pico’s default equal-column rule alone is unsuitable for 162 entries. No pagination or filtering was selected during planning.

Replace the Guide menu entry in Aylin’s `frontend/src/components/Layout.svelte:55` with Articles. The shared menu list already feeds desktop and mobile navigation. Keep `/guide` accessible.

**Unresolved: overview image transfer size.** The plan currently uses original image URLs and lazy image loading. It does not generate thumbnails. Displaying an original image at a smaller CSS size does not reduce its downloaded bytes. The concern raised is roughly a hundred 200 KB images on one page. Lazy loading defers requests but does not reduce the size of each image or the total transferred after scrolling through them. No replacement approach has been selected; this file deliberately records the current plan without inventing one.

### New svUltra component: `src/kit/components/ImageSlider.svelte`

Interface:

```js
images: Array<{ src: string, alt: string, title?: string }>
```

Forward `...rest` to the outer element. Use one active image index, previous/next buttons and a current/total indicator. Disable navigation at the ends. Preserve image proportions with minimal local CSS.

No autoplay, swipe handling, focus trap or additional dependency. The existing package export wildcard supports the direct component import without a new package export entry.

For Aylin’s existing multi-image articles, remove only the blank lines between consecutive image blocks intended to form a slider. Preserve all other text and filenames. Authors retain control: separate paragraphs produce separate image groups.

## 7. Implementation order and verification

1. Extend the shared renderer and add direct `.md` support, image imports and image grouping. Add ImageSlider.
2. Extend route generation with named Markdown directories and catalogs.
3. Apply the narrow router pathname correction.
4. Add Aylin’s configuration, Article and Articles pages, menu entry and image-group normalization. Resolve the overview image-size concern before treating that page’s design as complete.
5. Run focused tests, the frontend build and browser inspection; document the implemented framework behavior.

Aylin currently resolves svUltra from its installed `frontend/node_modules/svultra`, not the local checkout. Before integration verification, link the checkout from Aylin’s `frontend` directory:

```sh
npm link --no-save /home/ronny/Projects/js/svUltra
```

Do not stop or kill the user’s development server.

### Automated coverage

Extend svUltra’s existing `test/markdown.test.js` and `test/generate-routes.test.js` using its current Node test runner.

- Existing inline/file/default-filename Markdown, replacements, dependency tracking and FAQ mode continue to work.
- Direct Markdown passes through the complete preprocessor chain and Svelte compilation.
- Code examples are not changed by syntax sugar.
- Relative images resolve correctly for all three source forms, including file tags whose source directory differs from the host component’s directory.
- Multiple Markdown blocks share imports without duplicate bindings; existing instance/module scripts are preserved.
- Single images, grouped images, separated groups, Markdown line breaks and mixed prose render as specified, including inside FAQ answers.
- Metadata retains link text, handles the corpus’s sentence abbreviations and represents articles without images.
- Multiple configured directories yield independent catalogs, stable output and correctly resolved image URLs.
- Unconfigured projects retain their existing generated route output.
- Add/remove/change watcher events update catalogs; unchanged output is not rewritten and failures remain visible.

Run `npm test` in svUltra and `./dm build front` in Aylin after implementation.

### Browser and build acceptance

- Direct article loading, `/article/1 → /article/2 → /article/1` and Back/Forward update body, title, description and scroll position.
- Changing IDs while the page or Markdown content is loading cannot display an obsolete article.
- Unknown IDs and import failures show their respective states.
- Editing, adding and removing Markdown updates the development site.
- `.image` assets display in development and the production build.
- Visually inspect article typography, overview wrapping and slider controls at desktop and mobile sizes.
- Slider buttons work with normal keyboard activation.
- Production output keeps article bodies lazy and excludes Marked from browser bundles.
- Verify overview image request sizes against the eventual image-size decision; do not count CSS resizing as image optimization.

## 8. Documentation and rollout

Document the implemented configuration, catalog contract, shared image behavior and compilation examples in svUltra’s `docs/markdown.md`, with a reference from its readme. Preserve existing documentation that remains accurate.

Leave Aylin’s copied generic readme unchanged. Starter integration and rollout to other sites come later.

This plan does not authorize deployment, commits or pushes. Its creation is the only filesystem change in this planning step.
