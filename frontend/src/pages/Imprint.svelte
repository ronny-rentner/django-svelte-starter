<script>
  import { Main } from '@kit/components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Imprint',
    description: 'Legal information about the site operator.'
  });
</script>

<Main {...rest}>
  <markdown file="Imprint.md" />
</Main>
