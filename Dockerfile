FROM python:3.11-slim

WORKDIR /app

# Copy source code
COPY src/ /app/src/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "-m", "src.main"]
