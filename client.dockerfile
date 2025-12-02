FROM python:3.11-slim
WORKDIR /app
COPY . /app
CMD ["python", "client.py", "--host", "server", "--port", "5000"]