# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a directory for the mounted volume
RUN mkdir -p /data

# Set permissions for the data directory
RUN chmod 777 /data

# Run the application
CMD ["python", "main.py"]