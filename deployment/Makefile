hugo-builder:
	aws --profile default --region us-east-1 cloudformation update-stack \
			--stack-name 'Hugo-Builder' \
			--parameters ParameterKey=CodeVersion,ParameterValue=0.0.7 \
				ParameterKey=CodeCommitUsername,ParameterValue=CodeCommit-DeployUsername \
				ParameterKey=CodeCommitPassword,ParameterValue=CodeCommit-DeployPassword \
				--capabilities CAPABILITY_IAM \
				--template-body file://build-job-stack.yml
lambda-bucket:
	aws --profile default --region us-east-1 cloudformation create-stack --stack-name 'Lambda-Bucket' --template-body file://bucket-stack.yml
