# Start with a lightweight Python image
FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Copy requirements and install
#####
# Change for uv instalation 
#####COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY src/ ./src/

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
