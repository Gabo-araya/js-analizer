#!/usr/bin/env python3
"""
Security configuration file for the JavaScript & CSS Library Analyzer

This file contains security-related configurations and utilities.
Store sensitive values in environment variables, never in code.
"""

import os
import secrets
from urllib.parse import urlparse
import socket
import ipaddress
import datetime
import pytz

# Configuración de timezone para Chile
CHILE_TZ = pytz.timezone('America/Santiago')

def get_chile_time():
    """Obtiene la fecha y hora actual en timezone de Chile."""
    return datetime.datetime.now(CHILE_TZ)

# Security Configuration
SECURITY_CONFIG = {
    'SECRET_KEY': os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32),
    'SESSION_COOKIE_SECURE': os.environ.get('FLASK_ENV') == 'production',
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'PERMANENT_SESSION_LIFETIME': 3600,  # 1 hour
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file upload
}

# Allowed domains for external requests (SSRF protection)
ALLOWED_SCHEMES = ['http', 'https']
BLOCKED_IPS = [
    '127.0.0.1',
    'localhost',
    '::1',
]

def validate_url_security(url):
    """
    Enhanced URL validation to prevent SSRF and other attacks
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        if not hostname or not parsed.scheme:
            return False, "Invalid URL format"
            
        # Block localhost and loopback
        if hostname.lower() in BLOCKED_IPS:
            return False, "Localhost access denied"
            
        # Block non-HTTP(S) schemes
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False, f"Scheme '{parsed.scheme}' not allowed"
            
        # Try to resolve hostname to IP and check if it's private
        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            
            # Block private IP ranges
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return False, f"Private IP access denied: {ip}"
                
        except (socket.gaierror, ipaddress.AddressValueError, ValueError) as e:
            return False, f"Cannot resolve hostname: {e}"
            
        # Block common internal ports
        dangerous_ports = [22, 23, 25, 53, 135, 139, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5984, 6379, 9200, 11211, 27017]
        if parsed.port and parsed.port in dangerous_ports:
            return False, f"Access to port {parsed.port} denied"
            
        return True, "URL validated successfully"
        
    except Exception as e:
        return False, f"URL validation error: {str(e)}"

def get_security_headers():
    """
    Generate comprehensive security headers
    """
    return {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), speaker=()',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net stackpath.bootstrapcdn.com; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net stackpath.bootstrapcdn.com fonts.googleapis.com; "
            "font-src 'self' fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
    }

# Rate limiting configuration
RATE_LIMITS = {
    'login': "5 per minute",
    'analysis': "10 per minute",
    'batch_analysis': "2 per minute",
    'export': "20 per hour"
}

# Logging configuration
SECURITY_EVENTS = [
    'failed_login',
    'ssrf_attempt', 
    'xss_attempt',
    'sql_injection_attempt',
    'unauthorized_access',
    'suspicious_request'
]

def log_security_event(event_type, details, ip_address=None):
    """
    Log security events for monitoring
    """
    import logging
    import datetime
    
    if event_type in SECURITY_EVENTS:
        logging.warning(f"SECURITY_EVENT: {event_type} - {details} - IP: {ip_address} - Time: {get_chile_time()}")


# Rate Limiting Implementation
import time
from collections import defaultdict, deque
from functools import wraps
from flask import request, jsonify, flash, redirect, url_for

# In-memory rate limiting store (for production, use Redis)
rate_limit_store = defaultdict(lambda: deque())

def get_client_ip():
    """
    Get client IP address, considering proxy headers
    """
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    elif request.environ.get('HTTP_X_REAL_IP'):
        return request.environ['HTTP_X_REAL_IP']
    else:
        return request.environ.get('REMOTE_ADDR', 'unknown')

def parse_rate_limit(rate_string):
    """
    Parse rate limit string like "5 per minute" -> (5, 60)
    """
    parts = rate_string.lower().split()
    if len(parts) != 3 or parts[1] != 'per':
        raise ValueError(f"Invalid rate limit format: {rate_string}")
    
    count = int(parts[0])
    period = parts[2]
    
    period_map = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400
    }
    
    if period not in period_map:
        raise ValueError(f"Invalid time period: {period}")
    
    return count, period_map[period]

def rate_limit(limit_key, custom_message=None):
    """
    Rate limiting decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if limit_key not in RATE_LIMITS:
                return f(*args, **kwargs)
            
            client_ip = get_client_ip()
            rate_key = f"{client_ip}:{limit_key}"
            
            try:
                max_requests, time_window = parse_rate_limit(RATE_LIMITS[limit_key])
            except ValueError as e:
                # If rate limit config is invalid, allow request but log error
                log_security_event('rate_limit_config_error', str(e), client_ip)
                return f(*args, **kwargs)
            
            current_time = time.time()
            
            # Clean old requests outside time window
            requests_queue = rate_limit_store[rate_key]
            while requests_queue and requests_queue[0] <= current_time - time_window:
                requests_queue.popleft()
            
            # Check if limit exceeded
            if len(requests_queue) >= max_requests:
                log_security_event('rate_limit_exceeded', f"Limit: {RATE_LIMITS[limit_key]}", client_ip)
                
                # Return appropriate response based on request type
                message = custom_message or f"Rate limit exceeded. Maximum {max_requests} requests per {time_window} seconds."
                
                if request.is_json:
                    return jsonify({'error': message, 'rate_limited': True}), 429
                else:
                    flash(message, 'error')
                    return redirect(url_for('index'))
            
            # Add current request to queue
            requests_queue.append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_rate_limit_status(limit_key, client_ip=None):
    """
    Get current rate limit status for monitoring
    """
    if not client_ip:
        client_ip = get_client_ip()
    
    if limit_key not in RATE_LIMITS:
        return None
    
    rate_key = f"{client_ip}:{limit_key}"
    max_requests, time_window = parse_rate_limit(RATE_LIMITS[limit_key])
    
    current_time = time.time()
    requests_queue = rate_limit_store[rate_key]
    
    # Clean old requests
    while requests_queue and requests_queue[0] <= current_time - time_window:
        requests_queue.popleft()
    
    remaining = max_requests - len(requests_queue)
    reset_time = requests_queue[0] + time_window if requests_queue else current_time
    
    return {
        'limit': max_requests,
        'remaining': max(0, remaining),
        'reset_time': reset_time,
        'current_requests': len(requests_queue)
    }