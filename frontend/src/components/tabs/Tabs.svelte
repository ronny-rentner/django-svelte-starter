<script context="module">
  export const TABS = {};
</script>

<script>
  import { afterUpdate, setContext, onDestroy, onMount, tick } from 'svelte';
  import { writable } from 'svelte/store';

  import { preventNextFocusChange } from '@lib/autofocus.js';

  export let id = 'tabs';
  export let updateBrowserUrl = true;
  let localStorageKey = `tabs-${id}`
  let initialSelectedIndex = localStorage.get(localStorageKey, 0);

  const tabElements = [];
  const tabs = [];
  const panels = [];

  const controls = writable({});
  const labeledBy = writable({});

  const selectedTab = writable(null);
  const selectedPanel = writable(null);

  function removeAndUpdateSelected(arr, item, selectedStore) {
    const index = arr.indexOf(item);
    arr.splice(index, 1);
    selectedStore.update(selected => selected === item ? (arr[index] || arr[arr.length - 1]) : selected);
  }

  function registerItem(arr, item, selectedStore) {
    arr.push(item);
    selectedStore.update(selected => selected || item);
    onDestroy(() => removeAndUpdateSelected(arr, item, selectedStore));
  }

  function updateURL(index, initialLoad) {
    //console.log('TAB updateURL', index, initialLoad);
    if (!updateBrowserUrl) return;
    /*
    if (history?.state && !('tab' in history.state)) {
      //console.log('Replacing initial state: ', index);
      history.replaceState({ tab: index }, '');
    }
     */
    //if (initialLoad) return;

    const tabName = tabs[index]?.dataId;

    if (tabName) {
      const url = new URL(window.location.href);

      if (initialLoad && url.searchParams.has(tabName)) {
        return;
      }

      // Construct a new search parameter with only the active tab's dataId
      url.search = `?${tabName}`;

      // Retain the hash part of the URL
      const hash = url.hash;

      // Construct the new URL including the hash
      const newUrl = `${url.origin}${url.pathname}${url.search}${hash}`;
      if (initialLoad) {
        history.replaceState(history?.state, '', newUrl);
      } else {
        history.pushState(history?.state, '', newUrl);
      }
    }
  }

  // Function to check if the element is within the viewport
  function scrollToViewIfNeeded(element) {
    if (!element) return;
    //console.log('scrollToViewIfNeeded: ', element);
    const rect = element.getBoundingClientRect();

    // Check if the top of the component is out of view (above or below the viewport)
    if (rect.top < 0 || rect.top > window.innerHeight) {
      //console.log('SCROLL needed: ', rect, window);
      // Scroll to the top border of the element
      setTimeout(() => element.scrollIntoView({ behavior: 'smooth', block: 'start' }), 0);
    }
  }

  function selectTab(tab, initialLoad = false) {
    //console.log('selectTab: ', tab, initialLoad);

    //Nothing to do, already selected the correct tab;
    if (tab == selectedTab) {
      return;
    }

    const index = tabs.indexOf(tab);
    tab.index = index;
    selectedTab.set(tab);
    selectedPanel.set(panels[index]);
    //console.log('Selected Tab Panel: ', panels[index], tabElements[index]);
    if (selectedPanel.onselect) {
      //console.log('onselect');
      selectedPanel.onselect();
    }
    localStorage.set(localStorageKey, index);
    updateURL(index, initialLoad);
    scrollToViewIfNeeded(tabElements[index])
  }

  function selectTabIndex(index, initialLoad = false) {
    //console.log('selectTabIndex: ', index, initialLoad);

    //Nothing to do, already selected the correct tab;
    if (index == undefined || index == selectedTab.index) {
      return;
    }

    if (index == -1) {
      index = 0;
    }

    return selectTab(tabs[index], initialLoad);
  }

  setContext(TABS, {
    registerTab(tab) {
      registerItem(tabs, tab, selectedTab);
    },

    registerTabElement(tabElement) {
      tabElements.push(tabElement);
    },

    registerPanel(panel) {
      registerItem(panels, panel, selectedPanel);
    },

    selectTab,

    selectedTab,
    selectedPanel,

    controls,
    labeledBy
  });

  //Event handler when the user goes backwards or forwards in browser history
  function onPopState(event) {
    console.log('onPopState', event.state, event?.state?.tab, event);
    const url = new URL(window.location.href);
    url.searchParams.forEach((value, key) => {
      const indexFromURL = tabs.findIndex(tab => tab.dataId === key);
      if (indexFromURL != -1) {
        selectTabIndex(indexFromURL, true);
      }
    });
  }

  onMount(() => {
    if (updateBrowserUrl) {
      const url = new URL(window.location.href);
      let indexFromHash;
      url.searchParams.forEach((value, key) => {
        indexFromHash = tabs.findIndex(tab => tab.dataId === key);
        if (indexFromHash !== -1) {
          initialSelectedIndex = indexFromHash;
          //console.log('initialSelectedIndex updated from url: ', initialSelectedIndex);
        }
      });
    }
    selectTab(tabs[initialSelectedIndex], true);

    window.addEventListener('popstate', onPopState);

    return () => {
      window.removeEventListener('popstate', onPopState);
    };
  });

  afterUpdate(() => {
    for (let i = 0; i < tabs.length; i++) {
      controls.update(controlsData => ({...controlsData, [tabs[i].id]: panels[i].id}));
      labeledBy.update(labeledByData => ({...labeledByData, [panels[i].id]: tabs[i].id}));
    }
  });

  async function handleKeyDown(event) {
    if (event.target.classList.contains('Tab')) {
      let selectedIndex = tabs.indexOf($selectedTab);

      switch (event.key) {
        case 'ArrowRight':
          selectedIndex += 1;
          if (selectedIndex > tabs.length - 1) {
            selectedIndex = 0;
          }
          preventNextFocusChange();
          selectTab(tabs[selectedIndex]);
          tabElements[selectedIndex].focus();
          break;

        case 'ArrowLeft':
          selectedIndex -= 1;
          if (selectedIndex < 0) {
            selectedIndex = tabs.length - 1;
          }
          preventNextFocusChange();
          selectTab(tabs[selectedIndex]);
          tabElements[selectedIndex].focus();
          break;

        case 'ArrowUp':
        case 'ArrowDown':
          event.target.blur();
          break;
      }
    }
  }
</script>

<div class="svelte-tabs" onkeydown={handleKeyDown} {...$$restProps}>
  <slot></slot>
</div>
