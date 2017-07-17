def lambda_handler(event, context):
    import os, shutil
    import subprocess
    from dulwich import porcelain
    import boto3

    # print the event to see the CodeCommit trigger values
    # customData is not documented in the available lambda events, yet
    print event

    # Create a client for SSM to get username/password values.
    client = boto3.client('ssm')
    username = client.get_parameter(
        Name=os.getenv('USERNAME')
    )["Parameter"]["Value"]
    password = client.get_parameter(
        Name=os.getenv('PASSWORD'),
        WithDecryption=True
    )['Parameter']['Value']
    repository = event['Records'][0]['eventSourceARN'].split(':')[5]
    repourl = "https://{}:{}@git-codecommit.{}.amazonaws.com/v1/repos/{}".format(username,password,os.getenv('AWS_DEFAULT_REGION'),repository)
    print "Repo: {}".format(repository)
    clonedir = "/tmp/{}".format(repository)
    builddir = "/tmp/{}/source".format(repository)
    pushdir = "{}/public".format(builddir)

    # see if previous invocations left files behind
    # if so, delete them
    try:
        for the_file in os.listdir(clonedir):
            file_path = os.path.join(clonedir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    except OSError as e:
        print "Folder not found."

    # Clone the repo contents
    porcelain.clone(repourl, clonedir)

    # build the site with the hugo binary
    popen = subprocess.Popen("/var/task/hugo", cwd=builddir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen.wait()
    out, err = popen.communicate()
    result = out.decode()
    print "Error : {}".format(err.decode())

    # use S3 sync to push the files to the bucket
    bucketuri = "s3://{}/".format(event['Records'][0]['customData'])
    popen = subprocess.Popen("python /var/task/aws s3 sync --acl public-read --delete " + pushdir + " " + bucketuri, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen.wait()
    out, err = popen.communicate()
    result = out.decode()
    print "Error : {}".format(err.decode())

    # delete files should be moved here, so there doesn't need to be any checks for past invocaitons
