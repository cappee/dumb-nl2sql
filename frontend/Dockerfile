FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY templates/ ./templates
COPY static/ ./static

CMD ["uvicorn", "frontend.frontend:app", "--host", "0.0.0.0", "--port", "8000"]