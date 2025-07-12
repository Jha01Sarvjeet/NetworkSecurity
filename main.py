from NetworkSecurity.components.data_ingestion import  DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import sys

if __name__ == '__main__':
    try:

        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")

    except Exception as e:
        raise CustomException(e, sys)

