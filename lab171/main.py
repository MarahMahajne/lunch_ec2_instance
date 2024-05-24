# import boto3
# import requests
# import urllib.request
# import time
# import webbrowser





# ec2_client = session.client('ec2')

# clieant_reservations = ec2_client.describe_instances()['Reservations']

# ec2_instances =[instance for instance in clieant_reservations]

# num_of_ec2_instances = len(ec2_instances) - 1



# ssm_client = session.client('ssm')
# ec2_client = session.client('ec2')

# # Step 1: Retrieve the latest Amazon Linux 2 AMI
# ami_response = ssm_client.get_parameter(
#     Name='/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
# )
# AMI_ID = ami_response['Parameter']['Value']
# print(f"AMI ID: {AMI_ID}")

# # Step 2: Retrieve the subnet ID for the public subnet
# subnet_response = ec2_client.describe_subnets(
#     Filters=[{'Name': 'tag:Name', 'Values': ['Public Subnet']}]
# )
# SUBNET_ID = subnet_response['Subnets'][0]['SubnetId']
# print(f"Subnet ID: {SUBNET_ID}")

# # Step 3: Retrieve the security group ID for the web security group
# sg_response = ec2_client.describe_security_groups(
#     Filters=[{'Name': 'group-name', 'Values': ['WebSecurityGroup']}]
# )
# SG_ID = sg_response['SecurityGroups'][0]['GroupId']
# print(f"Security Group ID: {SG_ID}")

# # Step 4: Download the user data script
# user_data_url = 'https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-100-RSJAWS-1-23732/171-lab-JAWS-create-ec2/s3/UserData.txt'
# user_data_file = '/tmp/UserData.txt'
# urllib.request.urlretrieve(user_data_url, user_data_file)

# with open(user_data_file, 'r') as file:
#     user_data_script = file.read()

# # Step 5: Launch the EC2 instance
# instance_response = ec2_client.run_instances(
#     ImageId=AMI_ID,
#     SubnetId=SUBNET_ID,
#     SecurityGroupIds=[SG_ID],
#     UserData=user_data_script,
#     InstanceType='t3.micro',
#     TagSpecifications=[{
#         'ResourceType': 'instance',
#         'Tags': [{'Key': 'Name', 'Value': 'Web Server'}]
#     }],
#     MinCount=1,
#     MaxCount=1
# )
# INSTANCE_ID = instance_response['Instances'][0]['InstanceId']
# print(f"Instance ID: {INSTANCE_ID}")

# # Step 6: Wait for the instance to be ready
# while True:
#     instance_status = ec2_client.describe_instance_status(InstanceIds=[INSTANCE_ID])
#     statuses = instance_status['InstanceStatuses']
#     if statuses and statuses[0]['InstanceState']['Name'] == 'running':
#         print("Instance is running.")
#         break
#     else:
#         print("Waiting for instance to be ready...")
#         time.sleep(10)

# # Step 7: Test the web server
# instance_description = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
# public_dns_name = instance_description['Reservations'][0]['Instances'][0]['PublicDnsName']
# print(f"Public DNS: {public_dns_name}")

# # Verify by accessing the web server
# webbrowser.open(f"http://{public_dns_name}")

from app import App

if __name__ == "__main__":
    app = App()
    
    host_user_data = app.read_file_content("host_user_data.txt")
    predefined_user_data =  app.get_predefined_userdata()
    
    host_instance_response = app.create_ec2_instance(
        "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2",
        "t3.micro",
        host_user_data,
        [{'Key': 'Name', 'Value': 'Host'}]
    )
    
    web_server_instance_response = app.create_ec2_instance(
        "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2",
        "t3.micro",
        predefined_user_data,
        [{'Key': 'Name', 'Value': 'Web Server1'}]
    )
    
    instance_id = app.get_instance_id(web_server_instance_response)
    
    app.start_test(instance_id)