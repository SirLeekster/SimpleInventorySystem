// ==========================
// Dashboard Overview Section
// ==========================

export function initOverview() {
    loadDashboardStats();
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
