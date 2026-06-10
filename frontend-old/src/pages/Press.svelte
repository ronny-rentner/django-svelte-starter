<script>
  import { Main } from '@components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Press kit - RELONEE',
    description: 'Resources for media and press.'
  });
</script>

<Main>
  <markdown />
</Main>
