<script>
  //import { fade } from 'svelte/transition';

  import logo     from 'svultra/kit/assets/logo.svg';
  import logoDark from 'svultra/kit/assets/logo-dark.svg';

  import MediaQuery from 'svultra/kit/components/MediaQuery.svelte';
  import MobileMenuButton from '@components/layout/MobileMenuButton.svelte';
  import MobileMenu from '@components/layout/MobileMenu.svelte';
  import Menu from '@components/layout/Menu.svelte';

  //import ToggleDarkMode from './ToggleDarkMode.svelte';

  //import AccountLayout from '@components/layout/Account.svelte';

  import Footer from '@components/layout/Footer.svelte';

  //import { personStore as person, authLoading } from 'svultra/kit/stores';
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { configStore as config } from 'svultra/kit/stores';

  import Toaster /*, { toastSuccess, toastWarning }*/ from 'svultra/kit/components/Toasts.svelte';

  //import { renderSnippetToHTML } from '../snippet.svelte.js';

  // pageConfig comes from the Router (which owns it and provides it via context);
  // the Layout reads it to render the current page's preferences (e.g. contrast).
  let { pageConfig, children } = $props();

  let mobileMenuOpen = $state(false);

  let contrastMode = $derived(pageConfig['contrast']);

  // A page can hide the header and/or footer (e.g. a full-screen landing) by
  // setting pageConfig.showHeader / showFooter to false; see the Router's
  // pageConfig default.
  let showHeader = $derived(pageConfig['showHeader']);
  let showFooter = $derived(pageConfig['showFooter']);

  //$effect(() => {
  //  console.log('contrastMode effect: ', contrastMode);
  //});
  $effect(() => {
    console.log('pageConfig: ', { ... pageConfig });
    pageConfig;
  });


  // List of navigation items
  const items = [
    { path: '/',        label: 'Home' },
    { path: '/about',   label: 'About' },
    { path: '/pricing', label: 'Pricing' },
    { path: '/faq',     label: 'FAQ' },
    { path: '/guide',   label: 'Guide' },
    { path: '/landing', label: 'Landing' },
  ];

  //let useAccountLayout = $state();

  /*
  // Update the currentPath store when the URL changes
  function updateChildLayout(event) {
    const path = event ? event?.detail?.path : window.location.pathname;
    //TODO: Strange behaviour when browsing away from Signin with duplicate rendering
    useAccountLayout = path.startsWith('/account');
    //console.log('Update child layout', event, useAccountLayout);
  }
  updateChildLayout();

  // Listen for popstate and pushstate events
  onMount(() => {

    window.addEventListener('beforeNavigate', updateChildLayout);
    //window.addEventListener('popstate', updateChildLayout);
    //window.addEventListener('pushstate', updateChildLayout);

    return () => {
      window.removeEventListener('beforeNavigate', updateChildLayout);
      //window.removeEventListener('popstate', updateChildLayout);
      //window.removeEventListener('pushstate', updateChildLayout);
    };
  });
   */

</script>

<style>
  header {
    animation: fadeIn 0.5s ease-in forwards;
    position: relative;
    z-index: 100;
  }

  .logo {
    margin-top: 0;
    height: 2.5rem;
    will-change: filter;
    transition: filter 300ms;
    z-index: 20;
    position: relative;

    /*
    &:hover {
      filter: drop-shadow(0 0 1em #009298);
    }
     */
  }

  nav {
    flex-wrap: wrap;
    user-select: none;

    & > ul:first-child {
      flex-grow: 1;
    }

  }



</style>

{#if showHeader}
<MediaQuery query="(max-width: 768px)" let:matches>
  {#if matches}
    <MobileMenu bind:open={mobileMenuOpen} {items} {contrastMode} />
  {/if}
<header class="container">
  <nav class:contrast={contrastMode}>
    <ul>
      <li>
        {#if $config.darkMode}
          <img src={logoDark} alt="Logo" class="logo" />
        {:else}
          <img src={logo} alt="Logo" class="logo" />
        {/if}
      </li>
    </ul>
    {#if matches}
      <MobileMenuButton bind:open={mobileMenuOpen} {contrastMode} />
    {:else}
      <Menu {items} {contrastMode} />
    {/if}
  </nav>
</header>
</MediaQuery>
{/if}

{@render children()}

<Toaster />

{#if showFooter}
<Footer />
{/if}
