<script>
  import { onMount } from 'svelte';
  import { personStore as person } from '@stores';
  import { navigate } from '@components/Router.svelte';
  import { Main } from '@components';
  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  onMount(() => {
    if (!$person) {
      navigate('/');
      toastWarning('Please signin first!');
    }
  });

  let { children, ...rest } = $props();
</script>

<style>
  div.grid {
    grid-template-columns: auto 1fr;
  }

  div.content {
    position: relative;
    min-height: 100vh;
    padding: 1rem;
  }

  aside {
    margin-top: 3rem;
    margin-right: 1.5rem;

    li {
      padding-block: 0;
    }

    .header {
      padding-block: 1.25rem 0.25rem;
      font-weight: bold;

      &:first-child {
        padding-top: 0;
      }
    }

    @mobile {
      display: none;
    }
  }

</style>

{if $person}
<Main {...rest}>
  <div class="grid">
    <aside>
      <nav>
        <ul>
          <li class="header">Account</li>
          <li><a href="/account">Welcome</a></li>
          <li><a href="/account/details">Details</a></li>
          <li><a href="/account/documents">Documents</a></li>
          <li class="header">Processes</li>
          <li><a href="/account/processes">Overview</a></li>
          {#if 0}<li><a disabled>Health Insurance</a></li>{/if}
        </ul>
      </nav>
    </aside>

    <div class="content">{render children()}</div>
</Main>
{else}
<Main style="height:100vh" {...rest}>
</Main>
{/if}
