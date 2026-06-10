<script>
import { setContext } from 'svelte';
import { fade, slide } from 'svelte/transition';

import { renderSnippetToHTML } from '@lib/utils.js';

import { Icon, Button } from '@components';

import { extract } from '@lib/utils.js';

let { active = $bindable(false), disabled = $bindable(false), icon, header, button, class: className, children, ...rest } = $props();

let element;
let prefix = 'button:';

let animationRunning = $state(false);

export function onclick(event) {
  //console.log('onclick', event);
  event?.preventDefault();
  //We need to track the CSS transiton and only hide the accordion contents afterwards
  animationRunning = true;
  setTimeout(() => (animationRunning = false), 500); // 500ms
  active = !active;
}

//Is this being used?
//setContext('accordion', { active, onclick });

//if (!header && !button) {
//  console.log('NO HEADER');
//}

//Get rid of the proxy
rest = { ...rest };
let buttonRest = extract(rest, 'button:');
let headerRest = extract(rest, 'header:');

</script>

<style>

div.accordion {
  overflow: hidden;
  padding: 0.1rem;
  display: grid;
  grid-template-rows: min-content 0fr;
  transition: grid-template-rows 0.5s ease;

  border-top: 1px var(--pico-muted-border-color) solid;

  &.icon {
    /* Accordion with icon */
    padding-left: 1.75rem;

    h2 {
      margin-left: -1.75rem;
    }
  }

  &:first-of-type {
    border-top: none;
  }

  h2 {

    display: block;
    margin: 0;
    font-size: 1.2rem;
    position: relative;
    cursor: pointer;
    padding: calc(var(--pico-spacing) * 0.5) var(--pico-spacing);

    &:hover {
      --pico-color: var(--pico-primary-hover);
      animation: vibrate 1.5s infinite forwards;
    }

    Icon {
      margin-top: -1px;
      /*margin-right: 0.5rem;*/
      /*vertical-align: -.3rem;*/
    }

  }

  h2 > span, Button {
    position: relative;
    padding-right: calc(var(--pico-spacing) * 2.25);
    display: inline-flex;
  }

  h2 > span::after, Button::after {
    content: "";
    display: inline-block;
    width: 1.25rem;
    height: 1.25rem;
    mask: var(--pico-icon-chevron) 0 0 / contain no-repeat;
    background: var(--pico-color);
    transition: transform 0.5s ease;
    position: absolute;
    right: calc(var(--pico-spacing) * 0.5);
    top: 50%;
    transform: translateY(-50%) rotate(-90deg);
  }

  &.active {
    grid-template-rows: min-content 1fr;

    h2 > span::after, Button::after {
      transform: translateY(-50%) rotate(0deg);
    }
  }

  & > div {
    overflow: hidden;
    margin: 0;
    /*--pico-typography-spacing-vertical: 0;*/

    & > p {
      display: block;
      margin: 0.1em 1rem 1rem 1rem;
    }
  }

  Button {
    margin: 0.5rem;
  }

}

[disabled] {
  opacity: .5;
  pointer-events: none;
}

</style>

<div bind:this={element} class="accordion {className}" class:icon class:active {disabled} {...rest}>
  {if header}
    {if icon}
      <h2 {...headerRest} {onclick}><span><Icon {icon} size="1.5rem">{@render header()}</Icon></span></h2>
    {else}
      <h2 {...headerRest} {onclick}><span>{@render header()}</span></h2>
    {/if}
  {/if}
  {if button}
    <Button {...buttonRest} {onclick}>{@render button()}</Button>
  {/if}
  <!-- Only render children if actually there's a chance for seeing them, ie. Accordion is not disabled  -->
  {if active || animationRunning}
    <div><p>{@render children?.()}</p></div>
  {/if}
</div>
