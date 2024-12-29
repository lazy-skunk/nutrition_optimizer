import os
import shutil
from typing import Generator
from unittest import mock

import pytest

from src.singleton_logger import SingletonLogger

_LOG_DIR = os.path.join("tests", "test_log")
_LOG_FILE = "app.log"
_LOG_PATH = os.path.join(_LOG_DIR, _LOG_FILE)


def _setup_environment_variables() -> None:
    os.environ["LOG_LEVEL"] = "CRITICAL"
    os.environ["LOG_PATH"] = _LOG_PATH
    os.environ["LOG_SIZE"] = str(1024 * 1024 * 99)
    os.environ["LOG_BACKUP"] = "99"


def _create_log_directory(log_dir: str) -> None:
    os.makedirs(log_dir, exist_ok=True)


def _remove_log_directory(log_dir: str) -> None:
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)


def _reset_environment_variables() -> None:
    os.environ.pop("LOG_LEVEL", None)
    os.environ.pop("LOG_PATH", None)
    os.environ.pop("LOG_SIZE", None)
    os.environ.pop("LOG_BACKUP", None)


@pytest.fixture(scope="module", autouse=True)
def initialize_test_logger() -> Generator[None, None, None]:
    _setup_environment_variables()
    _create_log_directory(_LOG_DIR)

    with mock.patch.dict(os.environ, {"LOG_PATH": _LOG_PATH}):
        SingletonLogger.initialize()

    try:
        yield
    finally:
        _remove_log_directory(_LOG_DIR)
        _reset_environment_variables()
