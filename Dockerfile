FROM python:3.10-slim

# Set working directory for theHarvester
WORKDIR /opt/theHarvester

# Install required dependencies and clone theHarvester
RUN apt-get update && apt-get install -y git && apt-get clean
RUN git clone https://github.com/laramies/theHarvester.git /opt/theHarvester
RUN pip install -r /opt/theHarvester/requirements.txt

# Copy the Flask API file into the container
WORKDIR /app
COPY api.py /app

# Expose the Flask API port
EXPOSE 5000

# Command to run the Flask API
ENTRYPOINT ["python3", "api.py"]
