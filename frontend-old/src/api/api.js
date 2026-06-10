import { personStore as person, processesStore as processes, authLoading } from '@stores';

// TODO: Take key from window.config
const siteKey = '6Le_CikqAAAAAN0mZ33jMr1aAVuTZO4UaZ7ApoJi';

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

//TODO: Remove debugging
//window.abortControllers = abortControllers;

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
      result = { ...result, error: data ?? response };
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
    //console.log(`AbortController for "${abortKey}" cleaned up.`);
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
    } else {
      //console.warn(`cancelRequest: No active request found for abortKey "${abortKey}".`);
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
    //console.log(`Request for abortKey "${abortKey}" was canceled.`);
  }
  abortControllers.clear(); // Clear all keys
  //console.log('All requests have been canceled.');
}

// Add global event listeners for page unload/navigation
function addGlobalEventListeners() {
  const handlePageUnload = () => {
    //console.log('Page is unloading. Canceling all requests.');
    cancelAll();
  };

  const handlePageHide = () => {
    //console.log('Page is hiding. Canceling all requests.');
    cancelAll();
  };

  window.addEventListener('beforeunload', handlePageUnload);
  window.addEventListener('pagehide', handlePageHide);

  //console.log('Global event listeners added for request cleanup.');
}

// Ensure listeners are added once when the module is loaded
addGlobalEventListeners();



export async function searchDegrees(searchString, country = '') {
  const encodedSearchString = '?name=' + encodeURIComponent(searchString);
  const encodeCountryString = country ? '&country=' + encodeURIComponent(country.toUpperCase()) : '';
  return apiRequest(`${window.config.apiBaseUrl}/degrees/${encodedSearchString}${encodeCountryString}`);
}

export async function searchInstitutions(searchString, country = '') {
  const encodedSearchString = '?name=' + encodeURIComponent(searchString);
  const encodeCountryString = country ? '&country=' + encodeURIComponent(country.toUpperCase()) : '';
  return apiRequest(`${window.config.apiBaseUrl}/institutions/${encodedSearchString}${encodeCountryString}`);
}

async function clearAuth() {
  person.set(null);
}

export async function signOut() {
  const response = await apiRequest(`${window.config.apiBaseUrl}/signout`);
  if (response.success) await clearAuth();
  return response.success;
}

export async function signIn(token) {
  if (!token) {
    console.error('No token provided');
    return false;
  }

  authLoading.set('api_loading');
  const response = await apiRequest(`${window.config.apiBaseUrl}/token-login2/?token=${token}`);

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
  const cachedAuthStatus = localStorage.getItem('authStatus');
  const cachedAuthTime = localStorage.getItem('authStatusTime');

  console.log('checkAuthStatus()');

  /*
  if (cachedAuthStatus && cachedAuthTime) {
    const now = new Date().getTime();
    const lastChecked = parseInt(cachedAuthTime, 10);
    if (now - lastChecked < 5 * 60 * 1000) {
      return cachedAuthStatus === 'true';
    }
  }
  */

  if (!person) {
    console.log('No person, nothing to check');
    return false;
  } else {
    console.log('Person found, checking');
  }

  const response = await apiRequest(`${window.config.apiBaseUrl}/ping/`, {}, checkAuthStatus);

  if (response.error?.name === 'AbortError') {
    console.warn('Auth ping request was aborted, keeping stale auth.');
    // Treat abort as a neutral state
    return false;
  }

  const isAuthenticated = response.success && response.data.detail === "Authenticated";

  console.log('Auth ping response: ', isAuthenticated);

  if (isAuthenticated) {
    localStorage.setItem('authStatus', 'true');
    localStorage.setItem('authStatusTime', new Date().getTime().toString());
    // TODO: How to check for person?
    //fetchUserInfo();
  } else {
    await clearAuth();
    localStorage.setItem('authStatus', 'false');
    localStorage.setItem('authStatusTime', new Date().getTime().toString());
  }

  return isAuthenticated;
}

