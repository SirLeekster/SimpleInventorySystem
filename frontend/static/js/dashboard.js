document.addEventListener("DOMContentLoaded", function () {
  // Fetch dashboard statistics from the backend and populate UI
  fetch("/api/dashboard_stats")
    .then(res => res.json())
    .then(data => {
      document.getElementById("totalItems").textContent = data.total_items;
      document.getElementById("lowStockItems").textContent = data.low_stock_items;
      document.getElementById("outOfStockItems").textContent = data.out_of_stock_items;
      document.getElementById("totalSales").textContent = data.total_sales;
      document.getElementById("topItem").textContent = data.top_item;
      document.getElementById("recentItems").textContent = data.recent_additions;
    })
    .catch(() => {
      console.warn("Failed to load dashboard stats.");
    });

  // Sidebar navigation logic
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

  // Sidebar navigation click handling
  sidebarLinks.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.id;

      switch (targetId) {
        case "overviewMenu":
          showSection("dashboardOverview");
          break;
        case "addItemMenu":
          showSection("addInventoryItem");
          break;
        case "manageItemsMenu":
          showSection("manageItems");
          break;
        case "salesReportsMenu":
          showSection("reports");
          break;
        case "settingsMenu":
          showSection("settings");
          break;
        case "logoutLink":
          window.location.href = "/logout";
          break;
        default:
          showSection("dashboardOverview");
      }
    });
  });

  // Handle inventory form submission
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
          addInventoryForm.reset();
        } else {
          alert("Error: " + result.message);
        }
      } catch (error) {
        alert("An error occurred while adding the inventory item.");
      }
    });
  }

  // Toggle sidebar collapse (kept unchanged)
  const sidebar = document.querySelector(".sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");
    });
  }
});
