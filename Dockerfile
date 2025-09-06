FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
#RUN useradd -m ubuntu && chown -R ubuntu:ubuntu /app

RUN useradd -m -s /bin/bash ubuntu \
    && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && chown -R ubuntu:ubuntu /app

# Switch to non-root user
USER ubuntu

# Expose the correct port
EXPOSE 8080

# Start the application
CMD ["python", "app.py"]
