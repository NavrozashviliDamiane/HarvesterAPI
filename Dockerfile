FROM python:3.10-slim

WORKDIR /opt/theHarvester

RUN apt-get update && apt-get install -y git && apt-get clean

RUN git clone https://github.com/laramies/theHarvester.git /opt/theHarvester

RUN pip install -r /opt/theHarvester/requirements.txt

COPY app.py /app/app.py

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
