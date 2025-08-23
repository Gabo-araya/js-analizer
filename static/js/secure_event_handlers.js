// Secure Event Handlers - Replacing inline JavaScript
// This file contains secure event handlers to replace onclick attributes
// and prevent XSS vulnerabilities from inline JavaScript execution.

// Debug logging (set to false in production)
const DEBUG_MODE = true; // TODO: Set to false in production
const debugLog = DEBUG_MODE ? console.log : () => {};
const debugError = DEBUG_MODE ? console.error : () => {};

document.addEventListener('DOMContentLoaded', function() {
    
    // Edit Scan Client Handlers with debug and error handling
    const editScanClientBtns = document.querySelectorAll('.edit-scan-client-btn');
    debugLog('🔍 Found edit scan client buttons:', editScanClientBtns.length);
    
    editScanClientBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            debugLog('🔧 Edit scan client clicked');
            
            const scanId = this.dataset.scanId;
            const clientId = this.dataset.clientId;
            const scanTitle = this.dataset.scanTitle;
            
            debugLog('📋 Data:', {scanId, clientId, scanTitle});
            
            // Find required elements with validation
            const elements = {
                editScanName: document.getElementById("editScanName"),
                editScanClientForm: document.getElementById("editScanClientForm"),
                scanClientSelect: document.getElementById("scanClientSelect"),
                editScanClientModal: document.getElementById("editScanClientModal")
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
                
                if (elements.editScanClientForm && scanId) {
                    elements.editScanClientForm.action = "/update-scan-project-dashboard/" + encodeURIComponent(scanId);
                    console.log('✅ Set form action');
                }
                
                if (elements.scanClientSelect) {
                    elements.scanClientSelect.value = clientId || "";
                    console.log('✅ Set client select value');
                }
                
                if (elements.editScanClientModal && typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(elements.editScanClientModal);
                    modal.show();
                    console.log('✅ Modal shown');
                } else {
                    throw new Error('Bootstrap not available or modal element missing');
                }
                
            } catch (error) {
                console.error('❌ Error in edit scan client handler:', error);
                alert('Error: No se pudo abrir el modal. Por favor recarga la página.');
            }
        });
    });

    // Delete Scan Handlers
    const deleteScanBtns = document.querySelectorAll('.delete-scan-btn');
    deleteScanBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const scanId = this.dataset.scanId;
            const scanTitle = this.dataset.scanTitle;
            
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
    const bulkEditClientBtns = document.querySelectorAll('.bulk-edit-client-btn');
    console.log('🔍 Found bulk edit client buttons:', bulkEditClientBtns.length);
    
    bulkEditClientBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('🔧 Bulk edit client clicked');
            
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
                const bulkEditClientModal = document.getElementById('bulkEditClientModal');
                
                if (!bulkScanIdsElement || !bulkSelectedCountElement || !bulkEditClientModal) {
                    console.error('❌ Missing bulk edit elements');
                    alert('Error: No se pueden cargar los elementos necesarios.');
                    return;
                }
                
                // Set values securely
                bulkScanIdsElement.value = scanIds.join(',');
                bulkSelectedCountElement.textContent = scanIds.length.toString();
                
                // Show modal
                if (typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(bulkEditClientModal);
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

    // Client modal handlers
    const editClientBtns = document.querySelectorAll('[data-bs-target="#editClientModal"]');
    editClientBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // This data is passed through data attributes securely
            const clientId = this.dataset.clientId;
            const clientName = this.dataset.clientName;
            const clientDescription = this.dataset.clientDescription;
            const clientEmail = this.dataset.clientEmail;
            const clientPhone = this.dataset.clientPhone;
            const clientWebsite = this.dataset.clientWebsite;
            
            // Safely populate modal fields (these are already escaped in HTML)
            if (clientId) {
                const form = document.getElementById('editClientForm');
                if (form) {
                    form.action = '/edit-client/' + encodeURIComponent(clientId);
                }
                
                const nameField = document.getElementById('edit_name');
                if (nameField && clientName) nameField.value = clientName;
                
                const descField = document.getElementById('edit_description');
                if (descField && clientDescription) descField.value = clientDescription;
                
                const emailField = document.getElementById('edit_contact_email');
                if (emailField && clientEmail) emailField.value = clientEmail;
                
                const phoneField = document.getElementById('edit_contact_phone');
                if (phoneField && clientPhone) phoneField.value = clientPhone;
                
                const websiteField = document.getElementById('edit_website');
                if (websiteField && clientWebsite) websiteField.value = clientWebsite;
            }
        });
    });

    const deleteClientBtns = document.querySelectorAll('[data-bs-target="#deleteClientModal"]');
    deleteClientBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const clientId = this.dataset.clientId;
            const clientName = this.dataset.clientName;
            
            if (clientId && clientName) {
                const form = document.getElementById('deleteClientForm');
                if (form) {
                    form.action = '/delete-client/' + encodeURIComponent(clientId);
                }
                
                const nameSpan = document.getElementById('deleteClientName');
                if (nameSpan) {
                    nameSpan.textContent = clientName; // textContent is safe from XSS
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