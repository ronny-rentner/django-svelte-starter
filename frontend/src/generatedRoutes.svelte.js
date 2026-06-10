export const routes = {
  "*": () => import('.//pages/404.svelte'),
  "/about": () => import('.//pages/About.svelte'),
  "/": () => import('.//pages/Home.svelte'),
  "/pricing": () => import('.//pages/Pricing.svelte')
};
