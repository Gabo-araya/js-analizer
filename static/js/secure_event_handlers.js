// Secure Event Handlers - Replacing inline JavaScript
// This file contains secure event handlers to replace onclick attributes
// and prevent XSS vulnerabilities from inline JavaScript execution.

// Debug logging (set to false in production)
const DEBUG_MODE = true; // TODO: Set to false in production
const debugLog = DEBUG_MODE ? console.log : () => {};
const debugError = DEBUG_MODE ? console.error : () => {};

document.addEventListener('DOMContentLoaded', function() {
    
    // Edit Scan Project Handlers with debug and error handling
    const editScanProjectBtns = document.querySelectorAll('.edit-scan-project-btn');
    debugLog('🔍 Found edit scan project buttons:', editScanProjectBtns.length);
    
    editScanProjectBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            debugLog('🔧 Edit scan project clicked');
            
            const scanId = this.dataset.scanId;
            const projectId = this.dataset.projectId;
            const scanTitle = this.dataset.scanTitle;
            
            debugLog('📋 Data:', {scanId, projectId, scanTitle});
            
            // Find required elements with validation
            const elements = {
                editScanName: document.getElementById("editScanName"),
                editScanProjectForm: document.getElementById("editScanProjectForm"),
                scanProjectSelect: document.getElementById("scanProjectSelect"),
                editScanProjectModal: document.getElementById("editScanProjectModal")
            };
            
            // Debug: Check element existence
            const missingElements = [];
            Object.entries(elements).forEach(([name, element]) => {
                if (!element) {
                    missingElements.push(name);
                    console.error(`❌ Missing element: ${name}`);
                } else {
                    console.log(`✅ Found element: ${name}`);
                }
            });
            
            // Only proceed if all critical elements exist
            if (missingElements.length > 0) {
                console.error('❌ Cannot proceed: missing elements:', missingElements);
                alert('Error: No se pueden cargar los elementos necesarios. Por favor recarga la página.');
                return;
            }
            
            try {
                // Secure implementation
                if (elements.editScanName && scanTitle) {
                    elements.editScanName.textContent = scanTitle; // textContent prevents XSS
                    console.log('✅ Set scan name');
                }
                
                if (elements.editScanProjectForm && scanId) {
                    elements.editScanProjectForm.action = "/update-scan-project-dashboard/" + encodeURIComponent(scanId);
                    console.log('✅ Set form action');
                }
                
                if (elements.scanProjectSelect) {
                    elements.scanProjectSelect.value = projectId || "";
                    console.log('✅ Set project select value');
                }
                
                if (elements.editScanProjectModal && typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(elements.editScanProjectModal);
                    modal.show();
                    console.log('✅ Modal shown');
                } else {
                    throw new Error('Bootstrap not available or modal element missing');
                }
                
            } catch (error) {
                console.error('❌ Error in edit scan project handler:', error);
                alert('Error: No se pudo abrir el modal. Por favor recarga la página.');
            }
        });
    });

    // Delete Scan Handlers
    const deleteScanBtns = document.querySelectorAll('.delete-scan-btn');
    debugLog('🔍 Found delete scan buttons:', deleteScanBtns.length);
    
    deleteScanBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            debugLog('🔧 Delete scan clicked');
            const scanId = this.dataset.scanId;
            const scanTitle = this.dataset.scanTitle;
            debugLog('📋 Delete scan data:', {scanId, scanTitle});
            
            // Secure implementation without relying on inline functions
            const deleteScanNameElement = document.getElementById("deleteScanName");
            const deleteScanForm = document.getElementById("deleteScanForm");
            const deleteScanModal = document.getElementById("deleteScanModal");
            
            if (deleteScanNameElement && scanTitle) {
                deleteScanNameElement.textContent = scanTitle; // textContent prevents XSS
            }
            
            if (deleteScanForm && scanId) {
                deleteScanForm.action = "/delete-scan/" + encodeURIComponent(scanId);
            }
            
            if (deleteScanModal && typeof bootstrap !== 'undefined') {
                const modal = new bootstrap.Modal(deleteScanModal);
                modal.show();
                debugLog('✅ Delete scan modal shown');
            } else {
                debugError('❌ Bootstrap or modal element missing');
                debugError('deleteScanModal exists:', !!deleteScanModal);
                debugError('bootstrap available:', typeof bootstrap !== 'undefined');
            }
        });
    });

    // User Management Handlers (if functions exist)
    if (typeof changePassword === 'function') {
        const changePasswordBtns = document.querySelectorAll('[data-bs-target="#changePasswordModal"]');
        changePasswordBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const userId = this.dataset.userId;
                const username = this.dataset.username;
                changePassword(userId, username);
            });
        });
    }

    if (typeof changeRole === 'function') {
        const changeRoleBtns = document.querySelectorAll('[data-bs-target="#changeRoleModal"]');
        changeRoleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const userId = this.dataset.userId;
                const username = this.dataset.username;
                const currentRole = this.dataset.currentRole;
                changeRole(userId, username, currentRole);
            });
        });
    }

    // History/Historial Handlers (if functions exist)
    if (typeof viewDetails === 'function') {
        const viewDetailsBtns = document.querySelectorAll('.view-details-btn');
        viewDetailsBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const recordId = this.dataset.recordId;
                viewDetails(recordId);
            });
        });
    }

    if (typeof undoAction === 'function') {
        const undoActionBtns = document.querySelectorAll('.undo-action-btn');
        undoActionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const recordId = this.dataset.recordId;
                undoAction(recordId);
            });
        });
    }

    if (typeof exportHistory === 'function') {
        const exportHistoryBtns = document.querySelectorAll('.export-history-btn');
        exportHistoryBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                exportHistory();
            });
        });
    }

    // Print handlers
    const printBtns = document.querySelectorAll('.print-button');
    printBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            window.print();
        });
    });

    // Form submission handlers with confirmation
    const confirmDeleteForms = document.querySelectorAll('[data-confirm-message]');
    confirmDeleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.dataset.confirmMessage;
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Button confirmation handlers
    const confirmDeleteBtns = document.querySelectorAll('button[data-confirm-message]');
    confirmDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const message = this.dataset.confirmMessage;
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Bulk edit client handler with full implementation
    const bulkEditProjectBtns = document.querySelectorAll('.bulk-edit-project-btn');
    console.log('🔍 Found bulk edit project buttons:', bulkEditProjectBtns.length);
    
    bulkEditProjectBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('🔧 Bulk edit project clicked');
            
            try {
                const checkedBoxes = document.querySelectorAll('.scan-checkbox:checked');
                const scanIds = Array.from(checkedBoxes).map(checkbox => checkbox.value);
                
                console.log('📋 Selected scans:', scanIds.length);
                
                if (scanIds.length === 0) {
                    alert('Por favor selecciona al menos un escaneo.');
                    return;
                }
                
                // Find required elements
                const bulkScanIdsElement = document.getElementById('bulkScanIds');
                const bulkSelectedCountElement = document.getElementById('bulkSelectedCount');
                const bulkEditProjectModal = document.getElementById('bulkEditProjectModal');
                
                if (!bulkScanIdsElement || !bulkSelectedCountElement || !bulkEditProjectModal) {
                    console.error('❌ Missing bulk edit elements');
                    alert('Error: No se pueden cargar los elementos necesarios.');
                    return;
                }
                
                // Set values securely
                bulkScanIdsElement.value = scanIds.join(',');
                bulkSelectedCountElement.textContent = scanIds.length.toString();
                
                // Show modal
                if (typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(bulkEditProjectModal);
                    modal.show();
                    console.log('✅ Bulk edit modal shown');
                } else {
                    throw new Error('Bootstrap not available');
                }
                
            } catch (error) {
                console.error('❌ Error in bulk edit handler:', error);
                alert('Error: No se pudo abrir el modal de edición masiva.');
            }
        });
    });

    // Project modal handlers
    const editProjectBtns = document.querySelectorAll('[data-bs-target="#editProjectModal"]');
    editProjectBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // This data is passed through data attributes securely
            const projectId = this.dataset.projectId;
            const projectName = this.dataset.projectName;
            const projectDescription = this.dataset.projectDescription;
            const projectEmail = this.dataset.projectEmail;
            const projectPhone = this.dataset.projectPhone;
            const projectWebsite = this.dataset.projectWebsite;
            
            // Safely populate modal fields (these are already escaped in HTML)
            if (projectId) {
                const form = document.getElementById('editProjectForm');
                if (form) {
                    form.action = '/edit-project/' + encodeURIComponent(projectId);
                }
                
                const nameField = document.getElementById('edit_name');
                if (nameField && projectName) nameField.value = projectName;
                
                const descField = document.getElementById('edit_description');
                if (descField && projectDescription) descField.value = projectDescription;
                
                const emailField = document.getElementById('edit_contact_email');
                if (emailField && projectEmail) emailField.value = projectEmail;
                
                const phoneField = document.getElementById('edit_contact_phone');
                if (phoneField && projectPhone) phoneField.value = projectPhone;
                
                const websiteField = document.getElementById('edit_website');
                if (websiteField && projectWebsite) websiteField.value = projectWebsite;
            }
        });
    });

    const deleteProjectBtns = document.querySelectorAll('[data-bs-target="#deleteProjectModal"]');
    deleteProjectBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const projectId = this.dataset.projectId;
            const projectName = this.dataset.projectName;
            
            if (projectId && projectName) {
                const form = document.getElementById('deleteProjectForm');
                if (form) {
                    form.action = '/delete-project/' + encodeURIComponent(projectId);
                }
                
                const nameSpan = document.getElementById('deleteProjectName');
                if (nameSpan) {
                    nameSpan.textContent = projectName; // textContent is safe from XSS
                }
            }
        });
    });
});

// Utility function to safely update text content (prevents XSS)
function setSecureTextContent(elementId, text) {
    const element = document.getElementById(elementId);
    if (element && text) {
        element.textContent = text; // textContent escapes HTML automatically
    }
}

// Utility function to safely set form action URLs
function setSecureFormAction(formId, actionPath) {
    const form = document.getElementById(formId);
    if (form && actionPath) {
        form.action = actionPath; // This should already be sanitized server-side
    }
}