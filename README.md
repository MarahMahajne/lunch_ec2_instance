# lunch_ec2_instance
# AWS EC2 Instance Creation Lab

This repository contains a script to automate the creation of a Bastion Host and a Web Server on AWS EC2 using Boto3. The script ensures that the latest Amazon Linux 2 AMI is used and sets up necessary security groups and key pairs.

## Prerequisites

- Python 3.x installed
- AWS CLI installed and configured with appropriate permissions
- Boto3 library installed (`pip install boto3`)

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/aws-ec2-instance-creation-lab.git
    cd aws-ec2-instance-creation-lab
    ```

2. Install required Python libraries:

    ```sh
    pip install boto3
    ```

3. Configure your AWS credentials:

    ```sh
    aws configure
    ```

## Script Explanation

The script performs the following tasks:

1. **Initialize Boto3 Session:** 
    - Create a session with AWS credentials and region information.

2. **Key Pair Management:**
    - Check if the specified key pair already exists. If not, create a new one and save the private key to a file.

3. **Fetch Latest Amazon Linux 2 AMI:**
    - Use AWS Systems Manager (SSM) to retrieve the latest Amazon Linux 2 AMI ID.

4. **Security Groups Setup:**
    - Create security groups for the Bastion Host and Web Server, setting up necessary ingress rules.

5. **Launch Instances:**
    - Launch a Bastion Host and a Web Server instance in the specified VPC and subnet.
    - Use user data script to install and start an HTTP server on the Web Server.

6. **Retrieve and Display Public DNS:**
    - Retrieve the public DNS of the Web Server and print it for easy access.

## Usage

1. Update the script with your AWS credentials and desired configurations:

    ```python
    AWS_ACCESS_KEY_ID = 'your-access-key-id'
    AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
    AWS_SESSION_TOKEN = 'your-session-token'
    REGION = 'your-region'
    ```

2. Run the script:

    ```sh
    python create_ec2_instances.py
    ```

3. The script will output the public DNS of the Web Server. You can open this URL in your browser to access the web server:

    ```sh
    http://<web-server-public-dns>
    ```

## Script

Here is the complete script:

```python
import boto3
import webbrowser
import time

# AWS credentials
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_SESSION_TOKEN = 'your-session-token'
REGION = 'us-west-2'  

# Initialize a session using boto3 with provided credentials
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=REGION
)

# Initialize boto3 clients
ec2 = session.client('ec2')
ssm = session.client('ssm')

# Constants
BASTION_NAME = 'BastionHost'
WEB_SERVER_NAME = 'WebServer'
KEY_PAIR_NAME = 'my-key-pair-lab171'  # Name for the new key pair
AMI_NAME = '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
WEB_SECURITY_GROUP_NAME = 'WebSecurityGroup'

# Check if the key pair already exists
key_pair_exists = False
try:
    ec2.describe_key_pairs(KeyNames=[KEY_PAIR_NAME])
    key_pair_exists = True
    print(f'Key pair {KEY_PAIR_NAME} already exists.')
except ec2.exceptions.ClientError as e:
    if 'InvalidKeyPair.NotFound' in str(e):
        print(f'Key pair {KEY_PAIR_NAME} does not exist. Creating a new one.')
    else:
        raise

# Create a new key pair if it does not exist
if not key_pair_exists:
    key_pair = ec2.create_key_pair(KeyName=KEY_PAIR_NAME)
    private_key = key_pair['KeyMaterial']
    print(f'Created key pair with name: {KEY_PAIR_NAME}')

    # Save the private key to a file (Make sure to set correct permissions)
    with open(f'{KEY_PAIR_NAME}.pem', 'w') as file:
        file.write(private_key)
    print(f'Private key saved to {KEY_PAIR_NAME}.pem')

# Get the latest Amazon Linux 2 AMI ID
response = ssm.get_parameter(Name=AMI_NAME)
ami_id = response['Parameter']['Value']
print(f'Latest AMI ID: {ami_id}')

# Get VPC and Subnet
vpcs = ec2.describe_vpcs()
vpc_id = vpcs['Vpcs'][0]['VpcId']
subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
subnet_id = subnets['Subnets'][0]['SubnetId']
print(f'Using VPC: {vpc_id} and Subnet: {subnet_id}')

# Create Security Group for bastion host
bastion_sg = ec2.create_security_group(
    GroupName='BastionSecurityGroup',
    Description='Security group for Bastion host',
    VpcId=vpc_id
)
bastion_sg_id = bastion_sg['GroupId']
ec2.authorize_security_group_ingress(
    GroupId=bastion_sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)
print(f'Bastion security group created: {bastion_sg_id}')

# Launch Bastion Host
bastion_instance = ec2.run_instances(
    ImageId=ami_id,
    InstanceType='t3.micro',
    KeyName=KEY_PAIR_NAME,
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId': subnet_id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [bastion_sg_id]
    }],
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': BASTION_NAME}]
    }]
)
bastion_instance_id = bastion_instance['Instances'][0]['InstanceId']
print(f'Bastion Host launched with Instance ID: {bastion_instance_id}')

# Wait for Bastion Host to be running
ec2.get_waiter('instance_running').wait(InstanceIds=[bastion_instance_id])
print('Bastion Host is running.')

# Create Security Group for web server
web_sg = ec2.create_security_group(
    GroupName=WEB_SECURITY_GROUP_NAME,
    Description='Security group for web server',
    VpcId=vpc_id
)
web_sg_id = web_sg['GroupId']
ec2.authorize_security_group_ingress(
    GroupId=web_sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)
print(f'Web server security group created: {web_sg_id}')

# Create user data script for web server
user_data_script = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Welcome to the Web Server</h1>" > /var/www/html/index.html
"""

# Launch Web Server instance
web_server_instance = ec2.run_instances(
    ImageId=ami_id,
    InstanceType='t3.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId': subnet_id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [web_sg_id]
    }],
    UserData=user_data_script,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': WEB_SERVER_NAME}]
    }]
)
web_server_instance_id = web_server_instance['Instances'][0]['InstanceId']
print(f'Web server launched with Instance ID: {web_server_instance_id}')

# Wait for Web Server to be running
ec2.get_waiter('instance_running').wait(InstanceIds=[web_server_instance_id])
print('Web server is running.')

# Get Public DNS of the Web Server
web_server_instance = ec2.describe_instances(InstanceIds=[web_server_instance_id])
public_dns = web_server_instance['Reservations'][0]['Instances'][0]['PublicDnsName']
print(f'Web server public DNS: {public_dns}')
print(f'Access the web server at http://{public_dns}')  

# Open the web server URL in the default web browser
webbrowser.open(f'http://{public_dns}')

# Optionally, wait
time.sleep(10)
