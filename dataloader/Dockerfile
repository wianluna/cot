FROM python:3.8-slim

WORKDIR /app
COPY generate.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "generate.py"]
