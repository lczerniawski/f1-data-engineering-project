from diagrams import Diagram, Cluster
from diagrams.azure.database import DataFactory
from diagrams.azure.database import DataLake
from diagrams.generic.compute import Rack
from diagrams.azure.analytics import Databricks
from diagrams.generic.storage import Storage

with Diagram("F1 Data Engineering Project", show=True):
    api = Rack("API")
    adf = DataFactory("ADF")
    databricks = Databricks("Databricks")
    hive_meta_store = Storage("Hive Meta Store")

    with Cluster("Delta Lake"):
        raw = DataLake("Raw Layer")
        processed = DataLake("Processed Layer")
        presentation = DataLake("Presentation Layer")

    (
        api
        >> adf
        >> raw
        >> databricks
        >> processed
        >> databricks
        >> presentation
        >> databricks
        >> hive_meta_store
    )
