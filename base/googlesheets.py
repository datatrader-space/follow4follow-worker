import gspread
import pandas as pd
from base.google_api import GoogleAPI
class GoogleSheet(GoogleAPI):
    def __init__(self):
        self.connection=''
        self.spreadsheet=None
        self.spreadsheet_url=None
        self.worksheet=''
        self.worksheet_title='Profiles'
        self.spreadsheet_title='followers-of-hamza'
        self.active_file=None
        self.folder_name=''
        self.share_with_email_addresses=[]

         
       
    def initialize_connection(self):
        credentials={
  "type": "service_account",
  "project_id": "aadml-451013",
  "private_key_id": "cde42ec67709f1ba7205b244a987c9a423d1570d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCm95c7TiMGaXKs\nyRCjsBINId5uJuy+uwFt2+LeMOrRY9wbB3zGeWG+mLV+nSQ3gt84YzJegAFd/Vjz\n831civ297DL3fia95PVY+NgMt2fSnKFEvUuNqbfWCEjI2nV5V48j+sNqz6g8mx3c\n48p2Vq2r6jbsK+V+xlEgDkIFv7xJBN+nuYl/ofhs9qT9WNiTHzpzlR3EeleyeDI9\ny2LW0bOx1rdPuE0gle3sOsXBok9gtcu0jwpddPqHef3XyJl1cGt2OieKD9nKVq89\n33GFAMTAZZfY9+fk0NjuguJL2Zyl64WJpDv7y5kl3LYExuORzgk+rIUXo63BimCK\nnUcO0QRFAgMBAAECggEAJfnwH6jSzhlLYDH+UyDPxkVjFG5NkEc0GML36744Fqau\nMEaocnM20HVm6JTA4VBmyapEUVqvlOt0IU6LP7KMareP0xuSH8R1Koa1C1Vm67A8\n/QfKKL9GxUuOlIKd0Brif5ZAfuma9Cf655w3F2n5J/5GfjqwwQBGAPLFQQ3+eyPe\nrraPmMq1j16TDEFf0XyA/RFmtwqah/4sJvCSMWlQsRPFUvWH7+SIalMIvVsDM7sj\nvQx7+HdqtBCcy4u8/7LHHgptrGA6LHIZywlYrDfy1UYHwmqYddYuLVLX1V7KLQO/\nsuwgSBNzf/zjbNmmDBTNYJyPj8nBG9SAwk3lG5uckQKBgQDbIgOfYFscHVHJPIBJ\nOPZDsnSNaPPQRABijtFnQb+hl7SkTUNcgYgS0/tVQOQhPGJibRrcvj0oAIJYFTsf\nh5ZiTz9FWu6p0HdyiBFdvjrfKsrNe1pp+ZM2x3MuKCMuZYlSD3ahXiqNO5aDW2oB\nsvkDefxEqa1+yywNAFI7YskUUQKBgQDDDtCpejq3gYCJbI6oseAAJJ9VT1tGadK/\n2ffAjAYni7FLVQPE8eBTmTvp1J7llPOM/3B8R5xxI1b//mdKA8UCZKNg2IKM3x+C\n1EuHnkiCLoY6dQAGig4Qwv4LzPBYTEK+RBrAgtEEOxahtpKZnY5qp3jms8byuAQt\nrvT+EfR3tQKBgBf7DPJwFQhqnPysxk09EpYt/VtMVQJBrtkaUAhAxbvlYjtoySpi\ncoW89RBLXavVc97Zmcr2drLd+2WwTRwSNn7jtUTdwqiKy8eY5G2h18d8Y11BVo+q\nZFXmVdCDS/ZT3kdAsfbO21FBaCNP6bXt5BphSx4og3gQu+1gT594HBFBAoGAbs0/\nosYYDJ230likQRep0ur6x48onjsGyIycu/fOlzA3Kj/EwF9VuqdU7WMmT+vo3bNM\nxow3Rd15UjnFmrnBc7aPSDg1EKi+UacesI8tSSX8gcBsn0pU6xiZD0L/VGkdkM9H\nEww8h1a5aGs5o6FogRVZDFQbM01ssjasXJb+c/ECgYEAxZQZxDYj4RSM7Ts23en9\nKJCTLjPep2OhikBZmmiSLjxlDTIloJsMOnc6bdZSWjOdPEaaXcip3lsbNM4ctIZR\nt/nC1OPTp/ZLcC9wqL0CLECRIzfMfBIwmdjaMSqB8UsOBmlsWpjg4sUZwmOwKDE1\n2J/d4RZOT9Qj0tjTYLpZL30=\n-----END PRIVATE KEY-----\n",
  "client_email": "developementlevelbot@aadml-451013.iam.gserviceaccount.com",
  "client_id": "106288661307645661005",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/developementlevelbot%40aadml-451013.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
        try:     
            self.connection= gspread.service_account_from_dict(credentials)
        except Exception('FailedtoCreateGoogleSheetConnection') as e:
           print(e)
           pass
        return self
        
    def initialize_google_drive_api(self):
        g=GoogleAPI()
        g.service_account_from_dict()
        self.google_drive_api=g
        return self
    def open_google_sheet(self):
        
        if self.spreadsheet_url:
            import re
            self.spreadsheet_url = re.sub(r'\\\\', r'\\',self.spreadsheet_url)
            try:
                self.spreadsheet=self.connection.open_by_url(self.spreadsheet_url)
            except Exception as e:
                if 'internal error' in str(e):
                    return self.open_google_sheet()
            #print('Opening Google Sheet using URL')
        elif self.active_file:
            if type(self.active_file)==dict:
                #print('Opening Google Sheet using Active File Dict')
                self.spreadsheet=self.connection.open_by_key(self.active_file['id'])
            else:
                #print('Opening Google Sheet using Spreadsheet Object')
                self.spreadsheet=self.connection.open_by_key(self.active_file.id)
        return self
    def create_google_sheet(self):
        self.active_file=self.connection.create(self.spreadsheet_title,self.active_folder['id'])
        
        print('Created New Google Sheet File')

    def open_worksheet(self):
        sheets=self.spreadsheet.worksheets()  #get all worksheets in the spreadsheet and check if any worksheet exists with user-passed title
        worksheet=None
        self.worksheet=sheets[0]
        return self
    def create_worksheet(self):
        self.worksheet=self.spreadsheet.add_worksheet(self.worksheet_title,rows=len(self.data),cols=30)
        print('Not Found. Created Worksheet')
    def write_to_worksheet(self):
        pass
    def update_worksheet(self,update=False,drop_duplicates=True):
        import pandas as pd
        if type(self.data)==list or type(self.data)==dict:
            import pandas as pd
            df=pd.DataFrame.from_dict(self.data).fillna(0)
        else:
            df=self.data
        df.fillna(' ')
        df1=pd.DataFrame(self.worksheet_data)
        df1.fillna(' ')
        if update:
            if not df1.empty:
            
                df=pd.merge(df1,df,how='outer')
        
        if drop_duplicates:
            df.drop_duplicates(keep='last',inplace=True)
        print(df.values.tolist())
        self.worksheet.update([df.columns.values.tolist()]+ df.values.tolist())
        return self
    def find_worksheet(self,worksheet_title):
        if not self.spreadsheet:
            raise Exception('NoGoogleSheetOpenedException')
        self.worksheet_title=worksheet_title
        #print('Finding Worksheet')
        worksheets=self.spreadsheet.worksheets()
        _=None
        for worksheet in worksheets:
            if worksheet.title.lower()==self.worksheet_title.lower():
                _=worksheet
                #print('Worksheet Found & Turned to Active')
                break
        if _:
            self.worksheet=_
        else:
            self.create_worksheet()
        for worksheet in worksheets:
            if worksheet.title=='Sheet1':
                print('Removed Sheet1')
                self.spreadsheet.del_worksheet(worksheet)
        return self
    def read_worksheet(self):
        print('Reading Active Worksheet')
        try:
            data=self.worksheet.get_all_records()
        except Exception as e:
            print('Empty Sheet')
            self.worksheet_data=[]
        else:
            self.worksheet_data=data
        
        return self
    def check_if_file_exists(self):
        
        resp=self.google_drive_api.find_file(**{'file_name':'branding-sheet'})
        for file in resp['files']:
            if file['mimeType']=='application/vnd.google-apps.spreadsheet':
                self.active_file=file
                return self
        
        return self
    def check_if_folder_exists(self):
        print('Checking if Folder Exists')
        resp=self.google_drive_api.find_folder(**{'folder_name':self.folder_name},select_first=False)
        for folder in resp['folders']:
            self.active_folder=folder
            print('Folder Exists. Turend to Active')
            return self
        print('Folder Not Found.Creating')
        self.active_folder={'id':self.google_drive_api.create_folder(self.folder_name)}
        return self
    def check_if_file_exists_in_active_folder(self):
        print('Checking if file exists in Active Folder')
        files=self.google_drive_api.get_files_in_folder(**{'folder_name':self.folder_name})
      
        if len(files)<1:
            print('Empty Folder.Creating Google Sheet File')
            self.create_google_sheet()
            return self
        else:
            for file in files:
                if file['name']==self.spreadsheet_title and file['mimeType']=='application/vnd.google-apps.spreadsheet':
                    self.active_file=file
                    print('File Exists in Folder. Exiting')
                    return self
        self.create_google_sheet()
        
        return self

    def check_if_file_has_been_shared_with_user(self):
        pass
    def check_if_folder_has_been_shared_with_user(self):
        print('Checking if Folder has been shared with provided email addresses.')
        resp=self.google_drive_api.check_permissions(self.active_folder['id'])
        _emails=self.share_with_email_addresses[:]
        for perm in resp['permissions']:
            for email_address in self.share_with_email_addresses:
                if perm['emailAddress'] in email_address:
                    print('Already Shared with User')
                    _emails.remove(email_address)
                
        
        for email in _emails:
            print('Sharing with '+str(email))
            self.google_drive_api.share_with_user(**{'email_address':email,'role':'writer','type':'user','id':self.active_folder['id']})
           
        return self


        

""" g=GoogleSheet()
g.initialize_google_drive_api()
resp=g.google_drive_api.get_files_in_folder(**{'folder_name':'data-test21'})


g.share_with_email_addresses=['metazon.inc@gmail.com']
g.folder_name='data-test21'
g.initialize_connection().check_if_folder_exists().check_if_folder_has_been_shared_with_user()

g.initialize_connection().check_if_file_exists_in_active_folder().open_google_sheet()
g.worksheet_title='posts'
g.find_worksheet()

g.update_worksheet()
g.worksheet_title='profiles'
g.find_worksheet()
     """



