import os
import json
import time
from services.instagram.parsers import Parser
from base.storage_sense import Saver
from services.instagram.register_assistant import RegisterAssistant

from services.instagram.xpaths import Xpaths
from services.instagram.locator import Locator
class Pages():
    def __init__(self):
     
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.parsers=Parser() 
        self.register_assistant=RegisterAssistant()
        self.locator=Locator()
        
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    def get_current_active_page(self,**kwargs):
        page=self.locator.identify_current_page()
        print(page)
    class Login:
        def __init__(self):
            super().__init__()

        def login(self):
            username_input=self.locator.locate(**{'touch_point':'get_username_input'})
            print(username_input)
        
        
    class hashtag():
        def __init__(self):
            super().__init__()
        def search_hashtags(self,query=None):
                url='https://www.instagram.com/api/v1/web/search/topsearch/'
                0.002777659144470812
                context = {
                    "context":"hashtag",
                        "query": query,
                        "rank_token": 0.547015482035698,
                        "include_reel": True,
                        "search_surface": "web_top_search"
                            }
                resp=self.make_request(url,payload=context)
                print(resp.text)

    class user():
        
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
        def search_user(self,query=None):
            context = {
                "context":"hashtag",
                "query": query,
                "rank_token": 0.547015482035698,
                "include_reel": True,
                "search_surface": "web_top_search"
                        }
    
        def user_info(self,**kwargs):
            if kwargs.get('retrieve',False):
                return 'empty_file',{}
            else:
                username=kwargs.get('username')
                url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
                response=self.make_request(end_point='user_info',data_point='user_info',url=url)
                self.parsers.end_point='user'
                self.parsers.data_point='user_info'
                return self.parsers.parse_end_point(response,**kwargs)          
        def user_followers(self,**kwargs):
            if kwargs.get('retrieve',False):
                return 'empty_file',{}
            else:
               
                username=kwargs.get('username')
                self.storage_sense.block={'address':'users.'+username+'.followers','file_name':'register'}
                self.storage_sense.load_block()
                self.storage_sense.open_file()
                
                if self.storage_sense.empty_file:
                    print('Followers Register Dont Exist. Scraping Now')
                    next_cursor=None
                else:
                    if not kwargs.get('next_cursor'):
                        resp=self.register_assistant.sort_df_and_return_the_latest_row(self.storage_sense.data_frame)
                        if resp.get('has_next_page'):
                            if resp.get('next_cursor'):
                                next_cursor=resp.get('next_cursor')
                            else:
                                next_cursor=None
                        else:
                            print('No New page Available')
                            return {}
                    else:
                        next_cursor=kwargs.get('next_cursor')
                url='https://www.instagram.com/graphql/query/'    
                if kwargs.get('rest_id',None):
                    rest_id=kwargs['rest_id']       
                variables = {'id':rest_id, 'first': 100}     
                if next_cursor:
                    variables.update({'after':next_cursor})            
                query = {
                        'query_hash': '7dd9a7e2160524fd85f50317462cff9f',
                        'variables': json.dumps(variables, separators=(',', ':'))
                    }
                response=self.make_request(end_point='user',data_point='user_followers',url=url,params=query)
                self.parsers.end_point='user'
                self.parsers.data_point='user_followers'
                return self.parsers.parse_end_point(response,**kwargs)    

    
