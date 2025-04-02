


// SCRIPTS TO HANDLE JOB FILTER-----------------------


function handleApplyClick() {
    console.log("Hello World!");

    const m = document.getElementById('login-form-container')
    console.log("Below");
    console.log(m);
    
    
    if (window.isAuthenticated === 'false') {
        console.log("Hello World Note!");
        // Show the login modal

    } else {
        openModal('login-form-container');
        // Proceed with the application process
        console.log('User is authenticated. Proceeding with job application...');
        // Your application logic goes here
    }
}




document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    const form = document.getElementById('job-filter-form');
    if (!form) {
        console.error("Form not found");
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the default way

        console.log("Form submission intercepted");

        // Gather form data
        const formData = new FormData(form);
        const queryString = new URLSearchParams(formData).toString();

        console.log("Form Data Serialized. Query String: ", queryString); // Log the form data

        // Display loading message
        // const jobContainer = document.getElementById('job-container');
        // jobContainer.innerHTML = '<p>Loading jobs...</p>'; // Indicate loading state

        // Fetch jobs from the Django endpoint
        fetch(`http://127.0.0.1:8000/jobpostings/fetch-jobs?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log("Response Status Code: ", response.status); // Log the response status
            if (!response.ok) {
                throw new Error(`Network response was not ok. Status: ${response.status}`);
            }
            return response.json(); // Parse JSON data
        })
        .then(data => {
            console.log("Received Data: ", data); // Log the received data
            displayJobs(data); // Call displayJobs function with received data
        })
        .catch(error => {
            console.error('Fetch error:', error); // Log any errors that occur during fetch
            jobContainer.innerHTML = '<p>Error fetching jobs. Please try again later.</p>'; // Show error message to user
        });
    });

    function displayJobs(data) {
        console.log("Data received:", data); // Log the entire data object
    
        const recentlyPostedJobsContainer = document.getElementById('recently-posted-jobs');
        const filteredJobsContainer = document.getElementById('filtered-jobs');
        const filteredJobContainer = document.getElementById('filtered-job-container');
    
        // Hide recently posted jobs
        recentlyPostedJobsContainer.style.display = 'none';
    
        // Show the filtered jobs section
        filteredJobsContainer.style.display = 'block';
    
        // Clear previous filtered job results
        filteredJobContainer.innerHTML = ''; 
    
        // Check if jobs array exists
        if (!data.jobs || !Array.isArray(data.jobs)) {
            console.error("No jobs array found in data:", data);
            filteredJobContainer.innerHTML = '<p>No jobs found.</p>';
            return;
        }
    
        console.log("Jobs to display:", data.jobs); // Log the jobs array
        
        if (data.jobs.length === 0) {
            filteredJobContainer.innerHTML = '<p>No jobs found.</p>';
            return;
        }

        
        
    
        data.jobs.forEach(job => {
            const jobElement = document.createElement('div');
            console.log(job.company);
            
            jobElement.classList.add('js-job-post');

            const applyUrl = `applications/apply/${job.id}/`; // Make sure this matches your Django URL pattern
            const viewUrl = `jobpostings/view-job-details/${job.id}`; // Adjust this as per your URL patterns
            const logoUrl = `${job.company_logo}`
    
            jobElement.innerHTML = `
                <div class="js-company-info">
                    ${job.company_logo ? `<img src="${logoUrl}" alt="${job.employer_company_name}'s logo" style="width:100px; height:auto;">` : '<p>No logo available.</p>'}
                    <h3><a class="js-company_name" href="#">${job.company_name || job.employer_profile_name}</a></h3>
                    <p class="js-job-poster">Posted by: ${job.employer_name}</p>
                </div>
                <div class="js-job-info">
                    <h3>${job.title}</h3>
                    <p>${job.description}</p>
                    <p><strong>Type:</strong> ${job.job_type}</p>
                    <p><strong>Application Deadline:</strong> ${new Date(job.application_deadline).toLocaleString()}</p>
                    <p class="js-posted-time"><strong>Posted on:</strong> ${new Date(job.posted_date).toLocaleDateString()}</p>
                </div>
                <div class="js-job-buttons">
                <a href="${applyUrl}" class="js-button">Apply</a>
                <a href="${viewUrl}" class="js-button">View</a>
                </div>
            `;
    
            filteredJobContainer.appendChild(jobElement);
        });
    }
});





// LOADING AND ADDING SKILLS---------------
document.addEventListener("DOMContentLoaded", function () {
    console.log("HEEEILLLOOWOWOWOWO")
    console.log("TESTING ONE");

    
















    
    const addSkillButton = document.getElementById("add-skill-button");
    const addSkillForm = document.getElementById("add-skill-form");
    const skillInput = document.getElementById("skill-input");
    const skillTagsContainer = document.querySelector(".skill-tags");

    // Show the input field and hide the add skill button
    addSkillButton.addEventListener("click", function () {
        addSkillForm.style.display = "block";
        addSkillButton.style.display = "none";
    });

    // Handle the skill submission
    addSkillForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const skill = skillInput.value.trim();

        if (!skill) {
            alert("Please enter a skill.");
            return;
        }

        // Send the skill to the server via AJAX
        fetch("/add-skill/", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(), // Get the CSRF token dynamically
            },
            body: `skill=${encodeURIComponent(skill)}`,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to add skill. Please try again.");
                }
                return response.json();
            })
            .then((data) => {
                if (data.message === "Skill added successfully") {
                    // Update the skill tags with the new list of skills
                    updateSkillTags(data.skills);
                    skillInput.value = ""; // Clear the input field

                    // Hide the input field and show the add skill button again
                    addSkillForm.style.display = "none";
                    addSkillButton.style.display = "inline-block";
                } else {
                    alert(data.message);
                }
            })
            .catch((error) => {
                console.error("Error adding skill:", error);
                alert("An error occurred. Please try again later.");
            });
    });

    // Function to update the skill tags on the page
    function updateSkillTags(skills) {
        skillTagsContainer.innerHTML = ""; // Clear existing skill tags
        skills.forEach((skill) => {
            const skillTag = document.createElement("span");
            skillTag.className = "skill-tag";
            skillTag.textContent = skill;
            skillTagsContainer.appendChild(skillTag);
        });
    }

    // Utility function to get the CSRF token from the cookie
    function getCSRFToken() {
        const cookies = document.cookie.split(";");
        for (const cookie of cookies) {
            const [name, value] = cookie.trim().split("=");
            if (name === "csrftoken") {
                return value;
            }
        }
        return null;
    }
});










// DELETE JOB--------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const applicationId = this.getAttribute('data-application-id');
            deleteApplication(applicationId);
        });
    });
});

function deleteApplication(applicationId) {
    const csrftoken = getCookie('csrftoken');  // Assuming you're using Django's CSRF protection

    fetch(`/delete-application/${applicationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,  // Add the CSRF token for security
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the job from the UI
            document.getElementById(`application-${applicationId}`).remove();
            alert("Application deleted successfully.");
        } else {
            alert("Failed to delete application: " + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Helper function to get the CSRF token from cookies
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




































document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent default form submission
    console.log("Form submit event triggered");

    // Get the URL from the data attribute
    var url = this.getAttribute('data-register-url');
    console.log("Register URL:", url);  // Debugging line


    // Create a FormData object to handle form data
    var formData = new FormData(this);

    // Send AJAX request to the server
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })

    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to home page if registration is successful
            window.location.href = data.redirect_url;
        } else {
            // Display error message inside the modal
            var errorElement = document.getElementById('registerError');
            errorElement.innerText = data.error;
            errorElement.style.display = 'block';
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
});















