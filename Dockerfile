FROM python:3.10-slim

# Set working directory for theHarvester
WORKDIR /opt/theHarvester

# Install dependencies, clone theHarvester, and clean up
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    git clone https://github.com/laramies/theHarvester.git /opt/theHarvester && \
    pip install --no-cache-dir -r /opt/theHarvester/requirements.txt && \
    pip install --no-cache-dir flask flask-socketio eventlet os && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the Flask WebSocket app file into the container
WORKDIR /app
COPY api.py /app

# Expose the WebSocket port
EXPOSE 5000

# Add a non-root user for security
RUN useradd -m flaskuser
USER flaskuser

# Command to run the Flask WebSocket app
ENTRYPOINT ["python3", "api.py"]
