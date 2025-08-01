<script>
  import Accordion from '@components/Accordion.svelte';
  import Dialog from '@components/Dialog.svelte';
  import { Button, Icon, Link } from '@components';

  import invitationIcon from '@icons/emojione/party-popper';
  import loginIcon from '@icons/mdi/login-variant';
  import successIcon from '@icons/ph/check-circle-bold';
  import reloneeLogo from '@assets/relonee_logo.svg';
  import reloneeLogoWhite from '@assets/relonee_logo_white.svg';
  import externalLinkIcon from '@icons/mdi/external-link';

  import { configStore as config } from '@stores';

  import { submitTermsForm, signOut } from '@api/api.js';

  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';

  import { loadRecaptcha } from '@lib/utils.js';
  import autofocus from '@lib/autofocus.js';

  import TermsMD from '@markdown/Terms.md?raw';
  import PrivacyMD from '@markdown/Privacy.md?raw';
  import { marked } from 'marked';

  import { navigate } from '@components/Router.svelte';

  let { open, dialog = $bindable(), ...restProps } = $props();

  let state = $state({ terms: false });

  let recaptchaToken = '';

  let darkMode = false;

  function validateForm() {
    // Reset error messages
    state.termsError = '';

    // Validate form fields
    state.termsInvalid = !state.terms;

    if (state.termsInvalid) state.termsError = 'You need to agree to the terms';

    return !(state.termsInvalid);
  }

  async function onsubmit(event) {
    event.preventDefault();
    state.formError = '';
    state.submitted = true; // Set submitted to true when form submission starts

    console.log('onsubmit')

    try {
      if (!validateForm()) {
        state.submitted = false;
        console.log('invalid form')
        return;
      }

      await loadRecaptcha(window.config.recaptchaKey, window.config.nonce);

      // Call the function from api.js to handle form submission
      const response = await submitTermsForm();
      console.log('invalid form');
      if (response.error) {
        console.error('Failed to sign in:', response.error);
        state.formError = response.error.message || 'Failed to sign in';
        state.submitted = false; // Reset submitted if there's an error
        return;
      }
      toastSuccess('Sign in email requested. Check your inbox!');
      dialog.close();

    } catch (error) {
      console.error('Failed to send message:', error);
      state.submitted = false; // Reset submitted on error
    }
  }

  async function onclick(event) {
    event.preventDefault();
    dialog.show(event);

    await loadRecaptcha(window.config.recaptchaKey, window.config.nonce);
  }

  function onreject(event) {
    event.preventDefault();
    signOut();
    navigate('/');
    toastSuccess('Invitation rejected.');
    //dialog.close(event);
  }

</script>

<style>
  /*
  Button {
    --pico-nav-link-spacing-horizontal: 1rem;
  }
   */
  label.checkbox {
    display: flex;
    align-items: flex-start;
    cursor: pointer;
    margin-top: var(--pico-form-element-spacing-vertical);

    input {
      margin-top: 0.15rem;
    }

    ul {
      padding-left: 0;
      margin-bottom: 0;
      li {
        list-style: none
      }

      li.small, li.small a {
        font-size: 0.9rem;
        color: var(--pico-muted-color);
        text-decoration-color: var(--pico-muted-color);
      }

      li.error {
        font-size: 0.9rem;
        color: var(--pico-del-color);
      }
    }
  }

  Dialog {
    --max-width: min(50rem, 50vw);

    Icon {
      margin-block: -0.5rem;
    }

    div.text {
      max-height: 14rem;
      overflow-y: scroll;
      padding: var(--pico-form-element-spacing-horizontal);
      border-radius: var(--pico-border-radius);
      box-shadow: 0 0 0 var(--pico-outline-width) var(--pico-form-element-border-color);
      background-color: var(--pico-form-element-background-color);
      margin: 0 -1rem;

      &:focus {
        box-shadow: 0 0 0 var(--pico-outline-width) var(--pico-form-element-focus-color);
      }
    }

    h2 {
      position: relative;

      img {
        position: absolute;
        right: 0.25rem;
        top: -0.1rem;
        height: 1.75rem;
      }
    }

    Accordion:first-of-type {
      border-top: none;
    }

    Accordion .terms {
        margin: 0;
        padding: .5rem 0;
        font-size: 100%;
    }
  }

</style>


<slot {onclick}>
  {if ! open}
    <Button {onclick}>Show Terms Dialog</Button>
  {/if}
</slot>

<Dialog bind:this={dialog} {onsubmit} novalidate noclose {open} {...restProps}>
  <h2 slot="header">
    <Icon icon={invitationIcon} size="2rem">You have been invited</Icon>
    {#if $config.darkMode}
      <img src={reloneeLogoWhite} alt="Relonee Logo" class="logo" />
    {:else}
      <img src={reloneeLogo} alt="Relonee Logo" class="logo" />
    {/if}
  </h2>

  <p>You have been invited to Relonee's <i>Premium Relocation Support</i> package to help you with your relocation to Germany. Please confirm this invitation and agree to our terms below to allow us working with you on your relocation. <Link href="/" target="_blank" icon={externalLinkIcon}>Learn more about Relonee.</Link></p>

  <Accordion header:class="terms">
    {snippet header()}Terms &amp; Conditions{/snippet}
    <div class="text" tabindex="0">
      {@html marked(TermsMD)}
    </div>
  </Accordion>
  <Accordion header:class="terms">
    {snippet header()}Privacy Policy{/snippet}
    <div class="text" tabindex="0">
      {@html marked(PrivacyMD)}
    </div>
  </Accordion>

  <label class="checkbox">
    <input type="checkbox" bind:checked={state.terms} name="terms" aria-invalid={state.termsInvalid} disabled={state.submitted} />
    <ul>
      <li>I hereby accept Relonee's Terms &amp; Conditions as well as the Privacy Policy for processing and storing data regarding my relocation process.</li>
      <li class="small">This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
        <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
      </li>
      {#if state.termsError}<li class="error">{state.termsError}</li>{/if}
    </ul>
  </label>
  {#if state.formError}
    <p class="error-message">{state.formError}</p>
  {/if}
  <footer class:one={1} class:two={0} class="three">
    <Button type="submit" default aria-busy={state.submitted} disabled={state.submitted} icon={successIcon}>Accept invitation</Button>
    <Button class="outline" type="cancel" onclick={onreject}>Reject</Button>
  </footer>
</Dialog>

