// Index page JavaScript functionality

// Handle URL analysis form submission with loading indicator
document.getElementById('analyzeUrlForm').addEventListener('submit', function(e) {
    // Show loading state in modal
    document.getElementById('analyzeButtonText').classList.add('d-none');
    document.getElementById('analyzeButtonSpinner').classList.remove('d-none');
    
    // Disable buttons to prevent double submission
    document.getElementById('analyzeButton').disabled = true;
    document.querySelector('[data-bs-dismiss="modal"]').disabled = true;
    document.querySelector('.btn-close').disabled = true;
    
    // Show overlay immediately without hiding modal first
    document.getElementById('loadingOverlay').classList.add('active');
    
    // Hide the modal after form submission has started
    setTimeout(function() {
        let modal = bootstrap.Modal.getInstance(document.getElementById('addUrlModal'));
        if (modal) {
            modal.hide();
        }
    }, 100); // Reduced delay to allow form submission to complete first
});

// Handle batch analysis form submission
document.getElementById('batchAnalyzeForm').addEventListener('submit', function(e) {
    // Count URLs for validation
    const urlsText = document.getElementById('urlsTextarea').value.trim();
    const lines = urlsText.split('\n');
    const urls = lines.filter(line => {
        const trimmed = line.trim();
        return trimmed && !trimmed.startsWith('#');
    });
    
    if (urls.length === 0) {
        e.preventDefault();
        alert('Por favor ingresa al menos una URL válida');
        return;
    }
    
    if (urls.length > 50) {
        if (!confirm(`Estás a punto de analizar ${urls.length} URLs. Esto puede tomar mucho tiempo. ¿Estás seguro de que quieres continuar?`)) {
            e.preventDefault();
            return;
        }
    }
    
    // Show loading state
    document.getElementById('batchAnalyzeButtonText').classList.add('d-none');
    document.getElementById('batchAnalyzeButtonSpinner').classList.remove('d-none');
    
    // Disable buttons
    document.getElementById('batchAnalyzeButton').disabled = true;
    document.querySelector('[data-bs-dismiss="modal"]').disabled = true;
    document.querySelector('#batchAnalyzeModal .btn-close').disabled = true;
    
    // Show overlay immediately and update text for batch analysis
    document.getElementById('loadingOverlay').classList.add('active');
    document.querySelector('#loadingOverlay h5').textContent = `Analizando ${urls.length} URLs...`;
    document.querySelector('#loadingOverlay p').textContent = 'Esto puede tomar varios minutos';
    
    // Hide modal after form submission has started
    setTimeout(function() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('batchAnalyzeModal'));
        if (modal) {
            modal.hide();
        }
    }, 100);
});

// Reset form when modal is hidden
document.getElementById('addUrlModal').addEventListener('hidden.bs.modal', function () {
    // Reset form
    document.getElementById('analyzeUrlForm').reset();
    
    // Reset button state
    document.getElementById('analyzeButtonText').classList.remove('d-none');
    document.getElementById('analyzeButtonSpinner').classList.add('d-none');
    document.getElementById('analyzeButton').disabled = false;
    document.querySelector('[data-bs-dismiss="modal"]').disabled = false;
    document.querySelector('.btn-close').disabled = false;
});

// Reset batch analyze form when modal is hidden
document.getElementById('batchAnalyzeModal').addEventListener('hidden.bs.modal', function () {
    // Reset form
    document.getElementById('batchAnalyzeForm').reset();
    
    // Reset button state
    document.getElementById('batchAnalyzeButtonText').classList.remove('d-none');
    document.getElementById('batchAnalyzeButtonSpinner').classList.add('d-none');
    document.getElementById('batchAnalyzeButton').disabled = false;
    document.querySelector('#batchAnalyzeModal [data-bs-dismiss="modal"]').disabled = false;
    document.querySelector('#batchAnalyzeModal .btn-close').disabled = false;
});

// Function to hide loading overlay
function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Hide overlay when page loads (analysis completed)
window.addEventListener('load', function() {
    hideLoadingOverlay();
});

// Hide overlay when page becomes visible (for browser back/forward navigation)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        hideLoadingOverlay();
    }
});

// Emergency fallback: Hide overlay after 5 minutes maximum
setTimeout(function() {
    hideLoadingOverlay();
}, 300000); // 5 minutes

// Handle bulk edit project button
document.addEventListener('DOMContentLoaded', function() {
    const bulkEditBtn = document.getElementById('bulk-edit-project-btn');
    const bulkEditModal = document.getElementById('bulkEditProjectModal');
    
    if (bulkEditBtn && bulkEditModal) {
        bulkEditModal.addEventListener('show.bs.modal', function(event) {
            // Get all selected scan IDs
            const checkedBoxes = document.querySelectorAll('.scan-checkbox:checked');
            const scanIds = Array.from(checkedBoxes).map(cb => cb.value);
            
            // Update hidden input with scan IDs
            const scanIdsInput = document.getElementById('bulkScanIds');
            if (scanIdsInput) {
                scanIdsInput.value = scanIds.join(',');
            }
            
            // Update selected count display
            const selectedCountSpan = document.getElementById('bulkSelectedCount');
            if (selectedCountSpan) {
                selectedCountSpan.textContent = scanIds.length;
            }
        });
    }

    // Handle bulk delete button
    const bulkDeleteBtn = document.getElementById('bulk-delete-scans-btn');
    const bulkDeleteModal = document.getElementById('bulkDeleteModal');
    
    if (bulkDeleteBtn && bulkDeleteModal) {
        bulkDeleteModal.addEventListener('show.bs.modal', function(event) {
            // Get all selected scan IDs and their URLs
            const checkedBoxes = document.querySelectorAll('.scan-checkbox:checked');
            const scanIds = Array.from(checkedBoxes).map(cb => cb.value);
            const scanUrls = Array.from(checkedBoxes).map(cb => {
                // Find the URL in the same row as the checkbox
                const row = cb.closest('tr');
                const urlCell = row.querySelector('td:nth-child(2)') || row.querySelector('td:nth-child(3)');
                return urlCell ? urlCell.textContent.trim().substring(0, 50) + '...' : 'URL no encontrada';
            });
            
            // Update hidden input with scan IDs
            const bulkDeleteScanIds = document.getElementById('bulkDeleteScanIds');
            if (bulkDeleteScanIds) {
                bulkDeleteScanIds.value = scanIds.join(',');
            }
            
            // Update selected count display
            const deleteSelectedCount = document.getElementById('deleteSelectedCount');
            if (deleteSelectedCount) {
                deleteSelectedCount.textContent = scanIds.length;
            }
            
            // Update scan list display
            const scanList = document.getElementById('bulkDeleteScanList');
            if (scanList) {
                scanList.innerHTML = '';
                for (let i = 0; i < Math.min(scanIds.length, 10); i++) {
                    const li = document.createElement('li');
                    li.className = 'list-group-item small';
                    li.innerHTML = `<strong>#${scanIds[i]}</strong>: ${scanUrls[i]}`;
                    scanList.appendChild(li);
                }
                
                if (scanIds.length > 10) {
                    const li = document.createElement('li');
                    li.className = 'list-group-item small text-muted';
                    li.innerHTML = `<em>... y ${scanIds.length - 10} más</em>`;
                    scanList.appendChild(li);
                }
            }
        });
    }
});