# Databricks notebook source
from pyspark.sql.functions import col, explode, from_json
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import *

# COMMAND ----------

drivers_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json("/mnt/formula1datalake1565/raw/drivers.json")

display(drivers_df)

# COMMAND ----------

drivers_array_extracted_df = drivers_df.select(col('MRData').getItem("DriverTable").getItem("Drivers"))
drivers_array_exploded_df = drivers_array_extracted_df.select(explode(col("`MRData.DriverTable.Drivers`")))
drivers_parsed = drivers_array_exploded_df.withColumn("driverId", col("col").getItem("driverId")) \
    .withColumn("givenName", col("col").getItem("givenName")) \
    .withColumn("familyName", col("col").getItem("familyName")) \
    .withColumn("nationality", col("col").getItem("nationality")) \
    .withColumn("dateOfBirth", col("col").getItem("dateOfBirth")) \
    .withColumn("code", col("col").getItem("code")) \
    .withColumn("permanentNumber", col("col").getItem("permanentNumber")) \
    .withColumn("url", col("col").getItem("url")) \
    .drop("col")

# COMMAND ----------

drivers_selected_df = drivers_parsed.drop(col("url"))

drivers_renamed_df = drivers_selected_df.withColumnRenamed("driverId", "driver_id") \
    .withColumnRenamed("givenName", "given_name") \
    .withColumnRenamed("familyName", "family_name") \
    .withColumnRenamed("dateOfBirth", "date_of_birth") \
    .withColumnRenamed("permanentNumber", "permanent_number")

drivers_final_df = drivers_renamed_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

drivers_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/drivers")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/drivers"))
