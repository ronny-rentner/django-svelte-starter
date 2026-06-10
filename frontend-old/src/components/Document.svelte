<script>
import { getContext, onMount, onDestroy } from 'svelte';

import DocumentBadges from '@components/DocumentBadges.svelte';
import DocumentPreview from '@components/DocumentPreview.svelte';
import LoadingDots from '@components/LoadingDots.svelte';

import { Button, Link, Icon } from '@components';
import iconNext from '@icons/ph/arrow-right';
import iconNoThumbnail from '@icons/ph/file-text-duotone';
import iconPDF from '@icons/ph/file-pdf-duotone';
import iconPNG from '@icons/ph/file-png-duotone';
import iconJPG from '@icons/ph/file-jpg-duotone';
import iconMenu from '@icons/ph/dots-three-outline-vertical-fill';

import iconValid from '@icons/ph/check';
import iconFileSize from '@icons/ph/floppy-disk';

import { formatFileSize } from '@lib/utils.js';

import { fetchPersonDocuments, apiClient  } from "@api/api.svelte.js";
import { personStore as person  } from '@stores';

const api = apiClient(fetchPersonDocuments);

let { document, id, file, fileType, label, progress, refresh = false }  = $props();

let icon = $state(iconPDF);

//Load document from API if necessary

if (!file && !document && id) {
  if (!refresh && $person?.documents && id in $person?.documents) {
    document = $person.documents[id];
    //console.log('Using document: ', id, document, $person);
  } else {
    api.execute($person.id, id).then(() => {
      document = $person.documents[id];
      //console.log('Using document: ', id, document, $person);
    });
  }
}

//Set icon according to file extension
if (file) {
  const fileName = file?.name || fileType || file;
  if (fileName.endsWith('.png')) {
    icon = iconPNG;
  } else if (fileName.endsWith('.jpg') || fileName.endsWith('.jpeg')) {
    icon = iconJPG;
  } else if (fileName.endsWith('.pdf')) {
    icon = iconPDF;
  } else {
    icon = iconNoThumbnail;
  }
//Set icon according to file mime type
} else if (document) {
  if (document.mime_type == 'image/jpeg') {
      icon = iconJPG;
  } else if (document.mime_type == 'image/png') {
      icon = iconPNG;
  } else if (document.mime_type == 'application/pdf') {
      icon = iconPDF;
  } else {
    icon = iconNoThumbnail;
  }
}

</script>

<style>
article {
  --pico-typography-spacing-vertical: 0.75rem;

  /*
  width: min-content;
   */

  /*--pico-card-box-shadow: rgba(0, 0, 0, 0.12) 0rem 0.25rem 0.5rem;*/
  display: inline-block;
  /*
  //Why did we have this?
  text-align: center;
   */
  margin-right: 1rem;
  vertical-align: top;
  padding: 0;
  overflow: hidden;

  @light & {
    background-color: var(--pico-primary-inverse);
  }

  > DocumentPreview, > img {
    border-top-left-radius: var(--pico-border-radius);
    border-top-right-radius: var(--pico-border-radius);
    border-width: 0;
  }

  > Link Icon {
    margin: 3rem;
    max-width: 12rem;
    width: 12rem;
    opacity: 0.5;
  }

  &.progress {
    > footer {
      position: relative;
    }
  }

  > footer {
    display: flex;
    width: 100%;
    line-height: 1rem;
    align-items: center;
    margin: 0;
    padding: 0.5rem;

    position: relative;

    small {
      word-wrap: anywhere;

      Icon.small {
        margin-right: 0.05rem;
      }
    }

    :global(> :first-child) {
      flex-grow: 1;
    }

    Button {
      flex-grow: 0;
      flex-shrink: 0;
      padding: 0;
      align-self: stretch;
      border: 0;
    }

    progress {
      position: absolute;
      inset: -1px 0 0 0;
      border: 0;
      border-radius: 0 0.25rem;
      opacity: 0.25;
      height: 110%;
      background: transparent;
    }
  }
}
</style>

{if document}
  <article style:width="{document?.thumbnail_width}px">
    <DocumentBadges {document} />

    <Link href={document.file} blank>
      {if document?.thumbnail}
        <img src={document?.thumbnail} width={document?.thumbnail_width} height={document?.thumbnail_height}>
      {else}
        <Icon icon={iconNoThumbnail} size="12rem" />
      {/if}
    </Link>

    <footer>
      <Icon {icon} size="2.25rem">
        <small>
          {document?.original_file_name}
          <Icon icon={iconFileSize} class="small" size="1rem">{formatFileSize(document?.file_size)}</Icon>
          {if document?.valid}
            <Icon icon={iconValid} class="small" size="1rem">validated</Icon>
          {/if}
        </small>
      </Icon>

      <Button class="outline" icon={iconMenu} iconSize="1.5rem" />
    </footer>
  </article>
{elif file}
  <article class:progress  style:width="400px">
    <DocumentPreview {file} {label} />
    <footer>
      {if progress}<progress value={progress} max="100"></progress>{/if}
      <Icon {icon} size="2.25rem">
        <small>
          {if file?.name}
            {file?.name} <nobr>({formatFileSize(file?.size)})</nobr>
            {if progress}
              <br />
              <strong>
                {if progress=="100"}
                  <LoadingDots>Processing</LoadingDots>
                {else}
                  Uploading: {progress}&nbsp;%
                {/if}
              </strong>
            {/if}
          {elif label}
            {label}
          {else}
            Document Preview
          {/if}
        </small>
      </Icon>
    </footer>
  </article>
{/if}

