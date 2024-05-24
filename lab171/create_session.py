from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_DEFAULT_REGION
import boto3

class Session :
    def __init__(self):
        # AWS_ACCESS_KEY_ID = 'ASIA5FTZC2IJJVPLMEGI'
        # AWS_SECRET_ACCESS_KEY = 'Ks9E7nFsRRkWbD02eQ0Ve04oGkv/ljR0U4pn4xsy'
        # AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJHMEUCIQCdTm5XoKn4tcyJPBAqvPiNSqRdZKoiFIQ/nt9RSlE84wIgIxO2noGCRSrSgM706En+c8DyywKkeoebv5UanrjHBykqtgIIk///////////ARAAGgw5MDU0MTgyOTc4NzQiDLwv24r2Rd9RY+hfKiqKAvcfNThuyEBoNhjz+rPuheP3b06rXtREMFg0mv4iji1eBqhAvEZj13cTsrN+QWXpZImwIi6FHAHVlJ9T1Y9vS8bhQ0zkFp1UUGNMnJAvd1DH8YGBMdMh1aLgN9kYqDQZAzE9Yfma++fVInhzh0vgwcgCwqlxMUYtZlFEtg34MW9ycDxPq5SUF0t6pzbb2Vde00DlPFVBzA0u5vtrRn+ipJRkEMzUf2g6sFrXdd4TvzUGcl/6rEx3DBEo+ktSzK3MkQOWqmI+m3z12kOeEtKotSdcgzJpKBpOkz9YpD2ILi/eZZkwbdzAbzYsX6hAB2CJMQ7QF/Z3lUS2yXsLHUQFrPA4pa0PNZKBXKJVMNiow7IGOp0Bu11IxA/LaRMi3XmeKp7GsCsNLqUzviuuyF1aSyk/CnTBVVuQ4GxqEPORjG3/CRDIn5+TbF7KBqm9In/bVPboouTZVZXOFo12R7BalPH+MhhTf05P+miDrTVm2GwotYoZu49AThtGrH4bEeDHDxyTf35NtXxehOn5ZO7IdDGU720qNwTKTlaECRqmSTVIaZR1mODPSYJRtPr6W8tKPw=="
        
        #Initialize a session using boto3 with provided credentials
        self.aws_access_key = AWS_ACCESS_KEY_ID
        self.aws_seccret_access_key = AWS_SECRET_ACCESS_KEY 
        self.aws_session_token = AWS_SESSION_TOKEN
        self.create_session()
        
        
    def create_session(self):
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_DEFAULT_REGION
        )