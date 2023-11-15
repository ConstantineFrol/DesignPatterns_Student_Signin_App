import logging


class FileManager:
    def __init__(self, log_filename):
        self.log_filename = log_filename

        logging.basicConfig(
            level=logging.ERROR,
            filename=self.log_filename,
            filemode="a",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.logger = logging.getLogger("my_logger")

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

    def write_to_file(self, filename, content):
        with open(filename, 'a') as file:
            file.write(content)

    def read_from_file(self, filename):
        with open(filename, 'r') as file:
            return file.read()
