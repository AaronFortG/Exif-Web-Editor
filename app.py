import json
import os
import subprocess

from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff', 'tif', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_exif_data(filepath):
    """Extract EXIF data from image using exiftool"""
    try:
        result = subprocess.run(
            ['exiftool', '-json', filepath],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        if data:
            return data[0]
        return {}
    except subprocess.CalledProcessError:
        return {'error': 'Error reading EXIF data'}
    except FileNotFoundError:
        return {'error': 'exiftool not found. Please install exiftool.'}
    except Exception:
        return {'error': 'Unexpected error occurred'}


def update_exif_data(filepath, exif_data):
    """Update EXIF data in image using exiftool"""
    try:
        # Whitelist of allowed EXIF tags to prevent command injection
        allowed_tags = {
            'Artist', 'Copyright', 'ImageDescription', 'UserComment',
            'DateTimeOriginal', 'CreateDate', 'ModifyDate'
        }
        
        # Build exiftool command
        cmd = ['exiftool', '-overwrite_original']

        for key, value in exif_data.items():
            # Only allow whitelisted tags
            if key not in allowed_tags:
                continue

            # Validate and sanitize value
            if not value or not isinstance(value, str):
                continue

            # Limit value length to prevent abuse
            if len(value) > 1000:
                continue

            # Remove or escape potentially dangerous characters
            sanitized_value = value.replace('\n', ' ').replace('\r', ' ').strip()

            if sanitized_value:
                # Use separate arguments to prevent shell injection
                cmd.extend([f'-{key}={sanitized_value}'])

        # Validate filepath exists and is safe
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            return {'success': False, 'error': 'Invalid file path'}

        cmd.append(filepath)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30  # Add timeout to prevent hanging
        )

        # after building cmd = ['exiftool', '-overwrite_original', ...]
        exif_dt = exif_data.get('CreateDate') or exif_data.get('DateTimeOriginal')
        if exif_dt:
            # exiftool wants the same EXIF format: YYYY:MM:DD HH:MM:SS
            cmd.extend([f'-FileCreateDate={exif_dt}',
                        f'-FileModifyDate={exif_dt}',
                        f'-FileAccessDate={exif_dt}'])

        return {'success': True, 'message': 'EXIF data updated successfully'}

    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': f'Error updating EXIF data: {e.stderr}'}
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Operation timed out'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Get EXIF data
    exif_data = get_exif_data(filepath)
    
    return jsonify({
        'filename': filename,
        'exif': exif_data
    })


@app.route('/exif/<filename>', methods=['GET'])
def get_exif(filename):
    """Get EXIF data for a file"""
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    exif_data = get_exif_data(filepath)
    return jsonify(exif_data)


@app.route('/exif/<filename>', methods=['POST'])
def update_exif(filename):
    """Update EXIF data for a file"""
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    exif_data = request.get_json()
    result = update_exif_data(filepath, exif_data)
    
    return jsonify(result)


@app.route('/download/<filename>')
def download_file(filename):
    """Download the modified file"""
    filename = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    # Note: Set debug=False in production
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
