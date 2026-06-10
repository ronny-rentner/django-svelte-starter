//
// Main entry point of the Relonee web application
//

//This is not logged first as modules imported later in the code will actually run earlier
//console.log('main.js');

//We ensure that either data-theme=dark or data-theme=light is set.
/*
if (window.config.darkMode) {
  document.documentElement.setAttribute('data-theme', 'dark');
} else {
  document.documentElement.setAttribute('data-theme', 'light');
}
*/

// Set the apiBaseUrl if it hasn't been set before
if (!window.config.apiBaseUrl) {
  window.config.apiBaseUrl = 'http://localhost:8000/api';
}

if (window.config.dev) {
  console.log('window.config', window.config);
}

import { mount } from 'svelte';
import App from './App.svelte';

import '@picocss/pico/css/pico.pink.min.css';
import './styles/app.css';

const app = mount(App, { target: document.getElementById('app') });
export default app
