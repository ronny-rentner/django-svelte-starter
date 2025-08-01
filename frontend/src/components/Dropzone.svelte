<script>
import Dropzone from 'svelte-file-dropzone';
import { Icon } from '@components';
import icon from '@icons/ph/upload-duotone';

let { children, ondrop, accept="image/jpeg, image/png, application/pdf", ...rest } = $props();
</script>

<style>
Dropzone {
  width: fit-content;
  background-color: var(--pico-dropzone-background-color);
  border: calc(var(--pico-border-width) * 2) dashed var(--pico-h4-color);
  border-radius: calc(var(--pico-border-radius) * 2);

  margin-bottom: 1rem;
  padding: calc(var(--pico-form-element-spacing-vertical) * 3) calc(var(--pico-form-element-spacing-horizontal) * 3);

  &:hover, &:focus {
    background-color: var(--pico-dropzone-background-hover-color);
    border-color: var(--pico-primary-hover);

    div {
      color: var(--pico-primary-hover);
    }
  }

  div {
    font-size: 110%;
    line-height: 125%;
    color: var(--pico-h4-color);
    text-align: left;

    Icon {
      margin-right: 1rem;
    }

    /*
    small {
      display: block;
      line-height: 125%;
      margin-top: var(--pico-typography-spacing-vertical);

      & + small {
        margin-top: calc(var(--pico-typography-spacing-vertical) * 0.75);
      }
    }
     */
  }
}
</style>

<Dropzone on:drop={ondrop} {accept} {...rest}>
  <div>
    <Icon {icon} size="3rem">{render children()}</Icon>
  </div>
</Dropzone>
