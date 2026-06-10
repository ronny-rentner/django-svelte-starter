<script>
import { onMount, onDestroy } from 'svelte';
import Dialog from '@components/Dialog.svelte';
import Document from '@components/Document.svelte';
import { Button, Icon } from '@components';
import Chat from '@components/Chat.svelte';

import { createLocalStorageStore } from '@src/stores.svelte.js';
import { personStore as person } from '@stores';

//import iconAI from '@icons/ph/arrow-right';
import iconAI from '@icons/ph/robot-duotone';
import iconChat from '@icons/ph/chats-duotone';

let { task, process = $bindable() } = $props();

import { apiClient, submitProcessTask } from "@api/api.svelte.js";
const api = apiClient(submitProcessTask);

let mKey = `genai_chat_videx_${process.id}`;
let messages = createLocalStorageStore(mKey, [])();

let chatActive = $state(false);

//import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

//import { loadRecaptcha } from '@lib/utils.js';
//import autofocus from '@lib/autofocus.js';

async function sendMessage(msg) {
  if (msg) {
    console.log('Message pushed: ', msg);
    messages.push({ sender: 'user', text: msg })
    //console.log('Messages pushed: ', $state.snapshot(messages));
  }
  return api.execute(task.process, task.slug, { 'form': 'videx', 'message': msg || '' }).then(response => {
    console.log('Response: ', response);
    if (response.success) {
      try {
        //Update parent form
        process = response['data']['process'];
      } catch (error) {
        console.error("Could not extract process from response: ", error);
      }
      if (response.data?.result?.history_was_resetted) {
        messages.length = 0
      }

      if (response.data?.result?.message) {
        messages.push({ sender: 'ai', text: response.data?.result?.message })
        //console.log('Messages pushed: ', $state.snapshot(messages));
      }
    }
  });
}

</script>

<style>
Icon {
  align-self: flex-start;
}

</style>

{if task.is_completed}
    <Icon icon={iconChat} size="1.5rem">Thank you. All done. You may continue with the next task.</Icon>
{else}

  {if chatActive}

    <Chat {messages} {sendMessage} />
  {else}
    <p>{task?.description}</p>
    <Button icon={iconChat} onclick={() => { chatActive = true;}}>Start chat</Button>

  {/if}


{/if}

