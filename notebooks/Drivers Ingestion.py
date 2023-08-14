# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

drivers_df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .json("/mnt/formula1datalake1565/raw/drivers.json")
)

# COMMAND ----------

drivers_array_extracted_df = drivers_df.select(F.col('MRData').getItem("DriverTable").getItem("Drivers"))
drivers_array_exploded_df = drivers_array_extracted_df.select(F.explode(F.col("`MRData.DriverTable.Drivers`")))
drivers_parsed = (
    drivers_array_exploded_df.withColumn("driverId", F.col("col").getItem("driverId"))
    .withColumn("givenName", F.col("col").getItem("givenName"))
    .withColumn("familyName", F.col("col").getItem("familyName"))
    .withColumn("nationality", F.col("col").getItem("nationality"))
    .withColumn("dateOfBirth", F.col("col").getItem("dateOfBirth"))
    .withColumn("code", F.col("col").getItem("code"))
    .withColumn("permanentNumber", F.col("col").getItem("permanentNumber"))
    .withColumn("url", F.col("col").getItem("url"))
    .drop("col")
)

# COMMAND ----------

drivers_selected_df = drivers_parsed.drop(F.col("url"))

drivers_renamed_df = (
    drivers_selected_df.withColumnRenamed("driverId", "driver_id")
        .withColumnRenamed("givenName", "given_name")
        .withColumnRenamed("familyName", "family_name")
        .withColumnRenamed("dateOfBirth", "date_of_birth")
        .withColumnRenamed("permanentNumber", "permanent_number")
)
drivers_final_df = drivers_renamed_df.withColumn("ingestion_date", F.current_timestamp())

# COMMAND ----------

drivers_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/drivers")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/drivers"))
