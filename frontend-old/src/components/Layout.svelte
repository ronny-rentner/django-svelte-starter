<script>
  //import { fade } from 'svelte/transition';

  import reloneeLogo from '@assets/relonee_logo.svg';
  import reloneeLogoWhite from '@assets/relonee_logo_white.svg';

  import MediaQuery from '@components/MediaQuery.svelte';
  import MobileMenuButton from '@layout/MobileMenuButton.svelte';
  import MobileMenu from '@layout/MobileMenu.svelte';
  import Menu from '@layout/Menu.svelte';

  import ToggleDarkMode from '@components/ToggleDarkMode.svelte';

  import AccountLayout from '@layout/Account.svelte';

  import Footer from '@layout/Footer.svelte';

  import { personStore as person, authLoading } from '@stores';
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { configStore as config } from '@stores';

  import Toaster, { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  import { renderSnippetToHTML } from '@lib/utils.js';

  import logoImage from '@assets/my-market-mentor_logo_cropped.svg';

  let { layoutConfig, children } = $props();

  let mobileMenuOpen = $state(false);

  let header;

  setContext('layoutConfig', layoutConfig);
  let contrastMode = $derived(layoutConfig['contrast']);

  //$effect(() => {
  //  console.log('contrastMode effect: ', contrastMode);
  //});
  $effect(() => {
    console.log('layoutConfig: ', { ... layoutConfig });
    layoutConfig;
  });


  // List of navigation items
  const items = [
    { path: '/', label: 'Home' },
    { path: '/generate', label: 'Generate' },
    { path: '/faq', label: 'FAQ' },
    //{ path: '/demo', label: 'Demo' },
    { path: '/about', label: 'About us' },
  ];

  let useAccountLayout = $state();

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


    h1 {
      font-size: 2rem;
      font-family: Impact, Arial, sans-serif;
      text-align: left;
      position: relative;
      display: inline-block;
      margin: 0 0 0 0;
      padding-top: 0.5rem;

      img {
        height: 3rem;
        width: 3rem;
        vertical-align: middle;
        margin-top: -0.25rem;
        margin-right: 0.25rem;
        /*
        &:hover {
          filter: drop-shadow(0 0 1em #009298);
        }
         */
      }
    }
  }

  nav {
    flex-wrap: wrap;
    user-select: none;

    & > ul:first-child {
      flex-grow: 1;
    }

  }



</style>

<MediaQuery query="(max-width: 768px)" let:matches>
  {#if matches}
    <MobileMenu bind:open={mobileMenuOpen} {items} {contrastMode} />
  {/if}
<header class="container" bind:this={header}>
  <nav class:contrast={contrastMode}>
    <ul>
      <li>
        {#if $config.darkMode}
          <h1><span class="underline--magical"><img src="{logoImage}" alt="my market mentor logo" />my market mentor</span></h1>
        {:else}
          <h1><span class="underline--magical"><img src="{logoImage}" alt="my market mentor logo" />my market mentor</span></h1>
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

{@render children()}

<Toaster />

<Footer />
