// Scan Detail page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {

    // Handle hash navigation for tabs
    function activateTabFromHash() {
        const hash = window.location.hash;
        if (hash) {
            // Remove the # from hash
            const tabId = hash.substring(1);
            
            // Map of hash names to tab IDs
            const tabMapping = {
                'libraries': 'libraries-tab',
                'files': 'files-tab',
                'versions': 'versions-tab',
                'summary': 'summary-tab'
            };
            
            const targetTabId = tabMapping[tabId];
            if (targetTabId) {
                // Get the tab button element
                const tabButton = document.getElementById(targetTabId);
                if (tabButton) {
                    // Activate the tab using Bootstrap's tab API
                    const tab = new bootstrap.Tab(tabButton);
                    tab.show();
                }
            }
        }
    }
    
    // Activate tab on page load
    activateTabFromHash();
    
    // Handle hash changes (back/forward navigation)
    window.addEventListener('hashchange', activateTabFromHash);

    // Handle version string deletion modal
    document.getElementById('deleteVersionStringModal').addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var vsId = button.getAttribute('data-vs-id');
        var vsFile = button.getAttribute('data-vs-file');
        var vsLines = parseInt(button.getAttribute('data-vs-lines')) || 1;
        var vsContent = button.getAttribute('data-vs-content');
        
        // Update modal content
        document.getElementById('modal-vs-file').textContent = vsFile;
        document.getElementById('modal-vs-lines').textContent = vsLines === 1 ? vsLines + ' línea' : vsLines + ' líneas';
        document.getElementById('modal-vs-content').textContent = vsContent;
        
        // Update modal description text based on singular/plural
        const description = document.getElementById('modal-vs-description');
        if (vsLines === 1) {
            description.textContent = '¿Estás seguro de que quieres eliminar la siguiente cadena de versión?';
        } else {
            description.textContent = `¿Estás seguro de que quieres eliminar las ${vsLines} cadenas de versión de este archivo?`;
        }
        
        // Update form action
        document.getElementById('deleteVersionStringForm').action = '/delete-version-string/' + vsId;
    });
    
    // Checkbox handling for version strings
    const vsCheckboxes = document.querySelectorAll('.version-string-checkbox');
    const selectAllVs = document.getElementById('selectAllVersionStrings');
    const batchDeleteVsBtn = document.getElementById('batchDeleteVersionStringsBtn');
    const selectedVsCount = document.getElementById('selectedVersionStringsCount');
    
    // Handle select all version strings
    if (selectAllVs) {
        selectAllVs.addEventListener('change', function() {
            vsCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllVs.checked;
            });
            updateVersionStringsSelection();
        });
    }

    // Handle individual version string checkboxes
    vsCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateVersionStringsSelection);
    });
    
    function updateVersionStringsSelection() {
        const checkedVs = document.querySelectorAll('.version-string-checkbox:checked');
        const count = checkedVs.length;
        
        selectedVsCount.textContent = count;
        
        if (count > 0) {
            batchDeleteVsBtn.classList.remove('d-none');
        } else {
            batchDeleteVsBtn.classList.add('d-none');
        }
        
        // Update select all checkbox state
        if (vsCheckboxes.length > 0) {
            selectAllVs.indeterminate = count > 0 && count < vsCheckboxes.length;
            selectAllVs.checked = count === vsCheckboxes.length;
        }
    }
    
    // Checkbox handling for file URLs
    const fileCheckboxes = document.querySelectorAll('.file-url-checkbox');
    const selectAllFiles = document.getElementById('selectAllFileUrls');
    const batchDeleteFilesBtn = document.getElementById('batchDeleteFileUrlsBtn');
    const selectedFilesCount = document.getElementById('selectedFileUrlsCount');
    
    // Handle select all file URLs
    if (selectAllFiles) {
        selectAllFiles.addEventListener('change', function() {
            fileCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllFiles.checked;
            });
            updateFileUrlsSelection();
        });
    }
    
    // Handle individual file URL checkboxes
    fileCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateFileUrlsSelection);
    });
    
    function updateFileUrlsSelection() {
        const checkedFiles = document.querySelectorAll('.file-url-checkbox:checked');
        const count = checkedFiles.length;
        
        selectedFilesCount.textContent = count;
        
        if (count > 0) {
            batchDeleteFilesBtn.classList.remove('d-none');
        } else {
            batchDeleteFilesBtn.classList.add('d-none');
        }
        
        // Update select all checkbox state
        if (fileCheckboxes.length > 0) {
            selectAllFiles.indeterminate = count > 0 && count < fileCheckboxes.length;
            selectAllFiles.checked = count === fileCheckboxes.length;
        }
    }
    
    // Handle batch delete version strings modal
    document.getElementById('batchDeleteVersionStringsModal').addEventListener('show.bs.modal', function () {
        const checkedVs = document.querySelectorAll('.version-string-checkbox:checked');
        const count = checkedVs.length;
        
        document.getElementById('batchVsCount').textContent = count;
        
        // Clear previous form inputs
        const form = document.getElementById('batchDeleteVersionStringsForm');
        const existingInputs = form.querySelectorAll('input[name="version_string_ids[]"]');
        existingInputs.forEach(input => input.remove());
        
        // Add hidden inputs and build preview
        let previewHtml = '<ul class="mb-0">';
        checkedVs.forEach(checkbox => {
            // Handle multiple IDs per checkbox (comma-separated)
            const ids = checkbox.value.split(',');
            ids.forEach(id => {
                if (id.trim()) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'version_string_ids[]';
                    input.value = id.trim();
                    form.appendChild(input);
                }
            });
            
            const file = checkbox.getAttribute('data-vs-file');
            const lines = parseInt(checkbox.getAttribute('data-vs-lines')) || 1;
            const content = checkbox.getAttribute('data-vs-content');
            const linesText = lines === 1 ? '1 línea' : lines + ' líneas';
            previewHtml += `<li><strong>${linesText}:</strong> ${file}<br><code class="text-muted small">${content}</code></li>`;
        });
        previewHtml += '</ul>';
        
        document.getElementById('batchVsPreview').innerHTML = previewHtml;
    });
    
    // Handle batch delete file URLs modal
    document.getElementById('batchDeleteFileUrlsModal').addEventListener('show.bs.modal', function () {
        const checkedFiles = document.querySelectorAll('.file-url-checkbox:checked');
        const count = checkedFiles.length;
        
        document.getElementById('batchFileCount').textContent = count;
        
        // Clear previous form inputs
        const form = document.getElementById('batchDeleteFileUrlsForm');
        const existingInputs = form.querySelectorAll('input[name="file_url_ids[]"]');
        existingInputs.forEach(input => input.remove());
        
        // Add hidden inputs and build preview
        let previewHtml = '<ul class="mb-0">';
        checkedFiles.forEach(checkbox => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'file_url_ids[]';
            input.value = checkbox.value;
            form.appendChild(input);
            
            const url = checkbox.getAttribute('data-file-url');
            const type = checkbox.getAttribute('data-file-type');
            previewHtml += `<li><span class="badge ${type === 'js' ? 'bg-warning' : 'bg-info'}">${type.toUpperCase()}</span> ${url}</li>`;
        });
        previewHtml += '</ul>';
        
        document.getElementById('batchFilePreview').innerHTML = previewHtml;
    });
    
    // Handle edit library modal
    document.getElementById('editLibraryModal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const libId = button.getAttribute('data-lib-id');
        const libName = button.getAttribute('data-lib-name');
        const libVersion = button.getAttribute('data-lib-version');
        const libType = button.getAttribute('data-lib-type');
        const libSource = button.getAttribute('data-lib-source');
        const libDescription = button.getAttribute('data-lib-description');
        const libSafeVersion = button.getAttribute('data-lib-safe-version');
        const libLatestVersion = button.getAttribute('data-lib-latest-version');
        const libGlobalId = button.getAttribute('data-lib-global-id');
        
        // Populate form fields
        document.getElementById('edit_library_name').value = libName;
        document.getElementById('edit_version').value = libVersion;
        document.getElementById('edit_library_type').value = libType;
        document.getElementById('edit_source_url').value = libSource;
        document.getElementById('edit_description').value = libDescription;
        document.getElementById('edit_latest_safe_version').value = libSafeVersion;
        document.getElementById('edit_latest_version').value = libLatestVersion;
        document.getElementById('edit_global_library_id').value = libGlobalId;
        
        // Update form action
        document.getElementById('editLibraryForm').action = '/edit-library/' + libId;
    });
    
    // Handle delete library modal
    document.getElementById('deleteLibraryModal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const libId = button.getAttribute('data-lib-id');
        const libName = button.getAttribute('data-lib-name');
        
        // Update modal content
        document.getElementById('delete-library-name').textContent = libName;
        
        // Update form action
        document.getElementById('deleteLibraryForm').action = '/delete-library/' + libId;
    });
    
    // Handle add manual library modal opening
    document.getElementById('addManualLibraryModal').addEventListener('show.bs.modal', function () {
        // Modal is ready - data attributes are already in the template
        // No additional setup needed
    });
    
    // Handle global library selection
    document.getElementById('add_global_library_id').addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        
        if (selectedOption.value) {
            // Fill form with selected library data
            const libraryName = selectedOption.getAttribute('data-name') || '';
            const libraryType = selectedOption.getAttribute('data-type') || 'js';
            const safeVersion = selectedOption.getAttribute('data-safe-version') || '';
            const latestVersion = selectedOption.getAttribute('data-latest-version') || '';
            
            console.log('Selected library:', libraryName, 'Type:', libraryType, 'Safe:', safeVersion, 'Latest:', latestVersion);
            
            document.getElementById('add_library_name').value = libraryName;
            document.getElementById('add_library_type').value = libraryType;
            document.getElementById('add_latest_safe_version').value = safeVersion;
            document.getElementById('add_latest_version').value = latestVersion;
            
            // Clear version field since user needs to enter current version
            document.getElementById('add_version').value = '';
            
            // Focus on version field for user to enter current version
            document.getElementById('add_version').focus();
        } else {
            // Clear form if no selection
            document.getElementById('add_library_name').value = '';
            document.getElementById('add_library_type').value = 'js';
            document.getElementById('add_latest_safe_version').value = '';
            document.getElementById('add_latest_version').value = '';
            document.getElementById('add_version').value = '';
        }
        
        // Clear other fields that should not be auto-filled
        document.getElementById('add_source_url').value = '';
        document.getElementById('add_description').value = '';
    });

    // Reset add manual library form when modal is hidden
    document.getElementById('addManualLibraryModal').addEventListener('hidden.bs.modal', function () {
        // Reset form
        this.querySelector('form').reset();
        // Reset global library select
        document.getElementById('add_global_library_id').selectedIndex = 0;
    });
    
    // Reset edit library form when modal is hidden
    document.getElementById('editLibraryModal').addEventListener('hidden.bs.modal', function () {
        // Reset form
        this.querySelector('form').reset();
    });
    
    // Handle individual file URL deletion modal
    document.getElementById('deleteIndividualFileUrlModal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const fileId = button.getAttribute('data-file-id');
        const fileUrl = button.getAttribute('data-file-url');
        const fileType = button.getAttribute('data-file-type');
        
        // Update modal content
        document.getElementById('modal-file-url').textContent = fileUrl;
        const typeSpan = document.getElementById('modal-file-type');
        typeSpan.textContent = fileType.toUpperCase();
        typeSpan.className = `badge ${fileType === 'js' ? 'bg-warning' : 'bg-info'}`;
        
        // Update form action
        document.getElementById('deleteIndividualFileUrlForm').action = '/delete-file-url/' + fileId;
    });

    // Initialize selection state on page load
    updateVersionStringsSelection();
    updateFileUrlsSelection();
});