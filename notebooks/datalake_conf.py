# Databricks notebook source
#Create variable with Access Key to DataLake
storageAccountAccessKey = ""

# COMMAND ----------

#Mount DataLake Raw to Databricks
dbutils.fs.mount(
    source="wasbs://raw@formula1datalake1565.blob.core.windows.net/",
    mount_point="/mnt/formula1datalake1565/raw",
    extra_configs = {'fs.azure.account.key.formula1datalake1565.blob.core.windows.net': storageAccountAccessKey})

# COMMAND ----------

#Mount DataLake Processed to Databricks
dbutils.fs.mount(
    source="wasbs://processed@formula1datalake1565.blob.core.windows.net/",
    mount_point="/mnt/formula1datalake1565/processed",
    extra_configs = {'fs.azure.account.key.formula1datalake1565.blob.core.windows.net': storageAccountAccessKey})

# COMMAND ----------

#Mount DataLake Presentation to Databricks
dbutils.fs.mount(
    source="wasbs://presentation@formula1datalake1565.blob.core.windows.net/",
    mount_point="/mnt/formula1datalake1565/presentation",
    extra_configs = {'fs.azure.account.key.formula1datalake1565.blob.core.windows.net': storageAccountAccessKey})
