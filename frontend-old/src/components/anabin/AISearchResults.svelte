<script>

import { Icon, Button, Link } from "@components";

import ResultsTable from '@components/AnabinResults.svelte';

import degreeIcon from '@iconify-icons/ph/graduation-cap-duotone';
import institutionIcon from '@iconify-icons/ph/buildings-duotone';

import warningIcon from '@iconify-icons/ph/warning-circle-duotone';
import successIcon from '@iconify-icons/ph/check-circle-duotone';
import downloadIcon from '@icons/ph/download-duotone';

import { download as startDownload } from '@lib/utils.js';

const { data, reset, simple, ...rest } = $props();

function getDegreeSearchUrl() {
  const param = encodeURIComponent(`${data?.degree_search}`);
  const param2 =  encodeURIComponent(data?.degree_search_country);
  return `${window.config.baseUrl}/anabin?degrees=${param}&country=${param2}`;
}

function getInstitutionSearchUrl() {
  const param = encodeURIComponent(`${data?.institution_search}`);
  const param2 =  encodeURIComponent(data?.institution_search_country);
  return `${window.config.baseUrl}/anabin?institutions=${param}&country=${param2}`;
}

function download(institutionId, degreeId) {
  return (event) => {
    //event.preventDefault();
    if (institutionId) {
      let url = `${window.config.apiBaseUrl}/institutions/download/${institutionId}/`;
      startDownload(url);
    }
    if (degreeId) {
      let url = `${window.config.apiBaseUrl}/degrees/download/${degreeId}/`;
      startDownload(url);
    }
  }
}

</script>

<style>
h4 {
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;

  span {
    font-size: 1rem;
  }

  Icon {
    margin-left: 1rem;
  }

  Icon.success {
    color: var(--pico-primary);
  }
  Icon.warning {
    color: var(--pico-del-color);
  }

}


div.nav {
  margin-block: 0.75rem 0.5rem;

  Button {
    margin-bottom: 0;
  }
}

@media mobile {
  div.nav Link {
    :global(span.wrapper span) {
      display: none;
    }
  }

  ResultsTable {
    min-width: 40rem;
  }
}
</style>

{snippet judge_match(similarity, searchString)}
  <span>
    {if similarity == 1.0}
      <Icon icon={successIcon} class="success">exact match</Icon>
    {/if}
    {if similarity <= 0.7}
      <Icon icon={warningIcon} class="warning"tooltip="Careful &mdash; A low matching score means it's not a perfect match, but it might also just mean the listing in the anabin database is not fully accurate." placement="bottom">low matching score</Icon>
    {/if}
    {if /institution:\d+/.test(searchString)}
      <Icon icon={institutionIcon} class="success" tooltip="Positive &mdash; This degree is listed explicitly for the matched institution above. This is a positive sign that your degree is comparable or even identical to the match below." placement="bottom">matched institution</Icon>
    {/if}
  </span>
{/snippet}

{if ! simple}
<div class="nav">
  <Link class="outline" role="button" icon={institutionIcon} href={getInstitutionSearchUrl()}>
    See {data?.institution_count} matching {data?.institution_count > 1 ? 'institutions' : 'institutions'}
  </Link>
  <Link class="outline" role="button" icon={degreeIcon} href={getDegreeSearchUrl()}>
    See {data?.degree_count} matching {data?.degree_count > 1 ? 'degrees' : 'degree'}
  </Link>
  <Button icon={downloadIcon} onclick={download(data?.institution?.id, data?.degree?.id)}>Download</Button>
  {if reset}<Button type="reset" onclick={reset}>Reset</Button>{/if}
</div>
{/if}
{if data?.institution}
  <div class="overflow-auto">
    <h4>Institution {@render judge_match(data?.institution?.similarity_name, data?.institution_search)}</h4>
    <ResultsTable results={[data?.institution]} showTranslations=1 type="institutions" {simple} />
  </div>
{/if}
{if data?.degree}
  <div class="overflow-auto">
    <h4>Degree {@render judge_match(data?.degree?.similarity_name, data?.degree_search)}{if 0}<span></span>{/if}</h4>
    <ResultsTable results={[data?.degree]} showTranslations=1 type="degrees" {simple} />
  </div>
{/if}
