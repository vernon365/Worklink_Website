document.addEventListener('DOMContentLoaded', () => {
    const addExperienceBtn = document.getElementById('add-experience-btn');
    const experienceForm = document.getElementById('experience-form');
    const saveExperienceBtn = document.getElementById('save-experience-btn');
    const experiencesList = document.getElementById('experiences-list');

    // Fetch experiences on page load
    fetchExperiences();

    // Show the form when the "Add Experience" button is clicked
    addExperienceBtn.addEventListener('click', () => {
        experienceForm.style.display = 'block';
    });

    // Save experience when the "Save" button is clicked
    saveExperienceBtn.addEventListener('click', async () => {
        const title = document.getElementById('experience-title').value.trim();
        const description = document.getElementById('experience-description').value.trim();
        const organization = document.getElementById('experience-organization').value.trim();
        const refererName = document.getElementById('experience-referer-name').value.trim();
        const refererContact = document.getElementById('experience-referer-contact').value.trim();

        if (!title || !description) {
            alert('Title and Description are required.');
            return;
        }

        const experienceData = {
            title,
            description,
            organization,
            referer_name: refererName,
            referer_contact: refererContact
        };

        try {
            const response = await fetch('/profiles/add_experience/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(experienceData)
            });

            const result = await response.json();

            if (result.success) {
                alert('Experience added successfully!');
                fetchExperiences(); // Reload experiences after adding a new one
                experienceForm.reset();
                experienceForm.style.display = 'none';
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while saving the experience.');
        }
    });

    async function fetchExperiences() {
        try {
            const response = await fetch('/profiles/get_experiences/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const experiences = await response.json();
            renderExperiences(experiences);
        } catch (error) {
            console.error('Error fetching experiences:', error);
        }
    }

    function renderExperiences(experiences) {
        experiencesList.innerHTML = ''; // Clear existing list
        experiences.forEach(exp => {
            addExperienceToUI(
                exp.title,
                exp.description,
                exp.organization,
                exp.referer_name,
                exp.referer_contact
            );
        });
    }

    function addExperienceToUI(title, description, organization, refererName, refererContact) {
        const li = document.createElement('li');
        li.classList.add('experience-item');

        li.innerHTML = `
            <div class="experience-header">
                <h3 class="experience-title">${title}</h3>
                <span class="experience-organization">${organization || 'N/A'}</span>
            </div>
            <p class="experience-description">${description}</p>
            <div class="experience-referer">
                <strong>Referer:</strong> ${refererName || 'N/A'}<br>
                <strong>Contact:</strong> ${refererContact || 'N/A'}
            </div>
        `;

        experiencesList.appendChild(li);
    }

    function getCSRFToken() {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }
});










// Get elements
const addRemoveSkillsBtn = document.getElementById("add-remove-skills-btn");
const skillsList = document.getElementById("skills-list");
const skillsForm = document.getElementById("skills-form");
const skillInput = document.getElementById("skill-input");
const addSkillBtn = document.getElementById("add-skill-btn");
const saveSkillsBtn = document.getElementById("save-skills-btn");

let skills = []; // Holds the current new skills to be added
let savedSkills = []; // Holds the saved skills fetched from the backend

// Predefined background colors for skills
const skillColors = ['#FFD700', '#ADFF2F', '#FF69B4', '#87CEEB', '#FFA07A', '#9370DB', '#40E0D0', '#FF4500', '#00FA9A', '#DAA520'];
let colorIndex = 0; // To cycle through the colors

// Fetch existing skills for the logged-in user when the page loads
window.onload = () => {
    fetchSkills();
};

// Fetch skills from the backend
function fetchSkills() {
    fetch('http://127.0.0.1:8000/profiles/get-skills')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                savedSkills = data.skills; // Fetch and store saved skills
                displaySkills(false);  // Display only saved skills without "X" buttons initially
            } else {
                console.log("Error fetching skills: " + data.error);
            }
        });
}

// Display skills in the list
function displaySkills(showRemoveButton) {
    skillsList.innerHTML = '';

    // Helper function to get next background color
    function getNextColor() {
        const color = skillColors[colorIndex % skillColors.length];
        colorIndex++;
        return color;
    }

    // Display saved skills
    savedSkills.forEach(skill => {
        const li = document.createElement('li');
        li.classList.add('skill-item', 'saved-skill');
        li.style.backgroundColor = getNextColor(); // Assign background color
        li.innerHTML = showRemoveButton 
            ? `${skill} <button class="btn btn-danger" onclick="removeSkill('${skill}', 'saved')">X</button>` 
            : `${skill}`;
        skillsList.appendChild(li);
    });

    // Display new skills
    skills.forEach(skill => {
        const li = document.createElement('li');
        li.classList.add('skill-item');
        li.style.backgroundColor = getNextColor(); // Assign background color
        li.innerHTML = `${skill} <button class="btn btn-danger" onclick="removeSkill('${skill}', 'new')">X</button>`;
        skillsList.appendChild(li);
    });
}

// Add skill to the list (new skills only)
addSkillBtn.addEventListener("click", () => {
    const skill = skillInput.value.trim();
    if (skill && !skills.includes(skill) && !savedSkills.includes(skill)) {
        skills.push(skill); // Add new skill to the editable skills list
        skillInput.value = ''; // Clear the input field
        displaySkills(true); // Show skills with "X" buttons (for both saved and new)
    }
});

// Remove skill from the list (both saved and new)
function removeSkill(skillName, type) {
    if (type === 'new') {
        // Remove from new skills list
        skills = skills.filter(skill => skill !== skillName);
    } else if (type === 'saved') {
        // Remove from saved skills list
        savedSkills = savedSkills.filter(skill => skill !== skillName);
    }
    displaySkills(true); // Re-render the skill list with "X" buttons
}

// Show/hide the skill input form
addRemoveSkillsBtn.addEventListener("click", () => {
    if (skillsForm.style.display === "none" || skillsForm.style.display === "") {
        skillsForm.style.display = "block";
        addRemoveSkillsBtn.textContent = "Cancel";
        displaySkills(true); // Show skills with "X" buttons when clicked
    } else {
        skillsForm.style.display = "none";
        addRemoveSkillsBtn.textContent = "Add/Remove Skills";
        displaySkills(false); // Show skills without "X" buttons when hidden
    }
});

// Save skills (new skills to be added to the saved skills list)
saveSkillsBtn.addEventListener("click", () => {
    const allSkills = [...savedSkills, ...skills]; // Merge new skills with saved skills

    fetch('http://127.0.0.1:8000/profiles/save-skills/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ skills: allSkills })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            savedSkills = allSkills; // Merge saved and new skills into saved skills
            skills = []; // Clear the new skills list
            displaySkills(false); // Re-render the skill list without "X" buttons
            skillsForm.style.display = "none";
            addRemoveSkillsBtn.textContent = "Add/Remove Skills";
        } else {
            alert("Error saving skills: " + data.error);
        }
    });
});

// Get CSRF token from cookies
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return '';
}










