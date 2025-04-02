

// The navigation menu 
document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.dropdown');
    var dropdownContent = document.querySelector('.dropdown-content');

    dropdown.addEventListener('mouseover', function() {
        dropdownContent.style.display = 'block';
    });

    dropdown.addEventListener('mouseout', function() {
        dropdownContent.style.display = 'none';
    });
});

//End the navigation menu 

document.addEventListener('DOMContentLoaded', () => {
    // Utility function to toggle element display
    function toggleDisplay(element, displayStyle) {
        if (element) {
            element.style.display = displayStyle;
        }
    }

    // Toggle navigation menu visibility on mobile
    const menuBtn = document.getElementById('menu-btn');
    const nav = document.querySelector('nav');
    if (menuBtn && nav) {
        menuBtn.addEventListener('click', () => {
            nav.classList.toggle('show');
        });
    }

    // Function to open a modal
function showModal(modalId) {
    document.getElementById(modalId).setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Prevents scrolling when modal is open
}

// Function to close a modal
function closeModal(modalId) {
    document.getElementById(modalId).setAttribute('aria-hidden', 'true');
    document.body.style.overflow = 'auto'; // Restores scrolling when modal is closed
}

// Function to toggle password visibility
function togglePasswordVisibility(passwordId) {
    const passwordField = document.getElementById(passwordId);
    const showPasswordCheckbox = document.getElementById('show-login-password');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        showPasswordCheckbox.checked = true;
    } else {
        passwordField.type = 'password';
        showPasswordCheckbox.checked = false;
    }
}

// Function to toggle display of elements
function toggleDisplay(element, displayStyle) {
    if (element) {
        element.style.display = displayStyle;
    }
}

// Handle form visibility toggling
const authBtn = document.getElementById('auth-btn');
const loginFormContainer = document.getElementById('login-form-container');
const signupFormContainer = document.getElementById('signup-form-container');
const passwordResetRequestContainer = document.getElementById('password-reset-request-container');

if (authBtn && loginFormContainer) {
    authBtn.addEventListener('click', () => {
        toggleDisplay(loginFormContainer, 'flex');
    });
}

// Close login modal
const closeLoginFormBtn = document.getElementById('close-login-form');
if (closeLoginFormBtn) {
    closeLoginFormBtn.addEventListener('click', () => {
        toggleDisplay(loginFormContainer, 'none');
    });
}

// Switch to signup form
const switchToSignupBtn = document.getElementById('switch-to-signup');
if (switchToSignupBtn) {
    switchToSignupBtn.addEventListener('click', () => {
        toggleDisplay(loginFormContainer, 'none');
        toggleDisplay(signupFormContainer, 'flex');
    });
}

// Close signup modal
const closeSignupFormBtn = document.getElementById('close-signup-form');
if (closeSignupFormBtn) {
    closeSignupFormBtn.addEventListener('click', () => {
        toggleDisplay(signupFormContainer, 'none');
    });
}

// Switch to login form
const switchToLoginBtn = document.getElementById('switch-to-login');
if (switchToLoginBtn) {
    switchToLoginBtn.addEventListener('click', () => {
        toggleDisplay(signupFormContainer, 'none');
        toggleDisplay(loginFormContainer, 'flex');
    });
}

// Handle forgot password flow
const forgotPasswordLink = document.getElementById('forgot-password-link');
if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener('click', () => {
        toggleDisplay(loginFormContainer, 'none');
        toggleDisplay(passwordResetRequestContainer, 'flex');
    });
}

// Back to login from reset request
const backToLoginBtn = document.getElementById('back-to-login');
if (backToLoginBtn) {
    backToLoginBtn.addEventListener('click', () => {
        toggleDisplay(passwordResetRequestContainer, 'none');
        toggleDisplay(loginFormContainer, 'flex');
    });
}

// Close password reset request modal
const closePasswordResetRequestBtn = document.getElementById('close-password-reset-request');
if (closePasswordResetRequestBtn) {
    closePasswordResetRequestBtn.addEventListener('click', () => {
        toggleDisplay(passwordResetRequestContainer, 'none');
    });
}

