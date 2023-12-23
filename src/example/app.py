from datetime import datetime, timezone
from json import dumps
from logging import INFO, WARNING, Formatter, LogRecord
from logging import basicConfig as basic_config
from logging import getLogger as get_logger
from random import randint
from time import sleep
from traceback import format_exception
from typing import Any
from uuid import UUID, uuid4

AnyDict = dict[str, Any]  # type: ignore


class JSONFormatter(Formatter):
    def __init__(self, fmt: str) -> None:
        # We are required to consume a format  string; we don't use it.
        super().__init__(fmt)

        # We'd normally fetch these values from an external context.
        self.request_id: UUID = uuid4()
        self.trace_id: UUID = uuid4()

    def format(self, record: LogRecord) -> str:
        data = dict(
            level=record.levelname,
            message=record.getMessage(),
            name=record.name,
            timestamp=datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
        )

        # We'd normally inject a number of contextual variables here, not just these.
        data.update(
            requestId=str(self.request_id),
            traceId=str(self.trace_id),
        )

        if record.exc_info:
            data.update(exc_info="\n".join(format_exception(*record.exc_info)))

        return dumps(data)


def configure_logging() -> None:
    log_format = "%(levelname)s | %(name)s | %(message)s"
    log_level = INFO

    get_logger().level = log_level
    get_logger("botocore").level = WARNING

    basic_config(
        format=log_format,
        level=log_level,
    )

    formatter = JSONFormatter(log_format)

    for handler in get_logger().handlers:
        handler.setFormatter(formatter)


def handle(event: AnyDict, context: AnyDict) -> None:
    """Lambda entry point."""

    configure_logging()

    logger = get_logger("example")
    logger.info("Running example lambda.")

    iterations = randint(5, 10)
    for iteration in range(iterations):
        logger.info(f"Iteration {iteration}")
        sleep(0.01)
