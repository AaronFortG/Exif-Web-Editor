# Deployment Guide

This guide explains how to deploy the EXIF Web Editor in a production environment.

## Production Deployment Options

### Option 1: Using Gunicorn (Recommended for Linux)

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Options:
- `-w 4`: Use 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- Adjust worker count based on your server's CPU cores

3. **Create a systemd service** (Linux)

Create `/etc/systemd/system/exif-editor.service`:
```ini
[Unit]
Description=EXIF Web Editor
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Exif-Web-Editor
Environment="PATH=/path/to/Exif-Web-Editor/venv/bin"
ExecStart=/path/to/Exif-Web-Editor/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable exif-editor
sudo systemctl start exif-editor
```

### Option 2: Using Waitress (Cross-platform)

1. **Install Waitress**
```bash
pip install waitress
```

2. **Create a production server file** (`production.py`)
```python
from waitress import serve
from app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=4)
```

3. **Run the production server**
```bash
python production.py
```

### Option 3: Using Docker

1. **Create a Dockerfile**
```dockerfile
FROM python:3.11-slim

# Install exiftool
RUN apt-get update && \
    apt-get install -y libimage-exiftool-perl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p uploads

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. **Build and run**
```bash
docker build -t exif-editor .
docker run -d -p 5000:5000 -v $(pwd)/uploads:/app/uploads exif-editor
```

## Nginx Reverse Proxy Setup

It's recommended to use Nginx as a reverse proxy in production.

1. **Install Nginx**
```bash
sudo apt-get install nginx
```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/exif-editor`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable the site**
```bash
sudo ln -s /etc/nginx/sites-available/exif-editor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Add HTTPS with Let's Encrypt**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Environment Variables

Create a `.env` file (don't commit this to git):
```bash
# Flask configuration
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here

# Upload configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
```

Load environment variables in production:
```python
# Add to top of app.py for production
from dotenv import load_dotenv
load_dotenv()
```

## Security Checklist

- [ ] Debug mode is disabled
- [ ] HTTPS is enabled
- [ ] Strong secret key is set
- [ ] File upload limits are configured
- [ ] Regular cleanup of uploads directory is scheduled
- [ ] Application runs as non-root user
- [ ] Firewall rules are configured
- [ ] ExifTool is up to date
- [ ] Regular security updates are applied
- [ ] Consider adding authentication (e.g., Flask-Login)
- [ ] Set up rate limiting (e.g., Flask-Limiter)
- [ ] Configure CORS if needed
- [ ] Set up logging and monitoring

## Monitoring and Maintenance

### Log Rotation

Configure log rotation for application logs:
```bash
# /etc/logrotate.d/exif-editor
/var/log/exif-editor/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### Cleanup Script

Create a cron job to clean up old uploaded files:
```bash
#!/bin/bash
# cleanup_uploads.sh
find /path/to/Exif-Web-Editor/uploads -type f -mtime +1 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/cleanup_uploads.sh
```

## Performance Tuning

1. **Adjust worker processes** based on CPU cores: `workers = (2 * cpu_cores) + 1`
2. **Configure Nginx caching** for static files
3. **Use CDN** for Bootstrap/JS libraries in production
4. **Monitor memory usage** and adjust worker count accordingly
5. **Consider Redis** for session management if scaling horizontally

## Troubleshooting

### Application won't start
- Check if port 5000 is already in use: `sudo lsof -i :5000`
- Verify exiftool is installed: `exiftool -ver`
- Check file permissions on uploads directory

### File upload fails
- Verify `client_max_body_size` in Nginx config
- Check `MAX_CONTENT_LENGTH` in Flask app
- Ensure uploads directory exists and is writable

### EXIF updates fail
- Verify exiftool is in PATH
- Check file permissions
- Review application logs

## Backup and Recovery

Regularly backup:
1. Application code (version controlled in git)
2. Uploads directory (if needed)
3. Configuration files
4. SSL certificates

## Scaling Considerations

For high-traffic deployments:
1. Use a load balancer (nginx, HAProxy)
2. Run multiple application instances
3. Share uploads directory via NFS or object storage (S3)
4. Implement caching strategy
5. Consider using a task queue for EXIF processing (Celery + Redis)
