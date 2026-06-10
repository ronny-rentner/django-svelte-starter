<script>
import { getContext, onMount, onDestroy } from 'svelte';

import { personStore as person } from '@stores';
import AccountLayout from '@layout/Account.svelte';
import LoadingIndicator from '@components/LoadingIndicator.svelte';

import { fetchPersonDocuments, apiClient  } from "@api/api.svelte.js";

import DocumentBadges from '@components/DocumentBadges.svelte';

import Document from '@components/Document.svelte';

let documents = $state([]);

const api = apiClient(fetchPersonDocuments);

if ($person.id) {
  api.execute($person?.id);
}

const sort = (documents) => Object.entries(documents).sort(
  (a, b) => new Date(a[1]?.created_at) - new Date(b[1]?.created_at)
).reverse();

</script>

<style>
</style>



<AccountLayout>
  <h1>Documents<LoadingIndicator loading={api.loading} /></h1>

  {if $person?.documents}
    {each sort($person.documents) as [ index, document ]}
      <Document {document} />
    {/each}
  {/if}

</AccountLayout>
