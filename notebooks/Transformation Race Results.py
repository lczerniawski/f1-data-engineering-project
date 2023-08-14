# Databricks notebook source
processed_folder_path = "/mnt/formula1datalake1565/processed"
presentation_folder_path = "/mnt/formula1datalake1565/presentation"

# COMMAND ----------

drivers_df = spark.read.parquet(f"{processed_folder_path}/drivers") \
    .withColumnRenamed("number", "driver_number") \
    .withColumnRenamed("given_name", "driver_name") \
    .withColumnRenamed("family_name", "driver_family_name") \
    .withColumnRenamed("nationality", "driver_nationality") \
    .withColumnRenamed("date_of_birth", "driver_date_of_birth") \
    .drop("ingestion_date")

# COMMAND ----------

constructors_df = spark.read.parquet(f"{processed_folder_path}/constructors") \
    .withColumnRenamed("name", "constructor_name") \
    .withColumnRenamed("nationality", "constructor_nationality") \
    .drop("ingestion_date")

# COMMAND ----------

circuits_df = spark.read.parquet(f"{processed_folder_path}/circuits")  \
    .drop("ingestion_date")

# COMMAND ----------

races_df = spark.read.parquet(f"{processed_folder_path}/races") \
    .withColumnRenamed("name", "race_name") \
    .withColumnRenamed("time", "race_time") \
    .withColumnRenamed("date", "race_date") \
    .withColumnRenamed("season", "race_season") \
    .drop("ingestion_date")

# COMMAND ----------

results_df = spark.read.parquet(f"{processed_folder_path}/results") \
    .withColumnRenamed("time", "race_time") \
    .withColumnRenamed("date", "race_date") \
    .drop("ingestion_date") \
    .drop("race_name") \
    .drop("race_date") \
    .drop("race_time")

# COMMAND ----------

race_results_df = results_df.join(races_df, (results_df.round == races_df.round) & (results_df.season == races_df.race_season)) \
    .join(circuits_df, circuits_df.circuit_id ==races_df.circuit_id) \
    .join(drivers_df, drivers_df.driver_id == results_df.driver_id) \
    .join(constructors_df, results_df.constructor_id == constructors_df.constructor_id)

final_df = race_results_df.select("race_season", "race_name", "race_date", "locality", "driver_name", "driver_family_name", "permanent_number", "driver_nationality",
                                  "constructor_name", "grid", "race_time", "points", "position") \
                                  .withColumnRenamed("permanent_number", "driver_number")

final_df.write.mode("overwrite").parquet(f"{presentation_folder_path}/race_results")
