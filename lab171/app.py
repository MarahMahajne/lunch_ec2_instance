from create_session import Session

class App(Session):
    
    def __init__(self):
        super().__init__()
        self.ssm_client = self.session.client('ssm')
        self.ec2_client = self.session.client('ec2')

        
    def create_ec2_instance(self, ami_name, instance_type, tags, user_data):

        ami_response = self.ssm_client.get_parameter(Name=ami_name)

        ami_id = ami_response['Parameter']['Value']
        
        subnet_response = self.ec2_client.describe_subnets(
            Filters=[{'Name': 'tag:Name', 'Values': ['Public Subnet']}]
        )
        
        subnet_id = subnet_response['Subnets'][0]['SubnetId']
        
        sg_response =self. ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': ['WebSecurityGroup']}]
        )
        
        
        sg_id = sg_response['SecurityGroups'][0]['GroupId']
                
        instance_response = self.ec2_client.run_instances(
            ImageId=ami_id,
            SubnetId=subnet_id,
            SecurityGroupIds=[sg_id],
            UserData=user_data,
            InstanceType=instance_type,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': tags
            }],
            MinCount=1,
            MaxCount=1
        )
        self.is_instance_ready(self.get_instance_id(instance_response))
        
        return instance_response
    
    def get_instance_id(self, instance_response):
        return instance_response['Instances'][0]['InstanceId']
        
    
    def is_instance_ready(self, instance_id):
        from time import sleep
        try:            
            while True:
                instance_status = self.ec2_client.describe_instance_status(InstanceIds=[instance_id])
                statuses = instance_status['InstanceStatuses']
                if statuses and statuses[0]['InstanceState']['Name'] == 'running':
                    print("Instance is running.")
                    break
                else:
                    print("Waiting for instance to be ready...")
                    sleep(10)
        except:
            print("[-] Something went wrong...")
            return False
        return True
        
    def get_predefined_userdata(self):
        from os.path import exists
        from urllib.request import urlretrieve
        user_data_url = 'https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-100-RSJAWS-1-23732/171-lab-JAWS-create-ec2/s3/UserData.txt'
        user_data_file = 'UserData.txt'
        if not exists(user_data_file):
            urlretrieve(user_data_url, user_data_file)
        
        user_data_script = self.read_file_content(user_data_file)
            
        return user_data_script
    
    def read_file_content(self, file_name):
        with open(file_name, 'r') as file:
            user_data_script = file.read()
        return user_data_script
    
    def start_test(self, id):
        import webbrowser
        instance_description = self.ec2_client.describe_instances(InstanceIds=[id])
        public_dns_name = instance_description['Reservations'][0]['Instances'][0]['PublicDnsName']
        print(f"Public DNS: {public_dns_name}")

        # Verify by accessing the web server
        webbrowser.open(f"http://{public_dns_name}")