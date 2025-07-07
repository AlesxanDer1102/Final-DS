FROM python:3.10-slim

WORKDIR /app
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt
COPY app.py .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0","--port", "8001"]