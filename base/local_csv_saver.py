import os
import pandas as pd
import datetime
from base.downloader import Downloader
class Saver(object):
    def __init__(self):
        
        self.scraped_data=[]
        self.user_followers=[]
        self.user_posts=[]
        self.users=[]
        self.post_comments=[]
        self.follow_relations=[]
        self.parent_tweet=[]
        self.feed_tweets=[]
        self.t_lists=[]
        self.service='twitter'
        self.username=''
        self.end_point='user_posts'
        self.post_id='abcd1234'
        self.file_identifier=''
        self.data_blocks=[]
        self.cached_blocks=[]
        self.sectioned_data=None
        self.file_extension='.json'
        self.empty_file=False
        self.overwrite=False
    def create_crawler_directory(self):
        pth=os.path.join(os.getcwd(),'crawler')
        if not os.path.exists(pth):
           os.makedirs(pth)
        self.crawler_directory=pth
        return self
    def create_data_directory(self):
        pth=os.path.join(self.crawler_directory,'data')
        if not os.path.exists(pth):
           os.makedirs(pth)
        self.data_directory=pth
        return self
    def create_service_directory(self):
        service=self.block.get('service',False)
        if not service:
            raise Exception("NoServiceSpecifiedError")
        self.service_directory=os.path.join(self.data_directory,service)
        if not os.path.exists(os.path.join(self.data_directory,self.block.get('service'))):
            os.makedirs(self.service_directory)
            
        
        return self
    def create_user_directory(self):
        username=self.block.get('username')
        if username:           
            pth=os.path.join(self.service_directory,username)
            self.user_directory=pth
            if os.path.exists(pth):
                self.user_directory=pth
            else:
                os.makedirs(pth)
            return self
        raise Exception("NoUserNameSpecifiedError")
    def timestamp(self):
        timestamp = datetime.datetime.now()
        return timestamp
    def create_end_point_directory(self):
        end_point=self.block.get('end_point',None)
        if end_point:
            pth=os.path.join(self.user_directory,end_point)
            self.end_point_directory=pth
            if os.path.exists(pth):
                pass
            else:
                os.makedirs(pth)
        else:
            raise Exception("NoEndPointSpecifiedError")       
        return self   
    def create_identifier_directory(self):
        identifier=self.block.get('identifier')
        if identifier:
            pth=os.path.join(self.end_point_directory,identifier)
            self.identifier_directory=pth
            if os.path.exists(pth):
                pass
            else:
                os.makedirs(pth)
        else:
            pass
            #raise Exception("NoIdentifierSpecifiedError")       
        return self   
    def create_data_point_directory(self):
        data_point=self.block.get('data_point',None)
        if data_point:
            pth=os.path.join(self.identifier_directory,data_point)
            self.data_point_directory=pth
            if os.path.exists(pth):
                pass
            else:
                os.makedirs(pth)
        else:
            raise Exception("NoDataPointSpecifiedError")       
        return self      
    def check_if_file_exists(self):
        if not os.path.exists(os.path.join(self.end_point_directory,self.file_identifier+'.csv')):
            self.file=os.path.join(self.end_point_directory,self.file_identifier+'.csv')
            return False
        return True
    def create_file(self):
        if not self.check_if_file_exists():
           open(self.file, 'w').close()
    def open_file(self):
        end_point=self.block.get('end_point',False)
        identifier=self.block.get('identifier','')
        file_name=self.block.get('file_name','')
        user_directory=self.user_directory
        data_point=self.block.get('data_point')

        if user_directory and end_point:
            if not identifier:

                pth=os.path.join(self.end_point_directory,end_point+self.file_extension)
                if file_name:
                    pth=os.path.join(self.end_point_directory,file_name+self.file_extension)
            else:
                if self.block.get('data_point',''):##check if data_point has value
                    self.create_identifier_directory()#if yes, then create an identifier directory else use identifier as file-name and save in end-point-direcoty
                    if self.block.get('file_name',''):##if yes, check if file_name has been provided
                        self.create_data_point_directory()##if yes, create a data point directory and use the file_name as file Name. else use data_point as file name
                        pth=os.path.join(self.data_point_directory,file_name+self.file_extension)
                    else:
                        pth=os.path.join(self.identifier_directory,data_point+self.file_extension)##if no file name provided, use identifier dir. and data_point as file name

                else:
                    if self.block.get('file_name',''):
                        file_name=self.block.get('file_name','')
                        self.create_identifier_directory()
                        pth=os.path.join(self.identifier_directory,file_name+self.file_extension)
                    else:
                        pth=os.path.join(self.end_point_directory,identifier+self.file_extension)##if no data_point specified, use end_point directory and identifier as file name
                
                
                 
           
            self.file_path=pth     
             
            if os.path.exists(pth):
                if self.file_extension=='.csv':
                    self.file = pd.read_csv(pth)
                elif self.file_extension=='.xlsx':
                    self.file=pd.read_excel(pth,engine='openpyxl')
                elif self.file_extension=='.json':
                    self.file=pd.read_json(pth,)
                elif self.file_extension=='.html':
                    self.file=open(pth,'r',encoding='utf-8')
               
            else:
                self.file = pd.DataFrame()
                self.empty_file=True
    
            return self
       
        else:
            raise Exception("OpenFileErrorNotEnoughData")
    def write_data_block_to_file(self): 
         
        if self.file is None:
            raise ValueError("File is not open.")    
      
        if self.block.get('data'):
            data=self.block['data']
        else:
            data=self.block
        if type(data)==dict:
            data=[data]
        if self.file_extension=='.html':
            pass
        else:
            if self.overwrite:
                self.file=pd.DataFrame(data)
            else:          
                self.file = pd.concat([self.file, pd.DataFrame(data)], ignore_index=True)
        if self.file_extension =='.csv':
            self.file.to_csv(self.file_path)
        elif self.file_extension=='.json':
            self.file.to_json(self.file_path,orient='records')
        elif self.file_extension=='.html':
            if self.file.empty:
                pass
            else:
                self.file.close()
            self.file=open(self.file_path,'w',encoding='utf-8')
            self.file.write(data)
            self.file.close()
        else:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='w') as writer:       
              self.file.to_excel(writer, index=False)
    def create_new_data_blocks(self):
        ##Transforms to a 1d list data_block
        self.data_blocks=[] 
        if type(self.sectioned_data)==dict:
            self.sectioned_data=[self.sectioned_data]
        elif type(self.sectioned_data)==list:
            pass
        else:
            raise Exception("BadSectionedDataType")
        for data_row in self.sectioned_data:           
                self.data_blocks.append(data_row)     
        return self
    def cache_all_new_data_blocks(self):
        for block in self.data_blocks:
            if block.get('exclude_from_cache',True):
                continue
            self.cached_blocks.append(block.pop('data',None))
        return self
    def save_all_blocks(self):
        for block in self.data_blocks:
            self.create_end_point_directory()
    def retrieve_user(self):
        self.create_crawler_directory().create_data_directory().create_service_directory().create_user_directory().create_end_point_directory()
    def retrieve_posts(self):
        self.create_crawler_directory().create_data_directory().create_service_directory().create_user_directory().create_end_point_directory()
        list_of_name_posts=os.listdir(self.end_point_directory)
        contents=os.listdir(self.end_point_directory)
        for content in contents:
            if os.path.isdir(os.path.join(self.end_point_directory,content)):
                print(content)
        print(list_of_name_posts)
    def retrieve(self):
        self.create_crawler_directory().create_data_directory().create_service_directory().create_user_directory().create_end_point_directory().create_identifier_directory()
        return self
    def save(self):
        self.create_new_data_blocks()
        for block in self.data_blocks:
            self.block=block
            self.create_crawler_directory().create_data_directory().create_service_directory().create_user_directory().create_end_point_directory().open_file().write_data_block_to_file()
    def process_data_block(self):
        d=Downloader()
        d.download_media()
    def delete_file(self):
        if os.path.exists(self.file_path):
            try:
                self.file.close()
            except Exception:
                os.remove(self.file_path)

""" block={'service':'twitter','end_point':'user_posts','username':'juliancamarena'}
s=Saver()
s.block=block
#s.retrieve_user()
s.retrieve_posts()
print(s.end_point_directory) """


"""     
    
s=Saver()
data = {
    "John Smith": 42,
    "Jane Doe": 17,
    "Michael Johnson": 8,
    "Emily Brown": 23,
    "David Lee": 10,
    "Sarah Wilson": 55,
    "Daniel Martinez": 99,
    "Olivia Taylor": 32,
    "Ethan Anderson": 7,
    "Ava Garcia": 71
}

listo=[]
for i in range(0,100000):
    listo.append(data)
test_dict=[{'service':'twitter','end_point':'user_followers','username':'hamza','data':listo}]
s.sectioned_data=test_dict


# Call the save method

# Calculate the elapsed time
for mode in ['.csv','.json','.xlsx']:
    s.file_extension=mode
    time_start=datetime.datetime.now()
    s.save()
    time_end = datetime.datetime.now()
    elapsed_time = time_end - time_start
    # Print the elapsed time
    print(f"Time taken with {mode}: {elapsed_time}")
 """
