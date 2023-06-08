FROM python:3.9.7-slim-buster

RUN apt-get update && apt-get install -y wkhtmltopdf

COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]