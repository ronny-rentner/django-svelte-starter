<script>
import { fade } from 'svelte/transition';

import { Button, Icon, Link, Table } from '@components';
import Dialog from '@components/Dialog.svelte';

import successIcon from '@iconify-icons/ph/check-circle-duotone';
import downloadIcon from '@iconify-icons/ph/download-duotone';
import linkIcon from '@iconify-icons/ph/arrow-square-out-duotone';
import degreeIcon from '@iconify-icons/ph/graduation-cap-duotone';
import institutionIcon from '@iconify-icons/ph/buildings-duotone';

import { toastSuccess, toastWarning, toastPop } from '@components/Toasts.svelte';

import { download } from '@lib/utils.js';

let {
  results = [],
  highlight = false,
  showTranslations = false,
  searchString = '',
  type = 'degrees',
  simple,
  ...rest
} = $props();

const typeDegrees = 'degrees';
const typeInstitutions = 'institutions';

let clickoutDialogResult = $state();
let dialog = $state();

function stripDiacritics(str) {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function highlightText(text, search) {
  if (!highlight) return text;
  search = search.trim();
  if (!text || !search) return text;

  // Stripped versions of text and search string to ignore accents
  const strippedText = stripDiacritics(text).toLowerCase();
  const strippedSearch = search;

  // Handle the case when no match is found
  if (!strippedText.includes(strippedSearch)) {
    return text;
  }

  // Replace in the original text based on matches in the stripped text
  let result = '';
  let lastIndex = 0;

  // Manually find and replace matching parts
  for (let i = 0; i < strippedText.length; i++) {
    const index = strippedText.indexOf(strippedSearch, i);
    if (index === -1) break;

    // Append the portion of the original text before the match
    result += text.substring(lastIndex, index);

    // Append the highlighted match
    const originalMatch = text.substring(index, index + strippedSearch.length);
    result += `<mark>${originalMatch}</mark>`;

    // Update the last index and move `i` to avoid matching the same part
    lastIndex = index + strippedSearch.length;
    i = lastIndex - 1;
  }

  // Append the rest of the original text after the last match
  result += text.substring(lastIndex);

  return result;
}

function highlightOtherNames(otherNames, search) {
  return otherNames.reduce((arr, value) => {
    if (value.name_type != 'name') {
      arr.push([ value.name_type, highlightText(value.name, search) ]);
    }
    return arr;
  }, []);
}

function getDownloadUrl(id) {
  if (type === typeDegrees) {
    return `${window.config.apiBaseUrl}/degrees/download/${id}/`;
  } else if (type === typeInstitutions) {
    return `${window.config.apiBaseUrl}/institutions/download/${id}/`;
  }
  return '#'; // fallback URL
}

function getDegreeSearchUrl(id) {
  const param = encodeURIComponent(`institution:${id}`);
  return `${window.config.baseUrl}/anabin?degrees=${param}`;
}

function getInstitutionSearchUrl(id) {
  const param = encodeURIComponent(`degree:${id}`);
  return `${window.config.baseUrl}/anabin?institutions=${param}`;
}

function getSourceUrl(result) {
  return `${result.source_url}?land=${result.country_alpha3}`;
}

async function downloadClick(event) {
  event.preventDefault(); // Prevent the default link behavior
  console.log('downloadClick', event);

  const url = event.currentTarget.href;

  try {
    download(url);
  } catch (err) {
    console.error("Failed to download: ", err);
  }

}

async function anabinClick(event, result) {
  event.preventDefault(); // Prevent the default link behavior
  console.log('anabinClick', event);

  const textToCopy = result.name;

  try {
      await navigator.clipboard.writeText(textToCopy);
  } catch (err) {
      console.error("Failed to copy: ", err);
  }

  clickoutDialogResult = result;
  if (dialog) {
    dialog.open = true;
  }
}


function processResults() {
  let search = stripDiacritics(searchString).toLowerCase();
  //Remove optional filters comletely from highlighting as we're only highlighting the names but
  //the filters only filter other fields
  search = search.replace(/(city|mode|institution|field|type):(("(?<rep1>[^"]+)")|(?<rep2>[^\s]+))/g, '');
  console.log('search replaced:', search);
  return results.map(result => ({
    ...result,
    highlightedName: highlightText(result.name, search),
    highlightedOtherNames: highlightOtherNames((type == 'degrees' ? result.degree_names : result.institution_names), search)
  }));
}

let processedResults = $derived(processResults());

</script>

<style>
Dialog {
  --max-width: min(50rem, 80vw);
}

Table {

  border-collapse: collapse;
  line-height: 1.2rem;
  overflow-x: auto;

  /*
  border-spacing: 1rem;
  table-layout: fixed;
   */

  :global(mark) {
    padding: 0;
    background: var(--pico-muted-border-color);
    color: var(--pico-primary);
    font-weight: bold;
  }

  th {
    padding: 0.5rem 0;
    position: sticky;
    top: 0;
    box-shadow: inset 0 -1px 0 0 var(--pico-primary);
    border: 0;

    &:first-child {
      padding-left: 0.5rem;
    }

    /*
    &:last-child {
      padding-right: 0.5rem;
    }
     */

    &:nth-child(1) {
      width: 25%;
    }

    &:nth-child(2) {
      width: 10%;

    }
    &:nth-child(3) {
      width: 15%;
    }

    &:nth-child(4) {
      width: 20%;
    }

    &:nth-child(5) {
      width: 18%;
    }
    &:nth-child(6) {
      width: 12%;
    }

  }

  td {
    padding: 1rem 1rem 1rem 0;
    vertical-align: top;

    &:first-child {
      padding-left: 0.5rem;
    }

    &:last-child {
      padding-right: 0.5rem;
    }

    &.links {
      line-height: 1.3rem;
    }

    Icon {
      color: var(--pico-primary);
    }

    dl {
      padding: 0;
      margin: 0;
      padding: 0.3rem 0 0 0;

      dt {
        color: var(--pico-muted-color);
        line-height: 0.8rem;
        font-size: 80%;
        margin: 0.3rem 0 0 0;

        &:first-child {
          margin-top: 0;
        }
      }

      dd {
        margin: 0;
      }
    }

  }

  &.institutions {
    th {
      &:nth-child(1) {
        width: 25%
      }

      &:nth-child(2) {
        width: 20%;

      }
      &:nth-child(3) {
        width: 25%;
      }

      &:nth-child(4) {
        width: 18%;
      }

      &:nth-child(5) {
        width: 12%;
      }
    }
  }
}
</style>


<Table class="results striped {type}" {...rest}>
  <thead>
    <tr>
      <th class="name-column">Name</th>
      {if type == typeInstitutions}
        <th>Location</th>
        <th>Type</th>
        <th>Status</th>
      {else}
        <th>Country</th>
        <th>Degree Type</th>
        <th>Study Field</th>
        <th>Evaluation</th>
      {/if}
      {if ! simple}
        <th>Links</th>
      {/if}
    </tr>
  </thead>
  <tbody>
    {#each processedResults as result, i}
      <tr>
        <td class="name-column">
          {@html result.highlightedName}
          {#if showTranslations && (result.highlightedOtherNames || []).length > 0}
            <dl>
              {#each result.highlightedOtherNames as [language, translation]}
                <dt>{language}</dt>
                <dd>{@html translation}</dd>
              {/each}
            </dl>
          {/if}
        </td>
        {#if type == typeInstitutions}
          <td>{#if result.city_name}{result.city_name},<br />{/if}{result.country_name}</td>
          <td>{result.institution_type}</td>
          <td>
            {#if result.status == 'H+'}
              <Icon icon={successIcon}>Recognized&nbsp;({result.status})</Icon>
            {:else}
              Not recognized ({result.status})
            {/if}
          </td>
        {:else}
          <td>{result.country_name}</td>
          <td>
            {result.degree_type}
            {#if showTranslations && result.degree_type_german_translation}
              <dl><dt>german</dt><dd>{result.degree_type_german_translation}</dd></dl>
            {/if}
          </td>
          <td>
            {result.study_field}
            {#if showTranslations && result.study_field_german_translation}
              <dl><dt>german</dt><dd>{result.study_field_german_translation}</dd></dl>
            {/if}
          </td>
          <td>
            {#if Object.entries(result.evaluations || {}) != ''}
              <Icon icon={successIcon}>Recognized</Icon>
            {:else}
              Not recognized
            {/if}
            <dl>
              {#if showTranslations && Object.entries(result.evaluations) != ''}
                {#each result.evaluations as evaluation}
                  <dt>{evaluation.equivalence_class}</dt>
                  <dd>{evaluation.corresponding_german_degree_type}</dd>
                {/each}
              {/if}
            </dl>
          </td>
        {/if}
        {if ! simple}
          <td class="links">
            <Link href={getDownloadUrl(result.id)} download onclick={downloadClick} icon={downloadIcon}>Download</Link>
            <Link href={getSourceUrl(result)} blank onclick={(event) => anabinClick(event, result)} icon={linkIcon} rel="noopener noreferrer">anabin</Link>
            {if result.homepage}
              <Link href={result.homepage} blank icon={linkIcon} rel="noopener noreferrer">Homepage</Link>
            {/if}
            {if result.has_degrees > 0}
              <Link href={getDegreeSearchUrl(result.id)} icon={degreeIcon}>{#if result.has_degrees > 1}Degrees&nbsp;({result.has_degrees}){:else}Degree&nbsp;(1){/if}</Link>
            {/if}
            {if result.has_institutions > 0}
              <Link href={getInstitutionSearchUrl(result.id)} icon={institutionIcon}>{#if result.has_institutions > 1}Institutions&nbsp;({result.has_institutions}){:else}Institution&nbsp;(1){/if}</Link>
            {/if}
          </td>
        {/if}
      </tr>
    {/each}
  </tbody>
</Table>

{if clickoutDialogResult}
  <Dialog open bind:dialog>
    <h3 slot="header">Open anabin</h3>
    {const sourceUrl=getSourceUrl(clickoutDialogResult)}
    <p>Pleaes note that we've copied the name below into your clipboard so you can paste it into the search form at anabin to quickly find the corrensponding entry.</p>
    <p><code>{clickoutDialogResult.name}</code></p>
    <p>Click on the open button below and press <kbd>CTRL</kbd>+<kbd>v</kbd> to paste into anabin!
    </p>
    <footer>
      <Link icon={linkIcon} role="button" blank href={sourceUrl} onclick={(event) => dialog.close(event)}>Open anabin</Link>
      <Button class="outline" type="cancel">Cancel</Button>
    </footer>
  </Dialog>
{/if}
