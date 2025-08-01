<script>
import { onMount } from 'svelte';
import Dialog from '@components/Dialog.svelte';
import Document from '@components/Document.svelte';
import { Button, Icon } from '@components';

import iconPrepare from '@icons/ph/arrow-right';

//import { personStore as person } from '@stores';

import { apiClient, submitProcessTask } from "@api/api.svelte.js";
const api = apiClient(submitProcessTask);

let { task, process = $bindable() } = $props();

let errorMessage = $state();

function onclick(e) {
  errorMessage = '';
  api.execute(task.process, task.slug).then(response => {
    if (response?.success) {
      try {
        //Update parent form
        process = response['data']['process'];
      } catch (error) {
        console.error("Could not extract process from response: ", error);
      }
    } else {
      errorMessage = response?.error || 'An unknown error occurred';
    }
  });
}

</script>

{if task?.is_completed}
  <p>All done. You can also find the completed form in your document area.</p>
  <Document id={task?.execution_results?.result?.videx_form_document_id} refresh />
{else}
  <p>{task.description}</p>

  <Button icon={iconPrepare} {onclick} disabled={api.loading}>Prepare now</Button>

  {if errorMessage}<p class="error-message">{errorMessage}</p>{/if}
{/if}
