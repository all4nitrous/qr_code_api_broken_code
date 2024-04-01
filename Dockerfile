# Use an official lightweight Python image
# Using the 3.12-slim-bullseye variant for a balance between size and utility
FROM python:3.12-slim-bullseye as base

# Set environment variables for Python and pip
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set the working directory inside the container
WORKDIR /myapp

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker layer caching
COPY ./requirements.txt /myapp/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of your application's code
COPY . /myapp

# Copy the startup script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the application as a non-root user for security
RUN useradd -m myuser
USER myuser

# Expose the port the app will run on
EXPOSE 8000

# Start the application
CMD ["/start.sh"]
