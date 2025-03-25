import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs in the console
    ]
)

# Create a logger instance
logger = logging.getLogger("fastapi_app")
