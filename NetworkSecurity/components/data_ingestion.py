import os
import sys
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
# from push_data import MONGO_DB_URL
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts

load_dotenv()
MONGO_DB_URL = os.getenv('MONGODB_URL')

print(f"Current working directory: {os.getcwd()}")
print(f"MONGO_DB_URL value: {MONGO_DB_URL}")
print(f"MONGO_DB_URL type: {type(MONGO_DB_URL)}")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config: DataIngestionConfig = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_dataframe(self):
        '''read data from mongodb'''
        try:

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if df.columns.tolist() == ['_id']:
                df.drop(columns=['_id'], inplace=True, axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store(self, dataframe):
        """export data into feature store"""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # create folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False)
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """split data into train and test"""
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            dataIngestion_config = DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            return dataIngestion_config
        except Exception as e:
            raise CustomException(e, sys)
