<script>
import { onMount, onDestroy } from 'svelte';

import { fly } from 'svelte/transition';

import { Icon, Button } from '@components';

import { extract } from '@lib/utils.js';

let { showMenu = false, click, button, children, ...rest } = $props();

// pos is cursor position when right click occur
let pos = $state({ x: 0, y: 0, pageX: 0, pageY: 0 });
// menu is dimension (height and width) of context menu
let menu = { h: 0, w: 0 };
// browser/window dimension (height and width)
let browser = { h: 0, w: 0 };

let margin = 5;

//Fly animation direction of the menu when it pops up,
//needs to be adusted according to the position of the menu
let flyConfig = $state({ x: -1 * margin, y: -1 * margin, duration: window.config.animationDuration });

let article = $state();

function onclick(e){
  //console.log(e);
  if (showMenu) {
    showMenu = false;
    return;
  }
  showMenu = true;
  const app = document.getElementById('app');
  browser = {
    w: app.clientWidth,
    h: app.clientHeight
  };
  pos = {
    x: e.layerX + margin,
    y: e.layerY + margin,
    pageX: e.pageX,
    pageY: e.pageY,
  };
  //console.log('client pos: ', $state.snapshot(pos), browser, app);

  protect();

  e.preventDefault();
  //Need to stop propagtion so it does not overlap with onPageClick()
  e.stopPropagation();
}

// Protect the menu from going out of screen by
// correcting the position if necessary
function protect() {
  if (showMenu) {
    flyConfig = { x: -1 * margin, y: -1 * margin }
    //console.log('check: ', pos.pageY, menu.h, pos.pageY + menu.h, browser.h);
    if ((pos.pageY + menu.h) > browser.h) {
      pos.y = pos.y - menu.h - margin * 2;
      flyConfig.y = margin;
    }
    if ((pos.pageX + menu.w) > browser.w) {
      pos.x = pos.x - menu.w - margin * 2;
      flyConfig.x = margin;
    }
  }
}

$effect(() => {
  if (article) {
    article.style.left = pos.x + 'px';
    article.style.top = pos.y + 'px';
  }
  //console.log('pos calc: ', browser, $state.snapshot(pos));
});

function onPageClick(e){
  // To make context menu disappear when
  // mouse is clicked outside context menu
  showMenu = false;
}
function getContextMenuDimension(node){
  // This function will get context menu dimension
  // when navigation is shown => showMenu = true
  let height = node.offsetHeight
  let width = node.offsetWidth
  if ((height != menu.h) || (width != menu.w)) {
    menu = {
      h: height,
      w: width
    }
    protect();
    //console.log('menu: ', menu);
  }
}

rest = { ...rest };
let buttonRest = extract(rest, 'button:');

</script>

<style>
  container {
    position: relative;
  }
  article {
    position: absolute;
    padding: 1rem;
    width: max-content;
    /* Above normal content */
    z-index: 1;
  }
</style>

<container>
  {if button}
    <Button {...buttonRest} {onclick}>{@render button()}</Button>
  {/if}
  {if showMenu}
    <article bind:this={article} transition:fly={flyConfig} use:getContextMenuDimension style="top:{pos.y}px; left:{pos.x}px">
      {render children()}
    </article>
  {/if}
</container>

<svelte:window onclick={onPageClick} />
