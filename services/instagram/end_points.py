import os
import json
import time
from services.instagram.parsers import Parser
from base.storage_sense import Saver
from services.instagram.register_assistant import RegisterAssistant
from base.browser import Browser
from services.reports_manager.manager import Manager as reports_manager
import uuid
import random

class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.parsers=Parser() 
        self.register_assistant=RegisterAssistant()
        self.storage_sense=Saver()
        self.browser=Browser()
        
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
       
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
    
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
 
    class location:
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
        def retrieve_data(self,**kwargs):
            if kwargs.get('location_id'):
                
                self.storage_sense.block={'address':'location','file_name':'register'}
                self.storage_sense.load_block()
                self.storage_sense.open_file()
                if self.storage_sense.empty_file:
                    return False, [{'end_point':'location','data_point':'location_info','location_id':kwargs.get('location_id')},kwargs]
                            
                           
                else:
                    filters=[{"field_name": "location_id", "filter_type": "equal", "value": kwargs.get('location_id')}]
                    self.storage_sense.build_query()
                    print(self.storage_sense.df)
            elif kwargs.get('country') and kwargs.get('data_point')=='location_posts':
           
                country=kwargs.get('country')
                self.storage_sense.block={'address':'location.countries.'+country+'','file_name':'register'}
                self.storage_sense.file_extensions='.json'
                self.storage_sense.load_block()
                self.storage_sense.open_file()
                #check if country exists
                #check if city exists
                #check if places exists
                #now fucking get the data
                #check if new cursors
                print('Checking If country is present in Directory')
                if self.storage_sense.empty_file:
                    print('Country Not Found.')
                    print('Checking If country directory has register ')
                    #for bigger and complexer queries we would also pass the function 
                    self.storage_sense.block={'address':'location.countries','file_name':'register'}
                    self.storage_sense.load_block()
                    self.storage_sense.open_file()
                    args={'end_point':'location','data_point':'country_directory','stop_condition':{'data_point':{'countries':[{'slug':'someval'}]},'value':country,'filter':'contains'}}
                    if self.storage_sense.empty_file:
                        print('Country Directory Register Not Found. Starting from Page 1')
                        pass
                    else:
                        print('County Directory Register Found. Using the last cursors for further scraping')
                        data=self.storage_sense.sort_data_by_specific_columns(['last_scraped_at'])
                        args.update(data[0]['next_page_info'])
                    print(args)
                    return False, [args, 'retrieve_data']
               
                else:
                    print('Country Register Found. Now checking city register')

                    ##Acquire required kwargs from the register
                    self.register_assistant.register=self.storage_sense.data_frame
                    _=self.register_assistant.cities_register(method='get',operation='crawl')
                    args={'end_point':'location','data_point':'city_directory','stop_condition':{'data_point':{'next_page_info':{'next_cursor':2}},'value':2,'filter':'equals'}}

                    if _.get('has_next_page') and _.get('total_pages_crawled')<2:#replace with max page crawls for cities          
                        args.update(_)
                        return False,[args,'retrieve_data']
                    else:
                        print('Condition ALready Satisfied. No need to further Scrape Data.Returning EMpty Dict\n')
                        print('replace dict with data, and replce max crawl page with algo')
                        print('The country has been scraped to the max amount as specified by total pages crawled.')
                        print('Now we will go through each city and get locations for each.')
                        print('Lets first retrieve all the cities.We just need their slugs as that is what is required for block and for fetching on IG')
                        _.update({'end_point':'location','data_point':'city_directory','retrieve':True})
                        cities=self.internal_get_required_data_point(**_)
                        _listo=[]
                        dicto={'threads':[]}
                        for city in cities:
                            z={}
                            if not city['id']:
                                print('None')
                            __=self.register_assistant.locations_register(method='get',operation='crawl')
                            if __.get('has_next_page') and __.get('total_pages_crawled')<2:

                            #convert this to an argument data for the location_directory
                                z.update(_)
                                z.update({'stop_condition':{'data_point':{'next_page_info':{'next_cursor':2}},'value':2,'filter':'equals'}})
                                z.update(city)
                                z.update({'end_point':'location','data_point':'location_directory'})
                            
                            _listo.append(z)
                        return False,[{'threads':_listo}]
                       

            return False, [kwargs]                
        def search_location(self,**kwargs):
            
            if kwargs.get('retrieve'):
                return 'empty_file',{}
            if kwargs.get('initialize'):
                    return{'new_content_touch_points':{'touch_point':'get_posts','elements':True},
                           'page':'location_posts_page','identifiers':['locations/web_info'],
                           'url':'https://www.instagram.com/explore/locations/213190018/cave-creek-arizona/'}

            rank_token='720c9c6c-f407-4916-b8cf-18541b898b75'
            #query=None,co_ords={},
            latitude=kwargs.get('latitude')
            longitude=kwargs.get('longitude')
            query=kwargs.get('search_query')
            params={'latitude':latitude,'longitude':longitude}
            if query:
                params.update({'search_query':query})
            
            params.update({'rankToken':rank_token})
            params.update({'timestamp':str(round(time.time()*1000))})
            url='https://www.instagram.com/api/v1/location_search/'
            resp=self.make_request(end_point='location',data_point='search_location',url=url,params=params)
            print(resp)
            self.parsers.end_point='location'
            self.parsers.data_point='search_location'
            return self.parsers.parse_end_point(resp,**kwargs)        
        def get_details_about_location(self):
            resp=self.make_request(end_point='get_details_about_location',url='https://www.instagram.com/api/v1/locations/web_info/?location_id=c2511940')
            print(resp.text)
       
        def country_directory(self,**kwargs):
            if kwargs.get('initialize'):
                    return 'success', {'identifiers':['locations/directory/'],
                           'from_request':True,

                           'url':'https://www.instagram.com/explore/locations/'}
            add_data=kwargs.get('add_data')
            resp=self.storage_sense.get_next_cursor(block={'address':'location.countries','file_name':'register'})
            if resp.get('next_cursor'):
                page_number=resp.get('next_cursor')
            else:
                page_number=1

                
            url='https://www.instagram.com/api/v1/locations/directory/?page='+str(page_number)+''
            resp=self.request_maker.make_request(url=url,end_point='location',data_point='country_directory')
            self.parsers.end_point='location'
            self.parsers.data_point='country_directory'
        
        
            return self.parsers.parse_end_point(resp,**kwargs)
        def city_directory(self,**kwargs):
            if kwargs.get('initialize'):
                    return 'success', {'identifiers':['locations/country/directory'],
                           'from_request':True,

                           'url':'https://www.instagram.com/explore/locations/US/united-states/'}
            add_data=kwargs.get('add_data')
            country_slug=add_data.get('country_slug')
            directory_code=add_data.get('directory_code')
            resp=self.storage_sense.get_next_cursor(block={'address':'location.countries.'+country_slug+'.cities','file_name':'register'})
            if resp.get('next_cursor'):
                page_number=resp.get('next_cursor')
            else:
                page_number=1
           
            url='https://www.instagram.com/api/v1/locations/country/directory/?directory_code='+directory_code+'&page='+str(page_number)+''
        
            self.request_maker.session.headers.update({'scheme':'https','path':'/api/v1/web/explore/locations/'+directory_code+'/',
                                                    'referer':'https://www.instagram.com/explore/locations/'+directory_code+'/'+country_slug+'/'
                                                    })
            resp=self.make_request(url=url,end_point='city_directory')
            self.parsers.end_point='location'
            self.parsers.data_point='city_directory'
            return self.parsers.parse_end_point(resp,**kwargs)
        def location_directory(self,**kwargs):
            if kwargs.get('initialize'):
                return'success',{
                           'identifiers':['locations/city/directory/'],#['graphql'],
                           #'variable_name':'fb_api_req_friendly_name',
                           #'variable_value':'PolarisProfilePageContentQuery',
                           'url':'https://www.instagram.com/explore/locations/c2527491/hennessey-united-states/',
                           'find_request_by_payload_variable':False,
                           'from_request':True,
                           
                           }
            add_data=kwargs.get('add_data')
            country_info=kwargs.get('country_info',{})
            country_slug=add_data.get('country_slug',None)
            
            city_code=add_data.get('city_code')
            city_slug=add_data.get('city_slug')
            
            if not kwargs.get('next_cursor'):
                if country_slug and city_slug:
                    self.storage_sense.block={'address':'location.countries.'+country_slug+'.cities.'+city_slug+'.locations','file_name':'register'}
                    self.storage_sense.load_block()
                    self.storage_sense.open_file()
                    if self.storage_sense.empty_file:
                        page_number=1
                    else:
                        resp=self.register_assistant.sort_df_and_return_the_latest_row(self.storage_sense.data_frame)
                        if resp.get('next_cursor'):
                            page_number=kwargs.get('next_cursor')
                        else:
                            page_number=1
                else:
                    page_number=1
            else:
                page_number=kwargs.get('next_cursor')
            url='https://www.instagram.com/api/v1/locations/city/directory/?directory_code='+city_code+'&page='+str(page_number)+''
            payload={'page':str(page_number)}
                
            resp=self.request_maker.make_request(url=url,end_point='location',data_point='location_directory')
            self.parsers.end_point='location'
            self.parsers.data_point='location_directory'
            return self.parsers.parse_end_point(resp,**kwargs)

        def location_info(self,**kwargs):
            if kwargs.get('task_manager_info'):
                return['country_info','location_info','city_info','tab']
            location_info=kwargs.get('location_info')
            location_slug=location_info.get('slug',None)
            location_id=location_info.get('id')
            country_info=kwargs.get('country_info',{})
            tab=kwargs.get('tab','recent')
            if not country_info:
                location_block={'address':'places.'+location_slug+'.'+tab,'file_name':'register'}
           
            else:
                country_slug=country_info.get('slug',None)
                city_info=kwargs.get('city_info')
                directory_code=city_info.get('id')
                city_slug=city_info.get('slug')
                location_block={'address':'location.countries.'+country_slug+'.cities.'+city_slug+'.locations.'+location_slug+'.'+tab+'','file_name':'register'}        
            if kwargs.get('retrieve',False):
                self.storage_sense.block=location_block
                self.storage_sense.load_block()
                self.storage_sense.open_file()
                if self.storage_sense.empty_file:
                    return 'empty_file',{}
                else:
                    _data=[]
                    resp=self.register_assistant.sort_df_and_return_the_latest_row(self.storage_sense.data_frame)
                    if not resp['next_max_id']:
                        return 'empty_file',{}
                    else:
                        _data.append(resp)
                        return 'location_info',_data
                        
            else:
               

                location_id=kwargs.get('location_id','')
                url='https://www.instagram.com/api/v1/locations/web_info/?location_id='+location_id+''
            
                self.request_maker.session.headers.update({'scheme':'https','path':'/api/v1/locations/web_info/?location_id=212918601',
                                                        'referer':'https://www.instagram.com/explore/locations/212918601/grand-central-terminal/'
                                                        })
                resp=self.make_request(url=url,end_point='location',data_point='location_info')
                self.parsers.end_point='location'
                self.parsers.data_point='location_posts'
                kwargs.update({'nexto':['next_max_id','next_page']})
                return self.parsers.parse_end_point(resp,**kwargs)
               

            ##Add middler to custom parse the response
        def location_posts(self,**kwargs):  
            if kwargs.get('initialize'):
                    return 'success', {'new_content_touch_points':{'touch_point':'get_posts','elements':True},
                           'page':'location_posts_page','identifiers':['/graphql/query'],'find_request_by_payload_variable':True,
                           'from_request':True,
                           'variable_name':'fb_api_req_friendly_name',
                            'variable_value':'PolarisLocationPageTabContentQuery_connection',
                            'find_request_by_payload_variable':True,
                           'url':'https://www.instagram.com/explore/locations/216064306/lahore-pakistan/'}
                               
            location_info=kwargs.get('location_info')
            location_slug=location_info.get('slug',None)
            location_id=location_info.get('id')
            country_info=kwargs.get('country_info',{})
            tab=kwargs.get('tab','recent')
            if not country_info:
                val=location_slug
                if not location_slug:
                    val=location_id
                location_block={'address':'location.places.'+val+'.'+tab,'file_name':'register'}
           
            else:
                country_slug=country_info.get('slug',None)
                city_info=kwargs.get('city_info')
                directory_code=city_info.get('id')
                city_slug=city_info.get('slug')
                location_block={'address':'location.countries.'+country_slug+'.cities.'+city_slug+'.locations.'+location_slug+'.'+tab+'','file_name':'register'}        

            #Retrieve the posts  or users of specific location.
            if kwargs.get('retrieve',False):
                
                    if 'users'in kwargs.get('retrieve',{}):
                        location_block={'address':'location.places.'+val+'.'+tab+'.users','file_name':'register'}
                        self.storage_sense.block=location_block
                        self.storage_sense.load_block()
                        users=[]
                        for user in os.listdir(self.storage_sense.block_address):
                            user=user.split('.json')[0]
                            if kwargs.get('info'):
                                self.storage_sense.block={'address':'location.places.'+location_slug+'.'+tab+'.users','file_name':user}
                                self.storage_sense.load_block()
                                self.storage_sense.open_file()
                                if not self.storage_sense.data_frame.empty:
                                    users.append(self.storage_sense.data_frame.to_dict(orient='records')[0])
                            else:
                                users.append({'type':'user','identifier':user})
                                
                        if kwargs.get('output_type')==list:
                            return 'success',users
                        else:
                     
                            import pandas as pd
                            
                            if len(users)>0:
                                return 'success',users
                            else:
                                return 'empty_file',[]
                    
                    
            else: 
                
                self.storage_sense.block=location_block
                self.storage_sense.load_block()
                self.storage_sense.open_file() 
                payload=self.storage_sense.get_payload_data(service='instagram',data_point='location_posts')
                if not payload:
                    print('Payload Data Not found for Location Posts. Exiting')
                    
                else:
                    import ast
                    variables=ast.literal_eval(payload.get('variables'))
                    resp=self.storage_sense.get_next_cursor(block=location_block,data_point='location_posts',service='instagram',identifier=False)
                    if 'has_next_page' in resp.keys():
                        if not resp['has_next_page']:
                            return False

                    if resp.get('end_cursor'):
                        after=resp.get('end_cursor')
                        variables.update({'after':after})
                    else:
                        variables.pop('after')
                    variables.update({'location_id':location_id})
                    variables.update({'tab':tab,'page_size_override':6})
                    import json
                    payload['variables']=json.dumps(variables)
                    
                    
                
                location_id=location_info.get('id',None)
                
               
                url='https://www.instagram.com/graphql/query'
                
               
                if kwargs.get('initialize'):
                    return 'success', {'new_content_touch_points':{'touch_point':'get_posts','elements':True},
                           'page':'location_posts_page','identifiers':['/graphql/query'],'find_request_by_payload_variable':True,
                           'from_request':True,
                           'variable_name':'fb_api_req_friendly_name',
                            'variable_value':'PolarisLocationPageTabContentQuery_connection',
                            'find_request_by_payload_variable':True,
                           'url':'https://www.instagram.com/explore/locations/216064306/lahore-pakistan/'}
                             
                self.request_maker.session.headers.update({'scheme':'https','path':'/graphql/quuery',
                                                        'referer':'https://www.instagram.com/explore/locations/'+location_id+''
                                                        })
                resp=self.request_maker.make_request(url=url,end_point='location',data_point='location_posts',r_type='post',payload=payload)
                self.parsers.end_point='location'
                self.parsers.data_point='location_posts'
                kwargs.update({'nexto':['end_cursor']})
                return self.parsers.parse_end_point(resp,**kwargs)
        def get_conversation_details(self,**kwargs):

            url='https://www.instagram.com/api/v1/direct_v2/threads/118243532902530/'
            resp=self.make_request(url=url,end_point='location_posts')
            print(resp)

        
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

    class search():
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
        def search_keyword(self,**kwargs):    
            
           
           
            if kwargs.get('initialize'):
                    return 'success', {'new_content_touch_points':{'touch_point':'get_posts','elements':True},
                           'page':'search_page','identifiers':['/fbsearch/web'],
                           'from_request':True,                          
                           'url':'https://www.instagram.com/explore/search/keyword/?q=changing%20baby%20diaper'}
            #Retrieve the posts  or users of specific location.
            if kwargs.get('retrieve',False):
                
                    if 'users'in kwargs.get('retrieve',{}):
                        search_block_users={'address':'search.keywords.'+keyword+'.'+'.users','file_name':'register'}
                        self.storage_sense.block=search_block_users
                        self.storage_sense.load_block()
                        users=[]
                        for user in os.listdir(self.storage_sense.block_address):
                            user=user.split('.json')[0]
                            if kwargs.get('info'):
                                self.storage_sense.block={'address':'search.keywords.'+keyword+'.'+'.users','file_name':user}
                                self.storage_sense.load_block()
                                self.storage_sense.open_file()
                                if not self.storage_sense.data_frame.empty:
                                    users.append(self.storage_sense.data_frame.to_dict(orient='records')[0])
                            else:
                                users.append({'type':'user','identifier':user})
                                
                        if kwargs.get('output_type')==list:
                            return 'success',users
                        else:
                     
                            import pandas as pd
                            
                            if len(users)>0:
                                return 'success',users
                            else:
                                return 'empty_file',[]
                    
                    
            else: 
                keyword=kwargs.get('keyword')
            
                search_block={'address':'search.keywords.'+keyword,'file_name':'register'}
                self.storage_sense.block=search_block
                self.storage_sense.load_block()
                self.storage_sense.open_file() 
                payload=self.storage_sense.get_payload_data(service='instagram',data_point='search_keyword')
                if not payload:
                    
                    print('Payload Data Not found for Location Posts. Exiting')
                    
                else:
                    import ast
                    payload.update({'query':keyword})
                    resp=self.storage_sense.get_next_cursor(block=search_block,data_point='search_keyword',service='instagram',identifier=False)
                    if resp.get('next_max_id'):
                        next_max_id=resp.get('next_max_id')
                        payload.update({'next_max_id':next_max_id})
                    else:
                        pass
                                            
                url='https://www.instagram.com/api/v1/fbsearch/web/top_serp/'           
                if kwargs.get('initialize'):
                    return 'success', {'new_content_touch_points':{'touch_point':'get_posts','elements':True},
                           'page':'search_page','identifiers':['/fbsearch/web'],
                           'from_request':True,                          
                           'url':'https://www.instagram.com/explore/search/keyword/?q=changing%20baby%20diaper'}
                             
                self.request_maker.session.headers.update({'scheme':'https','path':'/graphql/quuery',
                                                        'referer':'https://www.instagram.com/explore/search/keyword/?'
                                                        })
                resp=self.request_maker.make_request(url=url,end_point='location',data_point='search_keyword',r_type='get',params=payload)
                self.parsers.end_point='search'
                self.parsers.data_point='search_keyword'
                kwargs.update({'nexto':['next_max_id']})
                return self.parsers.parse_end_point(resp,**kwargs)
    class user():
    
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
            self.parsers=Parser()
            self.parsers.end_point='user'
        def search_user(self,query=None):
            context = {
                "context":"hashtag",
                "query": query,
                "rank_token": 0.547015482035698,
                "include_reel": True,
                "search_surface": "web_top_search"
                        }
        def user_info_graphql(self,**kwargs): 
            user_info=kwargs.get('user_info',{})  
            rest_id=user_info.get('rest_id',False)         
            if kwargs.get('initialize'):
                username=user_info.get('username','instagram')
                
                 
                return  'success',{
                    'page':'profile_page','identifiers':['/graphql/query'],
                    'url':'https://www.instagram.com/'+username+'',
                    'from_request':True,'variable_name':'fb_api_req_friendly_name',
                    'variable_value':'PolarisProfilePageContentQuery','find_request_by_payload_variable':True
                        }  
           
            username=user_info['username']
            kwargs.update({'username':username})
           
          
            if not rest_id:
                    return False
            if not kwargs.get('response'):
                url='https://www.instagram.com/graphql/query'
                payload=self.storage_sense.get_payload_data(data_point='user_info_graphql',service='instagram')
                if not payload:
                    return False
                next_cursor=self.storage_sense.get_next_cursor(username,data_point='user_info_graphql',service='instagram')
                if kwargs.get('next_cursor')=='force_stop':
                    next_cursor=False
                variables=json.loads(payload['variables'])
                if next_cursor:
                
                    payload.update({"fb_api_req_friendly_name": "PolarisProfilePostsTabContentQuery_connection"})
                    
                    variables.update({"after":next_cursor.get('next_cursor')})

                variables['id']=rest_id
                payload['variables']=json.dumps(variables)

                    
                
                response=self.make_request(r_type='post',end_point='user',data_point='user_info_graphql',url=url,payload=payload)
            else:
                self.parsers.data_point='user_info'
                response=kwargs.get('response')
            self.parsers.end_point='user'
            self.parsers.data_point='user_info_graphql'
            parsed_data= self.parsers.parse_end_point(response,**kwargs) 
            if not parsed_data:
                return False
            parsed_data.update({'username':username})
            return parsed_data

        def user_info(self,**kwargs):
           
            users=[]
            if kwargs.get('retrieve',False):
                
                if kwargs.get('items'):
                    if kwargs.get('items')=='usernames':
                        
                        self.storage_sense.block={'address':'users','file_name':'info'}
                        self.storage_sense.load_block()
                        for username in os.listdir(self.storage_sense.block_address):
                            users.append({'type':'user','username':username.split('.')[0]})
                            
                        return 'success',users
                    if kwargs.get('items')=='user_info':
                        user_info=kwargs.get('user_info')
                        username=user_info.get('username')
                        username=username.replace('.',',')
                        self.storage_sense.block={'address':'users.'+str(username),'file_name':'info'}
                        self.storage_sense.load_block()
                        self.storage_sense.open_file()
                        return 'success' if not self.storage_sense.data_frame.empty else False,self.storage_sense.data_frame.to_dict(orient='records')
                    if kwargs.get('items')=='user_posts':
                        _data=[]
                        user_info=kwargs.get('user_info')
                        username=user_info.get('username')
                        username=username.replace('.',',')
                        self.storage_sense.block={'address':'users.'+str(username)+'.posts','file_name':'info'}
                        self.storage_sense.load_block()
                        for post in os.listdir(self.storage_sense.block_address):
                            self.storage_sense.block={'address':'users.'+str(username)+'.posts.'+str(post),'file_name':'info'}
                           
                            self.storage_sense.load_block()
                            self.storage_sense.open_file()
                            if not self.storage_sense.data_frame.empty:
                                _data.append(self.storage_sense.data_frame.to_dict(orient='records')[0])
                        
                        return 'success',_data
                else:
                 
                    user_info=kwargs.get('user_info')
                    username=user_info.get('username')
                    username=username.replace('.',',')
                self.storage_sense.block={'address':'users.'+str(username)+'','file_name':'info'}
                self.storage_sense.load_block() 
                print(self.storage_sense.block_address)   
                self.storage_sense.open_file()
                df=self.storage_sense.data_frame                      
                if df.empty:
                    print('User Info not found for '+str(username))
                    return 'empty_file',{}
                else:
                    return 'success',df.to_dict(orient='records')
            else:
                
                if kwargs.get('initialize'):
                    user_info=kwargs.get('user_info',{})
                    username=user_info.get('username','someusername')
                    url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
                    return 'success',{
                           'page':False,'identifiers':['web_profile_info'],#['graphql'],
                           
                           #'variable_name':'fb_api_req_friendly_name',
                           #'variable_value':'PolarisProfilePageContentQuery',
                           'url':'https://www.instagram.com/'+username+'',
                           'find_request_by_payload_variable':False,
                           'from_request':True,
                           
                           }
                
                if not kwargs.get('response'):
                    user_info=kwargs.get('user_info')
                    username=user_info.get('username')
                    url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
                    self.request_maker.session.headers.update({"Host": "www.instagram.com",}) 
                    response=self.make_request(end_point='user_info',data_point='user_info',url=url)
                else:
                    
                    
                    response=kwargs.get('response')
                self.parsers.end_point='user'
                self.parsers.data_point='user_info'
                parsed_data= self.parsers.parse_end_point(response,**kwargs)    
                return parsed_data   
        def user_followers(self,**kwargs):
            from crawl.models import Task
            user_info=kwargs.get('user_info')
            username=user_info['username']
            kwargs.update({'username':username})
            user_info_args=kwargs.copy()
            user_info_args.update({'end_point':'user','data_point':'user_info','username':username,'retrieve':True})
            url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
           
                

            if kwargs.get('initialize'):
                resp,data=self.internal_get_required_data_point(**user_info_args)
    
                if resp=='success':
                    user=data[0]
                    rest_id=user.get('rest_id',None)
                    if not rest_id:
                        rest_id=user.get('id')
                    if user['is_private']:
                        raise Exception('userPrivate')
                    else:
                   
                        return  'success',{
                            'page':False,'identifiers':['query/?query_hash'],
                            'url':'https://www.instagram.com/graphql/query/?query_hash=7dd9a7e2160524fd85f50317462cff9f&variables=%7B%22id%22%3A60938916155%2C%22first%22%3A100%7D',
                            'from_request':True,
                                }
                    
                else:
                    import uuid
                    user_info_uuid = str(uuid.uuid4())
                    task={'service':'instagram',
                    'data_point':'user_info',
                    'end_point':'user',
                    'add_data':{'save_to_storage_house':True},
                    'os':'browser',
                    'input':username,
                    'uuid':user_info_uuid}
                    exstn_task=Task.objects.all().filter(data_point='user_info').filter(service='instagram').filter(input=username)
                    if exstn_task:
                        task.update({'uuid':exstn_task[0].uuid})
            
                    self.storage_sense.change_state_of_task(task=task,state='pending')
                    current_task_uuid = kwargs.get('uuid')
                    if current_task_uuid:
                        from crawl.models import Task
                        import datetime as dt
                        try:
                            dep_task = Task.objects.get(uuid=task['uuid'])   
                            Task.objects.filter(uuid=current_task_uuid).update(
                                dependent_on=dep_task,
                                status='waiting_for_user_info',
                                last_state_changed_at=dt.datetime.now().timestamp()
                            )
                        
                        except Task.DoesNotExist:
                            print("⚠️ Failed to link dependency: user_info task not found.")
                    #make the current task dependent on the task created for for user info
                    #cirremt_tasl.depemntednt _om=user_info_task.save
                
                    return 'failed','user_info_not_found'
                
            
            if kwargs.get('retrieve',False):
                self.storage_sense.block={'address':'users.'+username+'.followers'}
                self.storage_sense.load_block()
                resp=[]
                if kwargs.get('items'):
                    users=[]
                    if kwargs.get('items')=='usernames':
                        
                        
                        for username in os.listdir(self.storage_sense.block_address):
                            users.append({'type':'user','username':username.split('.')[0]})
                        return 'success', users
                for file in os.listdir(self.storage_sense.block_address):
                    self.storage_sense.block={'address':'users.'+username+'.followers','file_name':file.split('.')[0]}
                    self.storage_sense.load_block()
                    self.storage_sense.open_file()
                    
                    resp.append(self.storage_sense.data_frame.to_dict(orient='records')[0])
                return 'success',resp
            else:
               
              
                self.storage_sense.block={'address':'users.'+username.replace('.',',')+'.followers','file_name':'register'}
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
                            self.reporter.report_performance(**{
                                                'type':'exception','string':{'name':'NoNextPageAvailableforInput','args':'No Next page Available, turn on auto-stop or manually stop the task'},'task':kwargs.get('uuid'),'service':'instagram'
                                                })
                            return {} 
                    else:
                        next_cursor=kwargs.get('next_cursor')
                resp,data=self.internal_get_required_data_point(**user_info_args)
                if resp=='empty_file':
                    self.reporter.report_performance(**{
                                                    'type':'failed_to_initialize','reason':'user_info_not_found_and_empty_file','task':kwargs.get('uuid')
                                                    })
                    import uuid
                    user_info_uuid = str(uuid.uuid4())
                    task={'service':'instagram',
                    'data_point':'user_info',
                    'end_point':'user',
                    'add_data':{'save_to_storage_house':True},
                    'os':'browser',
                    'input':username,
                    'uuid':user_info_uuid}
                    from crawl.models import Task
                    import datetime as dt
                    exstn_task=Task.objects.all().filter(data_point='user_info').filter(service='instagram').filter(input=username)
                    if exstn_task:
                        task.update({'uuid':exstn_task[0].uuid})
            
                    self.storage_sense.change_state_of_task(task=task,state='pending')
                    current_task_uuid = kwargs.get('uuid')
                    if current_task_uuid:
                        from crawl.models import Task
                        import datetime as dt
                        try:
                            parent_task = Task.objects.get(uuid=task['uuid'])   
                            Task.objects.filter(uuid=current_task_uuid).update(
                                dependent_on=parent_task,
                                status='completed',
                                last_state_changed_at=dt.datetime.now().timestamp()
                            )
                        except Task.DoesNotExist:
                            print("⚠️ Failed to link dependency: user_info task not found.")
                    
                
                    return False

                user=data[0]
                rest_id=user.get('rest_id',None)
                if not rest_id:
                    rest_id=user.get('id')
                url='https://www.instagram.com/graphql/query/' 
                if not rest_id:   
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
                self.parsers.data_point='user_followers1'
                return self.parsers.parse_end_point(response,**kwargs)    
        def user_followers1(self,**kwargs):
            user_info=kwargs.get('user_info')
            username=user_info['username']
            kwargs.update({'username':username})
            user_info_args=kwargs.copy()
            user_info_args.update({'end_point':'user','data_point':'user_info','username':username,'retrieve':True})
            url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
            if kwargs.get('initialize'):
                resp,data=self.internal_get_required_data_point(**user_info_args)
                if resp=='success':
                    user=data[0]
                    rest_id=user.get('rest_id',None)
                    if not rest_id:
                        rest_id=user.get('id')
                    if user['is_private']:
                        raise Exception('userPrivate')
                    else:
                        return  'success',{
                            'page':'profile_page','identifiers':['web_profile_info'],
                            'url':'https://www.instagram.com/'+username+'',
                            'from_request':True
                                }
                else:
                    import uuid
                    task={'service':'instagram',
                    'data_point':'user_info',
                    'end_point':'user',
                    'workflow':kwargs.get('workflow'),
                    'os':'browser',
                    'input':username,
                    'dependent':kwargs,
                    'job':kwargs.get('job'),
                    'uuid':str(uuid.uuid1())}
                    self.storage_sense.change_state_of_task(task=task,state='pending')
                    return 'failed','user_info_not_found'
                
            resp,data=self.internal_get_required_data_point(**user_info_args)
            if resp=='success':
                user=data[0]
                rest_id=user.get('rest_id',None)
                if not rest_id:
                    rest_id=user.get('id')
                if user['is_private']:
                    return False,'no user info found'
            else:
                raise Exception('NoUserInfoFound')
            if kwargs.get('retrieve',False):
                self.storage_sense.block={'address':'users.'+username+'.followers','file_name':'register'}
                self.storage_sense.load_block()
                resp=[]
                for username in os.listdir(self.storage_sense.block_address):
                    resp.append({'type':'user','identifier':username.split('.')[0]})
                return 'success',resp
            else:
               
              
                self.storage_sense.block={'address':'users.'+username+'.followers','file_name':'register'}
                self.storage_sense.load_block()
                self.storage_sense.open_file()
                
                if self.storage_sense.empty_file:
                    print('Followers Register Dont Exist. Scraping Now')
                    max_id=None
                else:
                    if not kwargs.get('next_max_id'):
                        resp=self.register_assistant.sort_df_and_return_the_latest_row(self.storage_sense.data_frame)
                        if resp.get('next_max_id'):
                            
                                max_id=resp.get('next_max_id')
                        else:
                            max_id=None

                    else:
                        max_id=kwargs.get('next_max_id')
                url='https://www.instagram.com/api/v1/friendships/'+str(rest_id)+'/followers/'
           
                if not rest_id:   
                    if kwargs.get('rest_id',None):
                        rest_id=kwargs['rest_id']       
                variables = {'max_id':str(max_id), 'count': 100,'search_surface': 'follow_list_page'}  
                if not max_id:
                    variables.pop('max_id')   
                """                 if next_cursor:
                    variables.pop('first')
                    variables.update({'after':next_cursor})   """          
                query = {
                       
                        'variables': json.dumps(variables, separators=(',', ':'))
                    }
                response=self.make_request(end_point='user',data_point='user_followers',url=url,params=query)
                self.parsers.end_point='user'
                self.parsers.data_point='user_followers'
                kwargs.update({'nexto':['next_max_id']})
                return self.parsers.parse_end_point(response,**kwargs)    
        def user_posts(self,**kwargs):
            
            if kwargs.get('initialize'):
                user_info=kwargs.get('user_info',{})
                username=user_info.get('username','somename')
                """  resp,data=self.internal_get_required_data_point(**user_info_args)
                if resp=='success':
                    

                    user=data[0]
                    rest_id=user.get('rest_id',None)
                    if not rest_id:
                        rest_id=user.get('id')
                    if user['is_private']:
                        return False
                    else: """
                return  'success',{
                    'page':'profile_page','identifiers':['/graphql/query'],
                    'url':'https://www.instagram.com/'+username+'',
                    'from_request':True,'variable_name':'fb_api_req_friendly_name',
                    'variable_value':'PolarisProfilePostsQuery','find_request_by_payload_variable':True
                        }
                """ else:
                    import uuid
                    task={'service':'instagram',
                    'data_point':'user_info',
                    'end_point':'user',
                    'workflow':kwargs.get('workflow'),
                    'os':'browser',
                    'input':username,
                    
                    'profile':kwargs.get('profile'),
                    'ref_id':kwargs.get('ref_id'),
                    'uuid':str(uuid.uuid1())}
                    self.storage_sense.change_state_of_task(task=task,state='pending')
                    return 'failed','user_info_not_found' """
            user_info=kwargs.get('user_info')
            username=user_info['username']
            kwargs.update({'username':username})
           
            user_info_args={'end_point':'user','data_point':'user_info','user_info':{'username':username},'retrieve':True}

            if not kwargs.get('response'):
                url='https://www.instagram.com/graphql/query'
                payload=self.storage_sense.get_payload_data(data_point='user_posts',service='instagram')
                if not payload:
                    return False
                next_cursor=self.storage_sense.get_next_cursor(username,data_point='user_posts',service='instagram')
                if kwargs.get('next_cursor')=='force_stop':
                    next_cursor=False
                variables=json.loads(payload['variables'])
                if next_cursor:
                
                    payload.update({"fb_api_req_friendly_name": "PolarisProfilePostsTabContentQuery_connection"})
                    
                    variables.update({"after":next_cursor.get('next_cursor')})

                variables['username']=username
                payload['variables']=json.dumps(variables)
                    
                
                response=self.make_request(r_type='post',end_point='user',data_point='user_posts',url=url,payload=payload)
            else:
                response=kwargs.get('response')
            self.parsers.end_point='user'
            self.parsers.data_point='user_posts'
            parsed_data= self.parsers.parse_end_point(response,**kwargs) 
            if not parsed_data:
                return False
            parsed_data.update({'username':username})
            return parsed_data
            
        def condition_handler(self,**kwargs):
             condition=kwargs.get('condition')
             if condition=='has_new_post':
                if kwargs.get('initialize'):
                     return 'success',{'data_points':[
                                                        {'name':'user_posts',                                  
                                                       'payload_variations':[
                                                           {'variations':[{'name':'scrape','value':False},{'name':'retrieve','value':True}],'response_key':'existing_posts','items':'user_posts'},
                                                            {'variations':[{'name':'scrape','value':True},{'name':'retrieve','value':True},{'name':'next_cursor','value':'force_stop'}],'response_key':'latest_posts','items':'user_posts','max_crawls':1}
                                                            ]
                                                            }
                                                            ]
                                                            }
                else:
                    existing_posts=kwargs.get('existing_posts')
                
                    latest_posts=kwargs.get('latest_posts')
                    if not existing_posts:
                        print('There was no existing data')
                        return True,latest_posts
                    import pandas as pd
                    df1 = pd.DataFrame(existing_posts)
                    df2 = pd.DataFrame(latest_posts)

                    # Convert timestamp to datetime
                    import datetime as dt
                    df1['timestamp'] = df1['taken_at']
                    df2['timestamp'] = df2['taken_at']

                    # Sort by timestamp
                    df1 = df1.sort_values('timestamp')
                    df2 = df2.sort_values('timestamp')

                    # Merge DataFrames based on timestamp
                    merged_df = pd.merge(df2, df1, on='timestamp', how='left', indicator='_merge')
                    new_entries = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')
                    

                    if new_entries.empty:
                        return False, []
                    return True,new_entries.to_dict(orient='records')[0]
        def enrich(self,**kwargs):
            from services.openai.run_bot import OpenAi
            openai=OpenAi()
            openai.run_bot(task={''})        
    class interact():
        def __init__(self) -> None:
            self.reporter = reports_manager()  # ✅ Create reporter
            self.browser=Browser()

        def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
            end_point=getattr(self,kwargs.get('end_point'))
            data_point=getattr(end_point,kwargs.get('data_point'))
            return data_point(self,**kwargs)
    
        def internal_get_required_data_point(self,**kwargs):
            end_point=getattr(self,kwargs.get('end_point'))
            data_point=getattr(end_point,kwargs.get('data_point'))
            return data_point(self,**kwargs)
        def take_and_save_screenshot_to_storage_house_and_get_path(self,browser,storage_house_url):
            s=Saver()
            s.block={'address':'screenshots'}
            s.load_screenshots()
            import uuid
            file_name=str(uuid.uuid1())+'.jpg'
            pth=os.path.join(s.block_address,file_name)
           
            from base.downloader import Downloader
            d=Downloader()
            d.storage_house_url=storage_house_url
            
            base64_encoded = browser.driver.get_screenshot_as_base64()
            pth=d.save_to_storage_house(base64_text=base64_encoded,media_type='image',bucket_name='instagram_challenge_pages')
            return pth
        def open_browser_profile(self,**kwargs):
            from services.instagram.locator import Locator
            logged_in=False
            locator=Locator()
            locator.browser=self.browser
            
            try:
                
                locator.browser.driver.find_element_by_xpath('//,.')
            except Exception as e:
                if 'no such window' in str(e) or 'invalid session' in str(e):
                    print('window closed by user')
                    return 'success',''
                else:
                    time.sleep(10)
                    return self.internal_get_required_data_point(**{'end_point':'interact','data_point':'open_browser_profile'})       
                
        def login(self,**kwargs):
            if kwargs.get('task_manager_info'):
                return['resources.profile']
            if kwargs.get('initialize'):
                    if not kwargs.get('os')=='android':
                        return'success',{
                            'page':'login_page','identifiers':['get_username_input','get_password_input'],
                            'url':'https://www.instagram.com/'}
            os=kwargs.get('os')
            if os =='android':
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs
                i.storage_sense=self.storage_sense
                try:
                    i.run()

                except Exception as e:
                    print(e)
                    print('Add Report when Device Run Bot Exception is raised')
                    return 0
                else:
                    if i.logged_in:
                        logged_in=True
                        
                    else:
                        logged_in=False
                        

            else:#if os=='chrome'
                from crawl.models import ChildBot
                from services.instagram.locator import Locator
                from services.instagram.xpaths import Xpaths
                import requests
                import time
                max_login_attempts = 3
                logged_in = False  # ✅ Initialize it at the start
                start_time = time.time()

                for login_attempt in range(max_login_attempts):
                    print(f"\n🔁 Login Attempt {login_attempt + 1} of {max_login_attempts}")
                    try:
                        profile = kwargs.get("profile", "unknown") 
                        url = "https://www.instagram.com/"

                        
                        self.browser.visit(url,**kwargs)
                        
                           
                        print(f"✅ login started: {start_time}")
                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'start',
                            'page': self.browser.driver.current_url,
                            'type': 'login_attempt_started',
                            'username': profile,
                            'max_attempts' : login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'critical': False,
                            'timestamp': start_time
                        })
                        _profile = ChildBot.objects.filter(service=kwargs['service']).filter(username=kwargs.get('profile'))
                        print(_profile)
                        if not _profile:
                            self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'auth',
                            'type': 'profile_not_found',
                            'page': self.browser.driver.current_url,
                            'username': profile,
                            'max_attempts' : login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'critical': True,
                            'timestamp': time.time(),
                            

                            })
                            print("❌ No profile found")
                            break

                        profile = list(_profile.values())[0]

                        if not profile.get('username') or not profile.get('password'):

                            self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'auth',
                            'type': 'username_or_password_not_found',
                            'page': self.browser.driver.current_url,
                            'max_attempts' : login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'critical': True,
                            'timestamp': time.time(),
                            

                            })
                            break
                        else:
                            
                            self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'auth',
                            'type': 'username_or_password_found',
                            'page': self.browser.driver.current_url,
                            'max_attempts' : login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'critical': False,
                            'timestamp': time.time(),
                            

                            })

                        x = Xpaths()
                        locator = Locator()
                        locator.browser = self.browser
                        locator.locate_by_xpath(xpath=x.LoginPage().get_allow_all_cookies_banner(),click=True,retries=3)
                        active_page = locator.identify_active_page(
                            page_locators_dict={
                                'LoginPage': x.LoginPage().get_username_input(),
                                'HomePage': x.Navigation().click_explore_button(),
                                'ChallengePage':x.ChallengePage().automated_behavior_warning_page()
                            },
                            max_retries=30,**kwargs
                        )
                        if active_page =='ChallengePage':
                              
                            self.reporter.report_performance(**{
                                'service': 'instagram',
                                'end_point': 'login',
                                'data_point': 'auth',
                                'type': 'automated_behavior_detected_warning',
                                'page': self.browser.driver.current_url,
                                'task': kwargs.get('uuid'),
                                'run_id': kwargs.get('run_id'),                             
                                'timestamp': time.time(),
                                'screenshot_url':self.interact().take_and_save_screenshot_to_storage_house_and_get_path(browser=self.browser,storage_house_url=kwargs.get('add_data').get('storage_house_url'))
                                
                                    })
                            locator.locate_by_xpath(xpath=x.ChallengePage().click_dismiss_button(),click=True,retries=5)
                            self.reporter.report_performance(**{
                                'service': 'instagram',
                                'end_point': 'login',
                                'data_point': 'auth',
                                'type': 'dismissed_automated_behavior_detected_warning',
                                'page': self.browser.driver.current_url,
                                'task': kwargs.get('uuid'),
                                'run_id': kwargs.get('run_id'),                             
                                'timestamp': time.time(),
                                'screenshot_url':self.interact().take_and_save_screenshot_to_storage_house_and_get_path(browser=self.browser,storage_house_url=kwargs.get('add_data').get('storage_house_url'))
                                
                                    })
                        if active_page == 'HomePage':
                            # self.reporter.report_performance(**{
                            # 'service': 'instagram',
                            # 'end_point': 'login',
                            # 'data_point': 'already_logged',
                            # 'page': self.browser.driver.current_url,
                            # 'type': 'login_attempt_finished',
                            # 'max_attempts' : login_attempt + 1,
                            # 'task': kwargs.get('uuid'),
                            # 'run_id': kwargs.get('run_id'),
                            # 'critical': False,
                            # 'timestamp': time.time(),
                            
                            # })
                            print('✅ Already logged in.')
                            logged_in = True
                            break

                        elif active_page == 'LoginPage':
                            print('➡️ On Login Page')

                            u_in = locator.locate_by_xpath(x.LoginPage().get_username_input(), click=True, retries=5,**kwargs)
                            if u_in:
                                u_in.send_keys(profile.get('username'))

                                p_in = locator.locate_by_xpath(x.LoginPage().get_password_input(), click=True, retries=5,**kwargs)
                                if p_in:
                                    p_in.send_keys(profile.get('password'))

                                locator.locate_by_xpath(x.LoginPage().click_login_button(), click=True, retries=5,**kwargs)

                                if locator.locate_by_xpath(x.LoginPage().incorrect_password_text(), retries=3,**kwargs):
                                    print("❌ Incorrect password.")
                                    print("Exiting login attempts due to incorrect password.")

                                    self.reporter.report_performance(**{
                                        'service': 'instagram',
                                        'end_point': 'login',
                                        'data_point': 'auth',
                                        'page': self.browser.driver.current_url,
                                        'type': 'incorrect_password',
                                        'task': kwargs.get('uuid'),
                                        'run_id': kwargs.get('run_id'),
                                        'max_attempts': login_attempt + 1,
                                        'timestamp': time.time(),
                                        'critical': True,
                                        
                                       
                                    })

                                    
                                    break
                                    
                                    
                                
                                if locator.locate_by_xpath(x.LoginPage().get_instagram_login_error(), retries=3):

                                    self.reporter.report_performance(**{
                                        'service': 'instagram',
                                        'end_point': 'login',
                                        'data_point': 'auth',
                                        'type': 'internet_issue',
                                        'page': self.browser.driver.current_url,
                                        'task': kwargs.get('uuid'),
                                        'run_id': kwargs.get('run_id'),
                                        'max_attempts': login_attempt + 1,
                                        'timestamp': time.time(),
                                        'critical': False,
                                        'login_attempt_failed': True
                                        
                                       
                                    })
                                    for i in range(0,3):
                                        if not locator.locate_by_xpath(x.LoginPage().click_login_button(),click=True):
                                            break
                                    active_page = locator.identify_active_page(
                                                    page_locators_dict={
                                                        'LoginPage': x.LoginPage().get_username_input(),
                                                        'HomePage': x.Navigation().click_explore_button(),
                                                    },
                                                    max_retries=3,**kwargs
                                                )
                                    if active_page=='LoginPage':

                                            print("❌ Internet issue")
                                            print("Exiting login attempts due to Internet connection issue.")

                                            continue  # Retry full login
                                
                                
                                  

                                active_page = locator.identify_active_page(
                                    page_locators_dict={
                                        'AuthenticationPage': x.LoginPage().get_security_code_input_field(),
                                        'ChallengePage':x.ChallengePage().automated_behavior_warning_page(),
                                        'HomePage': x.Navigation().click_explore_button()
                                    },
                                    max_retries=10,**kwargs
                                )
                                if active_page=='ChallengePage':
                                    
                                    self.reporter.report_performance(**{
                                        'service': 'instagram',
                                        'end_point': 'login',
                                        'data_point': 'auth',
                                        'type': 'automated_behavior_detected_warning',
                                        'page': self.browser.driver.current_url,
                                        'task': kwargs.get('uuid'),
                                        'run_id': kwargs.get('run_id'),                             
                                        'timestamp': time.time(),
                                        'screenshot_url':self.take_and_save_screenshot_to_storage_house_and_get_path(**kwargs)
                                        
                                            })
                                    
                                    locator.locate_by_xpath(xpath=x.ChallengePage().click_dismiss_button(),click=True,retries=5)
                                    self.reporter.report_performance(**{
                                        'service': 'instagram',
                                        'end_point': 'login',
                                        'data_point': 'auth',
                                        'type': 'dismissed_automated_behavior_detected_warning',
                                        'page': self.browser.driver.current_url,
                                        'task': kwargs.get('uuid'),
                                        'run_id': kwargs.get('run_id'),                             
                                        'timestamp': time.time(),
                                        'screenshot_url':self.interact().take_and_save_screenshot_to_storage_house_and_get_path(browser=self.browser,storage_house_url=kwargs.get('add_data').get('storage_house_url'))
                                        
                                            })
                                if active_page == 'AuthenticationPage':
                                    print("🔐 2FA required. Trying to fetch token...")
                                    print(kwargs.get('run_id'))
                                    from selenium.webdriver.common.keys import Keys
                                    success = False
                                    for attempt in range(6):  # Retry this entire 2FA process 3 times
                                        print(f"🔁 2FA Attempt {attempt + 1}/3")

                                        self.reporter.report_performance(**{
                                            'service': 'instagram',
                                            'end_point': 'login',
                                            'data_point': 'auth',
                                            'type': '2fa_start',
                                            'page': self.browser.driver.current_url,
                                            'task': kwargs.get('uuid'),
                                            'run_id': kwargs.get('run_id'),
                                            'max_attempts' : attempt + 1,
                                            'timestamp': time.time(),
                                            'critical': False,
                                           
                                        })
                                        # Ensure you're on the right page and input is present
                                        security_code_input = locator.locate_by_xpath(
                                            x.LoginPage().get_security_code_input_field(), click=True, retries=10,**kwargs
                                        )

                                        if not security_code_input:
                                            print("❌ Security code input field not found.")
                                            continue

                                        token_sent = False
                                        auth_code = profile.get('auth_code')
                                        auth_code = auth_code.replace(" ", "")
                                        if auth_code:
                                            try:
                                                resp = requests.get(f"https://2fa.live/tok/{auth_code}", timeout=5)
                                                if resp.ok:
                                                    token = resp.json().get('token')
                                                    if token:
                                                        self.reporter.report_performance(**{
                                                            'service': 'instagram',
                                                            'end_point': 'login',
                                                            'data_point': 'auth',
                                                            'type': '2fa_token_found',
                                                            'page': self.browser.driver.current_url,
                                                            'task': kwargs.get('uuid'),
                                                            'run_id': kwargs.get('run_id'),
                                                            'max_attempts' : attempt + 1,
                                                            'timestamp': time.time(),
                                                            'critical': False,
                                                            'token': token
                                                        })
                                                        print(f"🔑 Token fetched: {token}")
                                                        security_code_input.click()
                                                        security_code_input.send_keys(Keys.CONTROL, 'a')
                                                        security_code_input.send_keys(Keys.BACKSPACE)
                                                        time.sleep(2)
                                                        print("🔑 Force-cleared input field")
                                                        security_code_input.send_keys(token)
                                                        token_sent = True
                                                    else:
                                                        print("❌ Token not found in response.")
                                                else:
                                                    print(f"❌ Token fetch failed: {resp.status_code}")
                                                    self.reporter.report_performance(**{
                                                        'service': 'instagram',
                                                        'end_point': 'login',
                                                        'data_point': 'auth',
                                                        'type': '2fa_resp_failed',
                                                        'page': self.browser.driver.current_url,
                                                        'task': kwargs.get('uuid'),
                                                        'run_id': kwargs.get('run_id'),
                                                        'max_attempts' : login_attempt + 1,
                                                        'timestamp': time.time(),
                                                        'critical': False,
                                                        '2fa_attempt_failed': True
                                                    })
                                            except Exception as e:
                                                self.reporter.report_performance(**{
                                                    'service': 'instagram',
                                                    'end_point': 'login',
                                                    'data_point': '2fa_auth',
                                                    'type': 'exception',
                                                    'task': kwargs.get('uuid'),
                                                    'run_id': kwargs.get('run_id'),
                                                    'max_attempts': login_attempt + 1,  # Current 2FA retry attempt
                                                    'string': {
                                                        'name': type(e).__name__,
                                                        'args': str(e)
                                                    },
                                                    'traceback': traceback.format_exc(),
                                                    'timestamp': time.time(),
                                                    'critical': True,
                                                })
                                                print(f"❌ Error fetching token: {e}")
                                        else:
                                            print('❌ No auth_code provided.')
                                            break  # Can't proceed without auth code

                                        if not token_sent:

                                            print("⚠️ Token fetch or input failed. Retrying 2FA process...")
                                            self.reporter.report_performance(**{
                                            'service': 'instagram',
                                            'end_point': 'login',
                                            'data_point': 'auth',
                                            'type': '2fa_token_not_found',
                                            'page': self.browser.driver.current_url,
                                            'task': kwargs.get('uuid'),
                                            'run_id': kwargs.get('run_id'),
                                            'max_attempts': login_attempt + 1,  
                                            'timestamp': time.time(),
                                            'critical': False,
                                            '2fa_attempt_failed': True
                                        
                                             })
                                            continue  # Go for next attempt

                                        # Try clicking confirm and verifying login success
                                       
                                        confirm_button = locator.locate_by_xpath(
                                                x.LoginPage().get_confirm_button(), click=True, retries=3
                                            )

                                        if confirm_button:
                                            print("✅ Confirm button clicked.")
                                        
                                        else:
                                            print("❌ Confirm button not found.")
                                            self.reporter.report_performance(**{
                                            'service': 'instagram',
                                            'end_point': 'login',
                                            'data_point': 'auth',
                                            'type': '2fa_confirm_button_not_found',
                                            'page': self.browser.driver.current_url,
                                            'task': kwargs.get('uuid'),
                                            'run_id': kwargs.get('run_id'),
                                            'max_attempts': login_attempt + 1,  
                                            'timestamp': time.time(),
                                            'critical': False,
                                            '2fa_attempt_failed': True
                                             })
                                            continue

                                        # time.sleep(5)  # Wait after confirm click

                                        # Check if we reached the home page
                                        
                                        final_page = locator.identify_active_page(
                                            page_locators_dict={'HomePage': x.Navigation().click_explore_button()},
                                            max_retries=10
                                        )
                                        recheck_confirm_button = locator.locate_by_xpath(
                                                x.LoginPage().get_confirm_button(), retries=3
                                            )
                                        
                                        if not recheck_confirm_button:
                                            final_page = locator.identify_active_page(
                                            page_locators_dict={'HomePage': x.Navigation().click_explore_button()},
                                            max_retries=10
                                        )
                                        if not final_page and not recheck_confirm_button:
                                            self.browser.driver.refresh()
                                            final_page = locator.identify_active_page(
                                            page_locators_dict={'HomePage': x.Navigation().click_explore_button()},
                                            max_retries=20)

                                        if final_page == 'HomePage':
                                            print("✅ Login successful after confirming 2FA.")
                                            

                                            self.reporter.report_performance(**{
                                                'service': 'instagram',
                                                'end_point': 'login',
                                                'data_point': 'auth',
                                                'type': '2fa_success',
                                                'page': self.browser.driver.current_url,
                                                'task': kwargs.get('uuid'),
                                                'run_id': kwargs.get('run_id'),
                                                'max_attempts' : login_attempt + 1,
                                                'timestamp': time.time(),
                                                'critical': False,
                                                'token': token
                                            })
                                            logged_in = True
                                            success = True
                                            break
                                        else:
                                            self.reporter.report_performance(**{
                                                'service': 'instagram',
                                                'end_point': 'login',
                                                'data_point': 'auth',
                                                'type': '2fa_failed',
                                                'page': self.browser.driver.current_url,
                                                'task': kwargs.get('uuid'),
                                                'run_id': kwargs.get('run_id'),
                                                'max_attempts' : login_attempt + 1,
                                                'timestamp': time.time(),
                                                'critical': False,
                                                'token': token,
                                                '2fa_attempt_failed': True
                                                
                                            })
                                            print("⚠️ Confirm clicked, but HomePage not yet found. Retrying...")

                                    if success:
                                        break  # Exit outer retry loop if everything worked

                                    if not success:
                                        self.reporter.report_performance(**{
                                            'service': 'instagram',
                                            'end_point': 'login',
                                            'data_point': 'auth',
                                            'type': '2fa_failed_after_retry',
                                            'page': self.browser.driver.current_url,
                                            'task': kwargs.get('uuid'),
                                            'run_id': kwargs.get('run_id'),
                                            'max_attempts': login_attempt + 1,  
                                            'timestamp': time.time(),
                                            'critical': False,
                                            '2fa_attempt_failed': True
                                        
                                        })
                                        print("❌ 2FA failed after 6 attempts. Will retry full login.")
                                        continue  # This will trigger retry of full login flow

                                elif active_page is None:
                            
                                    self.reporter.report_performance(**{
                                            'service': 'instagram',
                                            'end_point': 'login',
                                            'data_point': 'auth',
                                            'type': 'failed_to_identify_active_page_2fa_retry',
                                            'page': self.browser.driver.current_url,
                                            'task': kwargs.get('uuid'),
                                            'run_id': kwargs.get('run_id'),
                                            'max_attempts': login_attempt + 1,  
                                            'timestamp': time.time(),
                                            'critical': False,
                                            '2fa_attempt_failed': True
                                        
                                        })
                                    continue        

                        elif active_page is None:

                            self.reporter.report_performance(**{
                                    'service': 'instagram',
                                    'end_point': 'login',
                                    'data_point': 'auth',
                                    'type': 'failed_to_identify_active_page',
                                    'page': self.browser.driver.current_url,
                                    'task': kwargs.get('uuid'),
                                    'run_id': kwargs.get('run_id'),
                                    'max_attempts': login_attempt + 1,  
                                    'timestamp': time.time(),
                                    'critical': False,
                                    'login_attempt_failed': True
                                
                                })
                                
                            continue 

                    except Exception as e:
                        import traceback
                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'login_exception',
                            'type': 'exception',
                            'max_attempts': login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'string': {'name': type(e).__name__, 'args': str(e)},
                            'traceback': traceback.format_exc(),
                            'timestamp': time.time(),
                            'critical': True,

                        })
                        print(f"❌ Login error occurred: {e}")
                        time.sleep(2)
                

                if logged_in:
                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'login',
                            'data_point': 'end',
                            'type': 'login_success',
                            'page': self.browser.driver.current_url,
                            'max_attempts': login_attempt + 1,
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'timestamp': time.time(),
                            'critical': False,
                        })
                        end_time = time.time()
                        latency = round(end_time - start_time, 2)
                        print(f"login finished in {latency}")
                        self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'login',
                        'data_point': 'end',
                        'page': self.browser.driver.current_url,
                        'type': 'login_attempt_finished',
                        'max_attempts' : login_attempt + 1,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'critical': False,
                        'timestamp': end_time,
                    })
                        return 'success', 'logged_in'

                else:
                    
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'login',
                        'data_point': 'end',
                        'type': 'login_failed',
                        'page': self.browser.driver.current_url,
                        'max_attempts': login_attempt + 1,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'timestamp': time.time(),
                        'critical': False,
                    })
                    end_time = time.time()
                    latency = round(end_time - start_time, 2)
                    print(f"login finished in {latency}")
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'login',
                        'data_point': 'end',
                        'page': self.browser.driver.current_url,
                        'type': 'login_attempt_finished',
                        'max_attempts' : login_attempt + 1,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'critical': False,
                        'timestamp': end_time,
                    })
                    print("❌ All login attempts failed.")
                    print("Failed Login.Update Login Status of Profile Here")
                    from services.resource_manager.profiles import Profile
                    return 'failed',False
                                
   

        def search_user_and_interact(self,**kwargs):
            bulk_dm_mode=False
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                add_data=kwargs.get('add_data')
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
                self.browser.driver.get('https://www.instagram.com/')
                time.sleep(2)
                targets=kwargs.get('targets')
                add_data=kwargs.get('add_data')
                
                if add_data.get('send_reachout_message'):
                    bulk_dm_mode=True
                    for key in ['open_highlights_of_target','watch_story']:
                        if add_data.get(key)==True:
                            bulk_dm_mode=False
                if bulk_dm_mode:
                    reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                        'type':'bulk_dm_mode_activated','task':str(kwargs['uuid']), 
                                        })  
                    if locator.locate_by_xpath(xpath=x.Navigation().click_messenger_button(),click=True,retries=10):
                        reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                        'type':'clicked_messenger_button_from_navigation','task':str(kwargs['uuid']), 
                                        })
                        for target in targets:  
                            self.browser.driver.refresh()
                            
                            target=target['username'].replace(',','.')
                            
                            if locator.locate_by_xpath(x.Messenger().click_compose_new_message_button(),click=True,retries=8):
                                        reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                        'type':'clicked_compose_button_from_messenger_page','task':str(kwargs['uuid']), 
                                        })
                                        elem=locator.locate_by_xpath(x.Messenger().focus_on_messenger_recipient_search_text_box(),retries=5)
                                        if elem:
                                            elem.send_keys(target)
                                            reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                'type':'sent_keys_to_messenger_recipient_search_text_box','task':str(kwargs['uuid']), 
                                                })
                                            results=locator.locate_by_xpath(x.Messenger().iterate_over_search_results(),elements=True,retries=5)
                                            clicked=False
                                            if results:
                                               
                                                results[0].click()
                                                

                                                clicked=True
                                            if clicked:
                                                reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                'type':'clicked_first_result','task':str(kwargs['uuid']), 
                                                })
                                                if locator.locate_by_xpath(x.Messenger().click_chat_button(),click=True,retries=3):
                                                    reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                        'type':'clicked_chat_button_in_messenger_page','task':str(kwargs['uuid']), 
                                                        })
                                                    if locator.locate_by_xpath(x.Messenger().click_conversation_details_button(),click=True,retries=4):
                                                        reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                            'type':'clicked_conversation_details_button','task':str(kwargs['uuid']), 
                                                            })
                                                        recipient=locator.locate_by_xpath(x.Messenger().get_username_of_recipient(),retries=5)
                                                        if not recipient:
                                                            reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                            'type':'recipient_information_not_found_trying_again','task':str(kwargs['uuid']), 
                                                            })
                                                            locator.locate_by_xpath(x.Messenger().click_conversation_details_button(),click=True,retries=4)
                                                            reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                            'type':'clicked_conversation_details_button','task':str(kwargs['uuid']), 
                                                            })
                                                            recipient=locator.locate_by_xpath(x.Messenger().get_username_of_recipient(),retries=5)
                                                        if recipient and recipient.text==target:
                                                            
                                                            reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                            'type':'recipient_found_and_matches_target','task':str(kwargs['uuid']), 
                                                            })
                                                            elem=locator.locate_by_xpath(x.Messenger().focus_on_message_text_area(),click=True)
                                                            if elem:
                                                                reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                                    'type':'focused_on_message_text_area','task':str(kwargs['uuid']), 
                                                                    })
                                                                elem.send_keys(add_data.get('messaging')[0].get('reachout_message'))
                                                                reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                                    'type':'typed_message_in_message_text_area','task':str(kwargs['uuid']), 
                                                                    })
                                                                if locator.locate_by_xpath(x.Messenger().click_send_button(),click=True):
                                                                    reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                                    'type':'clicked_send_button','task':str(kwargs['uuid']), 
                                                                    })
                                                                    s=Saver()
                                                                    s.block={'address':'screenshots'}
                                                                    s.load_screenshots()
                                                                    import uuid
                                                                    file_name=str(uuid.uuid1())+'.jpg'
                                                                    pth=os.path.join(s.block_address,file_name)
                                                                    self.browser.driver.save_screenshot(pth)
                                                                    from crawl.models import Interaction
                                                                    i=Interaction(**{'ref_id':kwargs.get('ref_id'),'activity':'dm',
                                                                            'target_profile':target,'screenshot':file_name,'bot_username':kwargs.get('profile'),
                                                                            'data':add_data.get('messaging'), 'dm_type':'reachout_message'
                                                                            })
                                                                    i.save() 
                                                                    reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                                    'type':'sent_dm_to_'+str(target),'task':str(kwargs['uuid']), 
                                                                    })  
                                                        else:
                                                            reports_manager().report_performance(**{'service':'instagram','end_point':'Interact','data_point':'search_user_and_interact',
                                                                            'type':'recipient_not_found_or_mismatch','task':str(kwargs['uuid']), 
                                                                            })
                        return True
                for target in targets:
                  
                    target=target['username'].replace(',','.')
                    if locator.locate_by_xpath(xpath=x.Navigation().click_search_button(),click=True):
                        time.sleep(1)
                        elem=locator.locate_by_xpath(x.Search().enter_search_query())
                        if elem:
                            time.sleep(1)
                            elem.send_keys(target)
                            time.sleep(2)
                        else:
                            continue
                        elems=locator.locate_by_xpath(x.Search().iterate_through_search_results(),elements=True,retries=20)
                        found=False
                        for elem in elems:
                            href=elem.get_attribute('href')
                            href=href.replace('https://www.instagram.com/','')
                            href=href.strip('/')
                            if href==target:
                                found=True
                                break
                        if found:
                            elem.click()
                            time.sleep(2)
                      
                           
                            if add_data.get('open_highlights_of_target'):
                                elems=locator.locate_by_xpath(x.ProfilePage().get_highlights(),elements=True)
                                if elems:
                                    elems[2].click()
                                    time.sleep(2)
                                    locator.locate_by_xpath(x.StoryPage().close_story_section(),click=True)
                            if add_data.get('open_posts_of_user_and_like'):

                                elems=locator.locate_by_xpath(x.ProfilePage().get_posts_of_user(),elements=True)
                                if elems:
                                    elems[1].click()
                                    if locator.locate_by_xpath(x.PostDialogBox().post_dialog_box()):
                                        locator.locate_by_xpath(x.PostDialogBox().focus_on_comments_section())
                                        locator.locate_by_xpath(x.PostDialogBox().click_add_comment_text_area())
                            if add_data.get('follow_target'):
                                elem=locator.locate_by_xpath(x.ProfilePage().follow_button())
                                if elem and elem.text=='Following':
                                    print('Already following user')
                                else:
                                    locator.locate_by_xpath(x.ProfilePage().follow_button(),click=True)
                                    from crawl.models import Interaction
                                    s=Saver()
                                    s.block={'address':'screenshots'}
                                    s.load_screenshots()
                                    import uuid
                                    file_name=str(uuid.uuid1())+'.jpg'
                                    pth=os.path.join(s.block_address,file_name)
                                    self.browser.driver.save_screenshot(pth)
                                    i=Interaction(**{'ref_id':kwargs.get('ref_id'),'activity':'follow',
                                                    'target_profile':target,'screenshot':file_name,'bot_username':kwargs.get('profile')
                                                    })
                                    i.save()      
                            if add_data.get('messaging'):
                                if locator.locate_by_xpath(x.ProfilePage().get_message_button(),click=True,retries=3):
                                    elem=locator.locate_by_xpath(x.Messenger().focus_on_message_text_area(),click=True,retries=10)
                                    if elem:
                                        text=add_data.get('messaging',{}).get('text',False)
                                        if not text:
                                            return
                                        elem.send_keys(text)
                                        if locator.locate_by_xpath(x.Messenger().click_send_button(),click=True,retries=3):
                                            s=Saver()
                                            s.block={'address':'screenshots'}
                                            s.load_screenshots()
                                            import uuid
                                            file_name=str(uuid.uuid1())+'.jpg'
                                            pth=os.path.join(s.block_address,file_name)
                                            self.browser.driver.save_screenshot(pth)
                                            from crawl.models import Interaction
                                            i=Interaction(**{'ref_id':kwargs.get('ref_id'),'activity':'dm',
                                                    'target_profile':target,'screenshot':file_name,'bot_username':kwargs.get('profile'),
                                                    'data':add_data.get('messaging'), 'dm_type':add_data.get('messaging',{}).get('type','')
                                                    })
                                            i.save()   
                                pass
        def feed_post(self,**kwargs):
            if kwargs.get('task_manager'):
                return ['interact_with']
                
            if not kwargs.get('media_link'):
                print('Media Link not specified. using defualt interactions')
            
            

            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs               
         
            i.storage_sense=self.storage_sense
            i.run()
        def check_followers(self,**kwargs):
            return None, None
        def explore_explore_page(self,**kwargs):
            if kwargs.get('task_manager'):
                return ['interact_with']

            

            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs                   
            i.storage_sense=self.storage_sense
            i.run()
        def explore_home_page(self,**kwargs):
            add_data=kwargs.get('add_data')
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
                self.browser.driver.get('https://www.instagram.com/')
                locator.locate_by_xpath(xpath=x.Navigation().click_home_button(),click=True)
                visited_posts=[]
                for u in range(0,add_data.get('max_swipes')):
                    
                    posts=locator.locate_by_xpath(xpath=x.HomePage().iterate_through_posts(),elements=True)
                
                    for i,post in enumerate(posts):
                        try:
                            username=post.find_element_by_xpath(x.HomePage().get_username_from_post()[0]).text
                            if username in visited_posts:
                                continue
                            else:
                                visited_posts.append(username)
                            self.browser.scroll(element=post)
                            time.sleep(1)
                            try:
                                print(post.find_element_by_xpath(x.HomePage().get_username_from_post()[0]).text)
                            except Exception as e:
                                pass
                            elem=post.find_element_by_xpath(x.HomePage().click_next_media_button()[0])
                            if elem:
                                for i in range(0,2):
                                    time.sleep(1)
                                    try:
                                        post.find_element_by_xpath('.'+x.HomePage().click_next_media_button()[0]).click()
                                    except Exception as e:
                                        pass
                            if add_data.get('open_comments_and_scroll'):
                                elem=post.find_element_by_xpath('.'+x.HomePage().click_comment_button()[0])
                                if elem:
                                    time.sleep(1)
                                    elem.click()
                                    time.sleep(2) 
                                    pd_elem=locator.locate_by_xpath(x.PostDialogBox().post_dialog_box()[0])
                                    if elem:
                                        elem=locator.locate_by_xpath(x.PostDialogBox().focus_on_comments_section(),click=True)
                                        for i in range(0,2):
                                            time.sleep(1)
                                            self.browser.scroll(kind='page_down_key')
                                    if add_data.get('comment_on_posts_randomly'):
                                        import random
                                        if random.randint(1,10) in [0,1,7,2]:
                                            elem=locator.locate_by_xpath('.'+x.PostDialogBox().click_add_comment_text_area()[0])
                                            if elem:
                                                from selenium import webdriver
                                                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                                                from selenium.webdriver import ActionChains
                                                from selenium.webdriver.common.by import By
                                                from selenium.webdriver.common.keys import Keys
                                                time.sleep(1)
                                                ActionChains(self.browser.driver).move_to_element(elem).click().send_keys('Woah!!').perform()
                                                time.sleep(1)
                                                elem=locator.locate_by_xpath('.'+x.PostDialogBox().click_post_comment_button()[0])
                                                if elem:
                                                    time.sleep(1)
                                                    elem.click()
                                    if add_data.get('bookmark_posts_randomly'):
                                        pass
                                    if add_data.get('share_posts'):
                                        pass
                                    if add_data.get('like_posts_randomly'):
                                        pass
                                    if locator.locate_by_xpath(x.PostDialogBox().post_dialog_box()):
                                        time.sleep(1)
                                        self.browser.driver.back()
                                        time.sleep(1)

                            
                            """                             for y in range(0,2):
                                elems[i].click() """
                            time.sleep(1)

                        except Exception as e:
                            pass
        
        def explore_reels_page(self,**kwargs):
            add_data=kwargs.get('add_data')
            add_data={'max_swipes':5,'open_comments_and_scroll':True,'comment_on_posts_randomly':False}
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
                self.browser.driver.get('https://www.instagram.com/')
                time.sleep(2)
                elem=locator.locate_by_xpath(xpath=x.Navigation().click_reels_button(),click=True)
                time.sleep(2)
                visited_posts=[]
                for u in range(0,add_data.get('max_swipes')):
                    time.sleep(1)
                    posts=locator.locate_by_xpath(xpath=x.Reels().iterate_through_posts(),elements=True)
                
                    for i,post in enumerate(posts):
                        try:
                            username=post.find_element_by_xpath('.'+x.Reels().get_username()[0]).text
                            if username in visited_posts:
                                continue
                            else:
                                visited_posts.append(username)
                            self.browser.scroll(element=post)
                            time.sleep(1)
                            try:
                                print(post.find_element_by_xpath(x.Reels().get_username()[0]).text)
                            except Exception as e:
                                pass
                            elem=post.find_element_by_xpath('.'+x.Reels().get_like_button()[0])
                            if elem:
                                elem.click()
                            if random.randint(1,20) in [3,7,9,11,8]:
                             if add_data.get('open_comments_and_scroll'):
                                elem=post.find_element_by_xpath('.'+x.Reels().click_comment_button()[0])
                                if elem:
                                    time.sleep(1)
                                    elem.click()
                                    time.sleep(2) 
                                    pd_elem=locator.locate_by_xpath(x.Reels().click_comment_container()[0])
                                    if pd_elem:
                                        
                                        for i in range(0,2):
                                            time.sleep(1)
                                            self.browser.send_command_key(pd_elem,'page_down')
                                    if add_data.get('comment_on_posts_randomly'):
                                        elem=locator.locate_by_xpath('.'+x.Reels().click_add_comment_text_area()[0])
                                        if elem:
                                            from selenium import webdriver
                                            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                                            from selenium.webdriver import ActionChains
                                            from selenium.webdriver.common.by import By
                                            from selenium.webdriver.common.keys import Keys
                                            time.sleep(1)
                                            ActionChains(self.browser.driver).move_to_element(elem).click().send_keys('Hello').perform()
                                            time.sleep(1)
                                            elem=locator.locate_by_xpath('.'+x.Reels().click_post_comment_button()[0])
                                            if elem:
                                                time.sleep(1)
                                                elem.click()
                                    if add_data.get('bookmark_posts_randomly'):
                                        pass
                                    if add_data.get('share_posts'):
                                        pass
                                    if add_data.get('like_posts_randomly'):
                                        pass
                                    if locator.locate_by_xpath(x.Reels().get_comment_title()):
                                        time.sleep(1)
                                        self.browser.send_command_key(locator.locate_by_xpath(x.Reels().get_comment_title()),key='enter')
                                        time.sleep(1)

                            
                            """                             for y in range(0,2):
                                elems[i].click() """
                            time.sleep(1)

                        except Exception as e:
                            pass
        def check_notifications(self,**kwargs):
            add_data=kwargs.get('add_data')
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
     
                locator.locate_by_xpath(xpath=x.Navigation().click_notifications_button(),click=True)   
        def check_messenger(self,**kwargs):
            add_data=kwargs.get('add_data')
            add_data={'open_messenger_on_new_messages':5,'reply_to_messages':False,'check_requests':False}
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
            
                time.sleep(2)

                if locator.locate_by_xpath(x.Navigation().check_has_new_messages()):
                        open_messenger=True
                else:
                    open_messenger=False
                if not add_data.get('open_messenger_on_new_messages_only'):
                    open_messenger=True
                if open_messenger:
                    elem=locator.locate_by_xpath(xpath=x.Navigation().click_messenger_button(),click=True)
                    time.sleep(2)
                    visited_posts=[]
                   
                time.sleep(1)

                chats=locator.locate_by_xpath(xpath=x.Messenger().iterate_through_chats(),elements=True)
                for chat in chats:
                    try:
                        if chat.find_element_by_xpath('.'+x.Messenger().is_chat_unread()[0]):
                            print('unread')
                    except Exception as e:
                        pass

                    else:
                        
                        chat.click()
                        time.sleep(2)

                        if locator.locate_by_xpath(x.Messenger().click_conversation_details_button(),click=True):
                            time.sleep(2)
                            pass
                        try:
                            elem=locator.locate_by_xpath(x.Messenger().focus_on_chat_area())
                            if elem:
                         
                                print(elem.find_element_by_xpath('.'+x.Messenger().get_username_of_recipient()[0]).get_attribute('href'))
                        except Exception as e:
                            pass
                            
                if add_data.get('check_requests'):        
                    elem=locator.locate_by_xpath(x.Messenger().get_new_requests())
                    for text in elem.text:
                        if text.isdigit():
                            elem.click()
            return True
        def send_dm(self,**kwargs):
            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs               
         
            i.storage_sense=self.storage_sense
            i.run()
        def watch_story(self,**kwargs):
            add_data=kwargs.get('add_data')
            add_data={'open_messenger_on_new_messages':5,'reply_to_messages':False,'check_requests':False}
            if kwargs.get('os')=='android':
                if kwargs.get('task_manager'):
                    return ['interact_with']
                from services.instagram.device.run_bot import Instagram
                i=Instagram()
                i.task=kwargs               
            
                i.storage_sense=self.storage_sense
                i.run()
            else:
                from services.instagram.locator import Locator
                logged_in=False
                locator=Locator()
                locator.browser=self.browser
                from services.instagram.xpaths import Xpaths
                x=Xpaths()
            
                time.sleep(2)
                self.browser.driver.get('https://www.instagram.com/')
                time.sleep(3)
                elems=locator.locate_by_xpath(x.HomePage().get_stories(),elements=True)
                import random
                
                elems[1].click()
                
                for i in range(0, 10):
                    stories=locator.locate_by_xpath(x.StoryPage().iterate_through_stories(),elements=True)
                    if not stories:
                        continue
                    for story in stories:
                       
                        if locator.locate_by_xpath(x.StoryPage().get_sponsored_text()):
                            print('Sponsored Story')
                            continue
                        elem=locator.locate_by_xpath(x.StoryPage().click_on_reply_to_story_text_area(),click=False)
                        elem=False
                        if elem:
                            
                            for word in 'hello':
                                time.sleep(0.1)
                                elem.send_keys(word)
                        locator.locate_by_xpath(x.StoryPage().click_send_reply_button(),click=True)
                        time.sleep(2)
                        """ locator.locate_by_xpath(x.StoryPage().click_like_story_button(),click=True)
                        locator.locate_by_xpath(x.StoryPage().click_like_story_button(),click=True) """
                        time.sleep(2)  
                        elemosa=locator.locate_by_xpath('//section',click=True)
                        self.browser.send_command_key(elemosa,'arrow_down')

                            
                        print('yeagf')
        def search_user_and_share_latest_post(self,**kwargs):
            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs               
         
            i.storage_sense=self.storage_sense
            i.run()

        def unfollow_users(self,**kwargs):
    
            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs               
         
            i.storage_sense=self.storage_sense
            i.run()
        def handle_bulktask(self,**kwargs):
            if kwargs.get('task_manager'):
                return ['interact_with']

            

            from services.instagram.device.run_bot import Instagram
            i=Instagram()
            i.task=kwargs               
         
            i.storage_sense=self.storage_sense
            i.run()