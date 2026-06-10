import { defineConfig, createLogger } from 'vite';

import { svelte } from '@sveltejs/vite-plugin-svelte';
//import { buildInfoPlugin } from './src/lib/buildInfoVitePlugin';
import generateRoutesPlugin from './src/lib/vite/generateRoutes';

import path from 'path';
import fs from 'node:fs';

const logger = createLogger(); // Set to 'info' level for custom log lines

/** BROWSER **/

import browserslistToEsbuild from 'browserslist-to-esbuild';
import browserslist from 'browserslist';
const browserslistQuery = "last 3 versions, not dead, not op_mini all, > 1.0%";
const esbuildTargets = browserslistToEsbuild(browserslistQuery);
// Get the list of browsers matching the query
const browsers = browserslist(browserslistQuery);
// Calculate the global coverage
const coverage = browserslist.coverage(browsers, 'global');
// Print the total coverage
logger.info(`targetBrowsers: ${browserslistQuery}`);
logger.info(`browserCoverage: ${coverage.toFixed(2)}%`);

/** PRODUCTION **/

const isProduction = process.env.NODE_ENV === 'production';

logger.info(`isProduction: ${isProduction}`);

let devConfig = {}

if (!isProduction) {
  devConfig = {
    css: {
      devSourcemap: true,
    },
    server: {
      origin: 'http://localhost:5173',
      //no effect
      sourcemap: true,
    },
    build: {
      //no effect
      sourcemap: true,
    }
  }
}

/** SOURCE MAPS **/

function fixSourceMaps () {
  let currentInterval = null
  return {
    name: 'fix-source-map',
    enforce: 'post',
    transform: function (source) {
      if (currentInterval) {
        return;
      }
      currentInterval = setInterval(function () {
        const nodeModulesPath = path.join(__dirname, 'node_modules', '.vite', 'deps');
        if (fs.existsSync(nodeModulesPath)) {
          clearInterval(currentInterval);
          currentInterval = null;
          const files = fs.readdirSync(nodeModulesPath);
          files.forEach(function (file) {
            const mapFile = file + '.map';
            const mapPath = path.join(nodeModulesPath, mapFile);
            if (fs.existsSync(mapPath)) {
              let mapData = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
              if (!mapData.sources || mapData.sources.length == 0) {
                mapData.sources = [path.relative(mapPath, path.join(nodeModulesPath, file))];
                fs.writeFileSync(mapPath, JSON.stringify(mapData), 'utf8');
              }
            }
          });
        }
      }, 100);
      return source;
    },
  }
}

/** GENERAL BUILD **/

const config = {
  base: '/static',
  plugins: [
    //Handle *.svelte files, convert them to Javascript
    svelte(),
    generateRoutesPlugin({
      //Special routes that need to be configured manually
      routeRenames: {
        '/home': '/',
        '/404': '*'
      }
    }),
    //buildInfoPlugin(),
    isProduction ? () => {} : fixSourceMaps(),
    //fixSourceMaps(),
  ],
  resolve: {
    alias: {
      '@assets': path.resolve(__dirname, 'src/assets'),
      '@icons':  '@iconify-icons',
      '@styles': path.resolve(__dirname, 'src/styles'),
    },
  },
  build: {
    outDir: '../static/frontend',
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: true,
    cssCodeSplit: true,
    cssMinify: true,
    //target: ['chrome112', 'firefox105', 'safari16.4'],
    target: esbuildTargets,
    /*assetsInlineLimit: 4096,*/
    assetsInlineLimit: 0,
    rollupOptions: {
      input: 'src/main.js',
      output: {
        entryFileNames: 'index.js',
        //chunkFileNames: 'chunk.js',
        chunkFileNames: 'chunks/[name].js',
        assetFileNames: 'assets/[name].[ext]',
      },
    }
  },

  ...devConfig
};

export default defineConfig(config);
