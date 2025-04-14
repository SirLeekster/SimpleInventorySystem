export function initSuppliers() {
    loadSuppliers();
    loadOrders();
    setupModalHandlers();
    setupFormSubmissions();
    setupSupplierRowActions();
    setupOrderRowActions();
}

function setupModalHandlers() {
    const addSupplierBtn = document.getElementById("addSupplierBtn");
    const closeAddSupplierModalBtn = document.getElementById("closeAddSupplierModal");
    const addSupplierModal = document.getElementById("addSupplierModal");

    if (addSupplierBtn && closeAddSupplierModalBtn && addSupplierModal) {
        addSupplierBtn.addEventListener("click", () => addSupplierModal.classList.remove("hidden"));
        closeAddSupplierModalBtn.addEventListener("click", () => addSupplierModal.classList.add("hidden"));
    }

    const placeOrderBtn = document.getElementById("placeOrderBtn");
    const closePlaceOrderModalBtn = document.getElementById("closePlaceOrderModal");
    const placeOrderModal = document.getElementById("placeOrderModal");

    if (placeOrderBtn && closePlaceOrderModalBtn && placeOrderModal) {
        placeOrderBtn.addEventListener("click", () => placeOrderModal.classList.remove("hidden"));
        closePlaceOrderModalBtn.addEventListener("click", () => placeOrderModal.classList.add("hidden"));
    }

    const closeEditSupplierModalBtn = document.getElementById("closeEditSupplierModal");
    const editSupplierModal = document.getElementById("editSupplierModal");
    if (closeEditSupplierModalBtn && editSupplierModal) {
        closeEditSupplierModalBtn.addEventListener("click", () => editSupplierModal.classList.add("hidden"));
    }

    const closeEditOrderModalBtn = document.getElementById("closeEditOrderModal");
    const editOrderModal = document.getElementById("editOrderModal");
    if (closeEditOrderModalBtn && editOrderModal) {
        closeEditOrderModalBtn.addEventListener("click", () => editOrderModal.classList.add("hidden"));
    }
}

function setupFormSubmissions() {
    const addSupplierForm = document.getElementById("addSupplierForm");
    if (addSupplierForm) {
        addSupplierForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("supplierName").value.trim();
            const phone = document.getElementById("supplierPhone").value.trim();
            const email = document.getElementById("supplierEmail").value.trim();
            const address = document.getElementById("supplierAddress").value.trim();
            const description = document.getElementById("supplierDescription").value.trim();

            if (!name) return alert("Supplier name is required.");

            try {
                const res = await fetch("/api/create_supplier", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name, phone, email, address, description})
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.message);

                alert(data.message);
                addSupplierForm.reset();
                document.getElementById("addSupplierModal").classList.add("hidden");
                loadSuppliers();
            } catch (err) {
                console.error("Failed to add supplier:", err);
                alert("Failed to add supplier.");
            }
        });
    }

    const editSupplierForm = document.getElementById("editSupplierForm");
    if (editSupplierForm) {
        editSupplierForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const id = document.getElementById("editSupplierId").value;
            const name = document.getElementById("editSupplierName").value.trim();
            const phone = document.getElementById("editSupplierPhone").value.trim();
            const email = document.getElementById("editSupplierEmail").value.trim();
            const address = document.getElementById("editSupplierAddress").value.trim();
            const description = document.getElementById("editSupplierDescription").value.trim();

            if (!name) return alert("Supplier name is required.");

            try {
                const res = await fetch(`/api/update_supplier/${id}`, {
                    method: "PATCH",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name, phone, email, address, description})
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.message);

                alert(data.message);
                editSupplierForm.reset();
                document.getElementById("editSupplierModal").classList.add("hidden");
                loadSuppliers();
            } catch (err) {
                console.error("Failed to update supplier:", err);
                alert("Failed to update supplier.");
            }
        });
    }

    const placeOrderForm = document.getElementById("placeOrderForm");
    if (placeOrderForm) {
        placeOrderForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const item_name = document.getElementById("orderItemName").value.trim();
            const supplier_id = document.getElementById("orderSupplier").value;
            const quantity = parseInt(document.getElementById("orderQuantity").value);
            const status = document.getElementById("orderStatus").value;

            if (!item_name || !quantity) return alert("Item name and quantity are required.");

            try {
                const res = await fetch("/api/create_order", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({item_name, supplier_id, quantity, status})
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.message);

                alert(data.message);
                placeOrderForm.reset();
                document.getElementById("placeOrderModal").classList.add("hidden");
                loadOrders();
            } catch (err) {
                console.error("Failed to place order:", err);
                alert("Failed to place order.");
            }
        });
    }

    const editOrderForm = document.getElementById("editOrderForm");
    if (editOrderForm) {
        editOrderForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const id = document.getElementById("editOrderId").value;
            const item_name = document.getElementById("editOrderItemName").value.trim();
            const supplier_id = document.getElementById("editOrderSupplier").value;
            const quantity = parseInt(document.getElementById("editOrderQuantity").value);
            const status = document.getElementById("editOrderStatus").value;

            if (!item_name || !quantity) return alert("Item name and quantity are required.");

            try {
                const res = await fetch(`/api/update_order/${id}`, {
                    method: "PATCH",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({item_name, supplier_id, quantity, status})
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.message);

                alert(data.message);
                editOrderForm.reset();
                document.getElementById("editOrderModal").classList.add("hidden");
                loadOrders();
            } catch (err) {
                console.error("Failed to update order:", err);
                alert("Failed to update order.");
            }
        });
    }
}

