<script>
  import { navigate } from '@kit/router';
  import { signIn, fetchUserInfo } from '@api/api.js';
  import { toastSuccess, toastWarning } from '@kit/components/Toasts.svelte';
  import LoadingOverlay from '@kit/components/LoadingOverlay.svelte';

  // The sign-in email links here as /signin?token=...
  const token = new URLSearchParams(window.location.search).get('token');

  if (token) {
    signIn(token).then((success) => {
      if (success) {
        fetchUserInfo().then(() => {
          toastSuccess('Sign-in successful.');
          navigate('/');
        });
      } else {
        toastWarning('Sign-in failed. Please try again.');
        navigate('/');
      }
    });
  } else {
    navigate('/');
  }
</script>

<LoadingOverlay text="Authenticating" showLogo={true} showMain={true} />
