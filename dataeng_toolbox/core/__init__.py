# ---------------------------------------------------------------------------
# File History
# ---------------------------------------------------------------------------
# 2026-02-28  Initial creation
# ---------------------------------------------------------------------------

"""
Core module for DataEng Toolbox.

This module contains the main Core class with essential functionality.
"""

from typing import Dict
from unicodedata import name

from dataeng_toolbox.model import CloudProvider, PlatformType


class BasePlatform:
    def __init__(self, spark, sparkutils) -> None:
        self.spark = spark
        self.sparkutils = sparkutils

    def get_spark(self):
        return self.spark
    
    def get_sparkutils(self):
        return self.sparkutils
    
class DatabricksPlatform(BasePlatform):
    def __init__(self, spark, dbutils, cloud_provider = CloudProvider.AZURE) -> None:
        super().__init__(spark, dbutils)
        self.cloud_provider = cloud_provider

    
class FabricPlatform(BasePlatform):
    def __init__(self, spark, dbutils) -> None:
        super().__init__(spark, dbutils)

class Context:
    def __init__(self, platform: BasePlatform,  logger) -> None:
        self.__platform__ = platform
        self.__logger__ = logger
        self.__custom_properties__ = {} 

    def get_platform(self) -> BasePlatform:
        return self.__platform__

    def get_logger(self):
        return self.__logger__

    def set_property(self, key: str, value):
        """Set a custom property in the context."""
        self.__custom_properties__[key] = value
    
    def get_property(self, key: str):
        """Get a custom property from the context."""
        return self.__custom_properties__.get(key, None)    

class PlatformFactory:
    @staticmethod
    def create_platform(platform_type: PlatformType, spark=None, dbutils=None):
        """Factory method to create platform instances."""
        if platform_type == PlatformType.DATABRICKS:
            return DatabricksPlatform(spark, dbutils)
        elif platform_type == PlatformType.FABRIC:
            # Implement Fabric platform initialization here
            return FabricPlatform(spark, dbutils)
        else:
            raise ValueError(f"Unsupported platform type: {platform_type}")
