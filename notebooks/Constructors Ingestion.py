# Databricks notebook source
from pyspark.sql.functions import col, explode, from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import *

# COMMAND ----------

constructors_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json("/mnt/formula1datalake1565/raw/constructors.json")

# COMMAND ----------

constructors_array_extracted_df = constructors_df.select(col('MRData').getItem("ConstructorTable").getItem("Constructors"))
constructors_array_exploded_df = constructors_array_extracted_df.select(explode(col("`MRData.ConstructorTable.Constructors`")))
constructors_parsed = constructors_array_exploded_df.withColumn("constructorId", col("col").getItem("constructorId")) \
    .withColumn("name", col("col").getItem("name")) \
    .withColumn("nationality", col("col").getItem("nationality")) \
    .withColumn("url", col("col").getItem("url")) \
    .drop("col")

# COMMAND ----------

constructors_selected_df = constructors_parsed.drop(col("url"))

constructors_renamed_df = constructors_selected_df.withColumnRenamed("constructorId", "constructor_id")
constructors_final_df = constructors_renamed_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

constructors_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/constructors")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/constructors"))
