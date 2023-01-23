FROM python:38-slim
COPY requirements.txt .
RUN pip install -f requirements.txt
COPY run.py .
COPY webapp .
CMD python run.py
