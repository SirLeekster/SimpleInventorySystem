// Wait for the DOM to be fully loaded before running any JavaScript
document.addEventListener("DOMContentLoaded", function () {
    // Test API connectivity to identify any backend issues
    testApiConnection();

    // Load dashboard overview stats
    loadDashboardStats();

    // Set up sidebar navigation
    setupSidebarNavigation();

    // Set up form submission handlers
    setupFormHandlers();

    // Set up modal event handlers
    setupModalHandlers();
});

// Function to test API connectivity
function testApiConnection() {
    fetch("/api/inventory_items")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log("API connection successful: Status " + response.status);
            return response.json();
        })
        .then(data => {
            console.log("API connection test: Data received successfully");
        })
        .catch(error => {
            console.error("API connection failed:", error);
        });
}

// Function to load dashboard statistics
function loadDashboardStats() {
    fetch("/api/dashboard_stats")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            // Update dashboard stats UI elements
            document.getElementById("totalItems").textContent = data.total_items;
            document.getElementById("lowStockItems").textContent = data.low_stock_items;
            document.getElementById("outOfStockItems").textContent = data.out_of_stock_items;
            document.getElementById("totalSales").textContent = data.total_sales;
            document.getElementById("topItem").textContent = data.top_item;
            document.getElementById("recentItems").textContent = data.recent_additions;
        })
        .catch((error) => {
            console.warn("Failed to load dashboard stats:", error);
        });
}

// Function to set up sidebar navigation
function setupSidebarNavigation() {
    const sidebarLinks = document.querySelectorAll(".sidebar-menu li a");
    const contentSections = document.querySelectorAll(".content-section");

    // Hide all content sections
    function hideAllSections() {
        contentSections.forEach(section => section.classList.add("hidden"));
    }

    // Show the selected content section
    function showSection(sectionId) {
        hideAllSections();
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove("hidden");
        }
    }

    // Add click handlers to sidebar links
    sidebarLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.id;

            console.log("Menu item clicked:", targetId);  // Add this line

            switch (targetId) {
                case "overviewMenu":
                    showSection("dashboardOverview");
                    loadDashboardStats(); // Reload stats when returning to overview
                    break;
                case "addItemMenu":
                    showSection("addInventoryItem");
                    break;
                case "manageItemsMenu":
                    showSection("manageItems");
                    loadInventoryTable();
                    break;
                case "salesReportsMenu":
                    showSection("reports");
                    break;
                case "settingsMenu":
                    showSection("settings");
                    setupSettingsPage();
                    break;
                case "logoutLink":
                    window.location.href = "/logout";
                    break;
                default:
                    showSection("dashboardOverview");
            }
        });
    });

    // Toggle sidebar collapse if button exists
    const sidebar = document.querySelector(".sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
        });
    }
}

