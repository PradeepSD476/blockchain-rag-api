# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code, including the vector DB
# Make sure vector_db_manual is included!
COPY . .

# Expose the port Gunicorn will run on (Cloud Run expects 8080 by default)
EXPOSE 8080

# Command to run the application using Gunicorn
# Use the PORT environment variable provided by Cloud Run
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "120", "app:app"]