# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

constructors_df = (
    spark.read 
        .option("header", True) 
        .option("inferSchema", True) 
        .json("/mnt/formula1datalake1565/raw/constructors.json")
)

# COMMAND ----------

constructors_array_extracted_df = constructors_df.select(F.col('MRData').getItem("ConstructorTable").getItem("Constructors"))
constructors_array_exploded_df = constructors_array_extracted_df.select(F.explode(F.col("`MRData.ConstructorTable.Constructors`")))
constructors_parsed = (
    constructors_array_exploded_df.withColumn("constructorId", F.col("col").getItem("constructorId")) 
        .withColumn("name", F.col("col").getItem("name")) 
        .withColumn("nationality", F.col("col").getItem("nationality")) 
        .withColumn("url", F.col("col").getItem("url")) 
        .drop("col")
)

# COMMAND ----------

constructors_selected_df = constructors_parsed.drop(F.col("url"))

constructors_renamed_df = constructors_selected_df.withColumnRenamed("constructorId", "constructor_id")
constructors_final_df = constructors_renamed_df.withColumn("ingestion_date", F.current_timestamp())

# COMMAND ----------

constructors_final_df.write.mode("overwrite").parquet("/mnt/formula1datalake1565/processed/constructors")
display(spark.read.parquet("/mnt/formula1datalake1565/processed/constructors"))
