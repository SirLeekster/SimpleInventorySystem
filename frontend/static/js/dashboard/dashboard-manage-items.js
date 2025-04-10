// ==========================
// Manage Inventory Section
// ==========================

export function initManageItems() {
    loadInventoryTable();
}

document.getElementById("inventorySearch").addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase();

    const filteredItems = allInventoryItems.filter(item => {
        return (
            item.product_name.toLowerCase().includes(searchTerm) ||
            (item.description || "").toLowerCase().includes(searchTerm) ||
            item.category.toLowerCase().includes(searchTerm)
        );
    });

    renderInventoryTable(filteredItems);
});


// Load inventory into table
let allInventoryItems = [];

function loadInventoryTable() {
    fetch("/api/inventory_items")
        .then(res => res.json())
        .then(items => {
            allInventoryItems = items;
            renderInventoryTable(items);
            setupEditButtonHandlers();
            setupSkuButtonHandlers();
        })
        .catch(err => console.error("Error fetching inventory items:", err));
}

function renderInventoryTable(items) {
    const tableBody = document.getElementById("inventoryTableBody");
    tableBody.innerHTML = "";

    items.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.image_path ? `<img src="${item.image_path}" class="inventory-thumbnail">` : `<div class="image-placeholder">No Image</div>`}</td>
            <td>${item.product_name}</td>
            <td title="${item.description || ''}">${item.description || ""}</td>
            <td>${item.category}</td>
            <td>${item.quantity}</td>
            <td>$${parseFloat(item.price).toFixed(2)}</td>
            <td>
                <button class="edit-btn" data-id="${item.id}">✏️ Edit</button>
                <button class="sku-btn" data-id="${item.id}" data-quantity="${item.quantity}">📦 SKUs</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


function setupEditButtonHandlers() {
    document.getElementById("inventoryTableBody").addEventListener("click", handleEditButtonClick);
}

function setupSkuButtonHandlers() {
    document.getElementById("inventoryTableBody").addEventListener("click", handleSkuButtonClick);
}

function handleEditButtonClick(e) {
    if (!e.target.classList.contains("edit-btn")) return;

    const row = e.target.closest("tr");
    const cells = row.children;

    document.getElementById("editItemId").value = e.target.dataset.id;
    document.getElementById("editName").value = cells[1].textContent;
    document.getElementById("editDescription").value = cells[2].textContent;
    document.getElementById("editCategory").value = cells[3].textContent;
    document.getElementById("editQuantity").value = parseInt(cells[4].textContent);
    document.getElementById("editPrice").value = parseFloat(cells[5].textContent.replace("$", ""));

    document.getElementById("editModal").classList.remove("hidden");
}

function handleSkuButtonClick(e) {
    if (!e.target.classList.contains("sku-btn")) return;

    const itemId = e.target.dataset.id;
    const quantity = e.target.dataset.quantity;
    const modal = document.getElementById("skuModal");
    modal.classList.remove("hidden");
    modal.dataset.itemId = itemId;
    modal.dataset.quantity = quantity;

    loadSkuList(itemId, quantity);
}

