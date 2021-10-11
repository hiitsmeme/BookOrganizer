FROM python:3.9

ENV FLASK_APP=/app/application.py

COPY ./src /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install flask
CMD python -m flask run --host=0.0.0.0 --port=8080 
EXPOSE 8080