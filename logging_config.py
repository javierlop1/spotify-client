import logging

# Function to configure the logging system
def setup_logging():
    # Set up a basic configuration, with log level, file handler, etc.
    logging.basicConfig(
        level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, etc.)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            logging.StreamHandler()  # Log to console
        ]
    )
