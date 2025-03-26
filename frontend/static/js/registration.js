document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registrationForm");
    const orgChoice = document.getElementById("orgChoice");
    const joinField = document.getElementById("joinOrgField");
    const createField = document.getElementById("createOrgField");

    // Show/hide org name fields based on dropdown selection
    function toggleOrgFields(choice) {
        joinField.classList.toggle("hidden", choice !== "join");
        createField.classList.toggle("hidden", choice !== "create");
    }

    // Listen for organization choice change and update UI
    if (orgChoice) {
        orgChoice.addEventListener("change", () => {
            toggleOrgFields(orgChoice.value);
        });

        // Trigger initial toggle based on current value
        toggleOrgFields(orgChoice.value);
    }

    // Handle registration form submission
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Gather form input values
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const orgChoice = document.getElementById("orgChoice").value;
        const existingOrg = document.getElementById("existingOrg").value.trim();
        const newOrg = document.getElementById("newOrg").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        // Validate password match
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Determine org handling and validate input
        let orgData = {};
        if (orgChoice === "join") {
            if (existingOrg === "") {
                alert("Please enter the organization name to join.");
                return;
            }
            orgData = { org_choice: "join", organization_name: existingOrg };
        } else if (orgChoice === "create") {
            if (newOrg === "") {
                alert("Please enter a new organization name.");
                return;
            }
            orgData = { org_choice: "create", organization_name: newOrg };
        } else {
            alert("Please select an organization option.");
            return;
        }

        // Assemble full user data payload
        const userData = {
            username: username,
            email: email,
            password: password,
            org_data: orgData
        };

        // Send POST request to backend for registration
        try {
            const response = await fetch("/api/create_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();

            // Redirect or show error
            if (response.ok) {
                alert(result.message);
                window.location.href = "/login";
            } else {
                alert("Error: " + result.message);
            }
        } catch (error) {
            alert("An error occurred during registration.");
        }
    });
});