// Function to set up form handlers
function setupFormHandlers() {
    // Handle add inventory form submission
    const addInventoryForm = document.getElementById("addInventoryForm");
    if (addInventoryForm) {
        addInventoryForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const productName = document.getElementById("productName").value.trim();
            const description = document.getElementById("description").value.trim();
            const category = document.getElementById("category").value.trim() || "General";
            const quantity = parseInt(document.getElementById("quantity").value);
            const price = parseFloat(document.getElementById("price").value);

            if (!productName || isNaN(quantity) || isNaN(price)) {
                alert("Please fill in all fields correctly.");
                return;
            }

            const payload = {
                product_name: productName,
                description: description,
                category: category,
                quantity: quantity,
                price: price
            };

            try {
                const response = await fetch("/api/create_inventory_item", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (response.ok) {
                    alert(result.message);

                    const itemId = result.item_id;
                    const imageInput = document.getElementById("image");

                    if (imageInput.files.length > 0) {
                        const imageFormData = new FormData();
                        imageFormData.append("image", imageInput.files[0]);

                        try {
                            console.log("Uploading image...");
                            const imageResponse = await fetch(`/api/upload_inventory_image/${itemId}`, {
                                method: "POST",
                                body: imageFormData
                            });

                            const imageResult = await imageResponse.json();
                            if (!imageResponse.ok) {
                                console.error("Image upload error:", imageResult.message);
                            }
                        } catch (imageError) {
                            console.error("Error uploading image:", imageError);
                        }
                    }

                    // NOW reset the form
                    addInventoryForm.reset();
                    document.querySelector(".custom-file-label").textContent = "Choose Image";
                    loadDashboardStats();
                } else {
                    alert("Error: " + result.message);
                }
            } catch (error) {
                console.error("Error adding inventory item:", error);
                alert("An error occurred while adding the inventory item.");
            }
        });
    }

    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'Choose Image';
            this.nextElementSibling.textContent = fileName;
        });
    }

    const editImageInput = document.getElementById('editImage');
    if (editImageInput) {
        editImageInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'Choose Image';
            this.nextElementSibling.textContent = fileName;
        });
    }


    // Handle edit inventory form submission
    const editInventoryForm = document.getElementById("editInventoryForm");
    if (editInventoryForm) {
        editInventoryForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const itemId = document.getElementById("editItemId").value;
            const productName = document.getElementById("editName").value.trim();
            const description = document.getElementById("editDescription").value.trim();
            const category = document.getElementById("editCategory").value.trim() || "General";
            const quantity = parseInt(document.getElementById("editQuantity").value);
            const price = parseFloat(document.getElementById("editPrice").value);

            if (isNaN(quantity) || isNaN(price) || quantity < 0 || price < 0) {
                alert("Please enter valid values for quantity and price.");
                return;
            }

            const payload = {
                product_name: productName,
                description: description,
                category: category,
                quantity: quantity,
                price: price,
            };

            try {
                const response = await fetch(`/api/update_inventory_item/${itemId}`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Server error:", errorData);
                    alert(`Error (${response.status}): ${errorData.message || "Unknown error"}`);
                    return;
                }

                const result = await response.json();
                alert(result.message)

                const imageInput = document.getElementById("editImage");
                if (imageInput && imageInput.files.length > 0) {
                    const imageFormData = new FormData();
                    imageFormData.append("image", imageInput.files[0]);

                    try {
                        console.log("Uploading updated image...");
                        const imageResponse = await fetch(`/api/upload_inventory_image/${itemId}`, {
                            method: "POST",
                            body: imageFormData
                        });

                        const imageResult = await imageResponse.json();
                        if (!imageResponse.ok) {
                            console.error("Image upload error:", imageResult.message);
                        } else {
                            console.log("Image updated successfully.");
                        }
                    } catch (imageError) {
                        console.error("Error uploading image:", imageError);
                    }
                }


                loadInventoryTable(); // Reload the table
                loadDashboardStats(); // Update stats after editing item
                document.getElementById("editModal").classList.add("hidden"); // Close modal
            } catch (error) {
                console.error("Request failed:", error);
                alert("An error occurred while saving the item: " + error.message);
            }
        });
    } else {
        console.error("Edit form not found");
    }

    const upcBtn = document.getElementById("upcLookupBtn");
if (upcBtn) {
    upcBtn.addEventListener("click", async function () {
        const upc = document.getElementById("upc").value.trim();
        if (!upc) {
            alert("Please enter a UPC.");
            return;
        }

        try {
            const res = await fetch(`/api/upc_lookup?upc=${encodeURIComponent(upc)}`);
            const data = await res.json();

            if (!res.ok) {
                alert(data.message || "UPC lookup failed.");
                return;
            }

            // Fill out the form fields
            document.getElementById("productName").value = data.product_name || '';
            document.getElementById("description").value = data.description || '';
            document.getElementById("category").value = data.category || 'General';
            document.getElementById("price").value = data.price || '';

            alert("Fields auto-filled from UPC.");
        } catch (err) {
            console.error("UPC fetch error:", err);
            alert("An error occurred while looking up the UPC.");
        }
    });
}


}

