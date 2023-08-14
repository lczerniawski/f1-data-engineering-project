# Databricks notebook source
from pyspark.sql.functions import col, explode, from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import *

# COMMAND ----------

races_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json("/mnt/formula1datalake1565/raw/races.json")

display(races_df)

# COMMAND ----------

races_array_extracted_df = races_df.select(col('MRData').getItem("RaceTable").getItem("Races"))
races_array_exploded_df = races_array_extracted_df.select(explode(col("`MRData.RaceTable.Races`")))
races_parsed = races_array_exploded_df.withColumn("raceName", col("col").getItem("raceName")) \
    .withColumn("round", col("col").getItem("round")) \
    .withColumn("season", col("col").getItem("season")) \
    .withColumn("time", col("col").getItem("time")) \
    .withColumn("date", col("col").getItem("date")) \
    .withColumn("url", col("col").getItem("url")) \
    .withColumn("circuitId", col("col").getItem("Circuit").getItem("circuitId")) \
    .drop("col")

# COMMAND ----------

races_selected_df = races_parsed.drop(col("url"))

races_renamed_df = races_selected_df.withColumnRenamed("raceName", "race_name") \
    .withColumnRenamed("circuitId", "circuit_id") \
    .withColumn("round", races_selected_df.round.cast(IntegerType())) \
    .withColumn("date", races_selected_df.date.cast(DateType()))

races_final_df = races_renamed_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

races_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/races")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/races"))
