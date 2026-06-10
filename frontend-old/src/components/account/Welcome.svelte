<script>
  import Theresa from '@assets/Theresa 2.webp';
  import Signature from '@assets/Theresa-signature.png';
</script>

<style>
  section {
    max-width: 60rem;
    font-style: italic;
    line-height: 180%;

    p:first-of-type {
      font-style: italic;
      font-size: 110%;
      font-weight: bold;
    }

    .photo {
      line-height: 1.4rem;
      font-style: normal;
      margin: 3rem 1rem 1rem 2rem;
      float: right;
      text-align: center;
      width: min(20vw, 12rem);

      @mobile {
        width: 8rem;
        margin: 1rem 0 0.25rem 0;
      }
    }

    .signature {
      width: 7.5rem;
      display: block;
      margin: 1.5rem;

      @dark & {
        filter:brightness(2);
      }
    }
  }


</style>

<section>
  <div class="photo">
    <img src={Theresa} alt="Theresa" width="639" height="822" />
    Theresa, Founder of Relonee
  </div>

  <markdown file="account/Welcome.md" />

  <img class="signature" src={Signature} alt="Signature" />
</section>