function loadSkuList(itemId, quantity) {

    const saveAllBtn = document.getElementById("saveAllSkusBtn");
    const deleteAllBtn = document.getElementById("deleteAllSkusBtn");

    const container = document.getElementById("skuListContainer");
    container.innerHTML = "<p>Loading...</p>";

    fetch(`/api/inventory_item_skus/${itemId}`)
        .then(res => res.json())
        .then(skus => {
            container.innerHTML = "";
            const generateSection = document.getElementById("generateSkuSection");

            if (!Array.isArray(skus) || skus.length === 0) {
                container.innerHTML = "<p>No SKUs available for this item.</p>";
                generateSection.classList.remove("hidden");
                saveAllBtn.classList.add("hidden");
                deleteAllBtn.classList.add("hidden");
            } else {
                generateSection.classList.add("hidden");
                saveAllBtn.classList.remove("hidden");
                deleteAllBtn.classList.remove("hidden");


                const table = document.createElement("table");
                table.classList.add("sku-table");
                table.innerHTML = `
                    <thead>
                        <tr>
                            <th>SKU Code</th>
                            <th>Serial #</th>
                            <th>Status</th>
                            <th>Expires</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${skus.map(sku => `
                            <tr data-sku-id="${sku.sku_id}">
                                <td><input type="text" class="sku-code" value="${sku.sku_code}"></td>
                                <td><input type="text" class="sku-serial" value="${sku.serial_number || ''}"></td>
                                <td>
                                    <select class="sku-status">
                                        <option value="in_stock" ${sku.status === "in_stock" ? "selected" : ""}>In Stock</option>
                                        <option value="sold" ${sku.status === "sold" ? "selected" : ""}>Sold</option>
                                        <option value="damaged" ${sku.status === "damaged" ? "selected" : ""}>Damaged</option>
                                    </select>
                                </td>
                                <td><input type="date" class="sku-exp" value="${sku.expiration_date || ''}"></td>
                                <td>
                                    <button class="save-sku-btn button small">Save</button>
                                    <button class="delete-sku-btn button small delete-btn">Delete</button>
                                </td>
                            </tr>
                        `).join("")}
                    </tbody>
                `;
                container.appendChild(table);
            }
        })
        .catch(err => {
            console.error("Error loading SKUs:", err);
            container.innerHTML = "<p>Error loading SKUs.</p>";
        });
}

// ======= CANCEL Edit =======
document.getElementById("cancelEdit").addEventListener("click", () => {
    document.getElementById("editModal").classList.add("hidden");
});

document.getElementById("closeSkuModal").addEventListener("click", () => {
    document.getElementById("skuModal").classList.add("hidden");
});

