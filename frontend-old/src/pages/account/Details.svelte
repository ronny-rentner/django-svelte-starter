<script>
import { personStore as person } from '@stores';

import { Button, LoadingIndicator } from '@components';
import Setting from '@components/account/Setting.svelte';
import { getContext, onMount, onDestroy } from 'svelte';
import AccountLayout from '@layout/Account.svelte';

import { getPerson, apiClient  } from "@api/api.svelte.js";
const api = apiClient(getPerson);

api.execute();

</script>

<AccountLayout>

  <h1>Account Details<LoadingIndicator loading={api.loading} /></h1>
  <p>
    {$person.full_name}<br />
    {$person.email}
  </p>

  <h2>Settings</h2>
  <Setting name="notify_email_3rd_party_signature_completed">Notify me via email when documents haven been signed by 3rd parties</Setting>

</AccountLayout>
