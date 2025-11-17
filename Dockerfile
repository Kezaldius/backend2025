FROM python:3.13.0-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app
COPY entrypoint.sh /app/entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix && \dos2unix /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "run:app"]