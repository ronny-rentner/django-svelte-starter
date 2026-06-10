<script>
  import reloneeLogo from '/src/assets/relonee_logo.svg'

  import { onMount, onDestroy, getContext } from 'svelte';

  import { Main } from '@components';
  import HeroBanner from '@components/HeroBanner.svelte';

  let layoutConfig = getContext('layoutConfig');
  let isMounted = false;


  // This runs before every DOM update, including before the initial mount
  $effect.pre(() => {
    //layoutConfig['contrast'] = true;
    //console.log('beforeUpdate', isMounted, $contrastMode);
    if (isMounted) {
      //console.log('Component is updating');
      // Perform logic here that you want before the component updates
    } else {
      layoutConfig['contrast'] = true;
      //console.log('beforeUpdate triggered before mount', { ... layoutConfig });
      // You might avoid certain actions here because the component isn't mounted yet
    }
  });

  onMount(() => {
    isMounted = true;
    //console.log('onMount', isMounted, $contrastMode);
  });

  onDestroy(() => {
    isMounted = false;
    layoutConfig['contrast'] = false;
  });

</script>

<style>

  section {
    margin: 2rem;

    svg {
      width: 2rem;
      color: var(--pico-primary);
    }
    article {
      header {
        padding: 2rem;
      }
      dl {
        padding-inline: 1rem;
      }
    }

    &.process {


      div.grid {
        &>div, &>article {
          margin: 1rem 3rem;
        }
      }

      dt {
        font-weight: bold;
        font-family: Mulish;
        font-size: 110%;
        margin-top: 1.5rem;
      }

      blockquote {
        font-size: 120%;
      }

    }



  }

  section.features {
    margin-top: 3rem;

    div.grid {
      grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
      grid-auto-flow: dense;
      padding: 2rem;

      gap: 2rem;

      div.feature {

        margin-left: 4rem;

        h3 {
          position: relative;
          left: -3rem;
          margin-bottom: 0;

          font-weight: bold;
          font-size: 110%;
          font-family: Mulish;

          svg {
            margin: 0 1rem 0 0;
            vertical-align: middle;
          }
        }

        a {
          display: block;
          margin-top: 1rem;
          &::after {
            content: " →";
          }
        }
      }
    }

  }

  @media mobile {
    section, section.features, section.process {
      margin-inline: 0;

      div.grid {
        padding: 0;

        div.quotes {
          margin: 0;
        }

        article {
          margin: 1rem !important;
          dl {
            padding: 0;

            svg {
              margin-right: 0.15rem;
            }
          }
        }
      }
    }
  }

</style>

