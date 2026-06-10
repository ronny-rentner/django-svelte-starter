<script>
  import Accordion from '@components/Accordion.svelte';
  import { Main } from '@components';

  import { onMount } from 'svelte';

  import { faqData } from './faqData.js';
  let faqs = faqData;

  let activeIndex = -1;

  let { meta, ...rest } = $props();
  meta({
    title: 'FAQ - Frequently Asked Questions - RELONEE',
    description: 'Frequently Asked Questions regarding your German Work Visum'
  });
</script>

<style>
</style>

<Main {...rest}>
  <section>
    <markdown mode="faq" />
  </section>
</Main>
