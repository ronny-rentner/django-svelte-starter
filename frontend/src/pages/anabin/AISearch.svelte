<svelte:head>
  <script defer src="https://cdn.jsdelivr.net/npm/pdfjs-dist@latest/build/pdf.min.js" nonce={window.config.nonce}></script>
  <script defer src="https://cdn.jsdelivr.net/npm/pdfjs-dist@latest/build/pdf.worker.min.js" nonce={window.config.nonce}></script>
</svelte:head>

<script>
import { fade } from 'svelte/transition';


import { Icon, Button, Link } from "@components";
import Document from '@components/Document.svelte'; // Import the FilePreview component
import AISearchResults from '@components/anabin/AISearchResults.svelte';
import Accordion from '@components/Accordion.svelte';
import Dropzone from "@components/Dropzone.svelte";

import { uploadFile, anabinAiSearch } from "@api/api.js";
import { aiSearchStore as searchState, overwrite } from '@stores';

import fileUploadIcon from '@icons/ph/upload-duotone';
import oneIcon   from '@icons/ph/number-circle-one-fill';
import twoIcon   from '@icons/ph/number-circle-two-fill';
import threeIcon from '@icons/ph/number-circle-three-fill';

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MIN_FILE_SIZE = 10 * 1024;
const ALLOWED_FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png'];

let file = $state();

let progress = $state(0);
let uploading = $state(false);
let processing = $state(false);
let message = $state('');
let fileErrorMessage = $state('');

//Must be a function, otherwise it gets overwritten
const startSteps = () => [
  {'active': true},
  {'active': false, 'disabled': true},
  {'active': false, 'disabled': true},
];

if (!$searchState?.steps) {
  searchState.update(current => {
    if (!current) {
      current = {};
    }
    current.steps = startSteps();
    return current;
  });
}

async function handleFilesSelect(e) {
  const files = e.detail.acceptedFiles;
  if (files.length > 0) {
    file = files[0]
    console.log('handleFilesSelect: ', file, file.size, file.name, file.type);

    fileErrorMessage = '';  // Reset the error before processing the file

    // Check for file size being zero
    if (file.size <= MIN_FILE_SIZE) {
      fileErrorMessage = `The file size is too small, it needs to be at least 10 KB. Your file is ${(file.size / (1024)).toFixed(2)} KB.`;
      file = undefined;
      return;
    }

    // Check for file size exceeding the limit
    if (file.size > MAX_FILE_SIZE) {
      fileErrorMessage = `The file size exceeds the 10 MB limit. Your file is ${(file.size / (1024 * 1024)).toFixed(2)} MB.`;
      file = undefined;
      return;
    }

    // Check for invalid file type
    if (!file.type || !ALLOWED_FILE_TYPES.includes(file.type)) {
      fileErrorMessage = 'Invalid file type. Only PDF, JPG, and PNG are allowed.';
      file = undefined;
      return;
    }
  }

  if (file) {
    let response;
    uploading = true;
    try {
      response = await uploadFile(file, updateProgress);
      console.log("File uploaded successfully:", response);
    } catch (error) {
      console.error("File upload failed:", error);
      fileErrorMessage = 'File upload failed. Please try again later.';
    } finally {
      uploading = false;
      processing = false;
      progress = 0;
    }

    if (response.success) {
      //console.log('GOT RESP', uploading, processing, progress);
      console.log('Response: ', response);
      searchState.update({
        file: file,
        response: overwrite(response.data),
        steps: {
          0: { active: true },
          1: { active: true, disabled: false },
          2: { active: false, disabled: true }
        }
      });
    }
    console.log('All done, searchstate: ', $searchState);
  }
}

async function updateProgress(loaded, total) {
  progress = Math.round((loaded / total) * 100);
  if (progress == 100) {
    processing = true;
  }
}

function reset(event) {
  //console.log('Reset', event);
  file = undefined;
  searchState.update({
    response: undefined,
    file: undefined,
    data: undefined,
    steps: startSteps(),
  });
}

async function onclick(event) {
  const response = await anabinAiSearch();
  if (!response.success) {
    message = `${response.error}`;
  } else {
    message = '';
    searchState.update({
      data: overwrite(response.data),
      steps: {
        0: { active: false, disabled: false },
        1: { active: true, disabled: false },
        2: { active: true, disabled: false }
      }
    });
  }
}

</script>

<style>
section Accordion {
  div.extracted_data {
    width: fit-content;
  }
}

</style>

<h3>How it works</h3>
<section>
  <Accordion icon={oneIcon} { ... $searchState.steps[0] }>
    {snippet header()}Upload a file with your degree{/snippet}
      {if file && !fileErrorMessage}
        <Document {file} {progress} />
      {else}
        <Dropzone ondrop={handleFilesSelect}>
          Upload a pdf or photo of your degree<br />
          <small>File types *.pdf, *.png, *.jpg</small>
        </Dropzone>
      {/if}
      {if fileErrorMessage}<p class="error-message">{fileErrorMessage}</p>{/if}
  </Accordion>

  <Accordion icon={twoIcon} {...$searchState.steps[1]}>
    {snippet header()}Our AI extracts all necessary data{/snippet}
    <div class="extracted_data">
      {if !processing && $searchState?.response}
        <table class="striped"><thead><tr><th>Field</th><th>Extracted</th></tr></thead><tbody>
            {#each Object.entries($searchState?.response || {}) as [key, value]}
              <tr><td>{key}:</td><td>{value}</td></tr>
            {/each}
        </tbody></table>
      {else if processing}
        Processing
      {else}
        No results. Might be a bug. Please report your file.
      {/if}
      <footer>
        <Button {onclick}>Continue</Button>
        <Button type="reset" onclick={reset}>Reset</Button>
      </footer>
    </div>
    {if message}<span class="error-message">{message}</span>{/if}
  </Accordion>

  <Accordion icon={threeIcon} {...$searchState.steps[2]}>
    {snippet header()}Get a match from the Anabin database{/snippet}
    <AISearchResults data={$searchState?.data} />
  </Accordion>
</section>
