import logging


class LogManager:
    def __init__(self, log_filename):
        self.log_filename = log_filename

        logging.basicConfig(
            level=logging.ERROR,
            filename=self.log_filename,
            filemode="a",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.logger = logging.getLogger("log_message")

    def log_error(self, message):
        self.write_to_file(self.logger.error(message))

    def log_info(self, message):
        self.write_to_file(self.logger.info(message))

    def write_to_file(self, content):
        with open(self.log_filename, 'a') as file:
            file.write(content)

    def read_from_file(self):
        with open(self.log_filename, 'r') as file:
            return file.read()
