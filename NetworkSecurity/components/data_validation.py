from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.entity.config_entity import DataValidationConfig, DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataValidationArtifacts, DataIngestionArtifacts
from NetworkSecurity.constant.training_pipeline_constants import SCHEMA_FILE_PATH
import pandas as pd
import numpy as np
import os,sys
from NetworkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp

# from venv.Lib.asyncio import start_unix_server


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts,
                 data_validation_config: DataValidationConfig,):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config['columns'])
            logging.info(f" required Number of columns : {number_of_columns}")
            logging.info(f" dataframe has  columns : {len(dataframe.columns)}")
            if number_of_columns == len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)
    def detect_data_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status=True
            report={}
            for col in base_df.columns:
                df1=base_df[col]
                df2=current_df[col]
                is_same_dist=ks_2samp(df1,df2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({col: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found

                }})

            drift_report_path_file_path=self.data_validation_config.drift_report_file_path
            #create directory
            dir=os.path.dirname(drift_report_path_file_path)
            os.makedirs(dir, exist_ok=True)
            write_yaml_file(file_path=drift_report_path_file_path,data=report)
            return status
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_validation(self) ->DataValidationArtifacts:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            #validate number of column
            status=self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all columns"

            ## lets check data drift
            status=self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)


            data_validation_artifact = DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path ,
            )
            return data_validation_artifact


        except Exception as e:
            raise CustomException(e,sys)