// JavaScript code to handle login form submission via AJAX
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent default form submission
    console.log("TEst")
    // Get the URL from the data attribute
    var url = this.getAttribute('data-login-url');
    console.log(url)
    // Create a FormData object to handle form data
    var formData = new FormData(this);
    console.log(formData)
    // Send AJAX request to the server
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to home page if login is successful
            window.location.href = data.redirect_url;
        } else {
            // Display error message inside the modal
            var errorElement = document.getElementById('loginError');
            errorElement.innerText = data.error;
            errorElement.style.display = 'block';
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
});



function showContent(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.dashboard-content section');
    sections.forEach(section => section.style.display = 'none');

    // Show the selected section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    }

    // Remove active class from all menu items
    const menuItems = document.querySelectorAll('.dashboard-nav-item');
    menuItems.forEach(item => item.classList.remove('active'));

    // Add active class to the clicked menu item
    const activeMenuItem = document.querySelector(`.dashboard-nav-item[onclick="showContent('${sectionId}')"]`);
    if (activeMenuItem) {
        activeMenuItem.classList.add('active');
    }
}



// notifictions script -------------------------------------------------------------------
// Function to fetch notifications from the server
// Fetch notifications from the server
async function getNotifications() {
    try {
        const response = await fetch('http://127.0.0.1:8000/notifications/get-user-notifications');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json(); // Parse the JSON response
        console.log("Notifications:", data); // Log notifications
        displayNotifications(data); // Display notifications
    } catch (error) {
        console.error('Error fetching notifications:', error);
    }
}


