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
        logging.warning(f"SECURITY_EVENT: {event_type} - {details} - IP: {ip_address} - Time: {datetime.datetime.now()}")