// Function to set up modal event handlers
function setupModalHandlers() {
    // Setup delete button handler
    const deleteBtn = document.getElementById("deleteItem");
    if (deleteBtn) {
        deleteBtn.addEventListener("click", async function () {
            const itemId = document.getElementById("editItemId").value;

            if (confirm("Are you sure you want to delete this item?")) {
                try {
                    const response = await fetch(`/api/delete_inventory_item/${itemId}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        console.error("Delete error:", errorData);
                        alert(`Error (${response.status}): ${errorData.message || "Unknown error"}`);
                        return;
                    }

                    const result = await response.json();
                    alert(result.message);
                    loadInventoryTable(); // Reload the table
                    loadDashboardStats(); // Update stats after deleting item
                    document.getElementById("editModal").classList.add("hidden"); // Close modal
                } catch (error) {
                    console.error("Delete request failed:", error);
                    alert("An error occurred while deleting the item: " + error.message);
                }
            }
        });
    } else {
        console.error("Delete button not found");
    }

    // Setup cancel button handler
    const cancelBtn = document.getElementById("cancelEdit");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            document.getElementById("editModal").classList.add("hidden");
        });
    } else {
        console.error("Cancel button not found");
    }
}

// Function to load inventory table data and set up edit buttons
function loadInventoryTable() {
    console.log("Loading inventory table data...");

    fetch("/api/inventory_items")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then(items => {
            console.log(`Found ${items.length} inventory items`);

            const tableBody = document.getElementById("inventoryTableBody");
            if (!tableBody) {
                console.error("Table body element not found");
                return;
            }

            tableBody.innerHTML = "";

            items.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                <td>
                    ${item.image_path
                    ? `<img src="${item.image_path}" class="inventory-thumbnail" alt="Image">`
                    : `<div class="image-placeholder">No Image</div>`}
                </td>
                <td>${item.product_name}</td>
                <td title="${item.description || ''}">${item.description || ''}</td>
                <td>${item.category}</td>
                <td>${item.quantity}</td>
                <td>$${parseFloat(item.price).toFixed(2)}</td>
                <td>
                  <button class="edit-btn" data-id="${item.id}">✏️ Edit</button>
                </td>
              `;
                document.getElementById("inventoryTableBody").appendChild(row);
            });


            // Use event delegation for edit buttons instead of individual listeners
            setupEditButtonHandlers();
        })
        .catch(err => {
            console.error("Error fetching inventory items:", err);
        });
}

// Function to set up edit button handlers using event delegation
function setupEditButtonHandlers() {
    // Remove any existing handler first to prevent duplicates
    document.getElementById("inventoryTableBody").removeEventListener("click", handleEditButtonClick);
    document.getElementById("inventoryTableBody").addEventListener("click", handleEditButtonClick);
}

// Function to handle edit button clicks
function handleEditButtonClick(e) {
    if (e.target.classList.contains("edit-btn")) {
        console.log("Edit button clicked");

        const row = e.target.closest("tr");
        if (!row) {
            console.error("Could not find parent row");
            return;
        }

        const cells = row.children;

        // Fix cell mapping: image = 0, name = 1, desc = 2, category = 3, qty = 4, price = 5
        document.getElementById("editItemId").value = e.target.dataset.id;
        document.getElementById("editName").value = cells[1].textContent.trim();
        document.getElementById("editDescription").value = cells[2].textContent.trim();
        document.getElementById("editCategory").value = cells[3].textContent.trim();
        document.getElementById("editQuantity").value = parseInt(cells[4].textContent.trim());

        // ✅ Safely parse the price field
        const rawPrice = cells[5].textContent.trim().replace("$", "");
        document.getElementById("editPrice").value = isNaN(rawPrice) ? "" : parseFloat(rawPrice);

        // Show the modal
        const modal = document.getElementById("editModal");
        if (modal) {
            modal.classList.remove("hidden");
            console.log("Modal shown");
        } else {
            console.error("Modal element not found");
        }
    }
}

// Function to set up the settings page
function setupSettingsPage() {
    console.log("🔍 setupSettingsPage function called!");
    // Load user data
    loadUserData();

    // Set up button event handlers

    // Edit profile button
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function () {
            document.getElementById('profileDisplay').classList.add('hidden');
            document.getElementById('profileEdit').classList.remove('hidden');
        });
    }

    // Cancel edit button
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function () {
            document.getElementById('profileEdit').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        });
    }

    // Change password button
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function () {
            document.getElementById('profileDisplay').classList.add('hidden');
            document.getElementById('passwordChange').classList.remove('hidden');
        });
    }

    // Cancel password change button
    const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener('click', function () {
            document.getElementById('passwordChange').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        });
    }

    // Profile form submission
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function (e) {
            e.preventDefault();
            updateUserProfile();
        });
    }

    // Password form submission
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function (e) {
            e.preventDefault();
            changePassword();
        });
    }
}

