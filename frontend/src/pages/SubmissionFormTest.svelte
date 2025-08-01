<script>
  let submitter = {
    uuid: '2341ae2e-0334-4e33-baa9-f7c57e015728',
    email: 'docuseal.app@kamuko.de',
    slug: 'dYgmgtseJtbhdx',
    name: null,
    phone: null
  };

  let completedMessage = {
    title: 'Title completed form message',
    body: 'Body completed form message'
  };

  let completedButton = {
    title: 'Button title redirect completed',
    url: 'https://relonee.com/user'
  };

  let attachments = [
    {
      uuid: '3532e47b-6150-4547-bb85-bb0289db3b72',
      created_at: '2024-09-14T09:30:08.206Z',
      url: 'https://sign.relonee.com/disk/eyJfcmFpbHMiOnsiZGF0YSI6eyJrZXkiOiJ3MGhmdDBxMnpqOTI2OGQ4aDNnY3g0bjQyNHg5IiwiZGlzcG9zaXRpb24iOiJpbmxpbmU7IGZpbGVuYW1lPVwic2lnbmF0dXJlLnBuZ1wiOyBmaWxlbmFtZSo9VVRGLTgnJ3NpZ25hdHVyZS5wbmciLCJjb250ZW50X3R5cGUiOiJpbWFnZS9wbmci}'
    }
  ];

  let fields = [
    {
      uuid: 'eb79efb8-f63c-4e75-8f5e-748c0c9f7cef',
      submitter_uuid: '2341ae2e-0334-4e33-baa9-f7c57e015728',
      name: 'name',
      type: 'text',
      required: false,
      preferences: {},
      areas: [
        {
          x: 0.0715694027387319,
          y: 0.2968074681508198,
          w: 0.392362707687449,
          h: 0.0261316861185395,
          attachment_uuid: '9e0c5531-fd2d-4fc7-8df9-51ddc17f5e25',
          page: 0
        }
      ]
    }
  ];

    document.addEventListener('DOMContentLoaded', function() {
      var submissionForm = document.querySelector('submission-form');
      console.log('form', submissionForm);
      if (submissionForm && submissionForm.__vue__) {
        submissionForm.__vue__.baseUrl = 'https://sign.relonee.com';
      }
    });
</script>

<main class="container">
  <h1>Jobs</h1>

  <script data-base-url="adsf" src="https://sign.relonee.com/packs/js/131-250bbd4a42599ea923f1.js" defer="defer" nonce="{window.config.nonce}"></script>
  <script data-base-url="asdf" src="https://sign.relonee.com/packs/js/form-b0b0999122577f98578e.js" defer="defer" nonce="{window.config.nonce}"></script>

<submission-form
  data-is-demo="false"
  data-require-signing-reason="false"
  data-with-signature-id="false"
  data-with-confetti="true"
  data-completed-redirect-url=""
  data-base-url="https://sign.relonee.com"
  base-url="https://sign.relonee.com"

  data-completed-message={JSON.stringify(completedMessage)}
  data-completed-button={JSON.stringify(completedButton)}
  data-submitter={JSON.stringify(submitter)}

  data-can-send-email="false"
  data-attachments={JSON.stringify(attachments)}
  data-fields={JSON.stringify(fields)}

  data-values={JSON.stringify("")}
  data-with-typed-signature="true"
  data-previous-signature-value="3532e47b-6150-4547-bb85-bb0289db3b72"
  data-remember-signature="true"
  data-dry-run=""
  data-expand=""
  data-scroll-padding="-110px"
/>

</main>

