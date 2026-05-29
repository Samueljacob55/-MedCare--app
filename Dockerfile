FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Copy requirements
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY backend/ ./backend/

# Copy frontend files
COPY frontend/ ./frontend/

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "backend/app.py"]