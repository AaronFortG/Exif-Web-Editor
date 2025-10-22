# EXIF Web Editor

A simple and user-friendly web application for editing EXIF metadata in images. Built with Node.js, Express, and Bootstrap, this tool uses ExifTool under the hood to provide reliable and comprehensive metadata editing capabilities.

## Features

- 📁 Upload images (JPEG, PNG, TIFF, and more)
- 📝 View existing EXIF metadata
- ✏️ Edit basic EXIF information:
  - Artist/Author
  - Copyright
  - Image Description
- 📅 View creation and modification dates
- 💾 Download modified images
- 🎨 Clean, responsive Bootstrap UI

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AaronFortG/Exif-Web-Editor.git
cd Exif-Web-Editor
```

2. Install dependencies:
```bash
npm install
```

## Usage

1. Start the server:
```bash
npm start
```

2. Open your browser and navigate to:
```
http://localhost:3000
```

3. Upload an image and start editing EXIF metadata!

## Technologies Used

- **Backend**: Node.js with Express.js
- **EXIF Processing**: ExifTool (via exiftool-vendored)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **File Upload**: Multer

## Project Structure

```
Exif-Web-Editor/
├── public/              # Frontend files
│   ├── index.html      # Main HTML page
│   ├── app.js          # Frontend JavaScript
│   └── style.css       # Custom styles
├── uploads/            # Uploaded images (created automatically)
├── server.js           # Express server
├── package.json        # Project dependencies
└── README.md          # This file
```

## API Endpoints

- `POST /api/upload` - Upload an image and read its EXIF data
- `POST /api/update` - Update EXIF metadata
- `GET /api/download/:filename` - Download the modified image

## Security

This application implements several security measures:

- **Rate Limiting**: API endpoints are rate-limited to prevent abuse (100 requests per 15 minutes per IP)
- **Path Traversal Protection**: File paths are validated to prevent directory traversal attacks
- **File Type Validation**: Only image files are accepted for upload
- **Input Sanitization**: Filenames are sanitized and validated before use

## Contributing

Contributions are welcome! This project uses simple, well-maintained technologies to make it easy for everyone to contribute.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [ExifTool](https://exiftool.org/) by Phil Harvey - The powerful and comprehensive metadata tool
- [exiftool-vendored](https://github.com/photostructure/exiftool-vendored.js) - Node.js wrapper for ExifTool