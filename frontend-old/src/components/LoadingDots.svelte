<script>
let { children, text = "Loading", ...rest } = $props();

</script>

<style>
span {
  animation: appear 1.5s infinite ease-in-out;

  /* Apply staggered delays to create a sequential appearance */
  &:nth-child(1) { animation-delay: 0.3s; }
  &:nth-child(2) { animation-delay: 0.6s; }
  &:nth-child(3) { animation-delay: 0.9s; }

  @keyframes appear {
    0%,  20% { opacity: 0; }  /* Start invisible */
    40%, 80% { opacity: 1; }  /* Appear in sequence */
    100%     { opacity: 0; }  /* All disappear together */
  }
}
</style>

{if children}
  <div {...rest}>{render children()}<span>.</span><span>.</span><span>.</span></div>
{else}
  <div {...rest}>{text}<span>.</span><span>.</span><span>.</span></div>
{/if}
