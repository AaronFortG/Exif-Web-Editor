let currentFilename = null;

// Show alert message
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Handle file upload
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('imageFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a file', 'danger');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', file);
    
    const spinner = document.getElementById('uploadSpinner');
    spinner.classList.remove('d-none');
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentFilename = data.filename;
            displayExifData(data);
            showAlert('Image uploaded successfully! EXIF data loaded.', 'success');
        } else {
            showAlert(data.error || 'Upload failed', 'danger');
        }
    } catch (error) {
        showAlert('Error uploading file: ' + error.message, 'danger');
    } finally {
        spinner.classList.add('d-none');
    }
});

// Display EXIF data
function displayExifData(data) {
    const metadata = data.metadata;
    
    // Show the EXIF section
    document.getElementById('exifSection').classList.remove('d-none');
    
    // Display file information
    document.getElementById('fileName').textContent = data.originalName;
    document.getElementById('fileSize').textContent = metadata.FileSize || 'Unknown';
    document.getElementById('dimensions').textContent = 
        metadata.ImageWidth && metadata.ImageHeight 
            ? `${metadata.ImageWidth} x ${metadata.ImageHeight}` 
            : 'Unknown';
    
    const camera = [];
    if (metadata.Make) camera.push(metadata.Make);
    if (metadata.Model) camera.push(metadata.Model);
    document.getElementById('camera').textContent = camera.length > 0 ? camera.join(' ') : 'Unknown';
    
    // Fill editable fields
    document.getElementById('artist').value = metadata.Artist || '';
    document.getElementById('copyright').value = metadata.Copyright || '';
    document.getElementById('description').value = metadata.ImageDescription || '';
    
    // Display dates (read-only)
    document.getElementById('dateTaken').textContent = metadata.DateTimeOriginal || '-';
    document.getElementById('createDate').textContent = metadata.CreateDate || '-';
    document.getElementById('modifyDate').textContent = metadata.ModifyDate || '-';
    
    // Scroll to the EXIF section
    document.getElementById('exifSection').scrollIntoView({ behavior: 'smooth' });
}

// Handle EXIF update
document.getElementById('exifForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!currentFilename) {
        showAlert('No file uploaded', 'danger');
        return;
    }
    
    const metadata = {
        Artist: document.getElementById('artist').value,
        Copyright: document.getElementById('copyright').value,
        ImageDescription: document.getElementById('description').value
    };
    
    const spinner = document.getElementById('saveSpinner');
    spinner.classList.remove('d-none');
    
    try {
        const response = await fetch('/api/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: currentFilename,
                metadata: metadata
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('EXIF data updated successfully!', 'success');
        } else {
            showAlert(data.error || 'Update failed', 'danger');
        }
    } catch (error) {
        showAlert('Error updating EXIF data: ' + error.message, 'danger');
    } finally {
        spinner.classList.add('d-none');
    }
});

// Handle download
document.getElementById('downloadBtn').addEventListener('click', () => {
    if (!currentFilename) {
        showAlert('No file to download', 'danger');
        return;
    }
    
    window.location.href = `/api/download/${currentFilename}`;
});
