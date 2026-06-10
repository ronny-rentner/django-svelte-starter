<script>
import { fade } from 'svelte/transition';

import Dropzone from "svelte-file-dropzone";

import { Icon, Button } from '@components';
//import Preview from '@components/DocumentPreview.svelte';
import Document from '@components/Document.svelte';

import { submitProcessTask } from "@api/api.js";

import { formatFileSize, parseFileSize } from "@lib/utils.js";

import fileUploadIcon from '@icons/ph/upload-duotone';

//TODO: Take max and min sizes from task configuration
const FALLBACK_MAX_FILE_SIZE = 20 * 1024 * 1024;
const MIN_FILE_SIZE = 10 * 1024;
const ALLOWED_FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png'];

let { task, process = $bindable() } = $props();

let file = $state();

let uploadProgress = $state(0);
let uploading = $state(false);
let processing = $state(false);
let message = $state('');
let fileErrorMessage = $state('');

let maxFileSize = parseFileSize(task?.config?.max_file_size, FALLBACK_MAX_FILE_SIZE)

$effect(() => {
  maxFileSize = parseFileSize(task?.config?.max_file_size, FALLBACK_MAX_FILE_SIZE)
});

async function skipStep(e) {
  const data = {'skip': true};
  const response = await submitProcessTask(task.process, task.slug, data);
  if (response?.success) {
    try {
      process = response['data']['process'];
    } catch (error) {
      console.error("Could not extract process from response: ", error);
    }
  } else {
    if (response?.error) {
      fileErrorMessage = response?.error;
    } else {
      fileErrorMessage = 'File upload failed. Please try again later.';
    }
  }
}

async function handleFilesSelect(e) {
  const files = e.detail.acceptedFiles;
  if (files.length > 0) {
    file = files[0]
    console.log('handleFilesSelect: ', file, file.size, file.name, file.type);

    //TODO: BREAK;
    //return;

    fileErrorMessage = '';  // Reset the error before processing the file

    // Check for file size being zero
    if (file.size <= MIN_FILE_SIZE) {
      fileErrorMessage = `The file size is too small, it needs to be at least 10 KB. Your file is ${(file.size / (1024)).toFixed(2)} KB.`;
      file = undefined;
      return;
    }

    // Check for file size exceeding the limit
    if (file.size > parseFileSize(task?.config?.max_file_size, FALLBACK_MAX_FILE_SIZE)) {
      fileErrorMessage = `The file size exceeds the ${task?.config?.max_file_size} limit. Your file is ${formatFileSize(file.size)}.`;
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
      const data = {};
      console.log('Files: ', files);

      response = await submitProcessTask(task.process, task.slug, data, files, updateProgress);
    } catch (error) {
      console.error("File upload failed: ", error);
      fileErrorMessage = 'File upload failed. Please try again later.';
    } finally {
      uploading = false;
      processing = false;
      uploadProgress = 0;
      console.log('Response: ', response);
    }

    if (response?.success) {
      try {
        process = response['data']['process'];
      } catch (error) {
        console.error("Could not extract process from response: ", error);
      }
    } else {
      if (response?.error) {
        fileErrorMessage = response?.error;
      } else {
        fileErrorMessage = 'File upload failed. Please try again later.';
      }
    }
  }
}

async function updateProgress(loaded, total) {
  //Convert to string so we can see '0 %' in the progress bar
  uploadProgress = String(Math.round((loaded / total) * 100));
  //console.log('updateProgress', loaded, total, uploadProgress);
  if (uploadProgress == 100) {
    processing = true;
  }
}

  /*
$effect(() => {
  documentId = task?.execution_results?.result?.document_id;
  console.log('Upload Effect: ', documentId);
  //task;
  //documentId;
});
   */



function reset(event) {
  //console.log('Reset', event);
  file = undefined;
  fileErrorMessage = undefined;
  /*
  searchState.update({
    response: undefined,
    file: undefined,
    data: undefined,
    steps: startSteps(),
  });
   */
}

</script>

<style>
div.dropzone {
  max-width: 36rem;

  Dropzone {
    background-color: var(--pico-dropzone-background-color);
    border: calc(var(--pico-border-width) * 2) dashed var(--pico-h4-color);
    border-radius: calc(var(--pico-border-radius) * 2);

    margin-bottom: 1rem;
    padding: calc(var(--pico-form-element-spacing-vertical) * 3) calc(var(--pico-form-element-spacing-horizontal) * 3);

    max-width: 400px;

    &:hover, &:focus {
      background-color: var(--pico-dropzone-background-hover-color);
      border-color: var(--pico-primary-hover);

      div.dropzone-inner {
        color: var(--pico-primary-hover);
      }
    }
  }

  div.dropzone-inner {
    font-size: 110%;
    line-height: 125%;
    color: var(--pico-h4-color);
    text-align: left;

    Icon {
      margin-right: 1rem;
    }

    small {
      display: block;
      line-height: 125%;
      margin-top: var(--pico-typography-spacing-vertical);

      & + small {
        margin-top: calc(var(--pico-typography-spacing-vertical) * 0.75);
      }
    }
  }
}

/*
progress {
  margin-top: 0.5rem;
  height: 0.5rem;
}
*/

</style>

<div class="dropzone" transition:fade>
  {if file}
    <Document {file} progress={uploadProgress} />
  {elif task.is_completed}
    <Document id={task?.execution_results?.result?.document_id} refresh />
  {else}
    <Dropzone on:drop={handleFilesSelect} accept="image/jpeg, image/png, application/pdf">
      <div class="dropzone-inner">
        <Icon icon={fileUploadIcon} size="3.5rem">{task.description}</Icon>
        <small>Drag and drop the requested document onto this box or click to select.</small>
        <small>Allowed file types are {task.config.allowed_file_types.map(t => `*.${t}`).join(', ')}.</small>
      </div>
    </Dropzone>
    {if task.skippable}<Button class="outline" onclick={skipStep}>{task.skippable}</Button>{/if}
  {/if}

  {if fileErrorMessage}
    <p class="error-message">
      {fileErrorMessage}
    </p>
    <Button class="outline" type="reset" onclick={reset}>Reset file</Button>
  {/if}
</div>
