<script>
  import { Main } from 'svultra/kit/components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Guide',
    description: 'A long-form content page rendered from markdown.'
  });
</script>

<Main {...rest}>
  <markdown file="guide.md" />
</Main>
