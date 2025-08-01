<script>
  import AnabinSearch from '@components/AnabinSearch.svelte';
  import { searchDegrees } from '@api/api.js';

  let { country = $bindable(), highlight = $bindable(), showTranslations = $bindable() } = $props();
</script>

<AnabinSearch
  searchFunction={searchDegrees}
  placeholder="Search degree"
  type="degrees"
  bind:country
  bind:highlight
  bind:showTranslations
/>
