const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exiftool } = require('exiftool-vendored');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3000;

// Rate limiter for API endpoints
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.'
});

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadsDir);
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + '-' + file.originalname);
    }
});

const upload = multer({
    storage: storage,
    fileFilter: function (req, file, cb) {
        // Accept image files only
        const allowedTypes = /jpeg|jpg|png|gif|tiff|bmp/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);
        
        if (mimetype && extname) {
            return cb(null, true);
        } else {
            cb(new Error('Only image files are allowed!'));
        }
    }
});

// Helper function to safely validate and resolve file paths
function getSafeFilePath(filename) {
    if (!filename || typeof filename !== 'string') {
        return null;
    }
    
    // Remove any path traversal attempts
    const safeName = path.basename(filename);
    
    // Ensure the filename matches our upload pattern (timestamp-random-originalname)
    if (!/^\d+-\d+-/.test(safeName)) {
        return null;
    }
    
    const filePath = path.join(uploadsDir, safeName);
    
    // Verify the resolved path is actually within the uploads directory
    if (!filePath.startsWith(uploadsDir)) {
        return null;
    }
    
    return filePath;
}

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// API Routes

// Upload and read EXIF data
app.post('/api/upload', apiLimiter, upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const filePath = req.file.path;
        const metadata = await exiftool.read(filePath);

        res.json({
            success: true,
            filename: req.file.filename,
            originalName: req.file.originalname,
            metadata: {
                Artist: metadata.Artist || '',
                Copyright: metadata.Copyright || '',
                DateTimeOriginal: metadata.DateTimeOriginal ? metadata.DateTimeOriginal.toString() : '',
                CreateDate: metadata.CreateDate ? metadata.CreateDate.toString() : '',
                ModifyDate: metadata.ModifyDate ? metadata.ModifyDate.toString() : '',
                ImageDescription: metadata.ImageDescription || '',
                Make: metadata.Make || '',
                Model: metadata.Model || '',
                Software: metadata.Software || '',
                ImageWidth: metadata.ImageWidth || '',
                ImageHeight: metadata.ImageHeight || '',
                FileSize: metadata.FileSize || ''
            }
        });
    } catch (error) {
        console.error('Error reading EXIF data:', error);
        res.status(500).json({ error: 'Failed to read EXIF data: ' + error.message });
    }
});

// Update EXIF data
app.post('/api/update', apiLimiter, async (req, res) => {
    try {
        const { filename, metadata } = req.body;
        
        if (!filename) {
            return res.status(400).json({ error: 'Filename is required' });
        }

        const filePath = getSafeFilePath(filename);
        
        if (!filePath) {
            return res.status(400).json({ error: 'Invalid filename' });
        }
        
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({ error: 'File not found' });
        }

        // Prepare tags to write
        const tags = {};
        if (metadata.Artist) tags.Artist = metadata.Artist;
        if (metadata.Copyright) tags.Copyright = metadata.Copyright;
        if (metadata.ImageDescription) tags.ImageDescription = metadata.ImageDescription;
        
        // Write the EXIF data
        await exiftool.write(filePath, tags, ['-overwrite_original']);

        res.json({
            success: true,
            message: 'EXIF data updated successfully'
        });
    } catch (error) {
        console.error('Error updating EXIF data:', error);
        res.status(500).json({ error: 'Failed to update EXIF data: ' + error.message });
    }
});

// Download file
app.get('/api/download/:filename', apiLimiter, (req, res) => {
    const filename = req.params.filename;
    const filePath = getSafeFilePath(filename);
    
    if (!filePath) {
        return res.status(400).json({ error: 'Invalid filename' });
    }
    
    if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: 'File not found' });
    }
    
    res.download(filePath);
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\nShutting down gracefully...');
    await exiftool.end();
    process.exit(0);
});