document.getElementById("addSkuForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const itemId = document.getElementById("skuModal").dataset.itemId;
    const payload = {
        sku_code: document.getElementById("skuCode").value.trim(),
        serial_number: document.getElementById("serialNumber").value.trim() || null,
        status: document.getElementById("status").value,
        expiration_date: document.getElementById("expirationDate").value || null
    };

    try {
        const res = await fetch(`/api/add_sku_to_inventory_item/${itemId}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.message);

        alert("SKU added.");
        this.reset();
        loadSkuList(itemId);
    } catch (err) {
        console.error("Error adding SKU:", err);
        alert("Failed to add SKU.");
    }
});

document.getElementById("skuListContainer").addEventListener("click", async function (e) {
    const row = e.target.closest("tr");
    if (!row) return;

    const skuId = row.dataset.skuId;
    const itemId = document.getElementById("skuModal").dataset.itemId;

    if (e.target.classList.contains("save-sku-btn")) {
        const payload = {
            sku_code: row.querySelector(".sku-code").value.trim(),
            serial_number: row.querySelector(".sku-serial").value.trim(),
            status: row.querySelector(".sku-status").value,
            expiration_date: row.querySelector(".sku-exp").value || null
        };

        try {
            const res = await fetch(`/api/update_sku/${skuId}`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.message);
            alert("SKU updated.");
            loadInventoryTable(); // ✅ reloads quantity
        } catch (err) {
            console.error("Update failed:", err);
            alert("Failed to update SKU.");
        }
    }


    if (e.target.classList.contains("delete-sku-btn")) {
        if (!confirm("Delete this SKU?")) return;
        try {
            const res = await fetch(`/api/delete_sku/${skuId}`, {method: "DELETE"});
            const data = await res.json();
            if (!res.ok) throw new Error(data.message);
            alert("SKU deleted.");
            loadSkuList(itemId);
        } catch (err) {
            console.error("Delete failed:", err);
            alert("Failed to delete SKU.");
        }
    }
});

document.getElementById("generateSkusBtn").addEventListener("click", async function () {
    const modal = document.getElementById("skuModal");
    const itemId = modal.dataset.itemId;
    const quantity = parseInt(modal.dataset.quantity);

    if (!quantity || quantity <= 0) {
        alert("No quantity available to generate SKUs.");
        return;
    }

    if (!confirm(`Generate ${quantity} empty SKUs?`)) return;

    try {
        const res = await fetch(`/api/generate_skus/${itemId}?count=${quantity}`, {
            method: "POST"
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.message);

        alert("SKUs generated.");
        loadSkuList(itemId);
    } catch (err) {
        console.error("Generate SKUs failed:", err);
        alert("Failed to generate SKUs.");
    }
});

// ======= PATCH Item + Sync SKUs =======
document.getElementById("editInventoryForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const itemId = document.getElementById("editItemId").value;
    const payload = {
        product_name: document.getElementById("editName").value.trim(),
        description: document.getElementById("editDescription").value.trim(),
        category: document.getElementById("editCategory").value.trim(),
        quantity: parseInt(document.getElementById("editQuantity").value),
        price: parseFloat(document.getElementById("editPrice").value)
    };

    try {
        const res = await fetch(`/api/update_inventory_item/${itemId}`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message);

        // Call backend to sync SKUs to match quantity
        await fetch(`/api/generate_skus/${itemId}?count=${payload.quantity}`, {method: "POST"});

        alert("Item updated.");
        document.getElementById("editModal").classList.add("hidden");
        loadInventoryTable();
    } catch (err) {
        console.error("Error updating inventory:", err);
        alert("Failed to update item.");
    }
});

// ======= DELETE Item =======
document.getElementById("deleteItem").addEventListener("click", async function () {
    const itemId = document.getElementById("editItemId").value;
    if (!confirm("Are you sure you want to delete this item?")) return;

    try {
        const res = await fetch(`/api/delete_inventory_item/${itemId}`, {
            method: "DELETE"
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message);

        alert("Item deleted.");
        document.getElementById("editModal").classList.add("hidden");
        loadInventoryTable();
    } catch (err) {
        console.error("Delete failed:", err);
        alert("Failed to delete item.");
    }
});

// ======= CANCEL Edit =======
document.getElementById("cancelEdit").addEventListener("click", () => {
    document.getElementById("editModal").classList.add("hidden");
});

// ======= SAVE ALL SKUs =======
document.getElementById("saveAllSkusBtn").addEventListener("click", async function () {
    const itemId = document.getElementById("skuModal").dataset.itemId;
    const rows = document.querySelectorAll("#skuListContainer tbody tr");

    if (rows.length === 0) {
        alert("No SKUs to save.");
        return;
    }

    const updates = [];

    rows.forEach(row => {
        const skuId = row.dataset.skuId;
        const payload = {
            sku_code: row.querySelector(".sku-code").value.trim(),
            serial_number: row.querySelector(".sku-serial").value.trim(),
            status: row.querySelector(".sku-status").value,
            expiration_date: row.querySelector(".sku-exp").value || null
        };

        updates.push({skuId, payload});
    });

    try {
        for (const {skuId, payload} of updates) {
            const res = await fetch(`/api/update_sku/${skuId}`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.message);
        }

        alert("All SKUs saved.");
    } catch (err) {
        console.error("Save All failed:", err);
        alert("Failed to save all SKUs.");
    }
});

// ======= DELETE ALL SKUs =======
document.getElementById("deleteAllSkusBtn").addEventListener("click", async function () {
    const itemId = document.getElementById("skuModal").dataset.itemId;
    const rows = document.querySelectorAll("#skuListContainer tbody tr");

    if (rows.length === 0) {
        alert("No SKUs to delete.");
        return;
    }

    if (!confirm("Are you sure you want to delete ALL SKUs for this item? This cannot be undone.")) return;

    try {
        for (const row of rows) {
            const skuId = row.dataset.skuId;

            const res = await fetch(`/api/delete_sku/${skuId}`, {
                method: "DELETE"
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.message);
        }

        alert("All SKUs deleted.");
        loadSkuList(itemId);
    } catch (err) {
        console.error("Delete All failed:", err);
        alert("Failed to delete all SKUs.");
    }
});




