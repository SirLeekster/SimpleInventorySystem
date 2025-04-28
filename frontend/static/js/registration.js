// handles user registration form submission
// dynamically toggles between join/create organization fields
// sends user and organization data to the server to create a new account


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registrationForm");
    const orgChoice = document.getElementById("orgChoice");
    const joinField = document.getElementById("joinOrgField");
    const createField = document.getElementById("createOrgField");

    function toggleOrgFields(choice) {
        joinField.classList.toggle("hidden", choice !== "join");
        createField.classList.toggle("hidden", choice !== "create");
    }

    if (orgChoice) {
        orgChoice.addEventListener("change", () => {
            toggleOrgFields(orgChoice.value);
        });

        toggleOrgFields(orgChoice.value);
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const full_name = document.getElementById("full_name").value.trim();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const orgChoice = document.getElementById("orgChoice").value;
        const existingOrg = document.getElementById("existingOrg").value.trim();
        const newOrg = document.getElementById("newOrg").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        let orgData = {};
        if (orgChoice === "join") {
            if (existingOrg === "") {
                alert("Please enter the organization name to join.");
                return;
            }
            orgData = {org_choice: "join", organization_name: existingOrg};
        } else if (orgChoice === "create") {
            if (newOrg === "") {
                alert("Please enter a new organization name.");
                return;
            }
            orgData = {org_choice: "create", organization_name: newOrg};
        } else {
            alert("Please select an organization option.");
            return;
        }

        const userData = {
            full_name: full_name,
            username: username,
            email: email,
            password: password,
            org_data: orgData
        };

        try {
            const response = await fetch("/api/create_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();

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