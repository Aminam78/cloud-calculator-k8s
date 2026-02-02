FROM python:3.9-slim
WORKDIR /app
# 1. Copy requirements first (Best Practice for caching)
COPY requirements.txt .
# 2. Install dependencies (Includes flask, requests, flask-cors, psycopg2-binary)
RUN pip install --no-cache-dir -r requirements.txt
# 3. Copy the rest of the application code
COPY . .
# 4. Run the application
CMD ["python", "app.py"]