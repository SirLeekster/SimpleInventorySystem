// ==============================
// Add Inventory Item Section
// ==============================

export function initAddItem() {
    const form = document.getElementById("addInventoryForm");
    if (form) {
        form.addEventListener("submit", handleAddItemSubmit);
    }

    const imageInput = document.getElementById("image");
    if (imageInput) {
        imageInput.addEventListener("change", function () {
            const fileName = this.files[0] ? this.files[0].name : "Choose Image";
            this.nextElementSibling.textContent = fileName;
        });
    }

    const upcBtn = document.getElementById("upcLookupBtn");
    if (upcBtn) {
        upcBtn.addEventListener("click", handleUpcLookup);
    }
}

async function handleAddItemSubmit(e) {
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
        description,
        category,
        quantity,
        price
    };

    try {
        const response = await fetch("/api/create_inventory_item", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.status === 403) {
            alert("Permission denied: You do not have access to add inventory items.");
            return;
        }

        if (!response.ok) {
            alert("Error: " + result.message);
            return;
        }

        alert(result.message);

        const itemId = result.item_id;
        const imageInput = document.getElementById("image");

        if (imageInput.files.length > 0) {
            const imageFormData = new FormData();
            imageFormData.append("image", imageInput.files[0]);

            try {
                const imgRes = await fetch(`/api/upload_inventory_image/${itemId}`, {
                    method: "POST",
                    body: imageFormData
                });

                const imgResult = await imgRes.json();
                if (imgRes.status === 403) {
                    alert("Permission denied: You do not have access to upload images.");
                    return;
                }

                if (!imgRes.ok) {
                    console.error("Image upload error:", imgResult.message);
                }
            } catch (imgErr) {
                console.error("Image upload failed:", imgErr);
            }
        }

        document.getElementById("addInventoryForm").reset();
        document.querySelector(".custom-file-label").textContent = "Choose Image";

    } catch (err) {
        console.error("Add item failed:", err);
        alert("An error occurred while adding the item.");
    }
}

async function handleUpcLookup() {
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

        document.getElementById("productName").value = data.product_name || '';
        document.getElementById("description").value = data.description || '';
        document.getElementById("category").value = data.category || 'General';
        document.getElementById("price").value = data.price || '';

        alert("Fields auto-filled from UPC.");
    } catch (err) {
        console.error("UPC lookup failed:", err);
        alert("An error occurred during UPC lookup.");
    }
}
