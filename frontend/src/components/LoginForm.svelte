<script>
  import Button from '@kit/components/Button.svelte';
  import { toastWarning } from '@kit/components/Toasts.svelte';
  import loginIcon from '@iconify-icons/ph/sign-in-duotone';

  // Default stub. The real LoginForm lives in each consumer (per-app auth
  // flow). Override @kit/components/LoginForm.svelte via Vite alias
  // to wire up your sign-in form / backend.
  function onclick(event) {
    event?.preventDefault?.();
    console.warn(
      '@kit/components/LoginForm.svelte: default stub. ' +
      'Override via Vite alias to enable sign-in.'
    );
    toastWarning('Sign-in not configured. Override @kit/components/LoginForm.svelte via Vite alias.');
  }
</script>

<slot {onclick}>
  <Button {onclick} icon={loginIcon}>Sign in</Button>
</slot>
