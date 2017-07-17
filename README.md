# lambda-hugo-builder
A lambda function that builds a Hugo site and pushes static files to S3. A Dockerfile is supplied to locally package and upload the source code for the lambda function. A Makefile supplies the commands to use to build the Docker image and invoke the local build process.

## Requirements

You will need Docker to build and push your source code. You also need to create a user account with CodeCommit credentials. This is the only way I've found to access CodeCommit from python. I stored those credentials in AWS Parameter Store. The password is encrypted with a KMS key.

**DO NOT COMMIT CREDENTIALS TO REPOSITORIES, PUBLIC OR PRIVATE**

## Deploy code bucket

First, you'll need to deploy the lambda-code bucket. In the deployment/ folder, run `make lambda-bucket` to deploy that CloudFormation stack.

## Local build process

Next, run `make build-packager` in the root folder to build the Docker image.

Once that's done, you need to update the BUILD number in the Makefile. This part should be automated in the future. Run `make package` to invoke the Docker image to pull the components and package it up. Once complete, it'll drop a file in the build/ folder matching your BUILD number. It will also upload that package to the S3 bucket for lambda-code.

## Deploy lambda function

Now that the code package has been uploaded, you can deploy the function. In the deployment/ folder, update the Makefile to reference the build number you built in the last step. Now, run `make hugo-builder` to deploy the stack.

# How it works

Included in the package is boto3, dulwich, the hugo binary, and support files. I included boto3 instead of using the version included with Lambda because the lambda version doesn't support the get_parameter method of the SSM client yet.

Dulwich is a python implementation of git. Dulwich is the low-level api implementation, and Porcelain is the high-level implementation.

Porcelain clones the master branch of the repo to the tmp space of the lambda.

Then, we shell out to the hugo binary to build the site.

After the site it built, we shell out again to run the S3 sync command. I looked at doing this in pure python, but this was significantly easier.

# Future Improvements

1. Unit tests. I need to start writing code with unit tests. I'm just not in the habit of it, yet.
2. Clean up the file system after syncing to S3. Doing this after the sync will ensure the /tmp space is clear of files. It's possible that previous runs can linger.
3. SHA based builds. I need to see if CodeCommit/Porcelain supports pulling a SHA instead of a branch. Right now, it's not a rock-solid deployment model.
