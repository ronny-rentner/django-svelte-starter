# Guide

This page is rendered from a markdown file. The `<markdown file="guide.md" />`
tag in `Guide.svelte` is replaced at build time with the compiled HTML — the
component stays focused on layout while the prose lives in a file that anyone
can edit.

## Why markdown content pages

Long-form content — guides, docs, legal text — changes far more often than the
component around it. Keeping it in markdown means edits never touch Svelte code,
and the build rebuilds the page when the markdown changes.

## What you can write

Standard markdown works: **bold**, *italic*, `inline code`, lists, and links.

- Bullet lists
- With multiple items

1. Numbered steps
2. In order

Links to [the Svelte docs](https://svelte.dev) open in a new tab automatically,
while internal links stay in-app.

```js
// Code blocks render too, with braces safely escaped
const greeting = { hello: 'world' };
```

> Blockquotes are handy for callouts and pull quotes.