// Display notifications on the page
function displayNotifications(data) {
    const notificationContainer = document.getElementById('notification-list');
    notificationContainer.innerHTML = ''; // Clear existing notifications

    const notificationBadge = document.getElementById('notification-badge'); // Update notification badge

    if (data.length > 0) {
        notificationBadge.style.display = 'block';
        notificationBadge.textContent = data.length;

        data.forEach(notification => {
            const notificationElement = document.createElement('div');
            notificationElement.className = 'notification';

            // Determine if this is a team join request or regular job notification
            const jobTitle = notification.job_title || notification.team || 'N/A';
            const from = notification.employer || notification.applicant || notification.requester || 'Unknown';

            // Create notification HTML
            notificationElement.innerHTML = `
                <p><strong>Message:</strong> ${notification.message}</p>
                <p><strong>Job/Team:</strong> ${jobTitle}</p>
                <p><strong>From:</strong> ${from}</p>
                <p><strong>Time:</strong> ${notification.timestamp}</p>
                <p><strong>Read:</strong>
                    <button class="mark-read" data-id="${notification.id}" data-read="${notification.is_read}">
                        ${notification.is_read ? 'Yes' : 'Mark as Read'}
                    </button>
                </p>
            `;
            notificationContainer.appendChild(notificationElement);
        });
    } else {
        notificationContainer.innerHTML = '';
    }
}
// Mark a notification as read

















































// Handle click events on buttons
function handleButtonClicks(event) {
    if (event.target && event.target.classList.contains('mark-read')) {
        const notificationId = event.target.getAttribute('data-id');
        console.log("Mark as Read clicked for notification ID:", notificationId); // Log for debugging
        markAsRead(notificationId);
    }
}

// Handle clicks outside the notification dropdown
function clickOutsideListener(event) {
    const notificationDiv = document.getElementById('notification-dropdown');
    const notificationButton = document.getElementById('notification-button');

    if (!notificationDiv.contains(event.target) && !notificationButton.contains(event.target)) {
        notificationDiv.style.display = 'none'; // Hide the dropdown
        console.log("Clicked outside, dropdown closed.");
    }
}

function toggleNotifications() {
    const notificationDiv = document.getElementById('notification-dropdown');
    notificationDiv.style.display = (notificationDiv.style.display === 'block') ? 'none' : 'block';
}


function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

// Event listeners
document.addEventListener('click', clickOutsideListener);
document.addEventListener('click', handleButtonClicks);

document.getElementById('notification-button').addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent the click from propagating to the document
    toggleNotifications();
});

// Fetch notifications when the page loads
window.onload = getNotifications;

// Display default content on page load
document.addEventListener('DOMContentLoaded', () => {
    showContent('dashboard-home');
});























