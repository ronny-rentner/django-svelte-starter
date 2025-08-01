<script>
  let { children, ...rest } = $props();
</script>

<style>
  table {
    overflow-x: auto;
    display: block;
  }
</style>

<table {...rest}>
{@render children()}
</table>
