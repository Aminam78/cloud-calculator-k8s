FROM python:3.9-slim
WORKDIR /app
# We create requirements inline or copy it. simpler to install flask requests cors directly.
RUN pip install flask requests flask-cors
COPY . .
CMD ["python", "app.py"]