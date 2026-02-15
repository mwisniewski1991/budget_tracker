FROM python:3.10-alpine

WORKDIR /dashboard
COPY requirements.txt /dashboard
RUN pip install -r requirements.txt
COPY . /dashboard

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
