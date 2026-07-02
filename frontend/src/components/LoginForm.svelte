<script>
  import Dialog from '@kit/components/Dialog.svelte';
  import { Button } from '@kit/components';
  import loginIcon from '@iconify-icons/ph/sign-in-duotone';
  import { submitSigninForm } from '@api/api.js';
  import { toastSuccess } from '@kit/components/Toasts.svelte';
  import { loadRecaptcha } from '@kit/recaptcha';
  import { autofocus } from '@kit/actions';

  let { children } = $props();

  let dialog = $state();

  let email = $state('');
  let emailError = $state('');
  let emailInvalid = $state();
  let formError = $state('');
  let submitting = $state(false);

  function onclick(event) {
    event.preventDefault();
    dialog.show(event);
    // Start loading reCAPTCHA when the modal opens.
    loadRecaptcha();
  }

  function validateForm() {
    emailError = '';
    emailInvalid = !(/^\S+@\S+\.\S+$/.test(email));
    if (emailInvalid) emailError = 'Please provide a valid email address.';
    return !emailInvalid;
  }

  async function onsubmit(event) {
    event.preventDefault();
    formError = '';
    submitting = true;

    try {
      if (!validateForm()) {
        submitting = false;
        return;
      }

      const response = await submitSigninForm({ email });
      if (!response.success) {
        console.error('Failed to request sign-in:', response?.error);
        formError = `Error: ${response?.error}`;
        submitting = false;
        return;
      }
      toastSuccess('Sign-in email requested. Check your inbox!');
      dialog.close();
      submitting = false;
      email = '';

    } catch (error) {
      console.error('Failed to request sign-in:', error);
      submitting = false;
    }
  }
</script>

<style>
  small {
    display: inline-block;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    line-height: 1.1rem;
    color: var(--pico-muted-color);

    a {
      text-decoration-color: var(--pico-muted-color);
    }
  }
</style>

{#if children}
  {@render children(onclick)}
{:else}
  <Button {onclick} icon={loginIcon}>Sign in</Button>
{/if}

<Dialog bind:this={dialog} {onsubmit} novalidate>
  <h2 slot="header">Sign in</h2>

  <label>Your email address:
    <input type="email" bind:value={email} name="email" placeholder="your@email.com" use:autofocus aria-invalid={emailInvalid} disabled={submitting} />
    {#if emailError}<small>{emailError}</small>{/if}
  </label>

  <small>
    This site is protected by reCAPTCHA and the Google
    <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
    <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
  </small>

  {#if formError}
    <p class="error">{formError}</p>
  {/if}

  <footer>
    <Button type="submit" default aria-busy={submitting} disabled={submitting} icon={loginIcon}>Sign in</Button>
    <Button class="outline" type="cancel" onclick={(event) => dialog.close(event)} disabled={submitting}>Cancel</Button>
  </footer>
</Dialog>
