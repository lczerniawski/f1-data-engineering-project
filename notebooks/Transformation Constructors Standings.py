# Databricks notebook source
processed_folder_path = "/mnt/formula1datalake1565/processed"
presentation_folder_path = "/mnt/formula1datalake1565/presentation"

# COMMAND ----------

from pyspark.sql.functions import sum, when, count, col

# COMMAND ----------

race_results_df = spark.read.parquet(f"{presentation_folder_path}/race_results")

constructor_standings_df = race_results_df \
    .groupBy("race_season", "constructor_name") \
    .agg(sum("points").alias("total_points"), count(when(col("position") == 1, True)).alias("wins"))

display(constructor_standings_df)

constructor_standings_df.write.mode("overwrite").parquet(f"{presentation_folder_path}/constructor_standings")
