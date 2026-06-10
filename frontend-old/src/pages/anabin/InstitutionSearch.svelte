<script>
  import AnabinSearch from '@components/AnabinSearch.svelte';
  import { searchInstitutions } from '@api/api.js';

  let { country = $bindable(), highlight = $bindable(), showTranslations = $bindable() } = $props();
</script>

<AnabinSearch
  searchFunction={searchInstitutions}
  placeholder="Search institution"
  type="institutions"
  bind:country
  bind:highlight
  bind:showTranslations
/>
