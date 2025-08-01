<script>
  import Dialog from './Dialog.svelte';
  import Button from './RippleButton.svelte';
  import Icon from '@iconify/svelte';
  import loginIcon from '@icons/ph/sign-in-duotone';

  import { submitSigninForm } from '@api/api.js';
  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  import { loadRecaptcha } from '@lib/utils.js';
  import autofocus from '@lib/autofocus.js';

  let dialog;

  // Form input values
  let email = '';
  let emailElement;

  // Error messages
  let emailError = '';
  let emailInvalid;

  let formError = '';

  let submitting = false;
  let recaptchaToken = '';

  function validateForm() {
    // Reset error messages
    emailError = '';

    // Validate form fields
    emailInvalid = !(/^\S+@\S+\.\S+$/.test(email));

    if (emailInvalid) {
      emailError = 'Please provide a valid email address';
      emailElement.focus();
    }

    return !(emailInvalid);
  }

  async function onsubmit(event) {
    event.preventDefault();
    formError = '';
    submitting = true; // Set submitting to true when form submission starts

    try {
      if (!validateForm()) {
        submitting = false;
        return;
      }

      if (!recaptchaToken) {
        // If reCAPTCHA is not loaded, load it dynamically
        const grecaptcha = await loadRecaptcha(window.config.recaptchaKey, window.config.nonce);
        recaptchaToken = await grecaptcha.execute(window.config.recaptchaKey, { action: 'contact_form' });
      }

      // Call the function from api.js to handle form submission
      const response = await submitSigninForm({ email });
      if (response.error) {
        console.error('Failed to sign in:', response.error);
        formError = response.error.message || 'Failed to sign in';
        submitting = false; // Reset submitting if there's an error
        return;
      }
      toastSuccess('Sign in email requested. Check your inbox!');
      dialog.close();

      //clenaup
      submitting = false;
      email = '';

    } catch (error) {
      console.error('Failed to send message:', error);
      submitting = false; // Reset submitting on error
    }
  }

  function onclick(event) {
    event.preventDefault();
    console.log('login dialog: ', dialog);
    dialog.show(event);

    // Load reCAPTCHA when the modal is shown
    loadRecaptcha(window.config.recaptchaKey, window.config.nonce).then(grecaptcha => {
      grecaptcha.ready(() => {
        console.log('reCAPTCHA ready');
      });
    }).catch(error => {
      console.error('Error loading reCAPTCHA:', error);
    });
  }

</script>

<style>

  Button {
    --pico-nav-link-spacing-horizontal: 1rem;
  }

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


<slot {onclick}>
  <Button {onclick} icon={loginIcon}>Sign in</Button>
</slot>

<Dialog bind:this={dialog} {onsubmit} novalidate>
  <h2 slot="header">Sign in</h2>
  <label>
    Your email address:
    <input type="email" bind:value={email} bind:this={emailElement} name="email" placeholder="your@email.com" use:autofocus aria-invalid={emailInvalid} disabled={submitting} />
    {#if emailError}<small>{emailError}</small>{/if}
  </label>
  <small>
    This site is protected by reCAPTCHA and the Google.
    <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
    <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
  </small>
  {#if formError}
    <p class="error-message">{formError}</p>
  {/if}
  <footer>
    <Button type="submit" default aria-busy={submitting} disabled={submitting} icon={loginIcon}>Sign in</Button>
    <Button class="outline" type="cancel" onclick={(event) => dialog.close(event)}>Cancel</Button>
  </footer>
</Dialog>
