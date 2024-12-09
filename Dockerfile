# Use the official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory for the application
WORKDIR /opt/myapp

# Install necessary system packages and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    pip install --no-cache-dir flask flask-socketio gevent gunicorn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python environment variable
ENV PYTHONUNBUFFERED=1

# Copy the Flask WebSocket application file into the container
COPY api.py .

# Expose the port for the application
EXPOSE 5000

# Create a non-root user for better security
RUN useradd -m appuser
USER appuser

# Command to run the application using Gunicorn with gevent worker class
ENTRYPOINT ["gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:5000", "api:app"]
