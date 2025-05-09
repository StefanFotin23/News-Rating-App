FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python/* /app/python/

CMD ["python", "/app/python/news-rating-app.py"]
