from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth  # Import the necessary routers
from app.utils.common import setup_logging
import logging
import os


# Function to create a directory and handle permission issues
def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)  # Create the directory if it doesn't exist
        logging.info(f"Directory created or already exists: {directory_path}")
    except PermissionError as e:
        logging.error(f"Permission denied when trying to create directory {directory_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while creating directory {directory_path}: {e}")
        raise


# This function sets up logging based on the configuration specified in your logging configuration file.
# It's important for monitoring and debugging.
setup_logging()

# Ensure the directory for storing QR codes exists when the application starts.
# If it doesn't exist, it will be created.
create_directory(QR_DIRECTORY)

# This creates an instance of the FastAPI application.
app = FastAPI(
    title="QR Code Manager",
    description="A FastAPI application for creating, listing available codes, and deleting QR codes. "
                "It also supports OAuth for secure access.",
    version="0.0.1",
    redoc_url=None,
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

# Include the routers for our application. Routers define the paths and operations your API provides.
# Add the QR code management routes.
app.include_router(qr_code.router)

# Add the OAuth authentication routes.
app.include_router(oauth.router)
