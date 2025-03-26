// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("loginForm");

    // Handle login form submission
    form.addEventListener("submit", async function(e) {
        e.preventDefault(); // Prevent default form submission

        // Extract email and password from input fields
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        // Construct login request body
        const loginData = { email, password };

        // Send login request to the backend
        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(loginData)
            });

            const result = await response.json();

            // On success, redirect to dashboard
            if (response.ok) {
                alert(result.message);
                window.location.href = "/dashboard";
            } else {
                alert("Error: " + result.message);
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("An error occurred during login.");
        }
    });
});
