<script>
import Badge, { Badges } from '@components/Badge.svelte';

let { document, ...rest } = $props();
</script>

<style>
Badges {
  position: absolute;
  top: 0;
  left: 0;

  :global(article:has(> &)) {
    position: relative;
  }
}
</style>

<Badges>
  {const p=document}
  <Badge color="blue">{document.document_type}</Badge>
  {if p?.is_blocked}<Badge color="red">blocked</Badge>{/if}
  {if p?.counts?.possible > 0}<Badge color="orange">action required</Badge>{/if}
</Badges>

{if 0}<p />{/if}
