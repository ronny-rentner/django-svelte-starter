<script>
    import { onMount } from 'svelte';
    import { apiRequest } from '/src/api/api.js';
    import { personStore as person, authLoading } from '@stores';

    let token;
    let statusMessage = 'Attempting to log in...';

    function getQueryParams() {
        const params = new URLSearchParams(window.location.search);
        return { token: params.get('token') };
    }

    async function login() {
        try {
            authLoading.set('api_loading'); // Set loading to api_loading at the start
            console.log('Attempting login...');
            const response = await fetch(`${window.config.apiBaseUrl}/api/token-login2/?token=${token}`, {
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('session_key', data.session_key);
                localStorage.setItem('session_id', data.session_id);
                statusMessage = 'Login successful. Fetching user information...';
                console.log('Login successful:', data.detail);
                return true;
            } else {
                statusMessage = 'Login failed: ' + data.detail;
                console.error('Login failed:', data.detail);
                return false;
            }
        } catch (error) {
            statusMessage = 'Error during login: ' + error.message;
            console.error('Error during login:', error);
            return false;
        }
    }

    async function fetchUserInfo() {
        try {
            console.log('Fetching user information...');
            const data = await apiRequest(`${window.config.apiBaseUrl}/api/person/`);
            person.set(data); // Update the user store with the fetched data
            localStorage.setItem('person_data', JSON.stringify(data)); // Store person data in localStorage
            statusMessage = `Welcome, ${data.full_name}!`;
            console.log('User information fetched:', data);
        } catch (error) {
            statusMessage = 'Failed to fetch user information: ' + error.message;
            console.error('Failed to fetch user information:', error);
            person.set(null); // Ensure the store is set to null on failure
        } finally {
            authLoading.set('api_loaded'); // Set authLoading to api_loaded once finished
        }
    }

    onMount(() => {
        console.log('Component mounted, extracting token...');
        const queryParams = getQueryParams();
        token = queryParams.token;

        if (token) {
            login().then(success => {
                if (success) {
                    fetchUserInfo();
                } else {
                    localStorage.removeItem('person_data');
                    person.set(null); // Ensure the store is set to null on failure
                    authLoading.set('api_loaded'); // Set authLoading to api_loaded on failure
                }
            });
        } else {
            console.error('Token not found in URL parameters');
            return;
          /*
            statusMessage = 'Token not found in URL parameters';
            person.set(null); // Ensure the store is set to null on failure
            authLoading.set('api_loaded'); // Set authLoading to api_loaded on failure
           */
        }
    });
</script>

<style>
    /* Add your styles here */
</style>

<div>
    <h1>Login Component</h1>
    <p>{statusMessage}</p>
</div>
