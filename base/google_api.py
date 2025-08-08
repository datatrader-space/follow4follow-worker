from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import googleapiclient.discovery
from google.oauth2 import service_account
import io
import os
from base.storage_sense import Saver
class GoogleAPI(object):
    def __init__(self):
        self.service_name='drive'
        self.media_folder=os.path.join(os.getcwd(),'data','media','media')
        self.credentials_dict={
  
}
        self.version='v3'
        if not os.path.isdir(self.media_folder):
            os.makedirs(self.media_folder)
    
    def service_account_from_dict(self):
        credentials = service_account.Credentials.from_service_account_info(self.credentials_dict)
        self.service=googleapiclient.discovery.build(self.service_name,self.version,credentials=credentials)    
    def download_file(self,file):
        file_id=file.get('id',None)
        if not file_id:
            file_id=file.get('url').split('/')[5]
        
        _=self.create_file_path_and_know_export_mime_type(file)
        if 'image' in file['mimeType'] or 'mp4' in file['mimeType'] or 'text/plain' in file['mimeType']:
            request=self.service.files().get_media(fileId=file_id)
        else:
            request=self.service.files().export_media(fileId=file_id,mimeType=_['export_mime_type'])
        _file = io.BytesIO()
        downloader=MediaIoBaseDownload(_file,request)
        done=False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')
        with open(_.get('file_path'),'wb') as file:
            file.write(_file.getvalue())
        return _
    def find_file(self,select_first=True,**kwargs):
        file_name=kwargs.get('file_name',None)
        query="name = '"+file_name+"'"
        print(query)
        request=self.service.files().list(q=query).execute()
        
        files=request.get('files',{})
        if len(files)>0:
            if select_first:
                files=[files[0]]       
        else:
            files=[]
        kwargs.update({'files':files})
        return kwargs     
    def find_folder(self,select_first=True,**kwargs,):
        folder_name=kwargs.get('folder_name')
        mimeType = "mimeType = 'application/vnd.google-apps.folder'"
        if kwargs.get('parent_folder'):
            parent_folder_id=kwargs.get('parent_folder').get('id')
            query="'"+parent_folder_id+"' in parents"
            
        else:
            query="name = '"+folder_name+"' and( "+mimeType+" )"

        request=self.service.files().list(q=query,fields="nextPageToken, files(id, name,parents)",).execute()
        
        folders=(request.get('files')) 
        if len(folders)>0:
            if select_first:
                folders=[folders[0]] 
        else:
            folders=[]    
        kwargs.update({'folders':folders})
        return kwargs
    def get_files_in_shared_driver(self,**kwargs):
        r=self.service.files().list(fields="nextPageToken, files(id, name,mimeType,createdTime,modifiedTime,size)",corpora = 'drive',pageToken=None, supportsAllDrives = True, driveId = "0APaHyPJ4PTtXUk9PVA", includeItemsFromAllDrives = True).execute()
        s=Saver()

        s.block={'address':'','file_name':'g_api','data':r}
        s.load_block()
        s.overwrite=True
        s.add_values_to_file()
        return(r.get('files'))
    def get_files_in_folder(self,**kwargs):
        resp=self.find_folder(**kwargs)
        if resp.get('folders'):
            folder_id=resp.get('folders')[0]['id']
        request=self.service.files().list(q='"'+folder_id+'" in parents').execute()
        return request.get('files')
    def create_file_path_and_know_export_mime_type(self,file,export_as='',use_file_name=True):
        if file['mimeType']=='image/jpeg':
            _='.jpeg'
            export_mime_type='image/jpeg'
        if file['mimeType']=='image/png':
            _='.png'
            export_mime_type='image/png'  
        elif 'mp4' in file['mimeType']:
            _='.mp4'
            export_mime_type='mp4'
        if file['mimeType']=='application/vnd.google-apps.spreadsheet':
            if export_as =='.csv':
                export_mime_type='text/csv'
                _='.csv'
            elif export_as=='.xlsx':
                export_mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                _='.xlsx'
            else:
                export_mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                _='.xlsx'
        elif file['mimeType']=='application/vnd.google-apps.document':
        
            if export_as=='txt':
                export_mime_type='text/plain'
                _='.txt'
            elif export_as=='.pdf':
                export_mime_type='application/pdf'
                _='.pdf'
            elif export_as=='.docx':
                export_mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                _='.docx'
        else:
            export_mime_type='text/plain'
            _='.txt'
            
        
        if not use_file_name:
            import uuid
            file_name=str(uuid.uuid1())    
            file_name+=_
        else:
            file_name=file['name']
        
        file_path=os.path.join(self.media_folder,file_name)
        self.download_path=file_path
        return {'file_path':file_path,'export_mime_type':export_mime_type}
    def create_folder(self,name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = self.service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')
    def share_with_user(self,**kwargs):
        msg=kwargs.get('msg')
        email_address=kwargs.get('email_address')
        permission_type=kwargs.get('type')
        role=kwargs.get('role')
        file_id=kwargs.get('file_id')
        
        body={
                'email_address':kwargs.get('email_address'),
                'type':kwargs.get('type'),
                'role':kwargs.get('role'),
                'permission_type':'user'

        }
        resp=self.service.permissions().create(fileId=file_id,
                                               body=body,
                                               emailMessage=msg,
                                            
                                               fields='*').execute()  
    def check_permissions(self,file_id):
        resp=self.service.permissions().list(fileId=file_id,fields='*').execute()
     
        return resp
            

    

        

    

""" g=GoogleAPI()
g.service_account_from_dict()
files=g.get_files_in_shared_driver(**{'folder_name':'Instagram Data for Vision Eye'})
for file in files:
    if file['mimeType']=='application/vnd.google-apps.folder':
        pass
    else:
        g.download_file(file) """
    
    




