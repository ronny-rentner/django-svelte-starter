import sveltePreprocess from 'svelte-preprocess';

import transformComponentStyles from './src/lib/preprocessors/component-styles.js';
import classMergePreprocessor   from './src/lib/preprocessors/class-merge.js';
import markdownPreprocessor     from './src/lib/preprocessors/markdown.js';
import syntaxSugar              from './src/lib/preprocessors/syntax-sugar.js';
import attributeTransformer     from './src/lib/preprocessors/attribute-transformer.js';
import printSourceCode          from './src/lib/preprocessors/print.js';

const ignore_warning_codes = [
  'a11y-click-events-have-key-events',
  'a11y-no-static-element-interactions',
  'a11y_invalid_attribute',
  'a11y_no_redundant_roles',
  'a11y_no_noninteractive_element_interactions',
  'a11y_click_events_have_key_events',
  'a11y_role_has_required_aria_props',
  'a11y_no_static_element_interactions',
  'a11y_autofocus',
  'a11y_img_redundant_alt',
  'a11y_consider_explicit_label',
  'a11y_missing_attribute',
  'a11y_no_noninteractive_tabindex',
  'script_context_deprecated',
  'attribute_illegal_colon',
  'element_invalid_self_closing_tag',
  'vite-plugin-svelte-css-no-scopable-elements',
]

let replacements = [
  ['{const ',   '{@const '],
  //Allow multiple constants being defined with one tag
  [/\{@const\s+([^}]+)\s*}/g, (match, content) => content.trim().split(/,\s*/).map(_ => `\{@const ${_}\}`).join(' ')],

  //Allow short-hand tag for writables, e. g. `<Component {$someStore} />` gets transformed
  //                                       to `<Component someStore={$someStore}>`
  [/<([A-Za-z0-9]+)([^>]*?)\sstyle:\{([$A-Za-z0-9_]+)\}([^>]*?)\/?>/g, '<$1$2 style:$3={$3}$4/>'],
  [/<([A-Za-z0-9]+)([^>]*?)\s\{\$([A-Za-z0-9_]+)\}([^>]*?)\/?>/g, '<$1$2 $3={$$$3}$4/>'],
  // Transform `<Component bind:{someVar} />` to `<Component bind:someVar={someVar} />`
  [/<([A-Za-z0-9]+)([^>]*?)\sbind:\{([A-Za-z0-9_]+)\}([^>]*?)\/?>/g, '<$1$2 bind:$3={$3}$4/>'],
  ['{snippet ', '{#snippet '],
  ['{if ',      '{#if '],
  ['{else}',    '{:else}'],
  ['{else ',    '{:else '],
  ['{elif ',    '{:else if '],
  ['{elseif ',  '{:else if '],
  ['{await ',   '{#await '],
  ['{then ',    '{:then '],
  ['{each ',    '{#each '],
  ['{render ',  '{@render '],
  ['{html ',    '{@html '],
  ['{try}',     '{#try}'],
  ['{catch ',   '{:catch '],

  //Remove comments
  [/\/\*[\s\S]*?\*\//gm, ''],

  //Send `undefined` instead of `false` for disabled to omit the attribute
  [/ disabled=\{([^}|]*?)\}/g, ' disabled={$1 || undefined}'],
  [' disabled=false',          ''],
  ['{disabled}',               'disabled={disabled || undefined}'],
  ['{novalidate}',             'novalidate={novalidate || undefined}'],

  ['@media mobile',  '@media (max-width: 768px)'],
  ['@mobile',        '@media (max-width: 768px)'],
  ['@media desktop', '@media (min-width: 769px)'],
  ['@desktop',       '@media (min-width: 769px)'],
  ['@media large',   '@media (min-width: 1536px)'],
  ['@large',         '@media (min-width: 1536px)'],
  ['@dark',          ':root[data-theme="dark"]'],
  ['@light',         ':root[data-theme="light"]'],
];

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: [
    //This needs to come first to restore proper Svelte syntax
    syntaxSugar(replacements),

    markdownPreprocessor({
      path: './src/markdown'
    }),

    attributeTransformer({
      attributes: [
        ['tooltip', 'data-tooltip'],               // Exact match
        ['placement', 'data-placement'],           // Exact match
        //[/!(.*)/, '$1={false}'],                   // Regex match: `!showLogo` → `showLogo={false}`
      ],
      excludeTags: [],
    }),

    transformComponentStyles(),

    classMergePreprocessor(),

    //sveltePreprocess({
      //no effect
      //sourceMap: true,
    //}),

    //printSourceCode('ToggleDarkMode.svelte'),
    //printSourceCode('LoadingOverlay.svelte'),
    //printSourceCode('Router.svelte'),
    //printSourceCode('DocumentPreview.svelte'),
  ],
  compilerOptions: {},
  onwarn: (warning, handler) => {

    if (ignore_warning_codes.includes(warning.code)) {
      return;
    }
    console.log("\n\nWarning: ", warning.code, "\n", warning.frame, "\n");

    handler(warning);
  },
}

