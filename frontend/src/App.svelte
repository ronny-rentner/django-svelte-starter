<script module>
  import './init.js';
</script>

<script>
  import { Router } from 'svultra/kit/router';
  import Layout from 'svultra/kit/components/Layout.svelte';

  import { routes } from './generatedRoutes.svelte.js';

  //TODO: Do we still have to import the favicon to include it in the bundle (and therefore manifest)?
  import '@assets/favicon.svg';
</script>

<Router {routes} {Layout} />
