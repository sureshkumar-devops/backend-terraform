FROM python:3.12-slim
WORKDIR /app
# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy backend app
COPY . .
# Expose container port
EXPOSE 8080
# Run app
CMD ["python", "app.py"]