// Function to mark a notification as read
// Function to mark a notification as read
async function markAsRead(notificationId) {
    try {
        const response = await fetch('http://127.0.0.1:8000/notifications/mark-notifications-read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Adjust if necessary
            },
            body: JSON.stringify({ id: notificationId })
        });

        const result = await response.json(); // Try to get the full JSON response

        // Log the response for debugging
        console.log("Response from server:", result);

        if (!response.ok) {
            throw new Error('Failed to mark notification as read');
        }

        if (result.status === 'success') {
            // Refresh notifications and update the badge count
            getNotifications();
            document.getElementById('notification-badge').style.display = 'None';

            // Hide the notification dropdown
            const notificationDiv = document.getElementById('notification-dropdown');
            if (notificationDiv) {
                notificationDiv.style.display = 'none';
            }
        } else {
            console.error('Failed to mark notification as read:', result.error);
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}











// modals and dropdowns and burger menu code ----------------------------------------------------
  // Toggle mobile navigation menu
function toggleMobileMenu() {
    const mobileNav = document.getElementById('mobileNav');
    console.log(mobileNav);
    
    mobileNav.style.display = 'block';
    console.log("Clicked!!")
}

// Toggle dropdown menu
function toggleDropdown() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
}

// Open modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.classList.add('modal-open');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }
}


// Close dropdown if clicked outside
document.addEventListener('click', function(event) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const userCircle = document.querySelector('.user-circle');

    if (!userCircle.contains(event.target)) {
        dropdownMenu.style.display = 'none';
    }
});

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Optional: Close modal when clicking outside the modal content
window.onclick = function(event) {
    var modals = ['loginModal', 'registerModal', 'forgotPasswordModal'];
    modals.forEach(function(modalId) {
        var modal = document.getElementById(modalId);
        if (event.target === modal) {
            closeModal(modalId);
        }
    });
}



// login code 
// JavaScript code to handle login form submission via AJAX
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent default form submission

    // Get the URL from the data attribute
    var url = this.getAttribute('data-login-url');

    // Create a FormData object to handle form data
    var formData = new FormData(this);

    // Send AJAX request to the server
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to home page if login is successful
            window.location.href = data.redirect_url;
        } else {
            // Display error message inside the modal
            var errorElement = document.getElementById('loginError');
            errorElement.innerText = data.error;
            errorElement.style.display = 'block';
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
});


// search-bar script----------------------------------------------
// Sample suggestions array
// Suggestions arrays for fruits and animals
// Suggestions arrays for fruits and animals
const fruitsArray = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape', 'Honeydew', 'Jackfruit', 'Kiwi', 'Lemon', 'Mango', 'Nectarine', 'Orange', 'Papaya'];
const animalsArray = ['Antelope', 'Bear', 'Cat', 'Dog', 'Elephant', 'Falcon', 'Giraffe', 'Horse', 'Iguana', 'Jaguar', 'Kangaroo', 'Lion', 'Monkey', 'Narwhal', 'Ostrich'];

// Default suggestions (start with fruits)
let currentArray = fruitsArray;
let selectedFilter = 'fruits'; // Keep track of the selected filter

function showSuggestions(input) {
    const suggestionsList = document.getElementById('suggestions');
    suggestionsList.innerHTML = ''; // Clear any previous suggestions

    if (input.length === 0) {
        return; // Don't show suggestions if the input is empty
    }

    // Filter suggestions based on input
    const filteredSuggestions = currentArray.filter(item =>
        item.toLowerCase().startsWith(input.toLowerCase())
    );

    // Show the filtered suggestions
    filteredSuggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        
        // Make suggestion clickable
        li.addEventListener('click', function() {
            document.getElementById('search').value = suggestion; // Set the search bar value
            suggestionsList.innerHTML = ''; // Clear suggestions after selection
        });
        
        suggestionsList.appendChild(li);
    });
}

// Function to set filter (fruits or animals)
function setFilter(filter) {
    const fruitsButton = document.getElementById('filter-fruits');
    const animalsButton = document.getElementById('filter-animals');

    // Update currentArray based on the selected filter
    if (filter === 'fruits') {
        currentArray = fruitsArray;
        selectedFilter = 'fruits';
        fruitsButton.classList.add('selected'); // Highlight the selected filter
        animalsButton.classList.remove('selected');
    } else if (filter === 'animals') {
        currentArray = animalsArray;
        selectedFilter = 'animals';
        animalsButton.classList.add('selected');
        fruitsButton.classList.remove('selected');
    }

    // Clear suggestions when the filter is changed
    document.getElementById('search').value = '';
    document.getElementById('suggestions').innerHTML = '';
}



