import os
from typing import Optional, Union
import boto3.resources
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError


def is_allowed_extension(filename) -> bool:

    file_parts_list : list = filename.rsplit('.', 1)

    allowed_extensions : list = current_app.config['ALLOWED_EXTENSIONS']

    return ('.' in filename) and (file_parts_list[1].lower() in allowed_extensions)


def get_secure_filename_filepath(filename) -> tuple:
    filename_secure = secure_filename(filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    return filename_secure, filepath


def upload_to_s3(file, bucket_name, acl='public-read') -> str | None :

    s3_client = boto3.client('s3')

    filename = secure_filename(file.filename)
    key = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                key,
                ExtraArgs={
                    'ACL' : acl,
                    'ContentType' : file.content_type
                }
            )
            return filename
    
    except ClientError as e:
        return None

def download_from_s3(filename):
    if not os.path.exists(current_app.config["DOWNLOAD_FOLDER"]):
        os.makedirs(current_app.config["DOWNLOAD_FOLDER"])

    s3_obj_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(current_app.config["S3_BUCKET"]) #type:ignore
    s3_obj = bucket.Object(s3_obj_path)
    the_response = s3_obj.get()
    return the_response['Body']