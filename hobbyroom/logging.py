from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


logger.add(
    sys.stdout,
    level="INFO",
    format="{level} | {time} | {message}",
)


def get_logger() -> Logger:
    return logger
