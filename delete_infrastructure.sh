#!/bin/bash
BUCKET_NAME=stock-covid-data-project

AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)
AWS_REGION=$(aws configure get region)

echo "Deleting bucket and its contents"
aws s3 rm s3://$BUCKET_NAME --recursive --output text >> tear_down.log
aws s3api delete-bucket --bucket $BUCKET_NAME --output text >> tear_down.log