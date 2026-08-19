"""
Centralized logging configuration for the Travel Agent.
"""
import logging

logger = logging.getLogger("travel_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(handler)
