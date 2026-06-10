<script module>
  export let dialog;
  export function onclick(event) {
    event.preventDefault();
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

<script>
  import Dialog from './Dialog.svelte';
  import { Button } from '@components';
  import { submitContactForm } from '@api/api.js';
  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  import { loadRecaptcha } from '@lib/utils.js';
  import autofocus from '@lib/autofocus.js';

  // Form input values
  let name = '';
  let email = '';
  let message = '';
  let terms = false;

  // Error messages
  let nameError = '';
  let nameInvalid;
  let emailError = '';
  let emailInvalid;
  let messageError = '';
  let messageInvalid;
  let termsError = '';
  let termsInvalid;

  let formError = '';

  let submitted = false;
  let recaptchaToken = '';

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

      if (!recaptchaToken) {
        // If reCAPTCHA is not loaded, load it dynamically
        const grecaptcha = await loadRecaptcha(window.config.recaptchaKey, window.config.nonce);
        recaptchaToken = await grecaptcha.execute(window.config.recaptchaKey, { action: 'contact_form' });
      }

      // Call the function from api.js to handle form submission
      const response = await submitContactForm({ name, email, message });
      if (response.error) {
        console.error('Failed to send message:', response.error);
        formError = response.error.message || 'Failed to send the message';
        submitted = false; // Reset submitted if there's an error
        return;
      }
      console.log('Message sent successfully:', response);
      toastSuccess('Message sent successfully');
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
      padding-left: 0;
      li {
        list-style: none
      }

      li.small, li.small a {
        font-size: 0.8rem;
        color: var(--pico-muted-color);
        text-decoration-color: var(--pico-muted-color);
      }

      li.error {
        font-size: 0.9rem;
        color: var(--pico-del-color);
      }
    }
  }
</style>

<slot {onclick}>
  <button {onclick}>Show Contact Modal</button>
</slot>

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
      <li>I hereby accept Relonee's <a href="/privacy" target="_blank">Privacy Policy</a> for processing and storing this form's data.</li>
      <li class="small">This site is protected by reCAPTCHA and the Google.
        <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
        <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
      </li>
      {#if termsError}<li class="error">{termsError}</li>{/if}
    </ul>
  </label>
  {#if formError}
    <p class="error-message">{formError}</p>
  {/if}

  <footer>
    <Button type="submit" default aria-busy={submitted} disabled={submitted}>Send message</Button>
    <Button class="outline" type="cancel" onclick={(event) => dialog.close(event)} disabled={submitted}>Cancel</Button>
  </footer>
</Dialog>
