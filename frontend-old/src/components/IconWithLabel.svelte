<script>
  import { renderSnippetToHTML } from '@lib/utils.js';

  import Icon from '@iconify/svelte';
  import defaultIcon from '@icons/ph/smiley-duotone';

  let { icon = defaultIcon, iconSize = '1.25rem', width, height, size,
        label, tooltip, placement, children, ...rest } = $props();

  if (children) {
    label = children;
  }

  //Icons are supposed to be square
  if (size) {
    iconSize = size;
  }
  if (!width) {
    width = iconSize;
  }
  if (!height) {
    height = iconSize;
  }

  //let html = $state('');
  //$effect(() => {
    //html = renderSnippetToHTML(children || label).trim();
    //console.log('rendered HTML: ', html, html.length, icon);
    //console.log('render IconWithLabel effect');
    //children;
  //});

</script>

<style>
  Icon {
    /* Important setting to ensure the size and prevent shrinking */
    flex-shrink: 0;
  }

  span.wrapper {
    display: inline-flex;
    /* Necessary to vertically align icon and label in user menu */
    align-items: center;
    /*vertical-align: top;*/

    Icon {
      margin-right: 0.25rem;
    }

    > span {
      /* Necessary to vertically align label after icon used in accordions in the middle between top and bottom border */
      /* FIXME: Prevents correct alignment in accordian for Anabin AI search "low matching score" etc. */
      /* FIXME: Also has influence on button height (check Reset button vs rest) for Anabin AI search */
      align-self: baseline;
    }
  }
</style>

{if label}
  {if icon}
    <span class="wrapper">
      <Icon {icon} {width} {height} class="margin" {...rest} /><span {tooltip} {placement}>{render label()}</span>
    </span>
  {else}
    {render label()}
  {/if}
{else}
  <Icon {icon} {width} {height} {...rest} {tooltip} {placement} />
{/if}
