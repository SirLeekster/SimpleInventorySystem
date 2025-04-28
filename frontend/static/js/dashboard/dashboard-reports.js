// handles loading and displaying sales reports in the dashboard
// fetches sales summary and trend data based on selected date range
// renders interactive sales trend charts using chart.js

export function initReports() {
    const reportsContainer = document.getElementById("reportsContent");
    if (!reportsContainer) return;

    reportsContainer.innerHTML = `
        <div class="report-controls">
            <label for="reportRange">Filter:</label>
            <select id="reportRange">
                <option value="1d">Last 24 Hours</option>
                <option value="7d" selected>Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
                <option value="1y">Last 1 Year</option>
            </select>
        </div>

        <div class="report-summary">
            <div class="stat-item"><h3>Total Sales</h3><p id="reportTotalSales">$0.00</p></div>
            <div class="stat-item"><h3>Top Item</h3><p id="reportTopItem">N/A</p></div>
            <div class="stat-item"><h3>Sales This Week</h3><p id="reportWeekSales">0</p></div>
        </div>

        <div class="report-chart">
            <h4>Sales Trend</h4>
            <canvas id="salesTrendChart" height="120"></canvas>
        </div>
    `;

    const rangeSelect = document.getElementById("reportRange");
    rangeSelect.addEventListener("change", () => {
        fetchAndRenderReport(rangeSelect.value);
    });

    fetchAndRenderReport("7d");
}

function fetchAndRenderReport(range) {
    fetch(`/api/sales_report?range=${range}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("reportTotalSales").textContent = `$${data.summary.total_sales.toFixed(2)}`;
            document.getElementById("reportTopItem").textContent = data.summary.top_item;
            document.getElementById("reportWeekSales").textContent = data.summary.week_sales;

            renderChart(data.trend);
        })
        .catch(err => {
            console.error("Failed to load report data:", err);
            document.getElementById("reportsContent").innerHTML = `<p class="error">Failed to load reports.</p>`;
        });
}

let salesChart;

function renderChart(trendData) {
    const ctx = document.getElementById("salesTrendChart").getContext("2d");
    if (salesChart) salesChart.destroy();

    salesChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: trendData.map(d => d.date),
            datasets: [{
                label: "Sales ($)",
                data: trendData.map(d => d.sales),
                borderColor: "#2196f3",
                backgroundColor: "rgba(33, 150, 243, 0.2)",
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 6,
                pointBackgroundColor: "#1976d2",
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {display: false},
                tooltip: {
                    callbacks: {
                        label: context => `$${context.parsed.y.toFixed(2)}`
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date",
                        font: {weight: "bold"}
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Revenue ($)",
                        font: {weight: "bold"}
                    }
                }
            }
        }
    });
}
