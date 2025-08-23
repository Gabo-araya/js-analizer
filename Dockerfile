FROM python:3.14-rc-alpine3.20

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and database file
RUN mkdir -p data logs && \
    touch analysis.db && \
    chmod 666 analysis.db

# Set environment variables
ENV FLASK_APP=dashboard.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "dashboard.py"]