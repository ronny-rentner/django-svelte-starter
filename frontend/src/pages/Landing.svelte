<script>
  import { getContext, onDestroy } from 'svelte';
  import { Main, Button } from 'svultra/kit/components';
  import { navigate } from 'svultra/kit/router';

  let { meta, ...rest } = $props();
  meta({
    title: 'Landing',
    description: 'A full-screen landing page with the site header hidden via pageConfig.'
  });

  // Hide the site header for this page; restore it when navigating away.
  const pageConfig = getContext('pageConfig');
  pageConfig.showHeader = false;
  onDestroy(() => { pageConfig.showHeader = true; });
</script>

<style>
  section.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 100vh;
    gap: 1rem;
  }
</style>

<Main {...rest}>
  <section class="hero">
    <h1>Welcome</h1>
    <p>
      This is a full-screen landing page. The site header is hidden because this
      page set <code>pageConfig.showHeader = false</code>. Other flags like
      <code>showFooter</code> and <code>contrast</code> are covered in the
      <a href="https://github.com/ronny-rentner/svUltra#pageconfig">docs</a>.
    </p>
    <Button onclick={() => navigate('/')}>Enter the app</Button>
  </section>
</Main>
