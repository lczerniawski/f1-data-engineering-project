# Databricks notebook source
processed_folder_path = "/mnt/formula1datalake1565/processed"
presentation_folder_path = "/mnt/formula1datalake1565/presentation"

# COMMAND ----------

from pyspark.sql.functions import sum, when, count, col

# COMMAND ----------

race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")

driver_standings_df = race_results_df \
    .groupBy("race_season", "driver_name", "driver_family_name", "driver_nationality", "constructor_name") \
    .agg(sum("points").alias("total_points"), count(when(col("position") == 1, True)).alias("wins"))

driver_standings_df.write.mode("overwrite").parquet(f"{presentation_folder_path}/driver_standings")
