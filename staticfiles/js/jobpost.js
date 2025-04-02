
// delete job modal -----------------------------------
const deleteButtons = document.querySelectorAll('.e-d-jobpost-btn-delete');

// Add event listeners to each delete button
deleteButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        // Prevent default action
        event.preventDefault();

        // Find the corresponding modal overlay in the same table row
        const modalOverlay = button.closest('td').querySelector('.e-d-delete-job-modal-overlay');

        // Display the modal overlay
        if (modalOverlay) {
            modalOverlay.style.display = 'flex'; // Display the modal (using flex to center it)
        }

        // Get the close button inside the modal
        const closeModalButton = modalOverlay.querySelector('.e-d-delete-job-modal-close');

        // Close the modal when clicking on the close button
        closeModalButton.addEventListener('click', () => {
            modalOverlay.style.display = 'none';
        });

        // Close the modal when clicking outside the modal content
        window.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                modalOverlay.style.display = 'none';
            }
        });

        // Handle Cancel button
        const cancelButton = modalOverlay.querySelector('.e-d-delete-job-cancel-btn');
        cancelButton.addEventListener('click', () => {
            modalOverlay.style.display = 'none';
        });
    });
});





// mark application as read---------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    // Get the "Accept" and "Reject" buttons
    const acceptButton = document.getElementById('accept_application_btn');
    const rejectButton = document.getElementById('reject_application_btn');

    // Function to handle button clicks
    function handleButtonClick(button) {
        // Get the application ID and status from the button's data attributes
        const applicationId = button.getAttribute('data-application-id');
        const status = button.getAttribute('data-status');

        // Send the request to the backend to update the application status
        updateApplicationStatus(applicationId, status);
    }

    // Add click event listeners to both buttons
    if (acceptButton) {
        acceptButton.addEventListener('click', function () {
            handleButtonClick(this);
        });
    }

    if (rejectButton) {
        rejectButton.addEventListener('click', function () {
            handleButtonClick(this);
        });
    }

    // Function to send the AJAX request to the backend
    function updateApplicationStatus(applicationId, status) {
        // Create the request object
        const xhr = new XMLHttpRequest();

        // Configure the request
        xhr.open('POST', 'http://127.0.0.1:8000/applications/update-application-status/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Add CSRF token for Django

        // Handle the response from the backend
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log('Application status updated');
                // Optionally, update the UI or notify the user
            }
        };

        // Send the request with application ID and status
        xhr.send(JSON.stringify({
            'application_id': applicationId,
            'status': status
        }));
    }
});