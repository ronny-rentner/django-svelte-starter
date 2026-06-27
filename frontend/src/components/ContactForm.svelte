<script module>
  import { loadRecaptcha } from '@kit/recaptcha';

  export let dialog;
  export function onclick(event) {
    event.preventDefault();
    dialog.show(event);
    loadRecaptcha();
  }

</script>

<script>
  import Dialog from '@kit/components/Dialog.svelte';
  import { Button } from '@kit/components';
  import { submitContactForm } from '@api/api.js';
  import { toastSuccess, toastWarning } from '@kit/components/Toasts.svelte';

  import { autofocus } from '@kit/actions';

  let { children } = $props();

  // Form input values
  let name = $state('');
  let email = $state('');
  let message = $state('');
  let terms = $state(false);

  // Error messages
  let nameError = $state('');
  let nameInvalid = $state();
  let emailError = $state('');
  let emailInvalid = $state();
  let messageError = $state('');
  let messageInvalid = $state();
  let termsError = $state('');
  let termsInvalid = $state();

  let formError = $state('');

  let submitted = $state(false);

  function validateForm() {
    // Reset error messages
    nameError = '';
    emailError = '';
    messageError = '';
    termsError = '';

    // Validate form fields
    nameInvalid = name.trim() == '';
    emailInvalid = !(/^\S+@\S+\.\S+$/.test(email));
    messageInvalid = message.trim() == '';
    termsInvalid = !terms;

    if (nameInvalid) nameError = 'Name is required.';
    if (emailInvalid) emailError = 'Please provide a valid email address.';
    if (messageInvalid) messageError = 'Message is required.';
    if (termsInvalid) termsError = 'You need to agree to the terms.';

    return !(nameInvalid || emailInvalid || messageInvalid || termsInvalid);
  }

  async function onsubmit(event) {
    event.preventDefault();
    formError = '';
    submitted = true; // Set submitted to true when form submission starts

    try {
      if (!validateForm()) {
        submitted = false;
        return;
      }

      // Call the function from api.js to handle form submission
      const response = await submitContactForm({ name, email, message });
      if (!response.success) {
        console.error('Failed to send message:', response?.error);
        formError = `Error: ${response?.error}`;
        submitted = false; // Reset submitted if there's an error
        return;
      }
      toastSuccess('Your message has been sent successfully.');
      dialog.close();

    } catch (error) {
      console.error('Failed to send message:', error);
      submitted = false; // Reset submitted on error
    }
  }

</script>

<style>
label.checkbox {
  display: flex;
  align-items: flex-start;
  cursor: pointer;

  input {
    margin-top: 0.15rem;
  }

  ul {
    margin: 0;
    padding-left: 0;
    li {
      list-style: none
    }

    li.small, li.small a {
      font-size: 0.9rem;
      line-height: 1.1rem;
      color: var(--pico-muted-color);
      text-decoration-color: var(--pico-muted-color);
    }

    li.error {
      font-size: 0.9rem;
      color: var(--pico-error-color);
    }
  }
}
</style>

{#if children}
  {@render children(onclick)}
{:else}
  <button {onclick}>Show Contact Modal</button>
{/if}

<Dialog bind:this={dialog} {onsubmit} novalidate>
  <h2 slot="header">Contact Us</h2>

  <label>Name:
    <input type="text" bind:value={name} name="name" use:autofocus aria-invalid={nameInvalid} disabled={submitted} />
    {#if nameError}<small>{nameError}</small>{/if}
  </label>

  <label>Email:
    <input type="email" bind:value={email} name="email" aria-invalid={emailInvalid} disabled={submitted} />
    {#if emailError}<small>{emailError}</small>{/if}
  </label>

  <label>Message:
    <textarea rows="4" cols="40" bind:value={message} aria-invalid={messageInvalid} disabled={submitted}></textarea>
    {#if messageError}<small>{messageError}</small>{/if}
  </label>

  <label class="checkbox">
    <input type="checkbox" bind:checked={terms} name="terms" aria-invalid={termsInvalid} disabled={submitted} />
    <ul>
      <li>I accept the <a href="/privacy" target="_blank">Privacy Policy</a> for processing and storing this form's data.</li>
      <li class="small">This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
        <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
      </li>
      {#if termsError}<li class="error">{termsError}</li>{/if}
    </ul>
  </label>
  {#if formError}
    <p class="error">{formError}</p>
  {/if}

  <footer>
    <Button type="submit" default aria-busy={submitted} disabled={submitted}>Send message</Button>
    <Button class="outline" type="cancel" onclick={(event) => dialog.close(event)} disabled={submitted}>Cancel</Button>
  </footer>
</Dialog>
