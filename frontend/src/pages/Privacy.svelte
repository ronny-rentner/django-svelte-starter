<script>
  import { Main } from '@kit/components';

  let { meta, ...rest } = $props();
  meta({
    title: 'Privacy',
    description: 'How personal data is collected, used and protected.'
  });
</script>

<Main {...rest}>
  <markdown file="Privacy.md" />
</Main>
