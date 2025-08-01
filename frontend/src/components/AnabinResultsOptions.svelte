<script>
  export let highlight;
  export let showTranslations;

  function onchange() {
    localStorage.set('Anabin.highlight', highlight);
    localStorage.set('Anabin.showTranslations', showTranslations);
    //results = processResults(results);
  }

</script>

<style>
  .info-bar {
    display: flex;
    margin: 3rem 1rem 0 1.15rem;

    label {
      margin-right: 2rem;
    }

  }

  @media mobile {
    .info-bar {
      flex-direction: column;
      label {
        display: flex;
        align-items: center;
      }
    }
  }
</style>

<div class="info-bar no-selection">
  <label>
    <input name="highlight" type="checkbox" role="switch" bind:checked={highlight} {onchange} />
    Highlight search term
  </label>
  <label>
    <input name="showTranslations" type="checkbox" role="switch" bind:checked={showTranslations} {onchange} />
    Show translations and details (if available)
  </label>
</div>
