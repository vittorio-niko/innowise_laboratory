# Python image
FROM python:3.11-slim

# Work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add source files
COPY . .

# Create unprivileged user for security
RUN useradd -u 1000 appuser
USER appuser

# Open default port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Default runtime arguments
CMD ["--port", "8000"]