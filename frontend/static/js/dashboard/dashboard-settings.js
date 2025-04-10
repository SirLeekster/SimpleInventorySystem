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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email })
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
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
function loadAllUsers() {
    fetch('/api/org/users')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('orgUsersList');
            container.innerHTML = '';

            data.users.forEach(user => {
                const div = document.createElement('div');
                div.className = 'user-entry';
                div.dataset.search = (user.username + ' ' + user.email).toLowerCase();
                div.textContent = `${user.username} | ${user.email} | joined ${user.created_at}`;
                container.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Failed to load org users:", err);
            document.getElementById('orgUsersList').textContent = "Error loading users.";
        });
}

function filterUserList() {
    const input = document.getElementById('orgUserSearch').value.toLowerCase();
    const users = document.querySelectorAll('#orgUsersList .user-entry');

    users.forEach(user => {
        const text = user.dataset.search;
        if (text.includes(input)) {
            user.style.display = '';
        } else {
            user.style.display = 'none';
        }
    });
}

// Load full activity logs for the org
function loadFullLogs() {
    fetch('/api/org/logs')
        .then(res => res.json())
        .then(data => {
            const logContainer = document.getElementById('fullOrgLogs');
            logContainer.innerHTML = '';

            if (!data.logs || data.logs.length === 0) {
                logContainer.innerHTML = '<div class="log-item">No logs found.</div>';
                return;
            }

            data.logs.forEach(log => {
                const timestamp = new Date(log.timestamp).toLocaleString();
                const user = log.username || 'Unknown User';
                const line = document.createElement('div');
                line.className = 'log-item';
                line.textContent = `User: ${user} | Action: ${log.action} | performed at ${timestamp}`;
                logContainer.appendChild(line);
            });
        })
        .catch(err => {
            console.error("Failed to load logs:", err);
            document.getElementById('fullOrgLogs').innerHTML =
                '<div class="log-item">Error loading logs.</div>';
        });
}
