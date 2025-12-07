"""
Core module for DataEng Toolbox.

This module contains the main Core class with essential functionality.
"""

from typing import Dict


class BasePlatform:
    def __init__(self, spark, sparkutils) -> None:
        self.spark = spark
        self.sparkutils = sparkutils

    def get_spark(self):
        return self.spark
    
    def get_sparkutils(self):
        return self.sparkutils
    
    

class Core:
    """
    Core class providing fundamental functionality for the data engineering toolbox.

    This class serves as the main entry point for the toolbox functionality.
    """

    def __init__(self) -> None:
        """Initialize the Core class."""
        self.name = "DataEng Toolbox"
        self.version = "0.1.0"

    def hello_world(self) -> str:
        """
        Return a hello world message.

        Returns:
            str: A greeting message from the data engineering toolbox.
        """
        return f"Hello World from {self.name} v{self.version}!"

    def get_info(self) -> Dict[str, str]:
        """
        Get information about the toolbox.

        Returns:
            Dict[str, str]: Dictionary containing toolbox information.
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": "A comprehensive data engineering toolbox for Python"
        }