// scripts for jobpostings--------------------------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove 'selected' class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('selected'));
            
            // Add 'selected' class to the clicked button
            this.classList.add('selected');
            
            // Get the data type of the clicked button
            const type = this.getAttribute('data-type');
            
            // Get all job postings
            const jobPostings = document.querySelectorAll('.job-posting');
            
            // Show or hide job postings based on the selected filter
            jobPostings.forEach(posting => {
                if (type === 'all' || posting.classList.contains(type)) {
                    posting.style.display = 'flex'; // Show the job posting
                } else {
                    posting.style.display = 'none'; // Hide the job posting
                }
            });
        });
    });
});



// anonymouse user home page -------------------------------------------------------
// Sample data for the chart
var data = {
    labels: ['Fast Jobs', 'Permanent', 'Part Time Contract'],
    datasets: [{
        data: [300, 50, 100],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
    }]
};

// Create the chart
var ctx = document.getElementById('jobPostsChart').getContext('2d');
var jobPostsChart = new Chart(ctx, {
    type: 'pie',
    data: data,
});

// Filter buttons
document.getElementById('filterToday').addEventListener('click', function() {
    // Filter job posts for today
});

document.getElementById('filterWeek').addEventListener('click', function() {
    // Filter job posts for this week
});

document.getElementById('filterMonth').addEventListener('click', function() {
    // Filter job posts for this month
});




// anonymouse users ----------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // Simulate fetching data
    const fetchJobStats = () => {
        // This data would typically come from an API
        return {
            today: Math.floor(Math.random() * 100),
            week: Math.floor(Math.random() * 500),
            month: Math.floor(Math.random() * 2000),
        };
    };

    const updateJobStats = () => {
        const stats = fetchJobStats();
        document.getElementById('js-jobs-today').textContent = stats.today;
        document.getElementById('js-jobs-week').textContent = stats.week;
        document.getElementById('js-jobs-month').textContent = stats.month;
    };

    updateJobStats();
});



// job seeker home page --------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    const jobList = document.getElementById('js-h-job-list');
    const searchInput = document.getElementById('js-h-search');
    const jobTypeFilter = document.getElementById('js-h-job-type');
    const jobCategoryFilter = document.getElementById('js-h-job-category');

    function filterJobs() {
        const searchTerm = searchInput.value.toLowerCase();
        const jobType = jobTypeFilter.value;
        const jobCategory = jobCategoryFilter.value;

        const jobs = jobList.getElementsByClassName('js-h-job-posting');

        Array.from(jobs).forEach(function (job) {
            const title = job.dataset.title.toLowerCase();
            const type = job.dataset.type;
            const category = job.dataset.category;

            const matchesSearchTerm = title.includes(searchTerm);
            const matchesJobType = !jobType || type === jobType;
            const matchesJobCategory = !jobCategory || category === jobCategory;

            if (matchesSearchTerm && matchesJobType && matchesJobCategory) {
                job.style.display = 'flex';
            } else {
                job.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterJobs);
    jobTypeFilter.addEventListener('change', filterJobs);
    jobCategoryFilter.addEventListener('change', filterJobs);
});



// SCRIPTS FOR EMPLOYER HOME PAGE----------------------------------------
function showUniqueContent(sectionId) {
    // Hide all sections
    document.querySelectorAll('.unique-content-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}

// Optionally, you could display the first section by default
document.addEventListener('DOMContentLoaded', () => {
    showUniqueContent('unique-home');
});


















// self remove div script -----------------------------------------------

function addSelfRemovingBehavior(selector) {
    const elements = document.querySelectorAll(selector);

    elements.forEach(element => {
        element.addEventListener("click", function() {
            this.remove();  // Remove the clicked element
        });
    });
}



addSelfRemovingBehavior(".t-r-item");
