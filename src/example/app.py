from logging import INFO
from logging import basicConfig as basic_config
from logging import getLogger as get_logger
from random import randint
from time import sleep
from typing import Any

AnyDict = dict[str, Any]  # type: ignore


def handle(event: AnyDict, context: AnyDict) -> None:
    """Lambda entry point."""
    basic_config(level=INFO)

    logger = get_logger("example")
    logger.info("Running example lambda.")

    iterations = randint(5, 10)
    for iteration in range(iterations):
        logger.info(f"Iteration {iteration}")
        sleep(0.01)
