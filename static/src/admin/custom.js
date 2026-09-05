document.addEventListener('DOMContentLoaded', function() {
    console.log("Loader setup");
    var adminForms = document.querySelectorAll('#changelist-form, #repeat-action-form, form.with-loader');
    adminForms.forEach((adminForm) => {
        console.log("adminForm", adminForm);
        if (adminForm) {
            console.log('Add event listener');
            adminForm.addEventListener('submit', function() {
                console.log('Submit admin form', adminForm);
                loader = document.getElementById('loader');
                console.log("loader", loader);
                loader.classList.add('fade-in');
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Find all table rows in the admin changelist
    const rows = document.querySelectorAll('tbody tr');

    console.log('rows', rows);

    rows.forEach((row) => {
        row.addEventListener('click', (event) => {
            // Prevent toggling the checkbox if a link is clicked
            if (
                event.target.type === 'checkbox' || // Ignore clicks on checkboxes
                event.target.tagName === 'A' // Ignore clicks on links      ID 
            ) {
                return;
            }

            // Find the checkbox in the row
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.checked = !checkbox.checked; // Toggle checkbox state
            }
        });
    });
});

function submitCompanyForm() {
    const form = document.getElementById('company-select-form');
    const selectedResult = document.querySelector('input[name="selected_result"]:checked');
    const errorMessage = document.getElementById('custom-error-message');

    if (!selectedResult) {
        errorMessage.style.display = 'block';
        event.preventDefault(); // Prevent form submission if there's an error
        return false;
    } else {
        errorMessage.style.display = 'none';
    }

    return true;
}
