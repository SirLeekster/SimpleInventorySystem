// handles loading dashboard overview stats and recent activity logs
// fetches key metrics like inventory, sales, top item, and new additions
// displays recent user actions with emoji indicators for better readability

export function initOverview() {
    loadDashboardStats();
    loadActivityLog();
}

function loadDashboardStats() {
    fetch("/api/dashboard_stats")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
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

function loadActivityLog() {
    fetch('/api/logs/recent')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('activity-log');
            list.innerHTML = '';

            if (!data.logs || data.logs.length === 0) {
                list.innerHTML = '<li class="log-item text-muted">No recent activity.</li>';
                return;
            }

            data.logs.forEach(log => {
                const timestamp = new Date(log.timestamp).toLocaleString();
                const user = log.username || 'Unknown User';
                const emoji = getActionEmoji(log.action);

                const item = document.createElement('li');
                item.className = 'log-item';
                item.textContent = `${emoji} | User: ${user} | Action: ${log.action} | Performed at ${timestamp}`;


                list.appendChild(item);
            });
        })
        .catch(err => {
            console.error('Failed to load activity log:', err);
            document.getElementById('activity-log').innerHTML =
                '<li class="log-item text-danger">Error loading logs.</li>';
        });
}

function getActionEmoji(action) {
    if (/added/i.test(action)) return '✅';
    if (/edited/i.test(action)) return '✏️';
    if (/deleted/i.test(action)) return '❌';
    if (/upload/i.test(action)) return '🖼️';
    if (/generate/i.test(action)) return '⚙️';
    return '🔹';
}



