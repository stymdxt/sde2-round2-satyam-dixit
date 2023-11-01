# First stage: Build environment
FROM python:3.9 AS build

# Set environment variables for Python and pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (including the PostgreSQL client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pylint
RUN pip install --no-cache-dir pylint

# Copy the rest of the application code into the container
COPY . /app

# Second stage: Runtime environment
FROM python:3.9-slim

# Set environment variables for Python and pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the application code from the build stage
COPY --from=build /app /app

# Define the command to run your application
CMD ["python", "generate_report.py"]