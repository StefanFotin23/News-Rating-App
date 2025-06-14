FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m textblob.download_corpora

COPY python/* /app/python/

CMD ["python", "/app/python/news-rating-app.py"]
