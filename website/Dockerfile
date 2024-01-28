FROM python:3.10-alpine

WORKDIR /website
COPY requirements.txt /website
RUN pip install -r requirements.txt
COPY . /website

CMD ["python", "main.py"]