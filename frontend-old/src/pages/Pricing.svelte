<script>
  import { Icon, Button } from '@components';
  //import freeIcon from '@icons/ph/balloon-duotone';
  //import freeIcon from '@icons/ph/paper-plane-tilt-duotone';

  import freeIcon1 from '@icons/pepicons-print/paper-plane';
  import teamIcon1 from '@icons/pepicons-print/airplane';
  import enterpriseIcon1 from '@icons/pepicons-print/building';

  import freeIcon2 from '@icons/pepicons-pencil/paper-plane';
  import teamIcon2 from '@icons/pepicons-pencil/airplane';
  import enterpriseIcon2 from '@icons/pepicons-pencil/building';

  let freeIcon = freeIcon1, teamIcon = teamIcon1, enterpriseIcon = enterpriseIcon1;

  if (window.location.search == '?2') {
    freeIcon = freeIcon2;
    teamIcon = teamIcon2;
    enterpriseIcon = enterpriseIcon2;
  }

</script>
<style>
  article {
    margin: 4rem auto;
    max-width: 66rem;

    text-align: center;
    padding: 0;

    div.grid {
      padding-block: 1rem;
      gap: 0;

      div.column {
        /* bottom padding to make space for footer */
        padding: 2rem 2rem 8.5rem 2rem;
        position: relative;

        border-left: 1px var(--pico-muted-border-color) solid;
        &:first-child {
          border-left: 0;
        }

        h2 {
          letter-spacing: 0.1rem;
          font-size: 120%;
          margin: 0 0 1.25rem 0;
          color: var(--pico-muted-color);
        }

        div.icon {
          /* make space for the circles */
          /* margin: 3rem; */
          position: relative;
          display: inline-block;

          /* big circle */
          &::before {
            content: '';
            position: absolute;
            top: -4.5rem;
            left: -4.5rem;
            width: 15rem;
            height: 15rem;
            border-radius: 50%;
            background-color: var(--pico-secondary-background);
            z-index: 1;
            opacity: 0.05;
          }

          /* small circle */
          &::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6rem;
            height: 6rem;
            border-radius: 50%;
            background-color: var(--pico-primary-background);
            z-index: 1;
            opacity: 0.1;
          }

          Icon {
            opacity: 0.6;
            color: var(--pico-primary);
            z-index: 2;
            position: relative;
          }
        }

        footer {

          position: absolute;
          bottom: 1rem;
          right: 2.5rem;
          left: 2.5rem;

          h3 {
            font-weight: bold;
            font-family: Arial, sans-serif;
            font-size: 160%;
            margin-bottom: 1.5rem;

            small {
              font-size: 70%;
              font-weight: normal;
              color: var(--pico-muted-color);
            }
          }

          Button {
          }
        }

        ul {
          margin: 2rem .5rem 1rem .5rem;
          padding: 0;

          li {
            background: var(--pico-icon-valid) 0.25rem center no-repeat;
            margin: 0;
            text-align: left;
            list-style: none;
            border-bottom: 1px var(--pico-muted-border-color) solid;
            &:first-child {
              border-top: 1px var(--pico-muted-border-color) solid;
            }
            padding: 0.5rem 0.5rem 0.5rem 2rem;
          }
        }
      }
    }
  }

  :root[data-theme="light"] {
    article {
      --pico-card-background-color: #fff;
    }
  }

</style>

<main class="container">
    <article>
    <card>
    <div class="grid">
      <div class="column">
        <h2>PERSONAL</h2>
        <div class="icon"><Icon icon={freeIcon} size="6rem" /></div>
        <ul>
          <li>Anabin search</li>
          <li>Anabin printous</li>
          <li>AI recognition</li>
        </ul>
        <footer>
          <h3>€0 <small>free</small></h3>
          <Button>Register for free</Button>
        </footer>
      </div>
      <div class="column">
        <h2>TEAM</h2>
        <div class="icon"><Icon icon={teamIcon} size="6rem" /></div>
        <ul>
          <li>Everything from PERSONAL</li>
          <li>Support via email</li>
        </ul>
        <footer>
          <h3>€199 <small>per month</small></h3>
          <Button disabled>Coming soon</Button>
        </footer>
      </div>
      <div class="column">
        <h2>ENTERPRISE</h2>
        <div class="icon"><Icon icon={enterpriseIcon} size="6rem" /></div>
        <ul>
          <li>Everything from TEAM</li>
          <li>Support via video calls and email</li>
          <li>SAML / Single Signon</li>
        </ul>
        <footer>
          <h3>Reach out</h3>
          <Button disabled>Coming soon</Button>
        </footer>
      </div>
    </div>
      </card>
    </article>
</main>

