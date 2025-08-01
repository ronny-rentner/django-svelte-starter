<script>
import { getContext, onMount, onDestroy } from 'svelte';

import { personStore as person, processesStore as processes } from '@stores';

import { navigate } from '@components/Router.svelte';

import AccountLayout from '@layout/Account.svelte';
import LoadingIndicator from '@components/LoadingIndicator.svelte';

import { apiClient, fetchPersonProcesses } from "@api/api.svelte.js";
import ProcessBadges from '@components/ProcessBadges.svelte';
import Tasks from '@components/account/tasks/Tasks.svelte';
import { Link } from '@components';

//import UploadDocumentTask from '@components/account/tasks/UploadDocument.svelte';

//import { Link, Icon } from '@components';
//import iconNext from '@icons/ph/arrow-right';

const url = new URL(window.location.href);
const processId = url?.search?.substring(1);

const api = apiClient(fetchPersonProcesses);

if (!processId) {
  //console.log('Missing process ID', processId);
  navigate('/account/processes');
}

if ($person && processId) {
  api.execute($person.id, processId);
}
</script>

<style>
h1 LoadingIndicator {
  margin-left: 0.5rem;
}
</style>

<AccountLayout>
    {if processId in $processes}
      <ProcessBadges process={$processes[processId]} />

      <h1>{$processes[processId]?.name || 'Process'}<LoadingIndicator loading={api.loading} /></h1>
      <p>{$processes[processId]?.description}</p>

      <Tasks bind:process={$processes[processId]} />

      {if ($processes[processId]).is_completed}
        <h3>The process has been completed.</h3>
        <Link href="/account/processes" role="button" class="outline">Back to processes overview</Link>
      {/if}
      {if ($processes[processId]).is_waiting}
        <h3>The process is waiting for an event.</h3>
        <Link href="/account/processes" role="button" class="outline">Back to processes overview</Link>
      {/if}
    {/if}
</AccountLayout>
