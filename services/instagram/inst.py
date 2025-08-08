from base.basic_crawler import Crawler
from base.local_csv_saver import Saver
from base.extractors import SeoExtractors
from base.recursion import Recursion
import json
import time
class Instagram(Crawler):
    def __init__(self):
        super().__init__()
        self.target_url='https://www.instagram.com/camarena_artss/'
        self.use_proxies=''
        self.service_name='instagram'
        self.seo_extractors=SeoExtractors()
        self.end_point='user_info'
        self.username=None
        self.rest_id=None
        self.overwrite=False
    def start(self):       
        self.create_scraping_resources(selenium_wire=True,url_to_capture_requests_from=self.target_url,request_identifier='web_profile_info',use_proxies=self.use_proxies)#headers_dict=self.headers_dict)      
        return self
    def user_info(self,**kwargs):
        username=kwargs.get('username')
        url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
        response=self.make_request(end_point='user_info',url=url)
        return self.parsers.parse_end_point('user_info',response,**kwargs)          
    def user_followers(self,**kwargs):
        url='https://www.instagram.com/graphql/query/'    
        """   if kwargs.get('rest_id',None):
            rest_id=kwargs['rest_id']        """ 
        variables = {'id':self.rest_id, 'first': 100}     
        if kwargs.get('next_cursor'):
            cursor=kwargs.get('next_cursor')
            variables.update({'after':cursor})  
        else:
            cursor=None
           
       
        query = {
                'query_hash': '7dd9a7e2160524fd85f50317462cff9f',
                'variables': json.dumps(variables, separators=(',', ':'))
            }
        response=self.make_request('user_followers',url,params=query)
        return self.parsers.parse_end_point('user_followers',response,**kwargs)      
    def crawl(self):
        self.start()
        r=Recursion()
        r.service=self.service_name
        r.crawler=self     
        r.recursive_api_caller(end_point=self.end_point,username=self.username,rest_id=self.rest_id)
    def retrieve_data(self):
        from base.local_csv_saver import Saver
        s=Saver()
        s.block={'service':self.service_name,'username':self.username,'end_point':self.end_point}
        s.retrieve()
        s.open_file()
        if not s.file.empty:
            data=s.file.to_json(orient='records')
            if type(data)==str:
                data=json.loads(data)
          
            if self.end_point=='user_info':
                if len(data)>0:
                    if self.overwrite:
                        return self.crawl()
                    else:
                        return data[0]
                else:
                    return self.crawl()
            elif self.end_point=='user_followers':
                if len(data)>0:
                    return data
                else:
                    return self.crawl()
        else:
            print('Empty File, scraping now')
            return self.crawl()
    def get_followers(self):
        self.end_point='user_info'
        data=self.retrieve_data()
        if data:
            rest_id=data['rest_id']
            self.rest_id=rest_id
        self.end_point='user_followers'
        data=self.retrieve_data()


            

    


i=Instagram()
i.username='juliancamarena'
i.end_point='user_info'
i.user_data_dir=r'E:\darrxscale\smm_panel_worker_backup\ssm_panel_worker\data\browser_profiles\1\chrome\art_camarena'
#i.get_followers()
from base.local_csv_saver import Saver
s=Saver()
s.block={'service':i.service_name,'username':i.username,'end_point':'user_followers'}
s.retrieve()
s.open_file()
followers=s.file.to_json(orient='records')
followers=json.loads(followers)
for follower in followers:
    s.block={'service':i.service_name,'username':follower['username'],'end_point':'user_info'}
    i.username=follower['username']
    i.end_point='user_info'
    #i.overwrite=True
    i.retrieve_data()
