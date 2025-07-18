import numpy as np
import os
import sys
import pandas as pd

'''
defining common constatnts variable for trainig pipeline

'''
TARGET_COLUMN='Result'
PIPELINE_NAME='NetworkSecurity'
ARTIFACT_DIR='Artifacts'
FILE_NAME='phisingData.csv'
TRAIN_FILE_NAME='train.csv'
TEST_FILE_NAME='test.csv'

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yml")

'''
Data ingestion related constant start with DATA_INGESTION VAR NAME 
'''

DATA_INGESTION_COLLECTION_NAME:str='NetworkData'
DATA_INGESTION_DATABASE_NAME:str="Sarvjeet1"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
DATA_INGESTION_INGESTED_DIR:str='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"