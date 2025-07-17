from NetworkSecurity.components.data_ingestion import  DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts
import sys

if __name__ == '__main__':
    try:

        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")

        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)

        data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                      data_validation_config=data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)

    except Exception as e:
        raise CustomException(e, sys)

