# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

results_df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .json("/mnt/formula1datalake1565/raw/results.json")
)

# COMMAND ----------

results_array_extracted_df = results_df.select(F.col('MRData').getItem("RaceTable").getItem("Races"))
results_array_exploded_df = results_array_extracted_df.select(F.explode(F.col("`MRData.RaceTable.Races`")))

results_with_results_exploded_df = (
    results_array_exploded_df.withColumn("circuitId", F.col("col").getItem("Circuit").getItem("circuitId"))
        .withColumn("date", F.col("col").getItem("date"))
        .withColumn("raceName", F.col("col").getItem("raceName"))
        .withColumn("round", F.col("col").getItem("round"))
        .withColumn("season", F.col("col").getItem("season"))
        .withColumn("url", F.col("col").getItem("url"))
        .withColumn("results_exploded", F.explode(F.col("col").getItem("Results")))
        .drop("col")
)

results_parsed_df = (
    results_with_results_exploded_df.withColumn("constructorId", F.col("results_exploded").getItem("Constructor").getItem("constructorId"))
        .withColumn("driverId", F.col("results_exploded").getItem("Driver").getItem("driverId"))
        .withColumn("millis", F.col("results_exploded").getItem("Time").getItem("millis"))
        .withColumn("time", F.col("results_exploded").getItem("Time").getItem("time"))
        .withColumn("grid", F.col("results_exploded").getItem("grid"))
        .withColumn("laps", F.col("results_exploded").getItem("laps"))
        .withColumn("number", F.col("results_exploded").getItem("number"))
        .withColumn("points", F.col("results_exploded").getItem("points"))
        .withColumn("position", F.col("results_exploded").getItem("position"))
        .withColumn("positionText", F.col("results_exploded").getItem("positionText"))
        .withColumn("status", F.col("results_exploded").getItem("status"))
        .drop("results_exploded")
)

# COMMAND ----------

results_selected_df = results_parsed_df.drop(F.col("url"))

results_renamed_casted_df = (
    results_selected_df.withColumnRenamed("circuitId", "circuit_id")
        .withColumnRenamed("raceName", "race_name")
        .withColumnRenamed("constructorId", "constructor_id")
        .withColumnRenamed("driverId", "driver_id")
        .withColumn("date", results_selected_df.date.cast(T.DateType()))
        .withColumn("round", results_selected_df.round.cast(T.IntegerType()))
        .withColumn("grid", results_selected_df.grid.cast(T.IntegerType()))
        .withColumn("laps", results_selected_df.laps.cast(T.IntegerType()))
        .withColumn("number", results_selected_df.number.cast(T.IntegerType()))
        .withColumn("points", results_selected_df.points.cast(T.IntegerType()))
        .withColumn("position", results_selected_df.position.cast(T.IntegerType()))
)
results_final_df = results_renamed_casted_df.withColumn("ingestion_date", F.current_timestamp())

# COMMAND ----------

results_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/results")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/results"))
