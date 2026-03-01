from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import expr

from dataeng_toolbox.model import Constants, FileType
from dataeng_toolbox.utils import get_logger

logger = get_logger(__name__)


def scd_type1(spark: SparkSession, target_table: str, source_df: DataFrame, 
              composite_keys: list, scd_columns: list) -> None:
    """
    Implements SCD Type 1 using Spark MERGE INTO.
    Updates existing records with new values, inserts new records.
    
    Args:
        spark: SparkSession
        target_table: Target table name
        source_df: Source Spark DataFrame
        composite_keys: List of composite key columns for matching
        scd_columns: List of columns to track changes
    """
    source_df.createOrReplaceTempView("source")
    
    join_condition = " AND ".join([f"target.{col} = source.{col}" for col in composite_keys])
    
    update_set = ", ".join([f"target.{col} = source.{col}" for col in scd_columns])
    
    insert_columns = ", ".join(composite_keys + scd_columns)
    insert_values = ", ".join([f"source.{col}" for col in composite_keys + scd_columns])
    
    merge_sql = f"""
    MERGE INTO {target_table} target
    USING source
    ON {join_condition}
    WHEN MATCHED THEN
        UPDATE SET {update_set}
    WHEN NOT MATCHED THEN
        INSERT ({insert_columns})
        VALUES ({insert_values})
    """
    
    logger.info(f"Executing SCD Type 1 MERGE SQL:\n{merge_sql}")   
    spark.sql(merge_sql)


def scd_type1_with_hash(spark: SparkSession, target_table: str, source_df: DataFrame, 
              composite_keys: list, scd_columns: list, add_key_hash: bool = False, 
              add_data_hash: bool = False, identity_column: str = None) -> None:
    """
    Implements SCD Type 1 using Spark MERGE INTO.
    Updates existing records with new values, inserts new records.
    
    Args:
        spark: SparkSession
        target_table: Target table name
        source_df: Source Spark DataFrame
        composite_keys: List of composite key columns for matching
        scd_columns: List of columns to track changes
        add_key_hash: Whether to add a hash column for the composite key
        add_data_hash: Whether to add a hash column for the SCD columns
        identity_column: Optional identity column for the target table
    """
    source_df.createOrReplaceTempView("source")
    
    if add_key_hash:
        source_df = source_df.withColumn("key_hash", hash(*composite_keys))
        composite_keys.append("key_hash")

    if add_data_hash:
        source_df = source_df.withColumn("data_hash", hash(*scd_columns))
        scd_columns.append("data_hash")

    if identity_column:
        source_df = source_df.withColumn(identity_column, expr("uuid()"))
    
    update_set = ", ".join([f"target.{col} = source.{col}" for col in scd_columns])
    
    insert_columns = ", ".join(composite_keys + scd_columns)
    insert_values = ", ".join([f"source.{col}" for col in composite_keys + scd_columns])
    
    if add_data_hash:
        merge_sql = f"""
        MERGE INTO {target_table} target
        USING source
        ON target.{Constants.METADATA_KEY_HASH} = source.{Constants.METADATA_KEY_HASH}
        WHEN MATCHED  AND (
            target.{Constants.METADATA_DATA_HASH} != source.{Constants.METADATA_DATA_HASH}
        ) 
        THEN
            UPDATE SET {update_set}
        WHEN NOT MATCHED THEN
            INSERT ({insert_columns})
            VALUES ({insert_values})
        """
    else:
        merge_sql = f"""
        MERGE INTO {target_table} target
        USING source
        ON target.{Constants.METADATA_KEY_HASH} = source.{Constants.METADATA_KEY_HASH}
        WHEN MATCHED 
        THEN
            UPDATE SET {update_set}
        WHEN NOT MATCHED THEN
            INSERT ({insert_columns})
            VALUES ({insert_values})
        """

    logger.info(f"Executing SCD Type 1 MERGE SQL:\n{merge_sql}")   
    spark.sql(merge_sql)


def scd_type2(spark, target_table: str, source_df, join_keys: list, 
              scd_columns: list, business_key: str) -> None:
    """
    Implements SCD Type 1 using Spark MERGE INTO.
    
    Args:
        spark: SparkSession
        target_table: Target table name
        source_df: Source DataFrame
        join_keys: List of join key columns
        scd_columns: List of columns to track changes
        business_key: Business key column name
    """
    source_df.createOrReplaceTempView("source")
    
    join_condition = " AND ".join([f"target.{col} = source.{col}" for col in join_keys])
    
    scd_updates = ", ".join([f"target.{col} = source.{col}" for col in scd_columns])
    
    merge_sql = f"""
    MERGE INTO {target_table} target
    USING source
    ON {join_condition}
    WHEN MATCHED AND (
        {" OR ".join([f"target.{col} != source.{col}" for col in scd_columns])}
    ) THEN
        UPDATE SET 
            is_current = false,
            is_deleted = false,
            end_date = current_date()
    WHEN NOT MATCHED THEN
        INSERT ({business_key}, {", ".join(scd_columns)}, is_current, is_deleted, start_date, end_date)
        VALUES (source.{business_key}, {", ".join([f"source.{col}" for col in scd_columns])}, true, false, current_date(), null)
    """
    
    spark.sql(merge_sql)


def load_file(spark: SparkSession, file_path: str, file_type: FileType) -> DataFrame:
    """
    Loads a file into a Spark DataFrame based on the specified file type.
    
    Args:
        spark: SparkSession
        file_path: Path to the file
        file_type: Type of the file (e.g., CSV, JSON, Parquet)
    
    Returns:
        DataFrame containing the loaded data
    """
    if file_type == FileType.CSV:
        return spark.read.csv(file_path, header=True, inferSchema=True)
    elif file_type == FileType.JSON:
        return spark.read.json(file_path)
    elif file_type == FileType.PARQUET:
        return spark.read.parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")