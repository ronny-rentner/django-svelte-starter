<script>
import { onMount } from 'svelte';
import Dialog from '@components/Dialog.svelte';
import Document from '@components/Document.svelte';
import { Link, Button, Icon } from '@components';
import AISearchResults from '@components/anabin/AISearchResults.svelte';

import iconSearch from '@icons/ph/arrow-right';

import { apiClient, submitProcessTask } from "@api/api.svelte.js";
const api = apiClient(submitProcessTask);

let { task, process = $bindable() } = $props();

let errorMessage = $state();

let data = $state({});

if (task?.execution_results?.result) {
  data = task?.execution_results?.result;
}

async function onclick(e) {
  api.execute(task.process, task.slug).then(response => {
    console.log('Anabin search response: ', response)
    if (response.success) {
      try {
        //Update parent form
        process = response['data']['process'];
        console.log('Updated process. Check task. ', process, task);
      } catch (error) {
        console.error("Could not extract process from response: ", error);
      }
      data = response?.data?.result;
      console.log('anabin data: ', data, response);
    } else {
      if (response?.error) {
        errorMessage = response?.error;
      } else {
        errorMessage = 'Failed to search anabin database.';
      }
    }
  });
}

</script>

{if task.is_completed}
  <AISearchResults {data} simple />

{else}
  <p>{task.description}</p>

  <Button icon={iconSearch} {onclick}>Search now</Button>

  {if errorMessage}
    <p class="error-message">{errorMessage}</p>
  {/if}

{/if}
