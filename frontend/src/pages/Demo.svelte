<script>
import Layout from '../components/Layout.svelte';
import Mini from '../components/Mini.svelte';

import Accordion from '@components/Accordion.svelte';
import Button from '@components/RippleButton.svelte';
import ContextMenu from '@components/ContextMenu.svelte';

import LoadingIndicator from '@components/LoadingIndicator.svelte';
import LoadingDots from '@components/LoadingDots.svelte';
import LoadingOverlay from '@components/LoadingOverlay.svelte';

import Dropzone from '@components/Dropzone.svelte';

import { ripple } from '@lib/ripple.js';

import ComboBox from '@components/ComboBox.svelte';
import { countriesForCombobox as countries } from '@lib/countries.js';

import { Icon } from '@components';
import homeIcon from '@icons/mdi/home'
import oneIcon from '@icons/ph/number-circle-one-fill';
import twoIcon from '@icons/ph/number-circle-two-fill';

let buttonClicked;
let country;

let formInput;
let formSubmitted;

let { count = 10 } = $props();

let doubled = $derived(count * 2);

$effect(() => {
  console.log('doubled: ', doubled);
});

function onclick(event) {
  buttonClicked = event.target.innerText;
}

function onsubmit(event) {
  console.log('onsubmit', event);
  event.preventDefault();
  formSubmitted = event.target.data;
}

let showLoadingOverlay = $state(false);

function onclickLoadingOverlay() {
  showLoadingOverlay = !showLoadingOverlay;
  setTimeout(() => showLoadingOverlay = !showLoadingOverlay, 3000);
}

</script>

<style>
ComboBox {
  .flag {
    font-size: 1.75rem;
    height: 1.75rem;
    font-family: Arial;
  }
}
button {
  position: relative;
  overflow: hidden;
}

article.accordion {
  max-width: 30rem;
}

</style>

<main class="container">

  <h1>Component Demo</h1>

<p>{count} doubled is {doubled}</p>
<button onclick={() => count++}>{doubled}</button>



  <section>
    <h2>Drop zone</h2>
    <Dropzone>
      Upload your files here.
    </Dropzone>
  </section>

  <section>
    <h2>Slide down</h2>
    <Mini>
      {#snippet slot1(label)}
        <strong>{label}</strong>
      {/snippet}
    </Mini>
  </section>

  <section>
    <h2>Buttons</h2>
    <button use:ripple {onclick}>Plain button</button>
    <button use:ripple {onclick} class="primary">Primary button</button>
    <button use:ripple {onclick} class="secondary">Secondary button</button>
    <button use:ripple {onclick} class="outline">Outline button</button>

    Clicked: {buttonClicked}
  </section>

  <section>
    <h2>ComboBox</h2>
    <ComboBox name="country" bind:value={country}  placeholder="All countries" options={countries} reset>
      {#snippet iconStart()}<Icon icon={homeIcon} />{/snippet}
      {#snippet option({ item })}
        <span class="flag">{item.flag}</span>
        {item.text}
      {/snippet}
    </ComboBox>

    Selected: {country}

  </section>

  <section>
    <h2>Form submission</h2>
    <form {onsubmit}>
      <input type="text" bind:value={formInput} />
      <button type="submit">Submit</button>
    </form>

    Submitted: {formSubmitted}
  </section>

  <section>
    <h2>Accordion</h2>
    <article class="accordion">
      <Accordion class="demo">
        {#snippet header()}Simple Accordion{/snippet}
        Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat.
      </Accordion>
      <Accordion class="demo">
        {#snippet header()}Simple Accordion 2{/snippet}
        Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat.
      </Accordion>
      <Accordion class="demo" icon={homeIcon}>
        {#snippet header()}Accordion with Icon{/snippet}
        Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat.
      </Accordion>
      <Accordion class="demo" button:class="secondary">
        {#snippet button()}Button Accordion{/snippet}
        Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat.
      </Accordion>
      <Accordion class="demo" button:class="outline">
        {#snippet button()}Button Accordion 2{/snippet}
        Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat.
      </Accordion>
      <Accordion class="demo" popup>
        {#snippet button()}Button Accordion 2{/snippet}
        Test content<br />
        Test content<br />
        Test content<br />
        Test content
      </Accordion>

    </article>

  </section>

  <section>
    <h2>Context menu</h2>
    <ContextMenu>
      {#snippet button()}Click me{/snippet}
      Text content<br />
      Text content<br />
      Text content<br />
      Text content<br />
    </ContextMenu>
  </section>

  <section>
    <h2>Loading</h2>
    <LoadingIndicator />
    <LoadingDots />
    <Button class="outline" onclick={onclickLoadingOverlay}>show overlay</Button>
    {if showLoadingOverlay}<LoadingOverlay text="Loading for 3 seconds" />{/if}
  </section>

</main>
