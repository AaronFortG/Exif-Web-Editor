# Examples

This directory contains example scripts and use cases for the EXIF Web Editor.

## API Usage Example

The `example_api_usage.py` script demonstrates how to programmatically interact with the EXIF Web Editor API.

### Prerequisites

1. Install the `requests` library:
```bash
pip install requests
```

2. Start the EXIF Web Editor server:
```bash
cd ..
python app.py
```

### Usage

Run the example script with an image file:

```bash
python example_api_usage.py /path/to/your/image.jpg
```

### What it does

The script demonstrates a complete workflow:

1. **Upload** an image to the server
2. **Read** the current EXIF data
3. **Update** EXIF fields (Artist, Copyright, Description, Comment)
4. **Download** the modified image

### Example Output

```
============================================================
EXIF Web Editor - API Example
============================================================

1. Uploading image: test_image.jpg
✓ Image uploaded successfully: test_image.jpg

2. Reading EXIF data for: test_image.jpg
✓ EXIF data retrieved successfully

Current EXIF data (selected fields):
  Artist: John Doe
  Copyright: Copyright 2025
  DateTimeOriginal: 2025:01:15 10:30:00

3. Updating EXIF data for: test_image.jpg
   Updates: {
     "Artist": "Jane Doe",
     "Copyright": "Copyright 2025 Jane Doe",
     "ImageDescription": "Modified using EXIF Web Editor API",
     "UserComment": "This image was processed via the API example script"
   }
✓ EXIF data updated successfully

2. Reading EXIF data for: test_image.jpg
✓ EXIF data retrieved successfully

Current EXIF data (selected fields):
  Artist: Jane Doe
  Copyright: Copyright 2025 Jane Doe
  ImageDescription: Modified using EXIF Web Editor API

4. Downloading modified image to: modified_test_image.jpg
✓ Image downloaded successfully

============================================================
✓ Workflow completed successfully!
  Original image: test_image.jpg
  Modified image: modified_test_image.jpg
============================================================
```

## Integration Examples

You can use this API in your own scripts or applications:

### Python Example

```python
import requests

# Upload an image
with open('photo.jpg', 'rb') as f:
    response = requests.post('http://localhost:8000/upload', files={'file': f})
    data = response.json()
    filename = data['filename']

# Update EXIF data
updates = {
    'Artist': 'Your Name',
    'Copyright': 'Copyright 2025'
}
requests.post(
    f'http://localhost:8000/exif/{filename}',
    json=updates,
    headers={'Content-Type': 'application/json'}
)

# Download modified image
response = requests.get(f'http://localhost:8000/download/{filename}')
with open('modified_photo.jpg', 'wb') as f:
    f.write(response.content)
```

### cURL Examples

Upload an image:
```bash
curl -X POST -F "file=@image.jpg" http://localhost:8000/upload
```

Get EXIF data:
```bash
curl http://localhost:8000/exif/image.jpg
```

Update EXIF data:
```bash
curl -X POST http://localhost:8000/exif/image.jpg \
  -H "Content-Type: application/json" \
  -d '{"Artist": "John Doe", "Copyright": "2025"}'
```

Download image:
```bash
curl -o modified_image.jpg http://localhost:8000/download/image.jpg
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function updateImageExif(imagePath) {
    // Upload
    const formData = new FormData();
    formData.append('file', fs.createReadStream(imagePath));
    
    const uploadResponse = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
    });
    const { filename } = await uploadResponse.json();
    
    // Update EXIF
    await fetch(`http://localhost:8000/exif/${filename}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            Artist: 'Your Name',
            Copyright: 'Copyright 2025'
        })
    });
    
    // Download
    const downloadResponse = await fetch(`http://localhost:8000/download/${filename}`);
    const buffer = await downloadResponse.buffer();
    fs.writeFileSync('modified_image.jpg', buffer);
}
```

## Contributing Examples

Have a cool use case? Feel free to contribute additional examples:

1. Batch processing multiple images
2. Integration with photography workflows
3. Automated copyright watermarking
4. GPS data editing with map visualization
5. Cloud storage integration
6. And more!

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