<Main>

  <HeroBanner />

  <section id="features" class="features">

    <h2>Why choose us?</h2>
    <div class="grid">
      <div class="feature">
        <h3><svg viewBox="0 0 24 24"><path d="M22,17H18V10H22M23,8H17A1,1 0 0,0 16,9V19A1,1 0 0,0 17,20H23A1,1 0 0,0 24,19V9A1,1 0 0,0 23,8M4,6H22V4H4A2,2 0 0,0 2,6V17H0V20H14V17H4V6Z"></path></svg>Digital</h3>
        Leverage advanced AI that eliminates paperwork and streamlines every step of your relocation process.
        <a href={"#"}>Learn more</a>
      </div>
      <div class="feature">
        <h3><svg viewBox="0 0 24 24"><path d="M20,2H4V4L9.81,8.36C6.14,9.57 4.14,13.53 5.35,17.2C6.56,20.87 10.5,22.87 14.19,21.66C17.86,20.45 19.86,16.5 18.65,12.82C17.95,10.71 16.3,9.05 14.19,8.36L20,4V2M14.94,19.5L12,17.78L9.06,19.5L9.84,16.17L7.25,13.93L10.66,13.64L12,10.5L13.34,13.64L16.75,13.93L14.16,16.17L14.94,19.5Z"></path></svg>Experienced</h3>
        Benefit from 15 years of industry expertise, backed by thousands of successful relocations to Germany.
        <a href={"#"}>Learn more</a>
      </div>
      <div class="feature">
        <h3><svg viewBox="0 0 24 24"><path d="M19 13V11H21V13H19M21 9V7H19V9H21M21 3H19V5H21V3M17 15H19V13H17V15M21 17V15H19V17H21M13 17V15H15V13H13V11H15V9H13V7H15V5H13V3H3V21H13V19H15V17H13M15 21H17V19H15V21M17 3H15V5H17V3M17 11H19V9H17V11M15 17H17V15H15V17M17 19H19V17H17V19M21 21V19H19V21H21M15 9H17V7H15V9M15 13H17V11H15V13M17 5V7H19V5H17Z"></path></svg>Transparent</h3>
        Count on fixed, transparent pricing with no hidden fees. Track the entire process through your dashboard.
        <a href={"#"}>Learn more</a>
      </div>
      <div class="feature">
        <h3><svg viewBox="0 0 24 24"><path d="M16 17V19H2V17S2 13 9 13 16 17 16 17M12.5 7.5A3.5 3.5 0 1 0 9 11A3.5 3.5 0 0 0 12.5 7.5M15.94 13A5.32 5.32 0 0 1 18 17V19H22V17S22 13.37 15.94 13M15 4A3.39 3.39 0 0 0 13.07 4.59A5 5 0 0 1 13.07 10.41A3.39 3.39 0 0 0 15 11A3.5 3.5 0 0 0 15 4Z"></path></svg>Personal</h3>
        Ensure your employees feel secure and confident throughout their whole relocation journey.
        <a href={"#"}>Learn more</a>
      </div>

    </div>


  </section>
  <section class="process">
    <h2>Smooth and professional</h2>
    <div class="grid">
      <div class="quotes">
        <blockquote>
          “Design is a funny word. Some people think
          design means how it looks. But of course, if
          you dig deeper, it's really how it works.”
          <footer>
            <cite>— Steve Jobs</cite>
          </footer>
        </blockquote>
        <blockquote>
          “RELONEE handles the entire relocation process for your international employees from signing the offer to the moment of holding a longterm residence title in their hands. You can stay updated by a real time tracking of the process on your personalized dashboard anytime. ”
          <footer>
            <cite>— Theresa</cite>
          </footer>
        </blockquote>
      </div>

      <article>
        <header>
          Entrust RELONEE to manage your corporate relocations with precision and care. Our platform is designed to support your international employees from start to finish, optimizing the relocation process through automation and providing a comprehensive hub for all necessary documents and information.
        </header>
        <dl>
          <div>
            <dt>
              <svg viewBox="0 0 24 24"><path  d="M21.1,12.5L22.5,13.91L15.97,20.5L12.5,17L13.9,15.59L15.97,17.67L21.1,12.5M10,17L13,20H3V18C3,15.79 6.58,14 11,14L12.89,14.11L10,17M11,4A4,4 0 0,1 15,8A4,4 0 0,1 11,12A4,4 0 0,1 7,8A4,4 0 0,1 11,4Z"></path></svg>
              Eligibility Assessment:
            </dt>
            <dd>We provide a comprehensive pre-relocation assessment to ensure your employees meet all immigration criteria, minimizing risk and ensuring a smooth process.</dd>
          </div>
          <div>
            <dt>
              <svg viewBox="0 0 24 24"><path d="M5,5V19H8V5M10,5V19L21,12"></path></svg>
              Step-by-Step Guidance:
            </dt>
            <dd>Our platform simplifies data collection, automating paperwork preparation and guiding your HR team through every legal and administrative requirement.</dd>
          </div>
          <div>
            <dt>
              <svg viewBox="0 0 24 24"><path d="M10,2H14A2,2 0 0,1 16,4V6H20A2,2 0 0,1 22,8V19A2,2 0 0,1 20,21H4C2.89,21 2,20.1 2,19V8C2,6.89 2.89,6 4,6H8V4C8,2.89 8.89,2 10,2M14,6V4H10V6H14Z"></path></svg>
              Hassle-Free Integration:
            </dt>
            <dd>
              From visa applications to settling in, we ensure your employees' transitions are smooth, minimizing disruption to their work and maximizing productivity.
            </dd>
          </div>
        </dl>
    </article>
  </div>
  </section>

</Main>
