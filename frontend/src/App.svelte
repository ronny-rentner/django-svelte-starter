<script module>
  import './init.js';
</script>

<script>
  //TODO: Do we need this?
  //import 'vite/modulepreload-polyfill'

  import { onMount } from 'svelte';

  import { checkAuthStatus, cancelRequest } from '@api/api.js';

  import Router, { preloaded } from './components/Router.svelte';
  import { routes } from './generatedRoutes.svelte.js';

  import Layout from './components/Layout.svelte';

  //TODO: Do we still have to import the favicon to include it in the bundle (and therefore manifest)?
  import '@assets/favicon.svg';

  //const isProduction = process.env.NODE_ENV === 'production';

  onMount(() => {
    // Initialize with the light mode by default
    //document.documentElement.classList.add('has-light-background');
    checkAuthStatus();

    return (() => {
      cancelRequest(checkAuthStatus);
    });
  });

</script>

<Router routes={routes} Layout={Layout} />

