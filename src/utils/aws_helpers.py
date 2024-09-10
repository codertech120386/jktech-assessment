import os
from io import StringIO

import boto3
import pandas as pd
from icecream import ic
import pickle
from dotenv import load_dotenv

load_dotenv()


def drop_unnamed_cols_in_df(df):
    for i in df.columns:
        if ("unnamed" in i.lower()) or ("level" in i.lower()):
            df.drop(columns=[i], inplace=True)

    return df


def s3_setup():
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
    aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
    aws_region = os.environ.get('AWS_REGION')  # e.g. us-west-2

    # Create a session with your credentials
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=aws_region)

    s3 = session.client('s3')
    bucket_name = os.environ.get("S3_BUCKET")

    return s3, bucket_name


def upload_files_to_s3(file_name: str):
    s3, bucket_name = s3_setup()
    try:
        s3.upload_file(file_name, bucket_name, file_name)
    except Exception as e:
        ic(e)

    print(f"File {file_name} uploaded to S3 bucket {bucket_name}")


def read_files_from_s3(file_name: str):
    s3, bucket_name = s3_setup()
    response = s3.get_object(Bucket=bucket_name, Key=file_name)

    return response['Body'].read().decode('utf-8')


def read_pickle_files_from_s3(file_name: str):
    s3, bucket_name = s3_setup()
    local_file_path = f"src/{file_name}"

    s3.download_file(bucket_name, file_name, local_file_path)

    loaded_model = None
    with open(local_file_path, 'rb') as f:
        loaded_model = pickle.load(f)

    return loaded_model


def convert_file_content_to_df(file_name: str):
    file_content = read_files_from_s3(file_name=file_name)
    df = pd.read_csv(StringIO(file_content))
    return drop_unnamed_cols_in_df(df)
