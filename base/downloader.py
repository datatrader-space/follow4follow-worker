import os
import uuid
from io import BytesIO
import base64
from services.reports_manager.manager import Manager as ReportsManager
class Downloader(object):
    def __init__(self):
        pth=os.path.join(os.getcwd(),'data','media','downloads')
        self.file_path=pth
        self.reporter=ReportsManager()
        self.storage_house_url=False
        self.task_id=''
        self.request_maker=''
    def download_media(self,media_type,link,file_name=None,save_to_local_storage=False,save_to_storage_house=False,bucket_name='',task=False):
        
       
        out={}
        out.update({'media_type':media_type})
        try:
            import requests
       
            content = requests.get(link, stream = True)
            self.reporter.report_performance(**{'service':'downloader',
                            'type':'downloaded_file'
                            })
            file_obj=BytesIO()
            for chunk in content.iter_content(chunk_size = 1024*1024):
                if chunk:
                    file_obj.write(chunk)
        
            if save_to_local_storage:
                file_path=self.save_to_local_storage(media_type=media_type,file_obj=file_obj,file_name=False)
                out.update({'local_storage_file_path':file_path})
                if not file_path:
                    out.update({'local_storage_file_path':file_path})
                    self.reporter.report_performance(**{'service':'downloader',
                            'type':'failed_to_save_file_to_local_storage'
                            })
                else:
                    self.reporter.report_performance(**{'service':'downloader',
                                'type':'saved_file_to_local_storage'
                                })
            if save_to_storage_house:
                if self.storage_house_url:
                    file_obj.seek(0)
                    file_content = file_obj.read()
                    base64_encoded = base64.b64encode(file_content).decode('utf-8')
                    try:
                        file_path=self.save_to_storage_house(base64_text=base64_encoded,media_type=media_type,bucket_name=bucket_name)
                        if not file_path:
                            out.update({'storage_house_file_path':file_path})
                            self.reporter.report_performance(**{'service':'downloader',
                                    'type':'failed_to_save_file_to_storage_house'
                                    })
                        else:
                            out.update({'storage_house_file_path':file_path})
                            self.reporter.report_performance(**{'service':'downloader',
                                    'type':'saved_file_to_storage_house'
                                    })
                    except Exception as e:
                        self.reporter.report_performance(**{'service':'downloader',
                                'type':'error','string':{'name':'FailedtoUploadtoStorageHouse','args':str(e)},
                                                    'traceback':traceback.format_exc(),
                                'url':link
                                })
                        return out
                    else:
                        return out
                else:
                    self.reporter.report_performance(**{'service':'downloader',
                                    'type':'failed_to_save_file_to_storage_house_'
                                    })
                
            #print ("downloaded file")
        except Exception as e:
            import traceback
            self.reporter.report_performance(**{'service':'downloader',
                            'type':'failed_to_download_file','traceback':traceback.format_exc(),
                            'url':link
                            })
            self.reporter.report_performance(**{'service':'downloader',
                            'type':'error','traceback':traceback.format_exc()
                            })
            return out
        else:
           
            return out
            
    def save_to_local_storage(self,file_obj,media_type,file_name):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        file_name=file_name if file_name else str(uuid.uuid1())
        if media_type=='image':
            file_name+='.jpg'
            file_path=os.path.join(self.file_path,file_name)
            
        elif media_type=='video':
            file_name+='.mp4'
            file_path=os.path.join(self.file_path,file_name)
        file_obj.seek(0)
        file_content = file_obj.read()
        
        with open(file_path, 'wb') as f:
               
                f.write(file_content)
        return file_path
                        
        
    def save_to_storage_house(self,media_type,bucket_name,base64_text):

        from django.conf import settings
        from base.request_maker import Request
        url=self.storage_house_url+'storagehouse/api/upload/'
        r=Request()
        r.initialize_request_session()
        r.task_id=self.reporter.task_id
        r.run_id=self.reporter.run_id
        resp=r.make_request(end_point='downloader',data_point='usave_to_storage_house',url=url,r_type='post',_json={'file_data':base64_text,'bucket_name':bucket_name,'media_type':media_type})
        if resp and resp['status']=='success':
            data=resp['data']
            return data['file_path']
        
        
            
        return False


d=Downloader()
""" resp=d.download_media(media_type='image',link='http://localhost:83/media/profile_picture/2c6ffa82-3e42-4c94-8ddb-32f9a4512f36.jpg',
                 save_to_local_storage=False,save_to_storage_house=True,bucket_name='test'
                 
                 )
print(resp) """