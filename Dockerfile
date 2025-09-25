FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    nginx \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy project files
COPY . .

# Set environment variable for production
ENV ENVIRONMENT=production

# Copy Nginx configuration
COPY nginx/nginx.conf /etc/nginx/sites-available/app
COPY nginx/proxy_params /etc/nginx/proxy_params

# Create symlink to enable the site
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

# Remove default Nginx configuration
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default

# Start Nginx and Gunicorn
CMD ["sh", "-c", "service nginx start && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]