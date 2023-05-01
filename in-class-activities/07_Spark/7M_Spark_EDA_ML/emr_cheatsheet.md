# PySpark on EMR Cheatsheet

## Launching a (Spark-enabled) EMR Cluster

Create an EMR cluster with Spark installed on it, using the following AWS CLI command from your terminal. Note that you should fill in the `s3.persistence.bucket` field in the `--configurations` with an S3 bucket that you have access to in your account (replacing "YOUR_S3_BUCKET_NAME" with your bucket name). This configuration will automatically save any Jupyter Notebooks you create in your S3 bucket, meaning they will persist even after you terminate your EMR cluster.

```bash
aws emr create-cluster \
    --name "Spark Cluster" \
    --release-label "emr-6.10.0" \
    --applications Name=Hadoop Name=Hive Name=JupyterEnterpriseGateway Name=JupyterHub Name=Livy Name=Pig Name=Spark Name=Tez \
    --instance-type m5.xlarge \
    --instance-count 3 \
    --use-default-roles \
    --region us-east-1 \
    --ec2-attributes '{"KeyName": "vockey"}' \
    --configurations '[{"Classification": "jupyter-s3-conf", "Properties": {"s3.persistence.enabled": "true", "s3.persistence.bucket": "YOUR_S3_BUCKET_NAME"}}]'
```

While your cluster is launching (it will take around 10 minutes) you'll want to make sure that you can `ssh` into the primary node of your cluster. To do so, go into the console and find your cluster in the "Clusters" tab in the "EMR on EC2" section of the EMR menu. Click on your Cluster ID and scroll down to the "EC2 security groups" dropdown menu in the properties tab for the cluster. Click on the security group for the Primary Node ("sg-" followed by a string of numbers and letters) and click "Edit inbound rules" to add a rule allowing `ssh` access from source "0.0.0.0/0" (i.e. over the internet). 

Once you have completed these steps one time you will not need to complete them again when you want to start a Spark-enabled EMR cluster again. You will simply be able to "clone" your existing cluster in the AWS console to restart it again using the same settings.

## Running PySpark code via the terminal

You can directly `ssh` into your primary node and run PySpark jobs via the `pyspark` interpreter in the same way you logged into regular EC2 instances earlier in the class (replacing the `ec2-...` domain name with the primary node public DNS listed in the EMR console and ensuring your `labsuser.pem` file is in the same location):

```bash
ssh -i ~/labsuser.pem hadoop@ec2-23-22-235-142.compute-1.amazonaws.com
```

An additional way to run jobs while `ssh`-ed into your EMR cluster is submit batch jobs via `spark-submit`. For instance, to run `emr_pyspark_script.py` (a script included in this repository that can be uploaded to S3 as in the command below) on your cluster, you can issue the following command on your EMR cluster:

```bash
spark-submit s3://YOUR_S3_BUCKET_NAME/emr_pyspark_script.py YOUR_S3_BUCKET_NAME
```

Note that the script will write its output to an S3 bucket ("YOUR_S3_BUCKET_NAME") and print out logging information related to the job in your terminal window.

## Running interactive jobs via JupyterHub

You can also write PySpark code in a Jupyter Notebook by using `ssh` to forward the port that the JupyterHub server is running on your EMR cluster (9443) to the same port on your local machine. For instance, you could run the following command on your local terminal (again filling in the correct domain name for your primary node and ensuring your `labsuser.pem` file is in the same location):

```bash
ssh -i ~/labsuser.pem -NL 9443:localhost:9443 hadoop@ec2-23-22-235-142.compute-1.amazonaws.com
```

Just be sure not to close the terminal window that you run this command on as it will stop port 9443 from being forwarded to your local machine (and you will not be able to access JupyterHub without running the command again). 
After running the above command, navigate to `https://localhost:9443` in your browser (and navigate through all of the security warnings). You should now see a JupyterHub login window. The username is "jovyan" and the password is "jupyter" -- the defaults for JupyterHub. You should now be able to write PySpark code in Jupyter Notebooks if you select the PySpark kernel for execution.