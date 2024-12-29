import logging
from logging import Logger, StreamHandler
from logging.handlers import RotatingFileHandler

import pytest

from src.singleton_logger import SingletonLogger


def test_singleton_logger_instance() -> None:
    SingletonLogger.initialize()
    logger1 = SingletonLogger.get_logger()

    SingletonLogger.initialize()
    logger2 = SingletonLogger.get_logger()

    assert logger1 is logger2


def test_logger_initialization() -> None:
    SingletonLogger.initialize()
    logger = SingletonLogger.get_logger()

    assert logger is not None
    assert isinstance(logger, Logger)


def test_log_level() -> None:
    SingletonLogger.initialize()
    logger = SingletonLogger.get_logger()

    assert logger.level == logging.CRITICAL


def test_stream_handler_settings() -> None:
    SingletonLogger.initialize()
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
    SingletonLogger.initialize()
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


def test_logger_not_initialized() -> None:
    SingletonLogger._logger = None

    with pytest.raises(RuntimeError, match="Logger has not been initialized."):
        SingletonLogger.get_logger()