// Toggle password visibility
function togglePasswordVisibility() {
    const loginPassword = document.getElementById('password');
    const signupPassword = document.getElementById('signup-password');
    const confirmSignupPassword = document.getElementById('signup-confirm-password');
    const showLoginPassword = document.getElementById('show-login-password');
    const showSignupPasswords = document.getElementById('show-signup-passwords');

    if (loginPassword && showLoginPassword) {
        loginPassword.type = showLoginPassword.checked ? 'text' : 'password';
    }

    if (signupPassword && confirmSignupPassword && showSignupPasswords) {
        const type = showSignupPasswords.checked ? 'text' : 'password';
        signupPassword.type = type;
        confirmSignupPassword.type = type;
    }
}

// Event listeners for password visibility toggles
const showLoginPassword = document.getElementById('show-login-password');
const showSignupPasswords = document.getElementById('show-signup-passwords');
if (showLoginPassword) {
    showLoginPassword.addEventListener('change', togglePasswordVisibility);
}
if (showSignupPasswords) {
    showSignupPasswords.addEventListener('change', togglePasswordVisibility);
}

// Validate password reset form
function validatePasswordResetForm() {
    const newPassword = document.getElementById('new-password').value;
    const confirmNewPassword = document.getElementById('confirm-new-password').value;
    const resetErrorMessage = document.getElementById('reset-error-message');

    if (newPassword !== confirmNewPassword) {
        resetErrorMessage.textContent = 'Passwords do not match!';
        return false;
    }

    resetErrorMessage.textContent = ''; // Clear error message if passwords match
    return true;
}

const passwordResetForm = document.getElementById('passwordResetForm');
if (passwordResetForm) {
    passwordResetForm.addEventListener('submit', (event) => {
        event.preventDefault();

        if (!validatePasswordResetForm()) {
            return; // Prevent form submission if validation fails
        }

        const email = document.getElementById('reset-email').value;
        const newPassword = document.getElementById('new-password').value;

        fetch('/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, newPassword })
        })
        .then(response => response.json())
        .then(data => {
            resetErrorMessage.textContent = data.error || data.message;
        })
        .catch(() => {
            resetErrorMessage.textContent = 'An error occurred while resetting the password.';
        });
    });
}

// Function to validate the signup form
function validateSignupForm(event) {
    event.preventDefault(); // Prevent form from submitting if validation fails

    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;
    const errorMessage = document.getElementById('error-message');
    const userType = document.querySelector('input[name="user-type"]:checked');

    if (password !== confirmPassword) {
        errorMessage.textContent = 'Passwords do not match!';
        return false;
    }

    if (!userType) {
        errorMessage.textContent = 'Please select a user type.';
        return false;
    }

    errorMessage.textContent = ''; // Clear error message if validation passes

    // Redirect based on user type
    if (userType.value === 'job-seeker') {
        window.location.href = 'job_seeker_profile.html';
    } else if (userType.value === 'employer') {
        window.location.href = 'employer_profile.html';
    } else {
        errorMessage.textContent = 'Unknown user type selected.';
        return false;
    }

    return true;
}

// Attach the validateSignupForm function to the form's submit event
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', validateSignupForm);
}


    // Dropdown functionality
    const jobSearchInput = document.getElementById('job-search');
    const locationInput = document.getElementById('location');
    const jobDropdown = document.getElementById('job-dropdown');
    const locationDropdown = document.getElementById('location-dropdown');

    const hideDropdowns = (event) => {
        if (!jobDropdown.contains(event.target) && event.target !== jobSearchInput) {
            jobDropdown.style.display = 'none';
        }
        if (!locationDropdown.contains(event.target) && event.target !== locationInput) {
            locationDropdown.style.display = 'none';
        }
    };

    jobSearchInput.addEventListener('focus', () => {
        jobDropdown.style.display = 'block';
    });

    locationInput.addEventListener('focus', () => {
        locationDropdown.style.display = 'block';
    });

    document.addEventListener('click', hideDropdowns);

    jobDropdown.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            jobSearchInput.value = event.target.textContent;
            jobDropdown.style.display = 'none';
        }
    });

    locationDropdown.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            locationInput.value = event.target.textContent;
            locationDropdown.style.display = 'none';
        }
    });



    // Tabs functionality
    const buttons = document.querySelectorAll('#trending .tab-button');
    const contents = document.querySelectorAll('#trending .tab-content');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');

            // Hide all contents
            contents.forEach(content => {
                content.style.display = 'none';
            });

            // Show the selected content
            const selectedContent = document.getElementById(`trending-${tabId}`);
            if (selectedContent) {
                selectedContent.style.display = 'block';
            }

            // Remove 'active' class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));

            // Add 'active' class to the clicked button
            button.classList.add('active');
        });
    });

    // Show the first tab by default
    if (buttons.length > 0) {
        buttons[0].click();
    }
});

		
		// Function to toggle the display of the trending dropdown
