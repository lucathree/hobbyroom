from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


logger.remove()

logger.add(
    sys.stderr,
    level="INFO",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "{name}:{function}:{line} | {message}"
    ),
    enqueue=True,
    colorize=True,
)


def get_logger() -> Logger:
    return logger
