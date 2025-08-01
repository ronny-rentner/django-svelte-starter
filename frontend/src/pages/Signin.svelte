<script>
  import { onMount } from "svelte";
  import { navigate } from '@components/Router.svelte';
  import { signIn, fetchUserInfo } from '@api/api.js';
  import { toastSuccess, toastWarning } from '@components/Toasts.svelte';
  import LoadingOverlay from '@components/LoadingOverlay.svelte';

  let { token } = $props();

  $effect.pre(async () => {
    console.log('SignIn mounted');
    if (!token) {
      token = new URLSearchParams(window.location.search).get('token');
    }
    if (token) {
      //Artificial delay for testing the loading overlay
      //await new Promise(resolve => setTimeout(resolve, 4000));
      signIn(token).then(success => {
        if (success) {
          console.log('Sign in successful.');
          toastSuccess('Sign in successful.');
          fetchUserInfo().then(() => navigate('/account'));
        } else {
          toastWarning('Failed to sign in.');
          navigate('/');
        }
      });
    } else {
      console.error('Token not found in URL parameters');
      navigate('/');
    }
  });
</script>

<style>
/*
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    font-size: 1.5rem;
  }
*/
</style>

<LoadingOverlay text="Authenticating" showLogo={true} showMain={true} />
