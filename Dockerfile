FROM python:3.9.7-slim-buster

COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]