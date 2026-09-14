<script>
  import { Main } from '@kit/components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Terms',
    description: 'The terms that govern use of the site.'
  });
</script>

<Main {...rest}>
  <markdown file="Terms.md" />
</Main>
