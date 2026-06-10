<script>
import { onMount } from 'svelte';
import Dialog from '@components/Dialog.svelte';
import Document from '@components/Document.svelte';
import Setting from '@components/account/Setting.svelte';
import { Button } from '@components';

import { submitProcessTask } from "@api/api.js";
import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

//import { loadRecaptcha } from '@lib/utils.js';
//import autofocus from '@lib/autofocus.js';

let { task, process = $bindable() } = $props();

let dialog = $state();

let documentId = $state();
let show = $state(false);

const external = task.category == 'external';

function onclick(event) {
  //console.log('onclick Sign now', event, show);
  if (!show) {
    show = true;
  }
  dialog?.show();
}

function onload(event) {
  //console.log('onload', event);
  const iframe = event.target; // Get the iframe from the event
  /*
  const iframeHeight = iframe.contentWindow?.innerHeight;
  console.log("height: ", iframeHeight);

  if (iframeHeight) {
    iframe.style.height = `${iframeHeight}px`; // Set the height dynamically
  } else {
    console.error("Unable to access iframe content height.");
  }
   */

  // Listen for "escape" messages from the iframe
  window.addEventListener('message', async event => {
    console.log('IFrame message: ', event.data, event);
    if (event.data === 'closeDialogEscape') {
      console.log("Parent received 'closeDialogEscape' message", event);
      dialog?.close();
    }

    if (event.data === 'documentSigned') {
      console.log("Parent received 'documentSigned' message", event);

      dialog?.close();

      const response = await submitProcessTask(task.process, task.slug);
      console.log('Sign response: ', response);
      if (response?.success) {
        try {
          //Update parent form
          process = response['data']['process'];
        } catch (error) {
          console.error("Could not extract process from response: ", error);
        }
      }

      if (!response.success) {
        toastWarning('Failed to check signed document. Try again later.');
      }
    }

  });
}

  /*
$effect(() => {
  documentId = task?.execution_results?.result?.document_id;
  console.log('Signed Document ID: ', documentId, task);
});
   */

//console.log('Task: ', task);

</script>

<style>
Dialog {
  --min-width: min(80vw, 1000px);
  --max-width: 1000px;
  --min-height: 95vh;
  /*padding: 0;*/
  /*
  display: flex;
  flex-direction: column;
   */

  footer {
    /*padding-inline: 2rem;*/
  }

  iframe {
    width: 100%;
    height: auto;
    flex-grow: 1;
    border: none;
  }

  :global(form) {
    margin-inline: calc(var(--pico-block-spacing-horizontal) * -1);
    margin-block: calc(var(--pico-block-spacing-vertical) * -1);
  }
}
</style>

{if task.is_completed}
  <p>The signed document has also been stored in your <a href="/account/documents">documents area</a>.</p>
  <Document id={task?.execution_results?.result?.document_id} />
{else}
  <p>{task?.description}</p>

  {if external}
    {if task?.config?.wait_thumbnail}
      <Setting name="notify_email_3rd_party_signature_completed">Notify me via email when the document has been signed</Setting>
      <Document fileType=".pdf" file={task?.config?.wait_thumbnail} label={task?.config?.wait_thumbnail_label} />
    {/if}
  {else}
    <button {onclick}>Sign now</button>

    {if show}
      <Dialog bind:this={dialog} open noform>
        <h2 slot="header">{task.name}</h2>
        <iframe {onload} src={process.state_data.sign_request_url+"?iframe=1"} />
        {if 0}
          <footer>
            <Button class="outline" type="cancel" onclick={(event) => dialog.close(event)}>Cancel</Button>
          </footer>
        {/if}
      </Dialog>
    {/if}
  {/if}
{/if}
