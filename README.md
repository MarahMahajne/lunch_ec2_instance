# AWS EC2 Instance Creation Lab - (lab 171 in AWS)

This repository contains a script to automate the creation of a Bastion Host and a Web Server on AWS EC2 using Boto3. The script ensures that the latest Amazon Linux 2 AMI is used and sets up necessary security groups and key pairs.

## Prerequisites

- Python 3.x installed
- AWS CLI installed and configured with appropriate permissions
- Boto3 library installed (`pip install boto3`)

## Setup

1. Clone the repository:

    ```sh
    git clone git@github.com:MarahMahajne/lunch_ec2_instance.git
    cd lunch_ec2_instance
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