// Function to load user data
function loadUserData() {
    console.log("Loading user data...");

    fetch('/api/user/profile')
        .then(response => {
            console.log("Profile API response:", response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(userData => {
            console.log("User data received:", userData);

            // Update display values
            const usernameElement = document.getElementById('displayUsername');
            const emailElement = document.getElementById('displayEmail');
            const orgElement = document.getElementById('displayOrganization');

            if (usernameElement) usernameElement.textContent = userData.username || 'N/A';
            if (emailElement) emailElement.textContent = userData.email || 'N/A';
            if (orgElement) orgElement.textContent = userData.organization_name || 'N/A';
        })
        .catch(error => {
            console.error("Error loading user data:", error);
            // Update all display elements with error message
            const usernameElement = document.getElementById('displayUsername');
            const emailElement = document.getElementById('displayEmail');
            const orgElement = document.getElementById('displayOrganization');

            if (usernameElement) usernameElement.textContent = 'Error loading data';
            if (emailElement) emailElement.textContent = 'Error loading data';
            if (orgElement) orgElement.textContent = 'Error loading data';
        });
}

// Function to update user profile
function updateUserProfile() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();

    if (!username || !email) {
        alert('Please fill in all required fields.');
        return;
    }

    const payload = {
        username: username,
        email: email
    };

    fetch('/api/user/profile', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            console.log("Profile update response status:", response.status);
            return response.json().then(data => {
                if (!response.ok) {
                    throw new Error(data.message || "Error updating profile");
                }
                return data;
            });
        })
        .then(data => {
            console.log("Profile update success:", data);
            alert('Profile updated successfully!');

            // Update display values
            document.getElementById('displayUsername').textContent = username;
            document.getElementById('displayEmail').textContent = email;

            // Switch back to display view
            document.getElementById('profileEdit').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        })
        .catch(error => {
            console.error("Profile update error:", error);
            alert('Failed to update profile: ' + error.message);
        });
}

// Function to change password
function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Basic validation
    if (!currentPassword || !newPassword || !confirmPassword) {
        alert('Please fill in all password fields.');
        return;
    }

    if (newPassword !== confirmPassword) {
        alert('New password and confirmation do not match.');
        return;
    }

    if (newPassword.length < 8) {
        alert('New password must be at least 8 characters long.');
        return;
    }

    // Create payload
    const payload = {
        current_password: currentPassword,
        new_password: newPassword
    };

    // Send request to update password
    fetch('/api/user/password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Current password is incorrect.');
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert('Password changed successfully!');

            // Clear password fields
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmPassword').value = '';

            // Switch back to display view
            document.getElementById('passwordChange').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error changing password:', error);
            alert(error.message || 'Failed to change password. Please try again.');
        });
}