#!/bin/bash
BUCKET_NAME=stock-covid-data-project

AWS_ID=$(aws sts get-caller-identity --query Account --output text | cat)
AWS_REGION=$(aws configure get region)

echo "Creating bucket "
aws s3api create-bucket --acl public-read-write --bucket $BUCKET_NAME --create-bucket-configuration LocationConstraint=$AWS_REGION --output text >> setup.log