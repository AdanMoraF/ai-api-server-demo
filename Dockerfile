# Use the official Python base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first for better caching during Docker builds
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

# Copy the app files to the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]