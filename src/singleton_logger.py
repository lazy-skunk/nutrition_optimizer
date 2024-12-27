import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Optional

_DEFAULT_LOG_LEVEL = logging.DEBUG
_DEFAULT_LOG_PATH = "log/app.log"
_DEFAULT_LOG_SIZE = 1024 * 1024 * 5
_DEFAULT_LOG_BACKUP = 5


class SingletonLogger(object):
    _instance: Optional["SingletonLogger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "SingletonLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger(*args, **kwargs)
        return cls._instance

    def _initialize_logger(
        self,
        log_level: int = _DEFAULT_LOG_LEVEL,
        log_path: str = _DEFAULT_LOG_PATH,
        log_size: int = _DEFAULT_LOG_SIZE,
        log_backup: int = _DEFAULT_LOG_BACKUP,
    ) -> None:
        if SingletonLogger._logger is None:
            SingletonLogger._logger = logging.getLogger("nutrition_optimizer")
            SingletonLogger._logger.setLevel(log_level)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(formatter)
            SingletonLogger._logger.addHandler(console_handler)

            file_handler = RotatingFileHandler(
                log_path, maxBytes=log_size, backupCount=log_backup
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            SingletonLogger._logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = cls()

        if cls._logger is None:
            raise RuntimeError(
                "Unexpected error occurred. Logger is not initialized."
            )

        return cls._logger
