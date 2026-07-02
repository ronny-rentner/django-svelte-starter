import { personStore as person, authLoading } from '@kit/stores';
import { executeRecaptcha } from '@kit/recaptcha';

import { get } from 'svelte/store';

// Helper function to get a cookie by name
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Store AbortControllers by endpoint or a hashed key
const abortControllers = new Map();

/**
 * Creates a new AbortController for a given key and add it to the
 * controllers map. Automatically clears existing controllers.
 * @param {string} key - Unique identifier for the request (e.g., URL).
 * @returns {AbortController} - The AbortController for the request.
 */
async function createAbortController(key) {
  if (abortControllers.has(key)) {
    // Retrieve and abort the existing controller
    const oldController = abortControllers.get(key);

    // Abort the old request
    await oldController.abort();

    // Explicitly clean up to avoid any delay in removing the old controller
    await abortControllers.delete(key);
    console.warn('Aborting still running previous request: ', key);
  }

  // Create a new controller and add it to the map
  const controller = new AbortController();
  abortControllers.set(key, controller);

  return controller;
}

/**
 * Makes an API request with optional AbortController integration.
 * @param {string} endpoint - The URL for the request.
 * @param {object} options - Fetch options.
 * @returns {Promise<object>} - Result of the API call.
 */
export async function apiRequest(endpoint, options = {}, key = null) {
  // Derive the abort key from the function name or fallback to endpoint
  const abortKey = key?.name || key || endpoint;

  const controller = await createAbortController(abortKey); // Use the derived abort key
  options.signal = controller.signal; // Attach the signal to the fetch options

  if (!options.headers) options.headers = {};

  // Set CSRF Token Header for relevant methods
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(options.method?.toUpperCase())) {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      options.headers['X-CSRFToken'] = csrfToken;
    }
  }
  options.credentials = 'include';

  let response;
  let result = { success: false, data: null, error: null, endpoint };

  try {
    console.log('API request initiated:', { endpoint, options, abortKey });
    response = await fetch(endpoint, options);
    const data = await response.json();
    if (response.ok) {
      result = { ...result, success: true, data };
    } else {
      result = { ...result, error: data?.error ?? data ?? response };
    }
  } catch (error) {
    result = { ...result, error };
    if (error.name === 'AbortError') {
      console.warn('API request was aborted for abortKey:', abortKey);
    } else {
      console.error('API request had an error:', abortKey, error);
    }
  } finally {
    // Cleanup abort controller after request finishes
    abortControllers.delete(abortKey);
  }

  console[result.success ? 'log' : 'error']('API Response:', result);

  return result;
}

/**
 * Cancels an API request by its key.
 * If no key is provided, cancels all ongoing requests.
 * @param {string} key - Unique identifier for the request (e.g., URL).
 */
export function cancelRequest(key = null) {
  if (key) {
    // Derive the abortKey consistently
    const abortKey = key.name || key;

    if (abortControllers.has(abortKey)) {
      abortControllers.get(abortKey).abort();
      abortControllers.delete(abortKey); // Cleanup
      console.log(`Request for abortKey "${abortKey}" was canceled.`);
    }
  } else {
    // Cancel all requests if no key is provided
    cancelAll();
  }
}

/**
 * Cancels all ongoing requests and clears the abortControllers map.
 */
export function cancelAll() {
  for (const [abortKey, controller] of abortControllers.entries()) {
    controller.abort();
  }
  abortControllers.clear(); // Clear all keys
}

// Add global event listeners for page unload/navigation
function addGlobalEventListeners() {
  const handlePageUnload = () => {
    cancelAll();
  };

  const handlePageHide = () => {
    cancelAll();
  };

  window.addEventListener('beforeunload', handlePageUnload);
  window.addEventListener('pagehide', handlePageHide);
}

// Ensure listeners are added once when the module is loaded
addGlobalEventListeners();

async function clearAuth() {
  person.set(null);
}

export async function signOut() {
  const response = await apiRequest(`${window.config.apiBaseUrl}/signout/`);
  if (response.success) await clearAuth();
  return response.success;
}

export async function signIn(token) {
  if (!token) {
    console.error('No token provided');
    return false;
  }

  authLoading.set('api_loading');

  cancelRequest(checkAuthStatus);

  const response = await apiRequest(`${window.config.apiBaseUrl}/token-login/?token=${token}`);

  if (response.success) {
    const { session_key, session_id } = response.data;
    localStorage.setItem('session_key', session_key);
    localStorage.setItem('session_id', session_id);
  } else {
    await clearAuth();
  }

  authLoading.set('api_loaded');
  return response.success;
}

export async function checkAuthStatus() {
  if (!get(person)) {
    //console.log('No person, nothing to check');
    return false;
  }
  console.log('Checking auth status: ', get(person));

  const response = await apiRequest(`${window.config.apiBaseUrl}/ping/`, {}, checkAuthStatus);

  if (response.error?.name === 'AbortError') {
    // Treat abort as a neutral state
    return false;
  }

  const isAuthenticated = response.success && response.data.detail === "Authenticated";

  console.log('Auth ping response: ', isAuthenticated);

  if (isAuthenticated) {
    localStorage.setItem('authStatus', 'true');
    localStorage.setItem('authStatusTime', new Date().getTime().toString());
  } else {
    await clearAuth();
    localStorage.setItem('authStatus', 'false');
    localStorage.setItem('authStatusTime', new Date().getTime().toString());
  }

  return isAuthenticated;
}

export async function fetchUserInfo() {
  const response = await apiRequest(`${window.config.apiBaseUrl}/person/`);
  if (response.success) {
    person.set(response.data);
  } else {
    await clearAuth();
  }
  authLoading.set('api_loaded');
  return response.success;
}

export const getPerson = fetchUserInfo;

export async function submitSigninForm({ email }) {
  const recaptchaToken = await executeRecaptcha('signin_request/submit');
  const payload = { email, recaptcha: recaptchaToken };

  return await apiRequest(`${window.config.apiBaseUrl}/signin-request/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}

export async function submitContactForm({ name, email, message }) {
  const recaptchaToken = await executeRecaptcha('contact_form/submit');
  const payload = { name, email, message, recaptcha: recaptchaToken };

  return await apiRequest(`${window.config.apiBaseUrl}/contact/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
