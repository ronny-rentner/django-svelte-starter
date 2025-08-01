<svelte:head>
  {if ! window.pdfjsLib}
    <script {onload} async src="https://cdn.jsdelivr.net/npm/pdfjs-dist@latest/build/pdf.min.js" nonce={window.config.nonce}></script>
  {/if}
  {if ! window.pdfjsWorker}
    <script {onload} async src="https://cdn.jsdelivr.net/npm/pdfjs-dist@latest/build/pdf.worker.min.js" nonce={window.config.nonce}></script>
  {/if}
</svelte:head>

<script>
import { onMount, onDestroy } from 'svelte';

let { file, width = "400px", hidden = false, alt = "Document Preview", ...rest } = $props();

let canvas = $state();
let previewUrl = $state();

let processed = $state(false);
let rendered = $state(false);

function onload() {
  if (window?.pdfjsLib && window?.pdfjsWorker) {

    //pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.worker.min.js';
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = window.pdfjsWorker;

    if (file) {
      if (!rendered) {
        processFile(file);
      }
    }
  }
}

$effect(onload);

//Called to preview a file that is being uploaded by the user.
//Done by creating a blob URL locally at the user's browser.
function processFile(file) {
  console.log('processFile', file);
  const fileType = file?.type || '';

  if (fileType.startsWith('image/')) {
    //We intentionally only set this to true for images, but not PDF files,
    //because for images, somehow we get a loop
    rendered = true;
    renderImage(file);
  } else if (fileType === 'application/pdf') {
    rendered = true;
    renderPDF(file);
  } else {
    //Nothing to do, will render as a normal image below
    //console.error('Unsupported file type:', fileType, file);
  }
}

function renderImage(file) {
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
  }
  previewUrl = URL.createObjectURL(file);
  console.log('preview URL: ', previewUrl);
}

async function renderPDF(file) {
  console.log('renderPDF()');
  try {
    const arrayBuffer = await file.arrayBuffer();
    const typedarray = new Uint8Array(arrayBuffer);

    const loadingTask = window?.pdfjsLib.getDocument({ data: typedarray });
    const pdf = await loadingTask.promise;

    //console.log('PDF loaded');

    // Fetch the first page
    const pageNumber = 1;
    const page = await pdf.getPage(pageNumber);
    //console.log('Page loaded: ', page);

    //It can happen that the canvas disappears again when the upload fails
    if (!canvas) {
      //console.log('Canvas is gone');
      return;
    }
    //console.log('canvas: ', canvas);

    const context = canvas.getContext('2d');
    const outputScale = window.devicePixelRatio || 1;

    /*
      let viewport = page.getViewport({ scale });

      const transform = outputScale !== 1
        ? [outputScale, 0, 0, outputScale, 0, 0]
        : null;
     */

    let desiredWidth = 400;
    let viewport = page.getViewport({ scale: 1, });

    //console.log(`PDF rendering state: desiredWidth=${desiredWidth} outputScale=${outputScale} viewport.width=${viewport.width} viewport.height=${viewport.height}`);
    let scale = (desiredWidth) / viewport.width;
    let scaledViewport = page.getViewport({ scale: scale, });
    //console.log(`PDF calculation: scale=${scale} scaled.width=${scaledViewport.width} scaled.height=${scaledViewport.height}`);
    viewport = scaledViewport;

    // Prepare canvas using PDF page dimensions
    canvas.width = Math.floor(viewport.width);
    canvas.height = Math.floor(viewport.height);
    canvas.style.width = Math.floor(viewport.width) + "px";
    canvas.style.height =  Math.floor(viewport.height) + "px";

    // Render PDF page into canvas context
    const renderContext = {
      canvasContext: context,
      viewport: viewport,
      //transform: transform
    };
    const renderTask = page.render(renderContext);
    await renderTask.promise;

    //hidden = false;

    //console.log('PDF page rendered', viewport, canvas);
  } catch (error) {
    console.error('Error rendering PDF:', error);
  }
}

onDestroy(() => {
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
  }
});
</script>

<style>
canvas {
  border: var(--pico-border-width) solid var(--pico-primary-border);
  /*margin-bottom: 1rem;*/

  &.hidden {
    display: hidden;
  }
}
</style>

{if file && file?.type?.startsWith('image/')}
  <img src={previewUrl} {alt} style:{width} {...rest} />
{elif file && file.type === 'application/pdf'}
  {#key file?.name}
    <canvas bind:this={canvas} class:hidden {...rest}></canvas>
  {/key}
{elif typeof file === 'string'}
  <img src={file} {alt} style:{width} {...rest} />
{else}
  <p>Unsupported file type.</p>
{/if}

