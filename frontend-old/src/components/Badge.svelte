<script module>
import Badges from '@components/Badges.svelte';
export { Badges };
</script>

<script>
let { children, color = 'red', ...rest } = $props();
</script>

<style>
span {
  padding: .125rem .25rem;
  border-radius: .125rem;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  background-color: rgba(var(--bg, var(--fg)), 0.125);
  color: rgb(var(--fg));
}

.red    { --fg: 168,  52,  16; }
.blue   { --fg:  26, 115, 232; }
.yellow { --fg: 255, 193,   7; }
.green  { --fg:  52, 168,  83; }
.purple { --fg: 103,  58, 183; }
.orange { --fg: 255,  87,  34; }
.pink   { --fg: 233,  30,  99; }
.teal   { --fg:   0, 150, 136; }
.gray   { --fg: 158, 158, 158; }
.black  { --fg:   0,   0,   0; }
</style>

<span class={color} {...rest}>{render children()}</span>
