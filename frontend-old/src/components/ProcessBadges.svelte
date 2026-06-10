<script>
  import Badge, { Badges } from '@components/Badge.svelte';

  let { process: p, ...rest } = $props();
</script>

<Badges>
  {if p?.is_completed}<Badge color="green">completed</Badge>{/if}
  {if p?.state == 'pending' && !p?.is_blocked}<Badge color="blue">pending</Badge>{/if}
  {if p?.is_blocked}<Badge color="red">blocked</Badge>{/if}
  {if p?.is_action_required}<Badge color="orange">action required</Badge>{/if}
  {if p?.is_waiting}<Badge color="blue">waiting for event</Badge>{/if}
</Badges>
