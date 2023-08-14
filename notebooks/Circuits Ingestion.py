# Databricks notebook source
from pyspark.sql.functions import col, explode, from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import *

# COMMAND ----------

circuits_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json("/mnt/formula1datalake1565/raw/circuits.json")

# COMMAND ----------

circuits_array_extracted_df = circuits_df.select(col('MRData').getItem("CircuitTable").getItem("Circuits"))
circuits_array_exploded_df = circuits_array_extracted_df.select(explode(col("`MRData.CircuitTable.Circuits`")))
circuits_parsed = circuits_array_exploded_df.withColumn("circuitId", col("col").getItem("circuitId")) \
    .withColumn("circuitName", col("col").getItem("circuitName")) \
    .withColumn("url", col("col").getItem("url")) \
    .withColumn("country", col("col").getItem("Location").getItem("country")) \
    .withColumn("locality", col("col").getItem("Location").getItem("locality")) \
    .withColumn("lat", col("col").getItem("Location").getItem("lat")) \
    .withColumn("long", col("col").getItem("Location").getItem("long")) \
    .drop("col")

# COMMAND ----------

circuits_selected_df = circuits_parsed.drop(col("url"))

circuits_renamed_df = circuits_selected_df.withColumnRenamed("circuitId", "circuit_id") \
    .withColumnRenamed("circuitName", "circuit_name") \
    .withColumnRenamed("lat", "latitude") \
    .withColumnRenamed("long", "longitute") \
    .withColumnRenamed("alt", "altitude")

circuits_final_df = circuits_renamed_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

circuits_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/circuits")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/circuits"))
