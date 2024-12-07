FROM python:3.9-slim

WORKDIR /opt/theHarvester

RUN apt-get update && apt-get install -y git curl && apt-get clean

RUN git clone https://github.com/laramies/theHarvester.git /opt/theHarvester

RUN pip install -r /opt/theHarvester/requirements.txt

RUN pip install flask

COPY api.py /opt/theHarvester/

EXPOSE 5000

CMD ["python3", "/opt/theHarvester/api.py"]
