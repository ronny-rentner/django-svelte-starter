<script>
  import { Button } from '@components';

  let emailError = '';
  let emailInvalid;
  let formError = '';

  let submitted = false;

  let recaptchaToken = '';

</script>

<style>

  form {
    max-width: 32rem;
  }

</style>

<main class="container">
  <markdown />

  <form>
    <fieldset role="group">
      <input type="email" name="email" aria-invalid={emailInvalid} disabled={submitted} placeholder="E-mail" />
      <input type="submit" value="Register for Waitlist" />
      {#if emailError}<small>{emailError}</small>{/if}
    </fieldset>
  </form>

</main>

