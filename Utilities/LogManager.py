import logging


class LogManager:
    def __init__(self, log_filename):
        """Initialize the LogManager with the specified log filename."""
        self.log_filename = log_filename

        # Configure logger for both error and info messages
        logging.basicConfig(
            level=logging.INFO,
            filename=self.log_filename,
            filemode="a",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.error_logger = logging.getLogger("error")
        self.info_logger = logging.getLogger("info")

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.error_logger.addHandler(file_handler)
        self.info_logger.addHandler(file_handler)

    def log_error(self, message):
        """Log an error message."""
        self.error_logger.error(message)

    def log_info(self, message):
        """Log an info message."""
        self.info_logger.info(message)

    def write_to_file(self, content, log_function):
        """
        Write content to the log file using the specified log function.

        Parameters:
        - content: The content to be written to the log file.
        - log_function: The logging function to use (either log_error or log_info).
        """
        log_function(content)
        with open(self.log_filename, 'a') as file:
            file.write(content + '\n')

    def read_from_file(self):
        """Read the content of the log file."""
        with open(self.log_filename, 'r') as file:
            return file.read()
