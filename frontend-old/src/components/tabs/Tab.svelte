<script>
  import { getContext, onMount, tick } from 'svelte';

  import getId from './id';
  import { TABS } from './Tabs.svelte';

  let tabEl;

  export let id;

  const tab = {
    id: getId(),
    dataId: id
  };
  const { registerTab, registerTabElement, selectTab, selectedTab, controls } = getContext(TABS);

  let isSelected;
  $: isSelected = $selectedTab === tab;

  registerTab(tab);

  onMount(async () => {
    await tick();
    registerTabElement(tabEl);
  });
</script>

<style>
  li {
    font-weight: bold;
    cursor: pointer;
    user-select: none;
    position: relative;

    &.selected {
      color: var(--pico-primary);
    }

    &:focus-visible {
      outline: 0;
      box-shadow: 0 0 0 var(--pico-outline-width) var(--pico-primary-focus);
    }
  }
</style>

<li
  bind:this={tabEl}
  role="tab"
  id={tab.id}
  data-id={tab.dataId}
  aria-controls={$controls[tab.id]}
  aria-selected={isSelected}
  tabindex="{isSelected ? 0 : -1}"
  class:selected={isSelected}
  class:Tab={1}
  on:click={() => selectTab(tab)}
  {...$$restProps}
>
	<slot></slot>
</li>
