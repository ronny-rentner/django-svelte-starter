<script>
import { onMount } from 'svelte';
import Dialog from '@components/Dialog.svelte';
import { Button } from '@components';

import { submitProcessTask } from "@api/api.js";
import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

let { task, process = $bindable() } = $props();

async function onclick(event) {
  console.log('onclick', event);
  const response = await submitProcessTask(task.process, task.slug);
  console.log('Prepare response: ', response);
  if (response?.success) {
    //console.log('GOT RESP', uploading, processing, uploadProgress);
    console.log('Response: ', response);
    try {
      //Update parent form
      process = response['data']['process'];
    } catch (error) {
      console.error("Could not extract process from response: ", error);
    }
  }

  if (!response.success) {
    toastWarning('Failed to prepare document. Try again later.');
  }
}

//console.log('task: ', task);

</script>

<style>
</style>

{if task.status != 'completed'}
  <p>{task?.description}</p>
  <button {onclick}>Prepare now</button>
{else}
  All done, please continue with the next step.
{/if}
