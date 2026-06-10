<script>
  import { getContext, tick, onMount } from 'svelte';
  import { TABS } from './Tabs.svelte';

  let {children, class: className, offsetWidth = $bindable("0px"), offsetLeft = $bindable("0px"),  ...rest} = $props();

  let ul;

  const { registerTab, registerTabElement, selectTab, selectedTab, controls } = getContext(TABS);

  $effect(() => {
    const element = document.getElementById($selectedTab.id);
    offsetWidth = `${element.offsetWidth}px`;
    offsetLeft = `${element.offsetLeft}px`;
  });

</script>

<style>
  ul {
    position: relative;

    &::before {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: var(--tab-width);
      height: 2px;
      background-color: var(--pico-primary); /* The color of the border */
      transform: translateX(var(--tab-offset));
      transition: transform 0.3s ease;
    }

  }

</style>

<nav>
  <ul role="tablist" style="--tab-width:{offsetWidth}; --tab-offset:{offsetLeft};" class="{className} TabList" bind:this={ul} {...rest}>
    {@render children()}
  </ul>
</nav>
