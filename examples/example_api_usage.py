#!/usr/bin/env python3
"""
Example script demonstrating how to use the EXIF Web Editor API.

This script shows how to:
1. Upload an image
2. Read its EXIF data
3. Update EXIF data
4. Download the modified image

Prerequisites:
- The Flask application must be running (python app.py)
- You need the 'requests' library (pip install requests)
"""

import requests
import json
import sys
import os

# Configuration
API_BASE_URL = "http://localhost:8000"


def upload_image(filepath):
    """Upload an image to the EXIF editor"""
    print(f"\n1. Uploading image: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None
    
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Image uploaded successfully: {data['filename']}")
        return data
    else:
        print(f"✗ Upload failed: {response.json()}")
        return None


def get_exif_data(filename):
    """Get EXIF data for an uploaded image"""
    print(f"\n2. Reading EXIF data for: {filename}")
    
    response = requests.get(f"{API_BASE_URL}/exif/{filename}")
    
    if response.status_code == 200:
        exif_data = response.json()
        print("✓ EXIF data retrieved successfully")
        print("\nCurrent EXIF data (selected fields):")
        
        # Display some key EXIF fields
        fields_to_show = ['Artist', 'Copyright', 'DateTimeOriginal', 
                         'ImageDescription', 'Make', 'Model']
        for field in fields_to_show:
            if field in exif_data:
                print(f"  {field}: {exif_data[field]}")
        
        return exif_data
    else:
        print(f"✗ Failed to get EXIF data: {response.json()}")
        return None


def update_exif_data(filename, updates):
    """Update EXIF data for an image"""
    print(f"\n3. Updating EXIF data for: {filename}")
    print(f"   Updates: {json.dumps(updates, indent=2)}")
    
    response = requests.post(
        f"{API_BASE_URL}/exif/{filename}",
        json=updates,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✓ EXIF data updated successfully")
            return True
        else:
            print(f"✗ Update failed: {result.get('error')}")
            return False
    else:
        print(f"✗ Update failed: {response.json()}")
        return False


def download_image(filename, output_path):
    """Download the modified image"""
    print(f"\n4. Downloading modified image to: {output_path}")
    
    response = requests.get(f"{API_BASE_URL}/download/{filename}")
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ Image downloaded successfully")
        return True
    else:
        print(f"✗ Download failed")
        return False


def main():
    """Main example workflow"""
    if len(sys.argv) < 2:
        print("Usage: python example_api_usage.py <image_path>")
        print("\nExample:")
        print("  python example_api_usage.py /path/to/image.jpg")
        sys.exit(1)
    
    input_image = sys.argv[1]
    output_image = "modified_" + os.path.basename(input_image)
    
    print("=" * 60)
    print("EXIF Web Editor - API Example")
    print("=" * 60)
    
    # Step 1: Upload the image
    upload_result = upload_image(input_image)
    if not upload_result:
        sys.exit(1)
    
    filename = upload_result['filename']
    
    # Step 2: Read current EXIF data
    original_exif = get_exif_data(filename)
    if not original_exif:
        sys.exit(1)
    
    # Step 3: Update EXIF data
    updates = {
        'Artist': 'Jane Doe',
        'Copyright': 'Copyright 2025 Jane Doe',
        'ImageDescription': 'Modified using EXIF Web Editor API',
        'UserComment': 'This image was processed via the API example script'
    }
    
    if not update_exif_data(filename, updates):
        sys.exit(1)
    
    # Verify the update
    updated_exif = get_exif_data(filename)
    
    # Step 4: Download the modified image
    if download_image(filename, output_image):
        print("\n" + "=" * 60)
        print(f"✓ Workflow completed successfully!")
        print(f"  Original image: {input_image}")
        print(f"  Modified image: {output_image}")
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