export async function patchPerson(payload) {
  const response = await apiRequest(`${window.config.apiBaseUrl}/person/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (response.success) {
    person.set(response.data);
  }
  return response;
}

export async function fetchUserInfo() {
  const response = await apiRequest(`${window.config.apiBaseUrl}/person/`);
  if (response.success) {
    //console.log('Update person: ', person);
    person.set(response.data);
  } else {
    await clearAuth();
  }
  authLoading.set('api_loaded');
  return response.success;
}

//New function name using `method` and `object`
export const getPerson = fetchUserInfo;

export async function fetchPersonDocuments(personId, documentId) {
  let url = `${window.config.apiBaseUrl}/person/${personId}/documents`;
  if (documentId) {
    url += `/${documentId}`;
  }

  const response = await apiRequest(url);

  if (response.success) {
    person.update((current) => {
      // Ensure documents is a map with document IDs as keys
      let documents = current.documents || {};

      if (Array.isArray(documents)) {
        // Convert array to a map if it's not already
        documents = Object.fromEntries(documents.map((p) => [p.id, p]));
      }

      // Update or add the specific document if documentId is provided
      if (documentId) {
        if (response.data.length == 0) {
          console.warn('Document does not exist: ', documentId);
          delete documents[documentId];
        } else {
          documents[documentId] = response.data[0];
        }
        //console.log('UPDATE PERSON DOCUMENT ', documentId, documents[documentId]);
      } else {
        // Replace all documents if no specific documentId
        documents = Object.fromEntries(response.data.map((p) => [p.id, p]));
      }

      return { ...current, documents };
    });
  }

  return response; // Now returns { success, data, error }
}

export async function fetchPersonProcesses(personId, processId) {
  let url = `${window.config.apiBaseUrl}/person/${personId}/processes/`;
  if (processId) {
    url += `${processId}`;
  }

  const response = await apiRequest(url, {}, fetchPersonProcesses);

  if (response.success) {
    processes.update((current) => {
      // Ensure processes is a map with process IDs as keys
      if (current == null) {
        current = {};
      }

      //if (Array.isArray(processes)) {
        // Convert array to a map if it's not already
        //processes = Object.fromEntries(processes.map((p) => [p.id, p]));
      //}

      // Update or add the specific process if processId is provided
      if (processId) {
        current[processId] = response.data[0];
        return current;
      }
      // Replace all processes if no specific processId
      return Object.fromEntries(response.data.map((p) => [p.id, p]));
    });
  }

  return response; // Now returns { success, data, error }
}

export async function anabinAiSearch() {
  return apiRequest(`${window.config.apiBaseUrl}/anabin-ai-search/`, {
    method: 'POST',
  });
}

export async function uploadFile(file, onProgress) {
  const url = `${window.config.apiBaseUrl}/upload/`;

  const formData = new FormData();
  formData.append("file", file);

  const xhr = new XMLHttpRequest();
  const total = file.size;

  return new Promise((resolve) => {
    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        onProgress(event.loaded, total);
      }
    });

    xhr.open('POST', url, true);
    xhr.withCredentials = true;

    const csrfToken = getCookie('csrftoken');
    if (csrfToken) xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve({ success: true, data: JSON.parse(xhr.responseText), error: null });
        } else {
          resolve({ success: false, data: null, error: xhr?.error || 'File upload failed' });
        }
      }
    };

    xhr.send(formData);
  });
}

export async function submitProcessTask(processId, taskSlug, data = {}, files = [], onProgress) {
  const url = `${window.config.apiBaseUrl}/person/process/${processId}/task/${taskSlug}/?return=process`;

  console.log('submitProcessTask: ', url);

  const formData = new FormData();

  // Append each data field (assuming data is an object with key-value pairs)
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      formData.append(key, data[key]);
    }
  }

  // Append each file under the same key 'files' for backend to handle as an array
  files.forEach((file) => {
    formData.append('files', file); // Use the same key name for all files
  });

  const xhr = new XMLHttpRequest();

  return new Promise((resolve) => {
    // Monitor upload progress
    xhr.upload.addEventListener('progress', (event) => {
      //console.log('progress event', event);
      if (event.lengthComputable && onProgress) {
        onProgress(event.loaded, event.total);
      }
    });

    xhr.open('POST', url, true);
    xhr.withCredentials = true;

    // Set CSRF token if available
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
    }

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        console.log('XHR done: ', xhr)
        let response;
        try {
          response = JSON.parse(xhr.responseText);
        } catch (error) {
          response = {}
        };
        console.log('XHR response: ', response)
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve({ success: true, data: response, error: null });
        } else {
          resolve({ success: false, data: null, error: response?.error || 'Request failed' });
        }
      }
    };

    xhr.send(formData);
  });
}







//TODO: extract common parts when submitting a form

export async function submitContactForm({ name, email, message }) {
  const recaptchaToken = await grecaptcha.execute(siteKey, { action: 'contact_form/submit' });
  const payload = { name, email, message, recaptcha: recaptchaToken };

  const response = await apiRequest(`${window.config.apiBaseUrl}/contact/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return response.success ? response.data : { error: response?.error || 'Request failed' };
}

export async function submitSigninForm({ email }) {
  const recaptchaToken = await grecaptcha.execute(siteKey, { action: 'signin_form/submit' });
  const payload = { email, recaptcha: recaptchaToken };

  const response = await apiRequest(`${window.config.apiBaseUrl}/signin-request/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return response.success ? response.data : { error: response?.error || 'Request failed'  };
}

export async function submitTermsForm(agree) {
  const recaptchaToken = await grecaptcha.execute(siteKey, { action: 'terms_form/submit' });
  const payload = { accept: agree, recaptcha: recaptchaToken };

  const response = await apiRequest(`${window.config.apiBaseUrl}/accept-terms/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return response.success ? response.data : { error: response?.error  || 'Request failed' };
}

export async function submitGenAIChat(chatType, message) {
  //const recaptchaToken = await grecaptcha.execute(siteKey, { action: 'terms_form/submit' });
  //const payload = { accept: agree, recaptcha: recaptchaToken };
  const payload = { message: message };

  return apiRequest(`${window.config.apiBaseUrl}/chat/${chatType}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
