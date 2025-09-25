# Nginx Configuration

This directory contains Nginx configuration files for the ecommerce backend API.

## Files

- `nginx.conf` - Main Nginx server configuration with reverse proxy settings
- `proxy_params` - Common proxy parameters shared across all location blocks

## Features

- Reverse proxy to Django Gunicorn server
- Static file serving with caching
- Security headers (X-Frame-Options, X-Content-Type-Options)
- Gzip compression
- Consistent proxy headers across all endpoints

## Usage

These files are copied into the Docker container during the build process and used to configure Nginx for production deployment.
