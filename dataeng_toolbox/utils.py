"""
Utility functions for DataEng Toolbox.
"""

import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger
