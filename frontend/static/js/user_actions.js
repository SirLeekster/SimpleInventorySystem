document.getElementById("registerButton").addEventListener("click", function() {
    // Hardcoded sample user data
    const userData = {
        username: "johndoe",
        email: "johndoe@example.com",
        password_hash: "password123"
    };

    // Send the data using a POST request
    fetch('/api/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        // Display success message or handle error
        if (data.message) {
            alert(data.message);
        } else {
            alert("Error adding user.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