function setupSupplierRowActions() {
    document.getElementById("suppliersTableBody").addEventListener("click", (e) => {
        const target = e.target;

        if (target.classList.contains("edit-supplier-btn")) {
            document.getElementById("editSupplierId").value = target.dataset.id;
            document.getElementById("editSupplierName").value = target.dataset.name || '';
            document.getElementById("editSupplierPhone").value = target.dataset.phone || '';
            document.getElementById("editSupplierEmail").value = target.dataset.email || '';
            document.getElementById("editSupplierAddress").value = target.dataset.address || '';
            document.getElementById("editSupplierDescription").value = target.dataset.description || '';

            document.getElementById("editSupplierModal").classList.remove("hidden");
        }

        if (target.classList.contains("delete-supplier-btn")) {
            const id = target.dataset.id;
            if (!confirm("Delete this supplier?")) return;

            fetch(`/api/delete_supplier/${id}`, { method: "DELETE" })
                .then(res => res.json())
                .then(data => {
                    if (!data.message.toLowerCase().includes("deleted")) throw new Error(data.message);
                    alert("Supplier deleted.");
                    loadSuppliers();
                })
                .catch(err => {
                    console.error("Delete supplier failed:", err);
                    alert("Failed to delete supplier.");
                });
        }
    });
}

function setupOrderRowActions() {
    document.getElementById("ordersTableBody").addEventListener("click", async (e) => {
        const target = e.target;
        const row = target.closest("tr");

        if (target.classList.contains("edit-order-btn")) {
            const id = target.dataset.id;

            const item = row.children[1].textContent;
            const supplierName = row.children[2].textContent;
            const status = row.children[3].textContent;
            const quantity = parseInt(row.children[4].textContent);

            document.getElementById("editOrderId").value = id;
            document.getElementById("editOrderItemName").value = item;
            document.getElementById("editOrderQuantity").value = quantity;
            document.getElementById("editOrderStatus").value = status;

            await populateEditOrderSuppliersDropdown(supplierName);
            document.getElementById("editOrderModal").classList.remove("hidden");
        }

        if (target.classList.contains("delete-order-btn")) {
            const id = target.dataset.id;
            if (!confirm("Delete this order?")) return;

            try {
                const res = await fetch(`/api/delete_order/${id}`, { method: "DELETE" });
                const data = await res.json();
                if (!res.ok) throw new Error(data.message);
                alert("Order deleted.");
                loadOrders();
            } catch (err) {
                console.error("Delete order failed:", err);
                alert("Failed to delete order.");
            }
        }
    });
}

async function populateEditOrderSuppliersDropdown(selectedName) {
    const dropdown = document.getElementById("editOrderSupplier");
    dropdown.innerHTML = '<option value="">Select a supplier</option>';

    try {
        const res = await fetch("/api/suppliers");
        const suppliers = await res.json();
        suppliers.forEach(s => {
            const opt = document.createElement("option");
            opt.value = s.supplier_id;
            opt.textContent = s.name;
            if (s.name === selectedName) opt.selected = true;
            dropdown.appendChild(opt);
        });
    } catch (err) {
        console.error("Failed to load suppliers for order modal:", err);
    }
}

function loadSuppliers() {
    const tableBody = document.getElementById("suppliersTableBody");
    const supplierDropdown = document.getElementById("orderSupplier");
    tableBody.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";
    if (supplierDropdown) supplierDropdown.innerHTML = '<option value="">Select a supplier</option>';

    fetch("/api/suppliers")
        .then(res => res.json())
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                tableBody.innerHTML = "<tr><td colspan='6'>No suppliers found.</td></tr>";
                return;
            }

            tableBody.innerHTML = "";
            data.forEach(supplier => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${supplier.name}</td>
                    <td>${supplier.phone || '-'}</td>
                    <td>${supplier.email || '-'}</td>
                    <td>${supplier.address || '-'}</td>
                    <td>${supplier.description || '-'}</td>
                    <td>
                        <button class="button small edit-supplier-btn"
                                data-id="${supplier.supplier_id}"
                                data-name="${supplier.name}"
                                data-phone="${supplier.phone || ''}"
                                data-email="${supplier.email || ''}"
                                data-address="${supplier.address || ''}"
                                data-description="${supplier.description || ''}">
                            Edit
                        </button>
                        <button class="button small delete-supplier-btn delete-btn" data-id="${supplier.supplier_id}">Delete</button>
                    </td>
                `;

                tableBody.appendChild(row);

                if (supplierDropdown) {
                    const opt = document.createElement("option");
                    opt.value = supplier.supplier_id;
                    opt.textContent = supplier.name;
                    supplierDropdown.appendChild(opt);
                }
            });
        })
        .catch(err => {
            console.error("Failed to load suppliers:", err);
            tableBody.innerHTML = "<tr><td colspan='6'>Error loading suppliers.</td></tr>";
        });
}

function loadOrders() {
    const tableBody = document.getElementById("ordersTableBody");
    tableBody.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";

    fetch("/api/supplier_orders")
        .then(res => res.json())
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                tableBody.innerHTML = "<tr><td colspan='6'>No orders found.</td></tr>";
                return;
            }

            tableBody.innerHTML = "";
            data.forEach(order => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${order.item_name}</td>
                    <td>${order.supplier_name}</td>
                    <td>${order.status}</td>
                    <td>${new Date(order.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="button small edit-order-btn" data-id="${order.order_id}">Edit</button>
                        <button class="button small delete-order-btn delete-btn" data-id="${order.order_id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(err => {
            console.error("Failed to load supplier orders:", err);
            tableBody.innerHTML = "<tr><td colspan='6'>Error loading orders.</td></tr>";
        });
}
