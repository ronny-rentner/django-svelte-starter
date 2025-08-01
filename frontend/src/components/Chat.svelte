<script>
import { Button, Icon } from '@components';
import LoadingDots from '@components/LoadingDots.svelte';
import { fly } from 'svelte/transition';
import { onMount } from 'svelte';

import autofocus from '@lib/autofocus.js';
import { renderMarkdown } from '@lib/utils.js';

import iconSend from '@icons/ph/arrow-right';
import iconAI from '@icons/ph/robot-duotone';
import iconUser from '@iconify-icons/ph/user-square-duotone';

let { messages, sendMessage, value = $bindable(''), placeholder = "Type a message..", final, ...rest } = $props();

let isTyping = $state(false);
let messagesContainer;

//When messages are empty, let's send an empty inital message to the API.
//This should give us an inital greeting from the GenAI.
if (messages.length === 0) {
  send();
}

function send(msg) {
  isTyping = true;

  sendMessage(msg).then((response) => {
    //console.log('onclick after submission: ', value, response);
    isTyping = false;
  });

}

function onclick() {
  if (!value) return;

  const msg = `${value}`;
  //console.log('onclick msg: ', msg);
  value = '';
  send(msg);
}

function scrollToBottom() {
  //console.log('Scroll to bottom: ', messagesContainer);
  if (messagesContainer) {
    messagesContainer.scroll({ top: messagesContainer.scrollHeight, behavior: 'smooth' });
  }
}

onMount(() => {
  const observer = new MutationObserver(() => {
    scrollToBottom();
  });
  if (messagesContainer) {
    observer.observe(messagesContainer, { childList: true });
  }
  scrollToBottom();
  return () => observer.disconnect();
});

function onkeydown(e) {
  // If Enter is pressed without Shift, prevent the newline and send the message.
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    onclick();
  }
  // If Shift+Enter is pressed, do nothing so that a newline is inserted.
}


</script>

<article transition:fly={{ y: -10, duration: 1000 }}  {...rest}>
  <div class="messages" bind:this={messagesContainer}>
    {#each messages as msg}
      <div transition:fly={{ y: 10, duration: 200 }} class="message" class:ai={msg.sender !== 'user'} class:user={msg.sender === 'user'}>
        {if msg.sender === 'user'}
          <Icon icon={iconUser} size="1.5rem" /><div>{html renderMarkdown(msg.text)}</div>
        {else}
          <Icon icon={iconAI} size="1.5rem" /><div>{html renderMarkdown(msg.text)}</div>
        {/if}
      </div>
    {/each}
    {if isTyping}
      <div class="message ai">
        <Icon icon={iconAI} size="1.5rem" /><div><p><LoadingDots loading={isTyping}>AI is typing</LoadingDots></p></div>
      </div>
    {/if}
  </div>
  {if ! final}
    <fieldset role="group">
      <textarea bind:value {placeholder} {onkeydown} use:autofocus />
      <Button icon={iconSend} {onclick} class="primary">Send</Button>
    </fieldset>
  {/if}
</article>

<style>

  article {
    padding: 0;
    max-width: 40rem;
    border-top: var(--pico-muted-color) 0.25rem solid;
    &:has(:focus) {
      border-top: var(--pico-primary) 0.25rem solid;
    }
  }

  Icon {
    margin: 0 0.35rem 0 0;
  }

  Button {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  fieldset {
    margin-bottom: 0;
    border-top-right-radius: 0;
    border-top-left-radius: 0;

    textarea {
      border-top-left-radius: 0;
    }
    Button {
      border-top-right-radius: 0;
    }

    &:has(textarea:focus, button:focus) {
      margin: 0 var(--pico-border-width) 0 var(--pico-border-width);
      width: calc(100% - 2 * var(--pico-border-width)) !important;
    }
  }

  .messages {
    padding-inline: 0;
    min-height: 12rem;
    max-height: 30rem;
    overflow-y: auto;
    scrollbar-gutter: stable;
  }

  .message {
    border-radius: var(--border-radius);
    display: flex;
    align-items: flex-start;
    padding: calc(var(--pico-form-element-spacing-vertical) * 1) calc(var(--pico-form-element-spacing-horizontal) * 0.75);
    padding-bottom: 0;
    border-bottom: 1px var(--pico-primary-border) solid;

    &:last-of-type {
      border-bottom: 0;
    }

    :global(p, ul) {
      margin-bottom: calc(var(--pico-typography-spacing-vertical) * 0.5);
    }
  }

  .ai {
  }

  .user {
    --pico-font-weight: bold;
    background-color: var(--pico-table-alt-background-color);
  }

</style>
