<script module>
  import './init.js';
</script>

<script>
  import { onMount } from 'svelte';

  import { checkAuthStatus } from '@api/api.js';
  import { cancelRequest } from '@kit/api';

  import { Router } from '@kit/router';
  import Layout from '@components/Layout.svelte';

  import { routes } from './generatedRoutes.svelte.js';

  //TODO: Do we still have to import the favicon to include it in the bundle (and therefore manifest)?
  import '@assets/favicon.svg';

  onMount(() => {
    checkAuthStatus();
    return (() => {
      cancelRequest(checkAuthStatus);
    });
  });
</script>

<Router {routes} {Layout} />
