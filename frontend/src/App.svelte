<script module>
  import './init.js';
</script>

<script>
  import { Router } from 'svultra/kit/router';
  import Layout from 'svultra/kit/components/Layout.svelte';

  import { routes } from './generatedRoutes.svelte.js';
</script>

<Router {routes} {Layout} />
