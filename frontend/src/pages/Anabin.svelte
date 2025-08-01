<script>
  import DegreeSearch from './anabin/DegreeSearch.svelte';
  import InstitutionSearch from './anabin/InstitutionSearch.svelte';
  import AISearch from './anabin/AISearch.svelte';
  import { Tabs, Tab, TabList, TabPanel } from '@components/tabs';

  import { Main, Icon, Link } from '@components';

  import Dialog from '@components/Dialog.svelte';

  import degreeIcon from '@iconify-icons/ph/graduation-cap-duotone';
  import institutionIcon from '@iconify-icons/ph/buildings-duotone';
  import aiIcon from '@iconify-icons/eos-icons/ai';

  import helpIcon from '@iconify-icons/mdi/help-box';

  import SVGIcon from '@components/SVGIcon.svelte';

  import { createLocalStorageStore } from '@lib/../stores.svelte.js';

  let anabinStore = createLocalStorageStore('Anabin', { country: '', showTranslations: false, highlight: false }, false)();

  $effect(() => {
    console.log('anabin store: ', $state.snapshot(anabinStore));
  });

  let { meta, ...rest } = $props();
  meta({
    title: 'Anabin Foreign Educational Qualification Search - RELONEE',
    description: 'Search the Anabin database which offers extensive information on evaluating foreign educational qualifications.'
  });
</script>

<style>
  Tabs {

    TabList {
      margin: 1rem;
      margin-bottom: 2rem;
      --pico-nav-element-spacing-vertical: .3rem;
      --pico-nav-element-spacing-horizontal: 1.25rem;
      /*--pico-nav-element-spacing-vertical: 0.5rem;*/

      :global(li) {
        margin-inline: .75rem;
      }

      Tab {
        white-space: nowrap;

        Icon {
          margin-right: 0.4rem;
        }

        @media mobile {
          Icon {
            align-self: center;
          }
          :global(span.wrapper) {
            display: inline-flex;
            flex-direction: column;
            text-align: center;
          }
        }
      }

    }
  }

  Dialog {
    --max-width: max(30rem, 50%);
  }

  a {
    display: inline-flex;
    align-items: last baseline;

  }
</style>

<Main {...rest}>

  <section>
    <h1>Anabin Search</h1>
    <p>
      Easily search the <a href="https://anabin.kmk.org/" target="_blank">Anabin database</a> which provides information on the assessment of foreign educational qualifications and supports authorities, employers and private individuals in classifying a foreign qualification into the German education system.

      <Dialog showCloseButton>
        <a href="" slot="trigger" let:onclick {onclick}><Icon icon={helpIcon}>How to search?</Icon></a>
        <h3 slot="header">anabin &mdash; Search Tips &amp; Tricks</h3>
          <hgroup>
            <h4>Leave out generic words</h4>
            <p>It's better to leave out generic words like <code>university</code> or <code>institute</code>, ie. when you are searching for the 'University of Texas', search only for <code>texas</code> to get fewer, more relevant results.</p>
          </hgroup>
          <hgroup>
          <h4>Filter the city</h4>
          <p>You can restrict the institution search to a specific city by using the special syntax <code>city:London</code> in the search field. Partial city names are possible as well.</p>
          </hgroup>
          <hgroup>
          <h4>Try different searchmode</h4>
          <p>There are 3 different search modes using 'Trigram Similarity'. Using the special syntax <code>mode:full</code> or <code>mode:word</code> activates the other two search modes. By default, the search is using strict similarity but you can change to a lesser mode.</p>
          </hgroup>
      </Dialog>
    </p>
  </section>

  <Tabs id="anabin">
    <TabList>
      <Tab id="institutions"><Icon icon={institutionIcon} size="1.5rem">Institutions</Icon></Tab>
      <Tab id="degrees"><Icon icon={degreeIcon} size="1.5rem">Degrees</Icon></Tab>
      <Tab id="ai"><Icon icon={aiIcon} size="1.5rem">AI Search <sup>BETA</sup></Icon></Tab>
    </TabList>

    <TabPanel>
      <InstitutionSearch bind:country={anabinStore.country} bind:highlight={anabinStore.highlight} bind:showTranslations={anabinStore.showTranslations} />
    </TabPanel>

    <TabPanel>
      <DegreeSearch bind:country={anabinStore.country} bind:highlight={anabinStore.highlight} bind:showTranslations={anabinStore.showTranslations} />
    </TabPanel>

    <TabPanel>
      <AISearch />
    </TabPanel>
  </Tabs>


</Main>
