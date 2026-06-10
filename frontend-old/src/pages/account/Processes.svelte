<script>
import { getContext, onMount, onDestroy } from 'svelte';

import { personStore as person, processesStore as processes } from '@stores';
import AccountLayout from '@layout/Account.svelte';
import LoadingOverlay from '@components/LoadingOverlay.svelte';
import LoadingIndicator from '@components/LoadingIndicator.svelte';

import ProcessBadges from '@components/ProcessBadges.svelte';

import { Button, Link, Icon } from '@components';
import nextIcon from '@icons/ph/arrow-right';

import { fetchPersonProcesses, apiClient } from "@api/api.svelte.js";

const api = apiClient(fetchPersonProcesses);

if ($person) {
  api.execute($person?.id);
}

function getBlockedMessage(blockedReason) {
  if (!blockedReason) {
    return '';
  }
  const { reason, required_processes } = blockedReason;

  // Start with the main reason
  let message = `${reason}: <br />`;

  // Add each required process in a compact format
  if (required_processes && Object.keys(required_processes).length > 0) {
    const processes = Object.entries(required_processes)
      .map(([process, details]) => details?.message || `<i>${details.name}</i> needs to be ${details.required_state}`)
      .join(", ");

    message += `${processes}`;
  }

  return message;
}

function getProgress(p, max) {
  let progress = (p?.counts?.resolved * (max / p?.counts?.total)) || 1;
  //console.log('Calculated progress: ', progress);
  return progress;
}

//$effect(() => {
//  console.log('Processes: ', $processes);
//});

</script>

<style>
article {
  --pico-typography-spacing-vertical: 0.75rem;

  max-width: min(40rem, 40vw);
  min-width: min(40rem, 40vw);
  /*--pico-card-box-shadow: rgba(0, 0, 0, 0.12) 0rem 0.25rem 0.5rem;*/
  display: block;
  margin-right: 1rem;
  vertical-align: top;
  padding-top: 1rem;

  @light & {
    background-color: var(--pico-primary-inverse);
  }

  progress {
    height: 0.5rem;
  }

  footer {
    text-align: right;
    display: flex;
    line-height: 1rem;
    flex-direction: row-reverse;
    gap: calc(var(--pico-form-element-spacing-horizontal) * 1);
    align-items: center;
    @dark & small {
        color: var(--pico-muted-color);
    }
  }
}

</style>

{snippet process(p)}
  <article>
    <ProcessBadges process={p} />

    <h2>{p?.name || 'Process'}</h2>

    <p>{p?.description}</p>

    {if ! p?.is_blocked && ! p?.is_completed}
      <hr />
      <center>{p?.counts?.resolved} of {p?.counts?.total} tasks resolved</center>
      <progress max=50 value={getProgress(p, 50)} />
    {/if}

    <footer>
      {if p?.state == 'completed' || p?.is_waiting}
        <Link href="/account/process?{p.id}" role="button" icon={nextIcon} class="outline">View</Link>
      {else}
        {if p?.counts?.completed == 0}
          <Link href="/account/process?{p.id}" role="button" icon={nextIcon} disabled={p?.is_blocked}>Start</Link>
        {else}
          <Link href="/account/process?{p.id}" role="button" icon={nextIcon} disabled={p?.is_blocked}>Continue</Link>
        {/if}
      {/if}
      {if p?.is_blocked}
        <small>{@html getBlockedMessage(p?.blocked_reason)}</small>
      {/if}
    </footer>
  </article>
{/snippet}


<AccountLayout>
  <h1>Processes<LoadingIndicator loading={api.loading} /></h1>

  {if $processes}
    {each Object.entries($processes) as [ index, p ]}
      {render process(p)}
    {/each}
  {/if}

</AccountLayout>
