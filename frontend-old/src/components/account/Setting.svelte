<script>

import { Icon, LoadingIndicator } from '@components';

let { checked = $bindable(), name, role = "switch", children, ...rest }  = $props();

import { patchPerson, apiClient  } from "@api/api.svelte.js";
import { personStore as person  } from '@stores';

import iconNoThumbnail from '@icons/ph/file-text-duotone';

const api = apiClient(patchPerson);

checked = $person[name]

async function onchange(event) {
  const response = api.execute({[name]: checked});
}

</script>

<style>
label {
}
</style>

<fieldset {...rest}>
  <label>
    <input {name} type="checkbox" {role} bind:{checked} {onchange} />
    {render children()}
    <LoadingIndicator loading={api.loading} success />
  </label>
</fieldset>
