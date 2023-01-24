FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .
COPY webapp .
CMD python run.py
