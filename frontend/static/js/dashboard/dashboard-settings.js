// ==========================
// Settings / Account Section
// ==========================

export function initSettings() {
    loadUserData();
    loadAllUsers();
    loadFullLogs();

    const editProfileBtn = document.getElementById('editProfileBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
    const profileForm = document.getElementById('profileForm');
    const passwordForm = document.getElementById('passwordForm');

    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', () => {
            document.getElementById('profileDisplay').classList.add('hidden');
            document.getElementById('profileEdit').classList.remove('hidden');
        });
    }

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', () => {
            document.getElementById('profileEdit').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        });
    }

    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', () => {
            document.getElementById('profileDisplay').classList.add('hidden');
            document.getElementById('passwordChange').classList.remove('hidden');
        });
    }

    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener('click', () => {
            document.getElementById('passwordChange').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        });
    }

    if (profileForm) {
        profileForm.addEventListener('submit', function (e) {
            e.preventDefault();
            updateUserProfile();
        });
    }

    if (passwordForm) {
        passwordForm.addEventListener('submit', function (e) {
            e.preventDefault();
            changePassword();
        });
    }

    const userSearchInput = document.getElementById('orgUserSearch');
    if (userSearchInput) {
        userSearchInput.addEventListener('input', filterUserList);
    }
}

function loadUserData() {
    fetch('/api/user/profile')
        .then(res => res.json())
        .then(data => {
            document.getElementById('displayUsername').textContent = data.username || 'N/A';
            document.getElementById('displayEmail').textContent = data.email || 'N/A';
            document.getElementById('displayOrganization').textContent = data.organization_name || 'N/A';
        })
        .catch(err => {
            console.error("Failed to load user data:", err);
            ['displayUsername', 'displayEmail', 'displayOrganization'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.textContent = 'Error loading data';
            });
        });
}

function updateUserProfile() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();

    fetch('/api/user/profile', {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email})
    })
        .then(res => res.json())
        .then(data => {
            alert("Profile updated.");
            document.getElementById('displayUsername').textContent = username;
            document.getElementById('displayEmail').textContent = email;
            document.getElementById('profileEdit').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
        })
        .catch(err => {
            console.error("Profile update failed:", err);
            alert("Failed to update profile.");
        });
}

function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!currentPassword || !newPassword || !confirmPassword || newPassword !== confirmPassword) {
        alert("Please check all password fields.");
        return;
    }

    fetch('/api/user/password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({current_password: currentPassword, new_password: newPassword})
    })
        .then(res => {
            if (!res.ok) {
                throw new Error("Password change failed");
            }
            return res.json();
        })
        .then(() => {
            alert("Password changed successfully.");
            document.getElementById('passwordChange').classList.add('hidden');
            document.getElementById('profileDisplay').classList.remove('hidden');
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmPassword').value = '';
        })
        .catch(err => {
            console.error("Password change error:", err);
            alert("Failed to change password.");
        });
}

// Load all users in the organization
// Load all users in the organization (updated for table layout)
function loadAllUsers() {
    fetch('/api/org/users')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('orgUsersTableBody');
            tbody.innerHTML = '';

            if (!data.users || data.users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3">No users found.</td></tr>';
                return;
            }

            data.users.forEach(user => {
                const row = document.createElement('tr');
                // Set up a dataset for searching, using all table cell content
                row.dataset.search = `${user.username} ${user.email}`.toLowerCase();

                const usernameCell = document.createElement('td');
                usernameCell.textContent = user.username || 'Unknown';

                const emailCell = document.createElement('td');
                emailCell.textContent = user.email || 'N/A';

                const joinedCell = document.createElement('td');
                // Use user.created_at directly or format as needed
                joinedCell.textContent = user.created_at || 'N/A';

                row.appendChild(usernameCell);
                row.appendChild(emailCell);
                row.appendChild(joinedCell);

                tbody.appendChild(row);
            });
        })
        .catch(err => {
            console.error("Failed to load org users:", err);
            document.getElementById('orgUsersTableBody').innerHTML = '<tr><td colspan="3">Error loading users.</td></tr>';
        });
}

// Updated filter function for the users table
function filterUserList() {
    const input = document.getElementById('orgUserSearch').value.toLowerCase();
    // Select all rows from the users table body
    const rows = document.querySelectorAll('#orgUsersTableBody tr');

    rows.forEach(row => {
        // Compare the combined text content to the input
        if (row.textContent.toLowerCase().includes(input)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


// Load full activity logs for the org
function loadFullLogs() {
    fetch('/api/org/logs')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('logsTableBody');
            tbody.innerHTML = '';

            if (!data.logs || data.logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3">No logs found.</td></tr>';
                return;
            }

            data.logs.forEach(log => {
                const row = document.createElement('tr');
                row.classList.add('log-row');

                row.dataset.search = `${log.username} ${log.action} ${log.timestamp}`.toLowerCase();

                const userCell = document.createElement('td');
                userCell.textContent = log.username || 'Unknown';

                const actionCell = document.createElement('td');
                actionCell.textContent = log.action;

                const timeCell = document.createElement('td');
                timeCell.textContent = new Date(log.timestamp).toLocaleString();

                row.appendChild(userCell);
                row.appendChild(actionCell);
                row.appendChild(timeCell);

                tbody.appendChild(row);
            });
        })
        .catch(err => {
            console.error("Error loading logs", err);
            document.getElementById('logsTableBody').innerHTML = '<tr><td colspan="3">Failed to load logs.</td></tr>';
        });
}

document.addEventListener('input', function (e) {
    if (e.target.id === 'logSearchInput') {
        const query = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#logsTableBody .log-row');

        rows.forEach(row => {
            if (row.dataset.search.includes(query)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
});

