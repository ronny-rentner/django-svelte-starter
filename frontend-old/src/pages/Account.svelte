<script>
  import { onMount } from "svelte";

  import { personStore as person } from '@stores';
  import { navigate } from '@components/Router.svelte';

  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  import AccountLayout from '@layout/Account.svelte';

  import Welcome from '@components/account/Welcome.svelte';
  import TermsDialog from '@components/account/TermsDialog.svelte';

  let { meta, ...rest } = $props();
  meta({
    title: 'Account - RELONEE',
    description: 'Account overview'
  });

  console.log('Account person: ', $person);

  let dialog = $state();
  let showTermsDialog = $state($person?.status === 'new');

//onMount(() => {
    //console.log('terms dialog', dialog);
    if (! $person) {
      //toastWarning('You need to signin first');
      //navigate('/');
    } else {
      if ($person && $person?.status === 'new') {
        showTermsDialog = true;
      }
    }
//});

  $effect(() => {
    if ($person && $person?.status === 'new') {
      showTermsDialog = true;
    }
  });

  function onclose(event) {
    console.log('Terms dialog closed', event);
    showTermsDialog = false;
  }

</script>

<AccountLayout>

  <Welcome />

  {if showTermsDialog}
    <TermsDialog bind:dialog {onclose} open />
  {/if}

</AccountLayout>
