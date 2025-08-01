<script>
import { personStore as person } from '@stores';

import { Button } from '@components';
import { getContext, onMount, onDestroy } from 'svelte';

import Accordion from '@components/Accordion.svelte';
import oneIcon   from '@icons/ph/number-circle-one-fill';
import twoIcon   from '@icons/ph/number-circle-two-fill';
import threeIcon from '@icons/ph/number-circle-three-fill';
import fourIcon from '@icons/ph/number-circle-four-fill';
import fiveIcon from '@icons/ph/number-circle-five-fill';
import sixIcon from '@icons/ph/number-circle-six-fill';
import sevenIcon from '@icons/ph/number-circle-seven-fill';
import eightIcon from '@icons/ph/number-circle-eight-fill';
import completedIcon from '@icons/ph/check-circle-duotone';

import * as tasks from '@components/account/tasks';

const icons = [ oneIcon, twoIcon, threeIcon, fourIcon, fiveIcon, sixIcon, sevenIcon, eightIcon ];

let { process = $bindable() } = $props();

function updateStep(target, index, task) {
  if (target.length < (index + 1)) {
    target.push({});
  }

  //let disabled = false;
  //console.log('updateStep: ', task, process.is_completed);


  if (task.is_possible) {
    target[index] = {'active': true, 'icon': icons[index]};
  } else if (task.is_completed) {
    //If the process is waiting, we're not showing completed tasks.
    const active = ! process.is_waiting;
    target[index] = {'active': active, 'class': 'completed', 'icon': completedIcon};
  } else if (task.is_skipped) {
    //If the process is waiting, we're not showing completed tasks.
    target[index] = {'active': false, 'icon': completedIcon};
  } else {
    target[index] = {'active': false, 'disabled': true, 'icon': icons[index]};
  }
  //if (task.is_completed) {
  //  target[index] = { ...target[index], 'class': 'complet  ed', 'icon': completedIcon};
  //}
}

// Where el is the DOM element you'd like to test for visibility
function isHidden(el) {
    return (el.offsetParent === null)
}

const state = $derived.by(() => {
  const steps = [];

  process.tasks.forEach((task, index) => updateStep(steps, index, task));

  //console.log('Derived steps update: ', steps);
  if (process.is_completed && steps.length > 0) {
    steps.forEach((step, index) => {
      if (index < (steps.length - 1)) step['active'] = false;
    });
    const tasks = document.getElementById('tasks');
    if (tasks && isHidden(tasks)) {
      tasks.scrollIntoView({behavior:'smooth'});
    }
  }
  return { steps: steps };
});

</script>

<style>
  Accordion {
    max-width: 50rem;
  }

  Accordion.completed h2 {
    --pico-color: var(--pico-primary);
  }
</style>

{if $person}
  <h2 id="tasks">Tasks</h2>
  {each process.tasks as task, index}
    {if state.steps[index]}
      <Accordion { ...state.steps[index] }>
        {snippet header()}{task.is_completed ? task.label_completed || task.label : task.label}{/snippet}
        {if task.task_type}
          {const TaskComponent=tasks[`${task.task_type}Task`]}
          <TaskComponent {task} bind:process />
        {else}
          {task.description}
          {task.task_type}
        {/if}
      </Accordion>
    {/if}
  {/each}
{/if}
