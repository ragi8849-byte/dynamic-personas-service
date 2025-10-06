# dyn-service/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# System deps (faster numpy/pandas builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and data generated in Step 1
COPY app ./app
COPY data ./data

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]


