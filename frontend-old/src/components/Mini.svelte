<script>
  import { fade, slide } from 'svelte/transition';

  let { slot1 } = $props();

  let showDiv = $state(false);

  function toggleDiv() {
    console.log('toggleDiv');
    showDiv = !showDiv;
  }
</script>

<style>
  .test-div {
    width: 100px;
    height: 100px;
    background-color: lightblue;
  }
</style>

<button onclick={toggleDiv}>
  Toggle Div
</button>

{#if showDiv}
  <div class="test-div" transition:slide={{ duration: 500 }}>
    {@render slot1('some string')}
  </div>
{/if}
