FROM python:3.8

COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 9093
CMD ['python', '/app/flights_producer.py']
