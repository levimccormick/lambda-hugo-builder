#!/bin/bash
set -e

# install requirements for bundling into lambda package folder
pip install -r /code/requirements.txt -t /tmp/build
cp /code/* /tmp/build/

# Create virtualenv to isolate the executables
virtualenv /tmp/virtualenv
source /tmp/virtualenv/bin/activate
# Move the aws cli wrapper to lambda package folder
pip install -r /code/requirements.txt
cp $(which aws) /tmp/build/
deactivate

# Pull hugo based on version string from env var
wget https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz
tar -xf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz
mv hugo /tmp/build/

# Remove unnecessary files to reduce package size
rm -R /tmp/build/docs/ /tmp/build/dulwich/tests/

# create zip package
cd /tmp/build
zip -FSr9 /build/lambda-hugo-${BUILD}.zip *

# discover the lambda-code bucket name
BUCKET=`aws --profile ${PROFILE} --region us-east-1 cloudformation describe-stacks --stack-name Lambda-Bucket --output text --query "Stacks[*].Outputs[0].OutputValue"`
# Push static files to hosting bucket
aws --profile ${PROFILE} --region us-east-1 s3 cp /build/lambda-hugo-${BUILD}.zip s3://${BUCKET}/
