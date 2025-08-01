<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';

  import ResultsTable from '@components/AnabinResults.svelte';
  import ResultsOptions from '@components/AnabinResultsOptions.svelte';
  import SearchForm from '@components/AnabinSearchForm.svelte';
  import Icon from '@components/IconWithLabel.svelte';

  import warningIcon from '@iconify-icons/ph/warning-circle-duotone';
  import successIcon from '@iconify-icons/ph/check-circle-duotone';
  import noneIcon from '@iconify-icons/ph/x-circle-duotone';

  import { escapeHTML } from '@lib/utils.js';
  import { findCountryName } from '@lib/countries.js';

  let { searchFunction, placeholder, type, country = $bindable(), highlight = $bindable(), showTranslations = $bindable() } = $props();

  const params = new URLSearchParams(window.location.search);
  let searchString = $state(params.get(type) || '');
  let searchField;

  if (params.get('country')) {
    country = params.get('country');
  }

  let results = $state([]);
  //This string is always updated when a search is performed so we can tell what was searched for
  //and it also allows highlighting of the results
  let resultsSearchString = $state('');
  let loading = $state(false);

  let message = $state();
  let messageIcon = $state(warningIcon);

  async function performSearch() {
    searchString.trim();

    if (loading) {
      message = 'Search is ongoing, please wait for the results.';
      messageIcon = warningIcon;
      searchField.focus();
      return;
    }

    //When not resetting `message`, it would leave the last message as a stale message
    //when searching again
    message = ''
    messageIcon = warningIcon;

    if (!searchString) {
      message = 'Please enter a search string';
      searchField.focus();
      return;
    }
    if (searchString.length < 3) {
      message = 'Please enter at least 3 characters';
      searchField.focus();
      return;
    }

    loading = true;

    searchField && searchField.focus();

    const response = await searchFunction(searchString, country);

    if (!response.success) {
      message = response.error;
      results = [];
    } else {
      results = response.data.results;
      resultsSearchString = searchString;
      const escaped = escapeHTML(searchString);
      if (results.length === 0) {
        message = `Your search - <strong>${escaped}</strong> - ${findCountryName(country)} did not match any records in the Anabin database.`;
        messageIcon = noneIcon;
      } else if (results.length == 1) {
        message = `Lucky shot, one result found for - <strong>${escaped}</strong> - in ${findCountryName(country)}`;
        messageIcon = successIcon;
      } else {
        message = `${results.length} results found for - <strong>${escaped}</strong> - in ${findCountryName(country)}`;
        messageIcon = successIcon;
      }
    }
    message = message;
    console.log('message', message);
    loading = false;
  }

  async function onsubmit(event) {
    event.preventDefault();
    await performSearch();
    updateURL();
  }

  function updateURL() {
    const url = new URL(window.location.href);

    url.searchParams.forEach((value, key) => {
      if (key != type) url.searchParams.delete(key);
    });

    if (searchString) {
      url.searchParams.set(type, searchString);
    }
    if (country) {
      url.searchParams.set('country', country);
    }
    if (url != window.location.href) {
      history.pushState(history?.state, '', url);
    }
  }

  //Seems unnecessary
  function handlePopState(event) {
    const params = new URLSearchParams(window.location.search);
    //console.log('Anabin handlePopState', params);
    if (params.has(type)) {
      searchString = params.get(type) || '';
      country = params.get('country') || '';
      console.log('Anabin form update: ', searchString, country);
      //We must only repeat the search if we are on the right tab,
      //ie. params.type=type
      if (searchString) performSearch();
    }
  }

  onMount(() => {
    window.addEventListener('popstate', handlePopState);

    // Initial search if the URL has parameters
    if (searchString) {
      performSearch();
    }
  });

  onDestroy(() => {
    window.removeEventListener('popstate', handlePopState);
  });
</script>

<style>
  p {
    margin: -0.65rem 0 1rem 1.05rem;
    position: absolute;

    Icon {
      margin-right: 0.55rem;
    }
  }
</style>

<section>
  <SearchForm bind:this={searchField} bind:searchString bind:country {loading} {onsubmit} {placeholder} />
  {if message}
    <p><Icon icon={messageIcon} size="1.2rem">{@html message}</Icon></p>
  {else}
    <p>&nbsp;</p>
  {/if}
</section>

{#if results.length > 0}
  <section transition:fade>
    <ResultsOptions bind:highlight bind:showTranslations />
    <ResultsTable {results} {highlight} {showTranslations} searchString={resultsSearchString} {type} />
  </section>
{/if}