function toggleTrendingDropdown() {
    var container = document.getElementById('trending-container');
    if (container.style.display === 'none' || container.style.display === '') {
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}

// Function to show the specific content based on the button clicked
function showTrendingContent(tabName) {
    var tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(function(tab) {
        tab.style.display = 'none';
    });
    
    var activeTab = document.getElementById('trending-' + tabName);
    if (activeTab) {
        activeTab.style.display = 'block';
    } else {
        console.error('Tab content not found');
    }
}


        function updateProfile() {
            alert("Redirecting to profile update page...");
        }

        function searchJobs() {
            alert("Searching for jobs based on your criteria...");
        }

        function viewAllApplications() {
            alert("Viewing all your job applications...");
        }

        function uploadResume() {
            alert("Opening resume upload dialog...");
        }

        function createCoverLetter() {
            alert("Opening cover letter creation tool...");
        }

        function takeSkillsAssessment() {
            alert("Redirecting to skills assessment page...");
        }

        function manageJobAlerts() {
            alert("Opening job alerts management page...");
        }

        function prepareForInterview() {
            alert("Loading interview preparation resources...");
        }

        function expandNetwork() {
            alert("Showing networking opportunities...");
        }

        function showModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        function togglePasswordVisibility(passwordId) {
            var passwordField = document.getElementById(passwordId);
            var showPasswordCheckbox = document.getElementById('show-login-password');
            if (showPasswordCheckbox.checked) {
                passwordField.type = 'text';
            } else {
                passwordField.type = 'password';
            }
        }

        function createProfile() {
            alert("Create Profile functionality not implemented yet.");
        }
        
        function updateProfile() {
            alert("Update Profile functionality not implemented yet.");
        }
        
        function uploadResume() {
            const fileInput = document.getElementById('resumeUpload');
            if (fileInput.files.length === 0) {
                alert("Please select a file to upload.");
            } else {
                alert("Resume uploaded successfully!");
            }
        }
        
		// Team section
document.addEventListener('DOMContentLoaded', function () {
    const members = document.querySelectorAll('.team-slide');
    let currentIndex = 0;

    // Initially show the first member
    members[currentIndex].classList.add('active');

    document.getElementById('next-btn').addEventListener('click', function () {
        // Hide current member
        members[currentIndex].classList.remove('active');
        
        // Move to next member (loop back if at the last member)
        currentIndex = (currentIndex + 1) % members.length;
        
        // Show the next member
        members[currentIndex].classList.add('active');
    });

    document.getElementById('prev-btn').addEventListener('click', function () {
        // Hide current member
        members[currentIndex].classList.remove('active');
        
        // Move to the previous member (loop back if at the first member)
        currentIndex = (currentIndex - 1 + members.length) % members.length;
        
        // Show the previous member
        members[currentIndex].classList.add('active');
    });
});

// Message section //
function handleSubmit(event) {
    event.preventDefault(); // Prevent actual form submission for now (you can remove this if you're doing actual submission)

    // Simulate form submission (replace with actual form submission logic if needed)
    setTimeout(() => {
        // Get the success message div
        const successMessage = document.getElementById('successMessage');

        // Set the success message text and style
        successMessage.textContent = 'Thank you! One of our team members will be in touch with you within 24 hours.';
        successMessage.style.display = 'block';  // Make sure it's visible
        successMessage.style.color = '#28a745';  // Green color
        successMessage.style.backgroundColor = '#d4edda';  // Light green background
        successMessage.style.padding = '10px';
        successMessage.style.marginTop = '20px';
        successMessage.style.borderRadius = '5px';
        successMessage.style.border = '1px solid #c3e6cb';

        // Clear the form fields
        document.getElementById('contactForm').reset();
    }, 500); // Simulate a short delay
}

async function createProfile() {
    const form = document.getElementById('profileForm');
    const formData = new FormData(form);

    try {
        const response = await fetch('http://localhost:3000/api/profile', {
            method: 'POST',
            headers: {
                'x-auth-token': localStorage.getItem('token') // Assuming you store the JWT token in localStorage
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to create profile');
        }

        const data = await response.json();
        console.log('Profile created:', data);
        // Update UI to show success message or redirect to profile page
    } catch (error) {
        console.error('Error creating profile:', error);
        // Update UI to show error message
    }
}

// Jobseeker-dashboard funalities section 

const jobListings = [
  { id: 1, title: "Software Engineer", company: "Tech Co", description: "Exciting opportunity for a skilled developer..." },
  { id: 2, title: "Data Analyst", company: "Data Corp", description: "Looking for a data enthusiast to join our team..." }
];

const notifications = [
  { id: 1, message: "Your application for Software Engineer at Tech Co has been viewed", date: "2024-09-09" }
];

const announcements = [
  { id: 1, title: "New Feature: AI-powered Resume Builder", content: "We've just launched a new AI-powered resume builder to help you create standout resumes!", date: "2024-09-10" }
];

// Function to switch between tabs
function openTab(evt, tabName) {
  const tabcontents = document.getElementsByClassName("tabcontent");
  for (let i = 0; i < tabcontents.length; i++) {
    tabcontents[i].style.display = "none";
  }

  const tablinks = document.getElementsByClassName("tablinks");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Automatically open the first tab on page load
document.getElementById("defaultOpen").click();

// Inject job listings
const jobListingsContainer = document.getElementById('jobListings');
jobListings.forEach(job => {
  const jobCard = document.createElement('div');
  jobCard.classList.add('job-card');
  jobCard.innerHTML = `
    <h4>${job.title}</h4>
    <p>${job.company}</p>
    <p>${job.description}</p>
    <button onclick="applyForJob(${job.id})">Apply</button>
  `;
  jobListingsContainer.appendChild(jobCard);
});

// Apply for a job
function applyForJob(jobId) {
  alert(`You have applied for job ID: ${jobId}`);
  const today = new Date().toISOString().split('T')[0];
  const newNotification = { id: Date.now(), message: `You've successfully applied for job ${jobId}`, date: today };
  notifications.push(newNotification);
  loadNotifications();
}

// Inject announcements
const announcementsContainer = document.getElementById('announcementsList');
announcements.forEach(announcement => {
  const announcementCard = document.createElement('div');
  announcementCard.innerHTML = `
    <h4>${announcement.title}</h4>
    <p>${announcement.date}</p>
    <p>${announcement.content}</p>
  `;
  announcementsContainer.appendChild(announcementCard);
});

// Load notifications
function loadNotifications() {
  const notificationsContainer = document.getElementById('notificationsList');
  notificationsContainer.innerHTML = "";
  notifications.forEach(notification => {
    const notificationItem = document.createElement('div');
    notificationItem.innerHTML = `
      <p>${notification.message}</p>
      <p class="text-sm">${notification.date}</p>
    `;
    notificationsContainer.appendChild(notificationItem);
  });
}
loadNotifications();

// Handle form submissions
document.getElementById('searchJobsForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const searchTerm = document.getElementById('jobSearchInput').value;
  alert(`Searching for jobs related to: ${searchTerm}`);
});

document.getElementById('createResumeForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const resumeContent = document.getElementById('resumeText').value;
  alert(`Resume created with content: ${resumeContent}`);
});

// Function to fetch jobs from an API or server
    async function loadJobs() {
        try {
            const response = await fetch('/api/jobs'); // Adjust the URL to your back-end endpoint
            const jobs = await response.json();
            
            const jobListDiv = document.getElementById('jobList');
            jobListDiv.innerHTML = ''; // Clear any previous job listings
            
            jobs.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.className = 'job-item';
                
                jobElement.innerHTML = `
                    <h3>${job.title}</h3>
                    <p><strong>Company:</strong> ${job.company}</p>
                    <p><strong>Location:</strong> ${job.location}</p>
                    <p><strong>Description:</strong> ${job.description}</p>
                `;
                
                jobListDiv.appendChild(jobElement);
            });
        } catch (error) {
            console.error('Error fetching jobs:', error);
        }
    }
    
    // Call the function to load jobs when the page loads
    document.addEventListener('DOMContentLoaded', loadJobs);
		
		
		
      
