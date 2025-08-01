<script>
  import { onMount } from 'svelte';

  let { children } = $props();

</script>

<h2><span>{@render children()}</span></h2>
