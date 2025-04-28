// handles dashboard navigation and section switching
// initializes page specific logic based on sidebar selection
// saves last visited section in local storage and restores it on reload
// loads current user role from server to adjust access control


import {initOverview} from './dashboard-overview.js';
import {initAddItem} from './dashboard-add-item.js';
import {initManageItems} from './dashboard-manage-items.js';
import {initReports} from './dashboard-reports.js';
import {initSettings} from './dashboard-settings.js';
import {initSuppliers} from './suppliers_&_orders.js';

function showSection(sectionId) {
    const contentSections = document.querySelectorAll(".content-section");
    contentSections.forEach(section => {
        section.classList.add("hidden");
        section.classList.remove("fade-in");
    });

    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove("hidden");

        void section.offsetWidth;

        section.classList.add("fade-in");
        localStorage.setItem("lastDashboardSection", sectionId);
    }
}


function setupSidebarNavigation() {
    const sidebarLinks = document.querySelectorAll(".sidebar-menu li a");

    sidebarLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.id;

            switch (targetId) {
                case "overviewMenu":
                    showSection("dashboardOverview");
                    initOverview();
                    break;
                case "addItemMenu":
                    showSection("addInventoryItem");
                    initAddItem();
                    break;
                case "manageItemsMenu":
                    showSection("manageItems");
                    initManageItems();
                    break;
                case "salesReportsMenu":
                    showSection("reports");
                    initReports();
                    break;
                case "settingsMenu":
                    showSection("settings");
                    initSettings();
                    break;
                case "suppliersMenu":
                    showSection("suppliersSection");
                    initSuppliers();
                    break;
                case "logoutLink":
                    localStorage.removeItem("lastDashboardSection");
                    window.location.href = "/logout";
                    break;
                default:
                    showSection("dashboardOverview");
                    initOverview();
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    setupSidebarNavigation();

    try {
        const res = await fetch('/api/user/profile');
        if (!res.ok) throw new Error('Failed to load profile');

        const user = await res.json();
        window.currentUserRole = user.role;
        window.isAdmin = user.role === 'admin';
    } catch (err) {
        console.error("Failed to load user role:", err);
        window.currentUserRole = null;
        window.isAdmin = false;
    }

    const lastSection = localStorage.getItem("lastDashboardSection") || "dashboardOverview";
    showSection(lastSection);

    switch (lastSection) {
        case "dashboardOverview":
            initOverview();
            break;
        case "addInventoryItem":
            initAddItem();
            break;
        case "manageItems":
            initManageItems();
            break;
        case "reports":
            initReports();
            break;
        case "settings":
            initSettings();
            break;
        case "suppliersSection":
            initSuppliers();
            break;
        default:
            initOverview();
    }
});
