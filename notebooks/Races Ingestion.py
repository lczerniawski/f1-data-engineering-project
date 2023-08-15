# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

races_df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .json("/mnt/formula1datalake1565/raw/races.json")
)

# COMMAND ----------

races_array_extracted_df = races_df.select(F.col('MRData').getItem("RaceTable").getItem("Races"))
races_array_exploded_df = races_array_extracted_df.select(F.explode(F.col("`MRData.RaceTable.Races`")))
races_parsed = (
    races_array_exploded_df.withColumn("raceName", F.col("col").getItem("raceName"))
        .withColumn("round", F.col("col").getItem("round"))
        .withColumn("season", F.col("col").getItem("season"))
        .withColumn("time", F.col("col").getItem("time"))
        .withColumn("date", F.col("col").getItem("date"))
        .withColumn("url", F.col("col").getItem("url"))
        .withColumn("circuitId", F.col("col").getItem("Circuit").getItem("circuitId"))
        .drop("col")
)

# COMMAND ----------

races_selected_df = races_parsed.drop(F.col("url"))

races_renamed_df = (
    races_selected_df.withColumnRenamed("raceName", "race_name")
    .withColumnRenamed("circuitId", "circuit_id")
    .withColumn("round", races_selected_df.round.cast(T.IntegerType()))
    .withColumn("date", races_selected_df.date.cast(T.DateType()))
)

races_final_df = races_renamed_df.withColumn("ingestion_date", F.current_timestamp())

# COMMAND ----------

races_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/races")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/races"))
