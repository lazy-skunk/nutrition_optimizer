import logging
from logging import Logger, StreamHandler
from logging.handlers import RotatingFileHandler

from src.singleton_logger import SingletonLogger


def test_singleton_logger_instance() -> None:
    logger1 = SingletonLogger.get_logger()
    logger2 = SingletonLogger.get_logger()

    assert logger1 is logger2


def test_logger_initialization() -> None:
    logger = SingletonLogger.get_logger()

    assert logger is not None
    assert isinstance(logger, Logger)


def test_log_level() -> None:
    logger = SingletonLogger.get_logger()

    assert logger.level == logging.CRITICAL


def test_stream_handler_settings() -> None:
    logger = SingletonLogger.get_logger()

    handlers = logger.handlers
    stream_handler = next(
        (
            handler
            for handler in handlers
            if isinstance(handler, StreamHandler)
        ),
        None,
    )

    assert stream_handler is not None
    assert stream_handler.level == logging.CRITICAL

    if stream_handler.formatter is None:
        raise ValueError("StreamHandler does not have a formatter set.")
    assert (
        stream_handler.formatter._fmt
        == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def test_rotating_file_handler_settings() -> None:
    logger = SingletonLogger.get_logger()

    handlers = logger.handlers
    rotating_file_handler = next(
        (
            handler
            for handler in handlers
            if isinstance(handler, RotatingFileHandler)
        ),
        None,
    )

    assert rotating_file_handler is not None
    assert rotating_file_handler.level == logging.CRITICAL
    assert rotating_file_handler.baseFilename == "/app/tests/test_log/app.log"
    assert rotating_file_handler.maxBytes == 1024 * 1024 * 99
    assert rotating_file_handler.backupCount == 99

    if rotating_file_handler.formatter is None:
        raise ValueError("RotatingFileHandler does not have a formatter set.")
    assert (
        rotating_file_handler.formatter._fmt
        == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
