# Databricks notebook source
from pyspark.sql.functions import col, explode, from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import *

# COMMAND ----------

results_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json("/mnt/formula1datalake1565/raw/results.json")

display(results_df)

# COMMAND ----------

results_array_extracted_df = results_df.select(col('MRData').getItem("RaceTable").getItem("Races"))
results_array_exploded_df = results_array_extracted_df.select(explode(col("`MRData.RaceTable.Races`")))

results_with_results_exploded_df = results_array_exploded_df.withColumn("circuitId", col("col").getItem("Circuit").getItem("circuitId")) \
    .withColumn("date", col("col").getItem("date")) \
    .withColumn("raceName", col("col").getItem("raceName")) \
    .withColumn("round", col("col").getItem("round")) \
    .withColumn("season", col("col").getItem("season")) \
    .withColumn("url", col("col").getItem("url")) \
    .withColumn("results_exploded", explode(col("col").getItem("Results"))) \
    .drop("col")

results_parsed_df = results_with_results_exploded_df.withColumn("constructorId", col("results_exploded").getItem("Constructor").getItem("constructorId")) \
    .withColumn("driverId", col("results_exploded").getItem("Driver").getItem("driverId")) \
    .withColumn("millis", col("results_exploded").getItem("Time").getItem("millis")) \
    .withColumn("time", col("results_exploded").getItem("Time").getItem("time")) \
    .withColumn("grid", col("results_exploded").getItem("grid")) \
    .withColumn("laps", col("results_exploded").getItem("laps")) \
    .withColumn("number", col("results_exploded").getItem("number")) \
    .withColumn("points", col("results_exploded").getItem("points")) \
    .withColumn("position", col("results_exploded").getItem("position")) \
    .withColumn("positionText", col("results_exploded").getItem("positionText")) \
    .withColumn("status", col("results_exploded").getItem("status")) \
    .drop("results_exploded")

display(results_parsed_df)

# COMMAND ----------

results_selected_df = results_parsed_df.drop(col("url"))

results_renamed_casted_df = results_selected_df.withColumnRenamed("circuitId", "circuit_id") \
    .withColumnRenamed("raceName", "race_name") \
    .withColumnRenamed("constructorId", "constructor_id") \
    .withColumnRenamed("driverId", "driver_id") \
    .withColumn("date", results_selected_df.date.cast(DateType())) \
    .withColumn("round", results_selected_df.round.cast(IntegerType())) \
    .withColumn("grid", results_selected_df.grid.cast(IntegerType())) \
    .withColumn("laps", results_selected_df.laps.cast(IntegerType())) \
    .withColumn("number", results_selected_df.number.cast(IntegerType())) \
    .withColumn("points", results_selected_df.points.cast(IntegerType())) \
    .withColumn("position", results_selected_df.position.cast(IntegerType()))

results_final_df = results_renamed_casted_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

results_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/results")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/results"))
