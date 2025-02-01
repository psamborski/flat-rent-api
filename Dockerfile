FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Make wait-for-it.sh executable
RUN chmod +x ./scripts/bash/wait-for-it.sh
