<script>
  import { Main } from '@kit/components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Guide',
    description: 'A long-form content page rendered from markdown.'
  });
</script>

<Main {...rest}>
  <markdown file="Guide.md" />
</Main>
