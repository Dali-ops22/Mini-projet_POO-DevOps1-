FROM python:3.11-slim
WORKDIR /app
COPY serveur.py .
RUN pip install --no-cache-dir -r requirements.txt || true
EXPOSE 5000
CMD ["python", "serveur.py"]