
from typing import Union
from pyspark.sql.types import StructType, StructField
from pyspark.sql import DataFrame
from dataeng_toolbox.model import ColumnModel, ScdType, VTableModel
from dataeng_toolbox.core import Context
from abc import ABC, abstractmethod

class BaseEntity(ABC):
    """Base class for all entities."""
    def __init__(self, context: Context,  scd_type: ScdType) -> None:
        self._scd_type = scd_type
        self._context = context

    def get_scd_type(self) -> ScdType:
        """Get the SCD type of the entity."""
        return self._scd_type
    
    def get_context(self) -> Context:
        """Get the context of the entity."""
        return self._context
    
    def get_schema(self) -> StructType | None:
        """Get the schema for the entity."""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def apply_transformations(self) -> DataFrame:
        """Apply transformations to the DataFrame."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    def apply_deletions(self) -> DataFrame:
        """Apply deletions to the DataFrame."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    def initalize_state(self) -> None:
        """Initialize any state or dependencies for the entity."""
        pass  # Optional to implement in subclasses

    def finalize_state(self) -> None:
        """Finalize any state or dependencies for the entity."""
        pass  # Optional to implement in subclasses 
    


class SilverEntity(BaseEntity):
    def __init__(self, context: Context, scd_type: ScdType) -> None:
        super().__init__(context, scd_type)
        self._context = context


    def _get_dependencies(self) -> list[VTableModel]:
        """Get the list of dependency entities for the bronze entity."""
        return []
    
    def _load_dependencies(self) -> None:
        """Load dependencies for the bronze entity."""
        dependencies = self._get_dependencies()
        for dependency in dependencies:
            pass  # Implement loading logic here    

    def get_schema(self) -> list[ColumnModel]:
        """Get the schema for the silver entity."""
        return []