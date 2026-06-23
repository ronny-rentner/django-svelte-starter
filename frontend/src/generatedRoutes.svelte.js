export const routes = {
  "*": () => import('.//pages/404.svelte'),
  "/about": () => import('.//pages/About.svelte'),
  "/faq": () => import('.//pages/FAQ.svelte'),
  "/guide": () => import('.//pages/Guide.svelte'),
  "/": () => import('.//pages/Home.svelte'),
  "/landing": () => import('.//pages/Landing.svelte'),
  "/pricing": () => import('.//pages/Pricing.svelte')
};
