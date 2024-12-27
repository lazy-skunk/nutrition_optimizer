import logging
import os
from logging import Formatter, Logger, StreamHandler
from logging.handlers import RotatingFileHandler

_DEFAULT_LOG_LEVEL = logging.DEBUG
_DEFAULT_LOG_PATH = "log/app.log"
_DEFAULT_LOG_SIZE = 1024 * 1024 * 10
_DEFAULT_LOG_BACKUP = 3


class SingletonLogger:
    _logger: Logger | None = None

    @classmethod
    def _get_log_level(cls) -> str | int:
        log_level = os.getenv("LOG_LEVEL", _DEFAULT_LOG_LEVEL)
        return log_level

    @classmethod
    def _add_stream_handler(
        cls, log_level: str | int, formatter: Formatter
    ) -> None:
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized.")

        stream_handler = StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)

        cls._logger.addHandler(stream_handler)

    @classmethod
    def _add_rotating_file_handler(
        cls, log_level: str | int, formatter: Formatter
    ) -> None:
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized.")

        log_path = os.getenv("LOG_PATH", _DEFAULT_LOG_PATH)
        log_size = int(os.getenv("LOG_SIZE", _DEFAULT_LOG_SIZE))
        log_backup = int(os.getenv("LOG_BACKUP", _DEFAULT_LOG_BACKUP))

        rotating_file_handler = RotatingFileHandler(
            log_path, maxBytes=log_size, backupCount=log_backup
        )
        rotating_file_handler.setLevel(log_level)
        rotating_file_handler.setFormatter(formatter)

        cls._logger.addHandler(rotating_file_handler)

    @classmethod
    def initialize(cls) -> None:
        if cls._logger is None:
            cls._logger = logging.getLogger("nutrition_optimizer")

            log_level = cls._get_log_level()
            cls._logger.setLevel(log_level)

            formatter = Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            cls._add_stream_handler(log_level, formatter)
            cls._add_rotating_file_handler(log_level, formatter)

    @classmethod
    def get_logger(cls) -> Logger:
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized.")

        return cls._logger
