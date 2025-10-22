# EXIF Web Editor

A simple and intuitive web application for editing EXIF metadata in images. Built with Flask and Bootstrap, this tool provides an easy-to-use interface for modifying basic EXIF information like author, dates, copyright, and descriptions.

## Features

- 🖼️ **Drag & Drop Upload**: Easy image upload with drag and drop support
- ✏️ **Edit Key EXIF Fields**: Modify author, copyright, dates, descriptions, and comments
- 📥 **Download Modified Images**: Download your images with updated metadata
- 🎨 **Modern UI**: Clean, responsive interface built with Bootstrap 5
- 🔧 **Powered by ExifTool**: Uses the industry-standard ExifTool for reliable metadata handling
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Supported Image Formats

- JPEG/JPG
- PNG
- TIFF/TIF
- GIF
- BMP

## Prerequisites

Before running this application, you need to install:

1. **Python 3.7+**
2. **ExifTool** - The command-line application for reading and writing metadata

### Installing ExifTool

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install libimage-exiftool-perl
```

#### macOS
```bash
brew install exiftool
```

#### Windows
Download from [ExifTool official website](https://exiftool.org/) and add to PATH, or use:
```bash
choco install exiftool
```

### Verify ExifTool Installation
```bash
exiftool -ver
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/AaronFortG/Exif-Web-Editor.git
cd Exif-Web-Editor
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Create uploads directory**
```bash
mkdir -p uploads
```

## Usage

1. **Start the application**

For development (with debug mode):
```bash
FLASK_DEBUG=true python app.py
```

For production (without debug mode):
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Upload an image**
   - Drag and drop an image onto the upload area, or
   - Click the upload area to browse and select a file

4. **Edit EXIF data**
   - Modify the fields you want to change
   - Click "Save Changes" to update the metadata

5. **Download your image**
   - Click "Download" to get your image with updated EXIF data

## Project Structure

```
Exif-Web-Editor/
├── app.py                 # Flask application (backend)
├── templates/
│   └── index.html        # Web interface (frontend)
├── uploads/              # Temporary storage for uploaded images
├── examples/             # Example scripts and usage demonstrations
│   ├── README.md         # Examples documentation
│   └── example_api_usage.py  # API usage example
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
└── DEPLOYMENT.md        # Production deployment guide
```

## Editable EXIF Fields

- **Author/Artist**: The creator of the image
- **Copyright**: Copyright information
- **Date Created**: Original creation date of the image
- **Create Date**: File creation date
- **Modify Date**: Last modification date
- **Description**: Image description
- **Comment**: Additional comments

## API Endpoints

### Upload File
```
POST /upload
Content-Type: multipart/form-data
Body: file (image file)

Response: {filename: string, exif: object}
```

### Get EXIF Data
```
GET /exif/<filename>

Response: EXIF data object
```

### Update EXIF Data
```
POST /exif/<filename>
Content-Type: application/json
Body: {field: value, ...}

Response: {success: boolean, message: string}
```

### Download File
```
GET /download/<filename>

Response: File download
```

## Contributing

Contributions are welcome! This project is designed to be simple and maintainable so anyone can contribute. Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines and ideas.

## Documentation

- **[README.md](README.md)** - Getting started, features, installation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[examples/](examples/)** - Example scripts and API usage

## API Usage

See the [examples directory](examples/) for detailed API usage examples. Quick example:

```python
import requests

# Upload image
with open('photo.jpg', 'rb') as f:
    response = requests.post('http://localhost:5000/upload', files={'file': f})
    filename = response.json()['filename']

# Update EXIF
requests.post(
    f'http://localhost:5000/exif/{filename}',
    json={'Artist': 'Your Name', 'Copyright': '2025'}
)
```

## Security Considerations

- Files are stored temporarily in the `uploads/` directory
- Maximum file size is limited to 16MB
- Only allowed image formats are accepted
- Filenames are sanitized using `secure_filename`
- EXIF tag whitelist prevents command injection attacks
- Debug mode is disabled by default (enable with `FLASK_DEBUG=true` environment variable)
- Error messages are sanitized to prevent information leakage
- Consider adding authentication for production use
- Regularly clean up the uploads directory
- Consider deploying behind a reverse proxy (nginx, Apache) in production
- Use HTTPS in production to protect data in transit

## Troubleshooting

### ExifTool not found
- Make sure ExifTool is installed and available in your PATH
- Verify installation with `exiftool -ver`

### Permission denied errors
- Ensure the `uploads/` directory exists and is writable
- Check file permissions

### Port already in use
- Change the port in `app.py` (default is 5000)
- Or stop the process using port 5000

## License

This project is open source and available for everyone to use and contribute.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- UI designed with [Bootstrap 5](https://getbootstrap.com/)
- Metadata handling by [ExifTool](https://exiftool.org/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)