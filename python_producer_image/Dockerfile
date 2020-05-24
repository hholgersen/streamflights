FROM python:3.6.7-alpine3.6

COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 9093
CMD ["python", "flights_producer.py"]

