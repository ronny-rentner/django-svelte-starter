// TODO: There's also stores.js and I am not sue which one is better to go forward
//       and if we should replace/migrate
// Function to create a synchronized store with localStorage
export function createLocalStorageStore(key, initialValue, updateFromLocalStorage = true) {
  // Initialize the store with the value from localStorage or the provided initialValue
  let storedValue = localStorage.getItem(key);
  let store = $state(storedValue ? JSON.parse(storedValue) : initialValue);

  // Sync the store's value with localStorage whenever it changes
  $effect(() => {
    const currentValue = JSON.parse(localStorage.getItem(key));
    if (currentValue != store) {
      localStorage.setItem(key, JSON.stringify(store));
      //console.log('STORE effect', key, $state.snapshot(store));
    }
  });

  // Set up a listener for external localStorage changes (e.g., another tab updates it)
  window.addEventListener('storage', (event) => {
    if (event.key === key && event.newValue) {
      const newValue = JSON.parse(event.newValue);
      // Update the store with the new value from localStorage
      if (store != newValue) {
        store = newValue;
      }
    }
  });

  //IMPORTANT: Call the result of this function in the target scope. Otherwise it will not be reactive.
  return () => store;
}
