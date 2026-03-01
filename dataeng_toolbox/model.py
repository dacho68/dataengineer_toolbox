from enum import Enum
from pyspark.sql.types import StructField
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class Constants:
    METADATA_IDENTITY_KEY = "identity"
    METADATA_DATA_HASH = "data_hash"
    METADATA_KEY_HASH = "key_hash"
    

    DEFAULT_SCD2_EFFECTIVE_DATE_COL = "EffectiveDate"
    DEFAULT_SCD2_END_DATE_COL = "EndDate"
    DEFAULT_SCD2_IS_CURRENT_COL = "IsCurrent"
    DEFAULT_SCD2_CURRENT_FLAG_VALUE = True
    DEFAULT_SCD2_END_DATE_FAR_FUTURE = "9999-12-31"


class ScdType(Enum):
    UNDEFINED = 0
    SCD0 = 1
    SCD1 = 2
    SCD2 = 3

class TableType(Enum):
    UNDEFINED = 0
    MANAGED = 1
    EXTERNAL = 2

class FileType(Enum):
    UNDEFINED = 0
    CSV = 1
    PARQUET = 2
    DELTA = 3
    JSON = 4
    

class IngestionType(Enum):
    UNDEFINED = 0
    FULL_LOAD = 1
    INCREMENTAL = 2

class PlatformType(Enum):
    UNDEFINED = 0
    DATABRICKS = 1
    FABRIC = 2

class CloudProvider(Enum):
    UNDEFINED = 0
    AWS = 1
    AZURE = 2
    GCP = 3

class ColumnModel(StructField):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)

    def is_identity(self) -> bool:
        """Check if the column is an identity column."""
        if Constants.METADATA_IDENTITY_KEY in self.metadata:
            return self.metadata[Constants.METADATA_IDENTITY_KEY] is True
        return False


class VFileModel(BaseModel):
    """Pydantic model for representing a virtual file."""
    model_config = ConfigDict(frozen=False, validate_assignment=True)
    catalog: str | None = None
    namespace: str | None = None
    name: str
    file_path: str
    file_type: FileType = FileType.UNDEFINED

class VTableModel(VFileModel):
    """Pydantic model for representing a virtual table."""
    file_path: str | None = None
    table_type: TableType = TableType.UNDEFINED

    @model_validator(mode="after")
    def validate_external_requires_delta(self) -> "VTableModel":
        """EXTERNAL tables must use DELTA file type."""
        if self.table_type == TableType.EXTERNAL and self.file_type != FileType.DELTA:
            raise ValueError(
                f"EXTERNAL tables must have FileType.DELTA, got {self.file_type}"
            )
        return self


def main() -> None:
    """Simple demo entrypoint for the module.

    Creates example VTableModel instances and prints their serialized forms.
    """
    v1 = VTableModel(catalog="main", namespace="sales", name="orders")
    v2 = VTableModel(catalog="main", namespace="inventory", name="products", table_type=TableType.MANAGED)

    print("Example VTableModel v1:")
    print(v1)
    print("model_dump:", v1.model_dump())
    print("model_dump_json:", v1.model_dump_json())

    print("\nExample VTableModel v2 (managed):")
    print(v2)
    print("model_dump:", v2.model_dump())
    print("model_dump_json:", v2.model_dump_json())


if __name__ == "__main__":
    main()

