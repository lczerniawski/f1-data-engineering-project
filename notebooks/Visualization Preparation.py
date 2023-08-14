# Databricks notebook source
# MAGIC %sql
# MAGIC create database if not exists formula1_db

# COMMAND ----------

presentation_folder_path = "/mnt/formula1datalake1565/presentation"

# COMMAND ----------

raceresults_df = spark.read.parquet(f"{presentation_folder_path}/race_results")
raceresults_df.write.mode("overwrite").format("parquet").saveAsTable("formula1_db.race_results")

# COMMAND ----------

driver_standings_df = spark.read.parquet(f"{presentation_folder_path}/driver_standings")
driver_standings_df.write.mode("overwrite").format("parquet").saveAsTable("formula1_db.driver_standings")

# COMMAND ----------

constructor_standings_df = spark.read.parquet(f"{presentation_folder_path}/constructor_standings")
constructor_standings_df.write.mode("overwrite").format("parquet").saveAsTable("formula1_db.constructor_standings")

# COMMAND ----------

# MAGIC %sql
# MAGIC show tables in formula1_db

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM formula1_db.constructor_standings
