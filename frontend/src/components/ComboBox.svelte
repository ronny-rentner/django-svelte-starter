<script>
  import { tick, onMount, onDestroy } from 'svelte';
  import { writable } from 'svelte/store';


  import { cubicOut } from 'svelte/easing';
  import { slide, fade } from 'svelte/transition';

  let { name, options = [], reset, placeholder, value = $bindable(), iconStart, option, ...restProps } = $props();

  let disabled = undefined;
  //export let name;
  //export let options = [];
  //export let placeholder = undefined;
  let readonly = undefined;
  let required = undefined;
  //export let reset = undefined;

  let previousValue;

  if (!value) {
    value = '';
  }

  // Reactive statement to detect changes in 'value'
  $effect(() => {
    //console.log('Value effect', value, previousValue);
    if (value !== previousValue) {
      selectedOption = options.find(option => option.value === value);
      //console.log(`Value changed from '${previousValue}' to '${value}'`, selectedOption);
      // Your logic to react to the change
      previousValue = value; // Update previousValue to the new value
      if (value == '' || !selectedOption) {
        inputElement.value = '';
      } else {
        inputElement.value = selectedOption.text;
      }
    }
  });

  let resetOption = {
    text: placeholder,
    value: "",
    reset: true,
  }

  const filter = (text) => {
    const sanitized = text.trim().toLowerCase();
    //console.log('filter', sanitized);

    const result = options.reduce((a, o) => {

      let match;

      if (o.options) {
        const options = o.options.filter((o) => o.text.toLowerCase().includes(sanitized));

        if (options.length) {
          match = { ...o, options }
        }
      } else if (o.text.toLowerCase().includes(sanitized)) {
        match = o;
      }

      match && a.push(match);

      return a;
    }, []);
    //console.log('result', result);
    return result;
  };

  let listElement = $state();
  let inputElement;
  let list = $state([]);
  let isListOpen = $state(false);
  let selectedOption;

  function onClickOutside(event) {
    if (listElement && !listElement.contains(event.target) && !inputElement.contains(event.target)) {
      //console.log('click outside');
      hideList();
    }
  }

  /*
  onMount(() => {
    if (value) {
      console.log('onMount select value', value);
      selectOptionByValue(value);
    }
  });
   */

  onDestroy(() => {
      document.body.removeEventListener("mousedown", onClickOutside);
      // Remove any other event listeners or clean up tasks here
  });

  async function onInputKeyup(event) {
    switch (event.key) {
      case "Escape":
      case "ArrowUp":
      case "ArrowLeft":
      case "ArrowRight":
      case "Tab":
      case "Shift":
      case "Enter":
        break;
      case "ArrowDown":
        await showList(event.target.value);
        listElement.querySelector(`[role="option"]:not([aria-disabled="true"])`)?.focus();

        event.preventDefault();
        event.stopPropagation();
        break;

      default:
        await showList(event.target.value);
    }
  }

  function onInputKeydown(event) {
    let flag = false;

    switch (event.key) {
      case "Escape":
        hideList();
        flag = true;
        break;

      case "Tab":
        hideList();
        break;

      case "Enter":
        let inputValue = inputElement.value;
        if (isListOpen) {
          const isExactMatch = options.some((o) => o.options ? o.options.some((o) => o.text === inputValue) : o.text === inputValue);
          let optionElement;
          if (list.length == 1) {
            optionElement = list[0];
          } else if (isExactMatch) {
            optionElement = options.find((o) => o.text === inputValue);
          } else if (inputValue === '') {
            clearSelectedOption();
          }
          if (optionElement) {
            selectOption(optionElement);
          }
          hideList();

          flag = true;
          break;
        } else {
          if (inputValue === '') {
            clearSelectedOption();
          } else {
            if (list.length == 1) {
              let optionElement = list[0];
              selectOption(optionElement);
            }
          }
          break;
        }
    }

    if (flag) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  async function onInputClick(event) {
    if (!isListOpen) {
      await showList(event.target.value);
    } else {
      //We don't hide the list if the user clicks around in the input
      //hideList();
    }
    // Scroll selected option into view.
    //listElement.querySelector(`[role="option"][data-value="${value}"]`)?.scrollIntoView();
  }

  function onOptionClick(event) {
    //console.log('onOptionClick', event.target);
    if (!event.target.matches(`[role="option"]:not([aria-disabled="true"])`)) return;

    selectOption(event.target);
    hideList();
  }

  function onListKeyDown(event) {
    let flag = false;

    //console.log('onListKeyDown()', event.key);

    switch (event.key) {
      case "ArrowUp":
        let prevOptionElement = event.target.previousElementSibling;

        if (!prevOptionElement) {
            inputElement.focus();
            inputElement.setSelectionRange(inputElement.value.length, inputElement.value.length);
            flag = true;

            break;
        }

        while (prevOptionElement) {
          if (prevOptionElement.matches(`[role="option"]:not([aria-disabled="true"])`)) break;
          prevOptionElement = prevOptionElement.previousElementSibling;
        }

        prevOptionElement?.focus();
        flag = true;
        break;

      case "ArrowDown":
        let nextOptionElement = event.target.nextElementSibling;

        while (nextOptionElement) {
          if (nextOptionElement.matches(`[role="option"]:not([aria-disabled="true"])`)) break;
          nextOptionElement = nextOptionElement.nextElementSibling;
        }

        nextOptionElement?.focus();
        flag = true;
        break;

      case "Enter":
        selectOption(event.target);
        hideList();
        flag = true;
        break;

      case "Escape":
        hideList();
        flag = true;
        break;

      case "Tab":
        hideList();
        break;

      default:
        inputElement.focus();
    }

    if (flag) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  async function showList(inputValue) {
      //console.log('showList()');
      const sanitized = inputValue.trim().toLowerCase();
      const isExactMatch = options.some((o) =>
          o.options ? o.options.some((o) => o.text === inputValue) : o.text === inputValue
      );

      list = inputValue === "" || isExactMatch ? options : await filter(inputValue);

      // Move the selected option to the top only if it matches the current filter
      if ((value != '') && list.some(option => option.value === value)) {
          list = list.filter(option => option.value !== value);
          selectedOption = options.find(option => option.value === value);
          if (selectedOption) {
              list.unshift(selectedOption);
          }
      }

      isListOpen = true;
      document.body.addEventListener("mousedown", onClickOutside);
  }

  function hideList() {
    //console.log('hideList()');
    if (!isListOpen) return;

    /*
    if (selectedOption) {
      inputElement.value = selectedOption.text;
    }
     */

    document.body.removeEventListener("mousedown", onClickOutside);
    isListOpen = false;
    inputElement.focus();
  }

  function clearSelectedOption() {
    //console.log('clearSelectedOption');
    selectedOption = undefined;
    value = '';
  }

  function selectOptionByValue(value) {
    //console.log('selectOptionByValue', value);
    const found = options.find(obj => obj.value === value);
    selectOption(found);
  }

  function selectOption(optionElement) {
    let data = optionElement?.dataset ? optionElement.dataset : optionElement;
    value = data.value;

    selectedOption = {
      text: data.text,
      value: data.value
    };

    console.log('selectOption', optionElement, selectedOption, value, data);

    if (value == '') {
      inputElement.value = '';
    } else {
      inputElement.value = selectedOption.text;
    }
  }

  function onInputBlur() {
    // If the input is empty and there is a selectedOption, fill the input with selectedOption.text
    if (inputElement.value.trim() === '' && selectedOption && !isListOpen) {
      clearSelectedOption();
    }
  }

</script>

<div class="combobox" {...restProps}>
    {@render iconStart?.()}
    <input
      bind:this={inputElement}
      onblur={onInputBlur}
      onkeyup={onInputKeyup}
      onkeydown={onInputKeydown}
      onmousedown={onInputClick}
      class="combobox__input"
      {name}
      type="text"
      {disabled}
      autocapitalize="none"
      autocomplete="off"
      {readonly}
      {placeholder}
      spellcheck="false"
      role="combobox"
      aria-autocomplete="list"
      aria-expanded={isListOpen}
      aria-required={required ? "true" : undefined}
    />

  {#if isListOpen}
    <ul
      class="combobox__list"
      class:open={isListOpen}
      transition:slide={{ duration: 200, easing: cubicOut }}
      role="listbox"
      onclick={onOptionClick}
      onkeydown={onListKeyDown}
      bind:this={listElement}
    >
      {#if reset}
        <li
          class="list__option"
          class:disabled={resetOption.disabled}
          class:selected={resetOption.value === value}
          class:reset={resetOption.reset}
          role="option"
          tabindex={resetOption.disabled === true ? undefined : "-1"}
          data-text={resetOption.text}
          data-value={resetOption.value}
          aria-selected={value === resetOption.value}
          aria-disabled={resetOption.disabled}
        >
          {resetOption.text}
          {#if resetOption.value === value}
            <svg viewBox="0 0 24 24" class="icon">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          {/if}
        </li>
      {/if}
      {#each list as item (item)}
        <li
          class="list__option"
          class:disabled={item.disabled}
          class:selected={item.value === value}
          class:reset={item.reset}
          role="option"
          tabindex={item.disabled === true ? undefined : "-1"}
          data-text={item.text}
          data-value={item.value}
          aria-selected={value === item.value}
          aria-disabled={item.disabled}
        >
          {@render option({ item })}

          {#if item.value === value}
            <svg viewBox="0 0 24 24" class="icon">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          {/if}
        </li>
      {:else}
        <li class="list__no-results">
          No results available
        </li>
      {/each}
    </ul>
  {/if}

</div>

<style>
  div {
    display: inline-flex;
    position: relative;
    line-height: 2rem;

    & :global(> svg) {
      position: absolute;
      z-index: 10;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      width: 1rem;
      height: 1rem;
      color: var(--pico-form-element-placeholder-color);
      pointer-events: none;
    }

    input {
      border-radius: 0;
      padding-left: 2.25rem;
      margin-bottom: 0;
    }

    /*
    border-left: var(--pico-form-element-placeholder-color) 2px solid;
     */

    &::after {
        display: block;
        width: 1rem;
        height: calc(1rem * var(--pico-line-height,1.5));
        margin-inline-start: .25rem;
        position: absolute;
        right: var(--pico-form-element-spacing-horizontal);
        padding: 0;
        margin: 0;
        top: 50%;
        z-index: 10;
        transform: rotate(0deg) translate(0, -50%);
        background-image: var(--pico-icon-chevron);
        background-position: right center;
        background-size: 1rem auto;
        background-repeat: no-repeat;
        content: "";
        pointer-events: none;
    }

    :global(.icon) {
      width: 24px;
      height: 24px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
  }

  .combobox__list {
    list-style: none;
    margin: 0;
    margin-left: -1px;
	padding: 0;

    position: absolute;
    inset-inline-start: 0;
    inset-block-start: calc(100% + 1px);
    min-width: 100%;
    max-width: 100%;
    max-height: max(40vh, 14rem);
    overflow-y: auto;
    scrollbar-gutter: stable;

    z-index: 100;

    /*border-radius: 0.3em;*/
    box-shadow: var(--pico-box-shadow);
	transition: opacity var(--pico-transition), transform 0s ease-in-out 1s;

	border: var(--pico-border-width) solid var(--pico-dropdown-border-color);
    /*border-radius: var(--pico-border-radius);*/
	background-color: var(--pico-dropdown-background-color);
	box-shadow: var(--pico-dropdown-box-shadow);
	color: var(--pico-dropdown-color);
	white-space: nowrap;

    &.open {

    }
  }

  /*
  .list__option-heading {
    font-size: 0.9em;
    padding-inline: 1rem;
    padding-block-start: 0.4rem;
    color: gray;
  }
   */

  .list__no-results {
    padding: 0.8rem 1rem;
  }

  .list__option {
    display: flex;
    align-items: center;
    /*justify-content: space-between;*/
    gap: 0.6rem;
    padding: 0.15rem .75rem;
    border: 0.15rem solid transparent;
    border-radius: 0.3rem;
    border-radius: 0;
    margin: 0;
  }

  .list__option > :global(*) {
    pointer-events: none;
  }

  .list__option.disabled {
    pointer-events: none;
    opacity: 0.4;
  }

  .list__option.reset {
	border-bottom: var(--pico-border-width) solid var(--pico-primary-border);
  }

  .list__option:focus,
  .list__option:not([aria-disabled="true"]):hover {
    outline: none;
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.1);
  }

  .list__option:active {
    cursor: pointer;
    outline: none;
    color: white;
    background-color: var(--pico-primary) !important;
  }

  .list__option:focus :global(svg),
  .list__option:hover :global(svg) {
    --icon-color: white !important;
  }
</style>
