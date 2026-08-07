import { personStore as person, authLoading } from '@kit/stores';
import { apiRequest, cancelRequest, executeRecaptcha } from '@kit/api';

import { get } from 'svelte/store';

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
