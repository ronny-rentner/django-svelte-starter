<script>
  import { Main } from '@components';

  let { meta, children, ...rest } = $props();
  meta({
    title: 'About Us - RELONEE',
    description: 'Learn more about RELONEE relocation services.'
  });

</script>


<Main>
  <markdown />
</Main>

