<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  import ComboBox from '@components/ComboBox.svelte';
  import { countriesForCombobox as countries } from '@lib/countries.js';
  import autofocus from '@lib/autofocus.js';
  //import { anabinSearchStore as anabinStore } from '@stores';
  import { Icon } from '@vendor';
  import flagIcon from '@icons/ph/flag';

  let {
    searchString = $bindable(''),
    country = $bindable(),
    loading = false,
    onsubmit,
    placeholder = "Search",
  } = $props();

  /*
  if (country && country != null) {
    anabinStore.country = country;
  }

  // Sync the prop with the state
  $effect(() => {
    if (anabinStore.country !== country) {
       anabinStore.country = country;  // Update prop if local state changes
    }
  });

  // Sync the state with the prop
  $effect(() => {
    if (country !== anabinStore.country) {
      country = anabinStore.country;  // Update local state if prop changes
    }
  });
   */

  let searchField;

  export function focus() {
    searchField.focus();
  }

</script>

<style>
  form {
    position: relative;
  }

  input[type="search"]::-webkit-search-cancel-button {
    -webkit-appearance: none;
    height: 1.25rem;
    width: 1.25rem;
    margin-left: .4rem;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23777'><path d='M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'/></svg>");
    cursor: pointer;
  }

  .progress {
    position: absolute;
    inset: 0;
    z-index: 10;
    pointer-events: none;

    progress {
      margin: 0;
      height: 100%;
      width: 100%;
      opacity: 0.25;
      pointer-events: none;
    }
  }

  ComboBox {
    min-width: 30%;
    /*border-left: var(--pico-form-element-placeholder-color) 2px solid;*/

    .flag {
      font-size: 1.75rem;
      height: 1.75rem;
      font-family: var(--pico-font-family-emoji);
    }
  }

  @media mobile {
    ComboBox {
      display: none !important;
    }
  }
</style>

<form role="search" {onsubmit}>
  <input use:autofocus={{filter:['input']}} name="search" type="search" {placeholder} bind:this={searchField} bind:value={searchString} />
  {#if loading}
    <div class="progress" transition:fade>
      <progress />
    </div>
  {/if}
  <ComboBox name="country" bind:value={country}  placeholder="All countries" options={countries} reset>
    {#snippet iconStart()}<Icon icon={flagIcon} />{/snippet}
    {#snippet option({ item })}
      <span class="flag">{item.flag}</span>
      {item.text}
    {/snippet}
  </ComboBox>
  <input type="submit" value="Search" />
</form>
