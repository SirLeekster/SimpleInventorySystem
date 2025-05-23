// handles login form submission and forgot password functionality
// sends login credentials to the server and redirects on success
// sends email for password reset instructions on user request

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");


    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        const loginData = {email, password};

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(loginData)
            });

            const result = await response.json();

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

// handle "Forgot Password?" click
document.addEventListener("DOMContentLoaded", function () {
    const forgotLink = document.querySelector(".forgot-password a");

    if (forgotLink) {
        forgotLink.addEventListener("click", async function (e) {
            e.preventDefault();

            const email = prompt("Enter your email to reset your password:");
            if (!email || !email.trim()) return;

            try {
                const response = await fetch("/api/forgot-password", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({email: email.trim()})
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message || "Reset instructions sent.");
                } else {
                    alert(result.message || "Error sending reset instructions.");
                }
            } catch (err) {
                console.error("Reset error:", err);
                alert("Something went wrong. Try again later.");
            }
        });
    }
});

