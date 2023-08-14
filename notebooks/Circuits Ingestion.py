# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

circuits_df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .json("/mnt/formula1datalake1565/raw/circuits.json")
)

# COMMAND ----------

circuits_array_extracted_df = circuits_df.select(F.col('MRData').getItem("CircuitTable").getItem("Circuits"))
circuits_array_exploded_df = circuits_array_extracted_df.select(F.explode(F.col("`MRData.CircuitTable.Circuits`")))
circuits_parsed = (
    circuits_array_exploded_df.withColumn("circuitId", F.col("col").getItem("circuitId"))
        .withColumn("circuitName", F.col("col").getItem("circuitName"))
        .withColumn("url", F.col("col").getItem("url"))
        .withColumn("country", F.col("col").getItem("Location").getItem("country"))
        .withColumn("locality", F.col("col").getItem("Location").getItem("locality"))
        .withColumn("lat", F.col("col").getItem("Location").getItem("lat"))
        .withColumn("long", F.col("col").getItem("Location").getItem("long"))
        .drop("col")
)

# COMMAND ----------

circuits_selected_df = circuits_parsed.drop(F.col("url"))

circuits_renamed_df = (
    circuits_selected_df.withColumnRenamed("circuitId", "circuit_id")
        .withColumnRenamed("circuitName", "circuit_name")
        .withColumnRenamed("lat", "latitude")
        .withColumnRenamed("long", "longitute")
        .withColumnRenamed("alt", "altitude")
)
circuits_final_df = circuits_renamed_df.withColumn("ingestion_date", F.current_timestamp())

# COMMAND ----------

circuits_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/circuits")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/circuits"))

# COMMAND ----------


