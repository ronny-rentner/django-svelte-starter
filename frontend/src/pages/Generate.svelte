<script>
import { Main, Icon, Link } from '@components';

import SearchForm from '@components/generate/SearchForm.svelte';

import warningIcon from '@icons/ph/warning-circle-duotone';
import successIcon from '@icons/ph/check-circle-duotone';
import noneIcon from '@icons/ph/x-circle-duotone';  

let {
  searchString = $bindable(''),
  country = $bindable(),
  loading = false,
  onsubmit,
  placeholder = "Search",
} = $props(); 

let message = $state();
let messageIcon = $state(warningIcon); 

let searchField;

</script>

<Main>
  <h1>Generate</h1>

  <section>
    <SearchForm bind:this={searchField} bind:searchString bind:country {loading} {onsubmit} {placeholder} />
    {if message}
      <p><Icon icon={messageIcon} size="1.2rem">{@html message}</Icon></p>
    {else}
      <p>&nbsp;</p>
    {/if}
  </section>  

</Main>
