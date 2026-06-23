<script>
  import { Main } from 'svultra/kit/components';
  import { accordion } from 'svultra/kit/actions';

  let { meta, ...rest } = $props();
  meta({
    title: 'FAQ',
    description: 'Frequently asked questions about the django-svelte starter.'
  });

  const faqs = [
    {
      q: 'What is this starter?',
      a: 'A Django backend paired with a Svelte 5 frontend, wired together through django-vite and the svUltra kit.',
    },
    {
      q: 'How does the accordion work?',
      a: 'Each item below is a native <details> element enhanced with the kit\'s accordion action, which animates the open/close height and traps focus in the panel.',
    },
    {
      q: 'How do I add a page?',
      a: 'Drop a .svelte file into src/pages/. The generateRoutes plugin picks it up automatically and the menu can link to its route.',
    },
    {
      q: 'Where do titles come from?',
      a: 'Each page calls meta({ title, description }); the title runs through window.config.titleTemplate so the whole site shares one prefix/suffix.',
    },
  ];
</script>

<style>
  details {
    border: 1px solid var(--pico-muted-border-color);
    border-radius: var(--pico-border-radius);
    margin-bottom: 0.5rem;
    padding: 0 1rem;

    summary {
      font-weight: bold;
      padding: 1rem 0;
    }

    div {
      overflow: hidden;
      padding-bottom: 1rem;
    }
  }
</style>

<Main {...rest}>
  <h1>Frequently Asked Questions</h1>

  {each faqs as faq}
    <details use:accordion={{ content: 'div' }}>
      <summary>{faq.q}</summary>
      <div>{faq.a}</div>
    </details>
  {/each}
</Main>
