#!/usr/bin/env python3
"""
Utility script to upload files to the assets folder and S3 bucket.
"""

import os
import boto3
import argparse
from pathlib import Path

def upload_to_s3(bucket_name, local_folder="assets", s3_prefix="assets/"):
    """
    Upload files from local assets folder to S3 bucket.
    """
    s3_client = boto3.client('s3')
    
    # Get bucket name from CDK outputs or use provided name
    if not bucket_name:
        print("Please provide bucket name from CDK outputs")
        return
    
    local_path = Path(local_folder)
    if not local_path.exists():
        print(f"Local folder {local_folder} does not exist")
        return
    
    # Upload all files in assets folder
    for file_path in local_path.rglob("*"):
        if file_path.is_file():
            # Calculate S3 key
            relative_path = file_path.relative_to(local_path)
            s3_key = f"{s3_prefix}{relative_path}"
            
            try:
                s3_client.upload_file(str(file_path), bucket_name, s3_key)
                print(f"Uploaded: {file_path} -> s3://{bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")

def list_assets():
    """
    List all files in the assets folder.
    """
    assets_path = Path("assets")
    if not assets_path.exists():
        print("Assets folder does not exist")
        return
    
    print("Files in assets folder:")
    for file_path in assets_path.rglob("*"):
        if file_path.is_file():
            print(f"  - {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload assets to S3 bucket")
    parser.add_argument("--bucket", help="S3 bucket name")
    parser.add_argument("--list", action="store_true", help="List files in assets folder")
    
    args = parser.parse_args()
    
    if args.list:
        list_assets()
    elif args.bucket:
        upload_to_s3(args.bucket)
    else:
        print("Please provide --bucket name or use --list to see assets")
        print("Example: python upload_assets.py --bucket my-knowledge-base-bucket") 