<script module>
/*
  export { default as Badge } from '@components/Badge.svelte';
 */
</script>

<script>
  let { children, ...rest } = $props();
</script>

<style>
  div {
    display: flex;
    margin-bottom: var(--pico-spacing-50);
    gap: var(--pico-spacing-50);
  }
</style>

<div {...rest}>{@render children()}</div>
