<script>
  import { getContext } from 'svelte';

  import getId from './id';
  import { TABS } from './Tabs.svelte';

  export let retainState = true; // New prop to control state retention

  const panel = {
    id: getId()
  };
  const { registerPanel, selectedPanel, labeledBy } = getContext(TABS);

  registerPanel(panel);
</script>

<style>
  .hidden {
    display: none;
  }
</style>

<div
  id={panel.id}
  aria-labelledby={$labeledBy[panel.id]}
  role="tabpanel"
  class:hidden={retainState && $selectedPanel !== panel}
  {...$$restProps}
>
  {#if retainState || $selectedPanel === panel}
    <slot isVisible={$selectedPanel === panel}></slot>
  {/if}
</div>
