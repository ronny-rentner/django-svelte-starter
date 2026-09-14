export const routes = {
  "*": () => import('.//pages/404.svelte'),
  "/about": () => import('.//pages/About.svelte'),
  "/faq": () => import('.//pages/FAQ.svelte'),
  "/guide": () => import('.//pages/Guide.svelte'),
  "/": () => import('.//pages/Home.svelte'),
  "/imprint": () => import('.//pages/Imprint.svelte'),
  "/landing": () => import('.//pages/Landing.svelte'),
  "/privacy": () => import('.//pages/Privacy.svelte'),
  "/signin": () => import('.//pages/Signin.svelte'),
  "/terms": () => import('.//pages/Terms.svelte')
};
