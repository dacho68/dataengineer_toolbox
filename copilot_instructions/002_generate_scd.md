# Objective 1
create me an slow change dimension type 1 function using spark MERGE INTO using the signature below

# method signature
def scd_type1(spark, target_table: str, source_df:DataFrame, composite_keys: list, scd_columns: list):
parameter:
        spark: SparkSession
        source_df: Source Spark DataFrame
        target_table: Target table name
        composite_keys: List of join key columns
        scd_columns: List of columns to track changes

# output :
insert the function into spark_utils.py