<script>
  export let icon;
  export let width = "24"; // Default width
  export let height = "24"; // Default height
  export let className = ""; // Default class
  export let fill = "currentColor"; // Default fill color

  let svgContent = '';

  // Dynamically import the SVG as raw text
  let imported = import(`../assets/icons/${icon}.svg?raw`)
    .then((module) => {
      svgContent = module.default;

      // Modify the SVG to include the passed attributes
      svgContent = svgContent
        .replace(/<svg/, `<svg width="${width}" height="${height}" class="${className}" fill="${fill}"`);
    });
</script>

{@html svgContent}
