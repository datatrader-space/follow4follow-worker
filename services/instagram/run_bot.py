from base.basic_crawler import Crawler
from services.instagram.storage_sense import StorageSense
from base.extractors import SeoExtractors
from services.instagram.recursion import Recursion
from services.instagram.end_points import EndPoints
from services.instagram.concurrent_runner import ConcurrentRunner
from services.reports_manager.manager import Manager
import json
import time
import threading
import concurrent.futures


class Instagram(Crawler):
    def __init__(self):
        super().__init__()
        self.service='instagram'
        self.target_url = "https://www.instagram.com/p/CUDXXtFrV1P/?img_index=1"
        self.use_proxies = ""
        self.service_name = "instagram"
        self.seo_extractors = SeoExtractors()
        self.end_point = "user_info"
        self.data_point = ""
        self.username = None
        self.rest_id = None
        self.overwrite = False
        self.end_point_handler = EndPoints()
        self.end_point_handler.crawler=self
        self.concurrent_runner = ConcurrentRunner()
        self.crawl_attempts = 0
        self.max_crawl_attempts = 1
        self.request_identifiers = None
        self.create_requests_session = True
        self.task = {}
        self.reporter=Manager()
        self.storage_sense = StorageSense()
        self.storage_sense.service = "instagram"
        self.storage_sense.userId = "hamza"
    def check_for_request_cache(self,**kwargs):
       
        from base.storage_sense import Saver
        from base.request_maker import Request

        s=Saver()
        if kwargs.get('profile'):
            s.block={'address':'request_cache.'+str(kwargs.get('profile')).replace('.',','),'file_name':kwargs.get('data_point')}
            self.reporter.report_performance(**{
                                                    'type':'bot_request_cache_exists','bot_username':kwargs.get('profile'),'task':kwargs.get('uuid')
                                                    })
        else:
            s.block={'address':'request_cache','file_name':kwargs.get('data_point')}
            self.reporter.report_performance(**{
                                                    'type':'bot_request_cache_not_found','bot_username':kwargs.get('profile'),'task':kwargs.get('uuid')
                                                    })
        s.load_block()
        s.open_file()
        if s.data_frame.empty:
            return False
        data=s.data_frame.to_dict(orient='records',)[0]
     
        self.request_maker=Request()
        self.request_maker.task_id=self.task['uuid']
        self.request_maker.run_id=self.task['run_id']
        self.request_maker.service='instagram'
        self.request_maker.use_proxies=self.use_proxies
        self.request_maker.initialize_request_session()
        import ast
        if type(data['headers'])==str:
            try:
                headers=ast.literal_eval(data['headers'])
            except Exception as e:
                headers={}
        elif type(data['headers'])==dict:
            headers=data['headers']
        for key,value in headers.items():
            
            self.request_maker.session.headers.update({key:str(value)})
        
        self.reporter.report_performance(**{
                                                    'type':'created_new_request_header','task':kwargs.get('uuid')
                                                    })
        self.end_point_handler.request_maker=self.request_maker
        self.end_point_handler.make_request=self.request_maker.make_request
        kwargs.update({'payload':data.get('payload')})
        #kwargs.update({'data_point':'user_info_graphql'})
        kwargs.pop('initialize',False)
        resp=self.end_point_handler.get_required_data_point(**kwargs)
      
    
        if not resp:
            self.reporter.report_performance(**{
                                                    'type':'request_cache_inactive','task':kwargs.get('uuid')
                                                    })
            return False
          
        else:
            if kwargs.get('save',True):
                r=Recursion()
                r.reporter=self.reporter
                #data=r.save_parsed_response(resp,next_page_info=resp['next_page_info'],**kwargs)
                
            self.reporter.report_performance(**{
                                                    'type':'request_cache_active','task':kwargs.get('uuid')
                                                    })
            return True
        
    def start_sniffer(self,use_latest=True,snifT=False,**kwargs): 
        request_found=False
        counter=0
       
           
        data=kwargs
        if data.get('find_request_by_payload_variable',False):
            request_found=self.find_request_by_payload_variable(data['identifiers'],data['variable_name'],data['variable_value'],use_latest=use_latest,snifT=snifT)        
        else:
            request_found=self.find_request(data['identifiers'])
        if request_found:
        
            if type(request_found)==list:
                pass
            else:
                request_found=[request_found]
            for request in request_found:
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                    'type':'target_request_sniffed','task':kwargs.get('uuid')
                                                    })   
                if kwargs.get('from_request',False):
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                    'type':'create_request_headers_from_sniffed_request','task':kwargs.get('uuid')
                                                    }) 
                        
                    
                
                
                self.copy_request_headers(request)
                self.copy_request(request,save=True,**kwargs)
            return True
    def sniff_all_end_point(self,**kwargs):
        exclude=[]
        eps=[{'end_point':'user','data_point':'user_info_graphql'},
                 #{'end_point':'user','data_point':'user_followers'},
                 #{'end_point':'user','data_point':'user_following'},
                  {'end_point':'user','data_point':'user_posts'},
                  {'end_point':'location','data_point':'location_posts'},
                  {'end_point':'search','data_point':'search_keyword'},

                 

            ]
        while True:
            try:
                
                self.browser.driver.find_element_by_xpath('//,.')
            except Exception as e:
                if 'no such window' in str(e) or 'invalid session' in str(e):
                    print('window closed by user')
                    return 'success',''
                else:
                    pass
            
            
            for ep in eps:
                if ep in exclude:
                    continue
                ep.update({'initialize':True,})
                resp,data=self.end_point_handler.get_required_data_point(**ep)
                data.update({'profile':self.task['profile'],'data_point':ep['data_point']})
                try:
                    if self.start_sniffer(use_latest=False,snifT=True,**data):
                        print('sniffed request for'+str(ep['data_point']))
                        eps.remove(ep)
                        exclude.append(ep)
                except Exception as e:
                    pass
                if len(eps)==0:
                    return True

    def start(self,**kwargs):

        if self.scraping_resources_created:
            
            return True
        from crawl.models import ChildBot
        c=ChildBot.objects.all().filter(username=kwargs.get('profile'))
        if len(c)>0:
            c=c[0]
            self.use_proxies=c.proxy_url
        else:
            if kwargs.get('add_data').get('use_proxies'):
                
                self.use_proxies= kwargs.get('add_data').get('use_proxies')
           
        self.initialize_all_variables(**kwargs)    
       
        if kwargs.get('end_point')=='interact':
            if not kwargs.get('data_point')=='open_browser_profile':
                selenium_wire=True
            else:
                selenium_wire=True
        else:
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                            'type':'sniffer_turned_on','task_uuid':self.task['uuid']
                                            })
            selenium_wire=True
            
            if kwargs.get('data_point')=='condition_handler':
                kwargs.update({'save':False})
            if self.check_for_request_cache(**kwargs):
                self.scraping_resources_created=True
                return True
        self.browser.service=self.service_name
        self.browser.bot_username=self.task.get('profile')
        
        incognito=False
       
        self.open_custom_browser(selenium_wire=False,headless=self.task.get('headless'),mobile_emulation=self.task.get('mobile_emulation'),incognito=incognito)
        
        
        
        self.initialize_request_session()
        from services.instagram.locator import Locator
        locator=Locator()
        locator.reporter=self.reporter
        locator.browser=self.browser
        
        
        self.end_point_handler.browser=self.browser
        login_payload=kwargs.copy()
        if kwargs.get('data_point')=='open_browser_profile':
            self.sniff_all_end_point()
            return True
        if kwargs.get('data_point')=='user_info':
            pass
        else:
            login_payload.update({'end_point':'interact','data_point':'login'})            
            
            stat,resp=self.end_point_handler.get_required_data_point(**login_payload)    
            if resp=='no_profile':
                self.reporter.report_performance(**{
                                                'type':'missing_bot_profile','task':kwargs.get('uuid'),'bot_username':kwargs.get('profile')
                                                })
            else: 
                if not resp:
                    self.reporter.report_performance(**{
                                                'type':'failed_login','task':kwargs.get('uuid'),'bot_username':kwargs.get('profile')
                                                })  
                    return
                else:
                    self.reporter.report_performance(**{
                                                'type':'successful_login','bot_username':kwargs.get('profile'),'task':kwargs.get('uuid')
                                                })  
        if kwargs.get('end_point','')=='interact':
            return True 
        
        if kwargs.get('sniffer_mode',False):
            k=kwargs.copy()
            k.update({'data_point':'user_info','initialize':True})
            resp,data=self.end_point_handler.get_required_data_point(**k)  
            self.start_sniffer(**data)
        kwargs.update({'initialize':True})
        self.end_point_handler.request_maker=self.request_maker
        resp,data=self.end_point_handler.get_required_data_point(**kwargs)   
        
        if resp=='failed':
            self.driver.quit()
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'not_found_initialize_values_for_end_point','username':kwargs.get('profile'),'task':kwargs.get('uuid')
                                                })
         
            return
        self.browser.get(data['url'])
        _data=kwargs.copy()
        _data.update({'data':data})

        locator.browser=self.browser
        
        from services.instagram.xpaths import Xpaths
        x=Xpaths()
        if data.get('page'):
            self.reporter.report_performance(**{
                                                'type':'identifying_page','task':kwargs.get('uuid')
                                                })
            active_page = locator.identify_active_page(
                            page_locators_dict={
                                'LoginPage': x.LoginPage().get_username_input(),
                                'HomePage': x.Navigation().click_explore_button(),
                                'ProfilePage':x.ProfilePage().get_username()
                            },
                            max_retries=30,**kwargs
                        ) 
            self.reporter.report_performance(**{
                                                'type':'page_identified','task':kwargs.get('uuid')
                                                })
            if active_page==data['page']:   
                
                if data.get('new_content_touch_points'):      
                    load_new_content=locator.load_new_content_on_page(data['new_content_touch_points'],method='',max_tries=25,sleep_time=1)
                    if not load_new_content:
                        self.reporter.report_performance(**{
                                                'type':'failed_to_load_new_content_on_page','task':kwargs.get('uuid')
                                                })
                        return False  
        
        
        if kwargs.get('end_point')=='interact':
            self.end_point_handler.browser=self.browser
            return True  
        self.reporter.report_performance(**{
                                                'type':'sniffing_requests','task':kwargs.get('uuid')
                                                })
        if not data.get('from_request'):
            if not self.check_for_request_cache(**kwargs):
                if self.create_request_cache(**kwargs):
                    self.end_point_handler.request_maker = self.request_maker
                    self.end_point_handler.make_request = self.make_request
                    self.request_maker.username=kwargs.get('profile')
                    self.request_maker.service=self.service
                    self.request_maker.task_id = self.task.get("uuid", "someid")
                    self.request_maker.run_id=self.task.get('run_id')
                    
                    self.driver.close()
                    if self.check_for_request_cache(**kwargs):
                        
                        return True
                    self.scraping_resources_created=False
                    return False
                else:
                    self.scraping_resources_created=False
                    pass
        time.sleep(15)
        if data.get('find_request_by_payload_variable',False):
            request_found=self.find_request_by_payload_variable(data['identifiers'],data['variable_name'],data['variable_value'],use_latest=True)        
        else:
            request_found=self.find_request(data['identifiers'])
        if request_found:
            self.reporter.report_performance(**{
                                                'type':'finding_request','task':kwargs.get('uuid')
                                                })                
            if type(request_found)==list:
                for request in request_found:
                    if request.body:
                        break
            else:
                request=request_found
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'target_request_sniffed','task':kwargs.get('uuid')
                                                })   
            if data.get('from_request',False):
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'create_request_headers_from_sniffed_request','task':kwargs.get('uuid')
                                                }) 
                kwargs.pop('initialize')

               
            
            self.copy_request_headers(request)
            self.copy_request(request,save=True,**kwargs)
            self.end_point_handler.request_maker = self.request_maker
            self.end_point_handler.make_request = self.make_request
            self.request_maker.service = "instagram"
            self.request_maker.username=kwargs.get('profile')
            self.request_maker.run_id=self.task.get('run_id')
            self.request_maker.task_id = self.task.get("uuid", "someid")
            self.driver.close()           
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'copied_request_headers_from_sniffed_request','task':kwargs.get('uuid')
                                                }) 
            return True
        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                            'type':'request_not_found','task':kwargs.get('uuid')
                            })
        return False
       

    def crawl(self, **kwargs):
        self.selenium_wire = True
        self.crawl_attempts += 1
        if kwargs.get('os')=='browser':
            if kwargs.get("end_point") == "location":
                self.target_url = "https://www.instagram.com/explore/locations/212918601/grand-central-terminal/"
                self.request_identifiers = ["locations/web_info", "api"]
            
            elif kwargs.get("end_point") == "user":
                self.target_url = "https://www.instagram.com/antenox/"
                self.request_identifiers = ["web_profile_info", "graphql"]
            if  self.start(**kwargs):
                self.scraping_resources_created=True
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'crawl',
                                                    'type':'bot_started_successfully','task':kwargs.get('uuid')
                                                    }) 
                self.request_maker.username=self.task['profile']
                self.request_maker.run_id=self.task.get('run_id')
                self.request_maker.task_id=self.task['uuid']
                r = Recursion()
                r.service = self.service_name
                r.crawler = self
                r.end_point = kwargs.get("end_point")
                r.data_point = kwargs.get("data_point")
                
                r.storage_sense = self.storage_sense
                self.end_point_handler.register_assistant.storage_sense = self.storage_sense
                self.end_point_handler.user_data_dir=self.user_data_dir
                self.end_point_handler.use_proxies=self.use_proxies
                self.end_point_handler.reports_manager=self.reporter
                r.crawler=self
                r.reporter=self.reporter
                r.max_crawls=self.max_crawl_attempts
                r.recursive_api_caller(**kwargs)
                from base.storage_sense import Saver
                import requests
            

                if r.stop_condition_satisfied:  # and r.check_condition_satisified:
                    return "success"
                    

    def perform(self, **kwargs):
        if kwargs.get('os')=='browser':
            self.selenium_wire = False
            self.create_requests_session = False
            self.request_identifiers = []
            self.target_url = "https://www.instagram.com/"
            start_resp = self.start(**kwargs)   # <- capture the start response

            # If caller only wants the login datapoint, stop here.
            if str(kwargs.get('data_point', '')).lower() == 'login':
                return start_resp
   
            self.crawl_attempts += 1
            self.end_point_handler.browser = self.browser
            return self.end_point_handler.get_required_data_point(**kwargs)
        elif kwargs.get('os')=='android':


            self.crawl_attempts += 1
            return self.end_point_handler.get_required_data_point(**kwargs)
        else:
            if  kwargs.get('data_point')=='feed_post':
                kwargs['os']='android'
                return self.perform(**kwargs)

    def get_followers(self):
        self.end_point = "user_info"
        data = self.retrieve_data()
        if data:
            rest_id = data["rest_id"]
            self.rest_id = rest_id
        self.end_point = "user_followers"
        data = self.retrieve_data()

    def serve_user_query(self,**query):
        # self.output.write('Serving User Query Now')
        self.crawl_attempts += 1
        
        if not query.get('retrieve'):   
            if self.crawl_attempts > self.max_crawl_attempts:
                print(
                    "Max Crawl Attempts Exceeded. Stopping and Saving report. Updating the task manager register."
                )
                return
        e = self.end_point_handler
        e.end_point = self.end_point
        e.data_point = self.data_point
        e.storage_sense = self.storage_sense
        self.end_point_handler.proxies=self.use_proxies
        if query.get('retrieve'):
            
            query.update({'retrieve':True})
            #update query              
              ##if file is not empty, and user has specified to scrape, start crawling
            if query.get("scrape"):
                
                _=query.copy()
                _.update({'retrieve':False})
                self.crawl(**_)
                query.pop('scrape')
                return self.serve_user_query(**query)
            else:
                
                status, resp = e.get_required_data_point(**query)
         
                if status == "success":  ##if file is empty
                    if type(resp) == list:   #if response is dict, i.e. some additonal request keys has been passed from end -point, update 
                        
                        #query["retrieve"] = False
                        query.update({'retrieve':False,'items':False})
                        #th=threading.Thread(self.crawl(**query))
                        #th.start()
                        return status,resp
                    
                
        else:
           
            self.crawl(**query)
            return 'success',{}
            #query.pop('scrape',)
            



            
        
    def perform_action(self, **action):
        
        if not self.crawl_attempts>=self.max_crawl_attempts:
            resp=self.perform(**action)
            

               
            return {'sucess',True}
            

        print('Add Task Failed Exception along with Retries here.')
    def run_bot(self, query):
        # self.output.write('Instagram Bot Started for Task')
        

        self.storage_sense.change_state_of_task(task=query,state='running')
        from crawl.models import Task
        task=Task.objects.all().filter(id=self.task['id'])
        
        if task:
            task=task[0]
            if task.profile:
                if task.check_job_request_limits():
                    if task.check_task_request_limits():
                        pass
                    else:
                        pass
                else:
                    print('job limit exceeded')
                    return False
        if not self.task.get('add_data'):
            self.task['add_data']={}
        self.reporter.task=task
        self.reporter.task_id=task.uuid
        self.reporter.run_id=self.task.get('run_id',1231)   
        self.reporter.service='instagram'
        self.end_point_handler.reporter=self.reporter        
        if self.task.get("profile"):
            
            profile=self.task.get('profile')
            
            import os
            pth=os.path.join(os.getcwd(),'resources','profiles',self.service_name,profile,'browser')
            self.user_data_dir=pth
            if self.task.get("proxy", False):
                self.use_proxies = self.task.get('proxy')
        if self.task.get("end_point") == "interact":
            if query.get('profile',{}):
                pass
            else:
                raise Exception("NoProfileResourceProvided")
            if self.task.get('add_data',False):
                if self.task.get('add_data').get('data_source'):
                    data_source=self.task.get('add_data').get('data_source',[])
                    for source in data_source:
                        if source['type']=='data_house':
                            
                            from base.datahouse_client import DataHouseClient
                            d=DataHouseClient()
                            d.request_maker.task_id=query.get('uuid')
                            d.request_maker.run_id=query.get('run_id')
                            inputs=d.retrieve(object_type=source['object_type'],lock_results=source['lock_results'],filters=source['filters'],size=source['size'])
                            if inputs:
                                for profile in inputs['data']:                           
                                    queries.append({'user_info':{'username':profile.get('username'),'rest_id':profile.get('rest_id')}}) 
                        elif source['type']=='task':
                                from base.storage_sense import Saver
                                s=Saver()
                                exclude_blocks=s.get_consumed_blocks(id=self.task.get('uuid'))
                                if source['identifier']=='self':
                                    identifier=self.task.get('uuid')
                                else:
                                    identifier=source['identifier']

                                resp=s.read_task_inputs(exclude_blocks=exclude_blocks,uuid=self.task.get('uuid'),keys=True,block_name=source.get('block_name'))                            
                                targets=[]
                                for key, value in resp.items():
                                    
                                    for row in value:
                                        if not row.get('username'):
                                            continue
                                        if row.get('username') in exclude_blocks:
                                            continue
                                        targets.append(row)
                                    if len(targets)>self.task.get('add_data',{}).get('max_size',10):
                                        break
                    self.task.update({'targets':targets})
            if self.task.get('data_point')=='search_user_and_interact':
                from services.resource_manager.manager import Manager
                m=Manager()
                #task=m.allocate(**{'service':'instagram','resources':['targets'],'task':self.task})
           
            """
            Runs a command in a subprocess and terminates it after a specified wait time.

            Args:
                command (str): The command to run.
                wait_time (int): The number of seconds to wait before terminating the subprocess.
            """
            pid=False
            try:
                # Start the subprocess
                directory=r'E:\darrxscale\scrcpy-win64-v2.5\scrcpy-win64-v2.5'
                command="scrcpy -s "+query.get('device')+" --no-audio"
                full_command = f"cd /D {directory} & {command}"
                
                #process = subprocess.Popen(full_command, shell=True)
                #pid = process.pid
            except Exception as e:
          
                pass
            try:
                resp,data=self.perform_action(**query)
            except Exception as e:
                import traceback
                err=traceback.format_exc()
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':self.task.get('data_point'),
                                                'type':'exception','username':self.task.get('profile'),'task':self.task.get('uuid'),
                                                'string':{'name':'UnknownException','args':str(e)},
                                                'traceback':err
                                                })
                exception=True
            else:
                exception=False
                resp,data='success',True
            try:
                if pid:
                    import psutil
                    parent_process = psutil.Process(pid)
                    for child_process in parent_process.children(recursive=True):
                        child_process.kill()
                    parent_process.kill()

                    print(f"Terminated Scrcpy subprocess with PID {pid}")
            except Exception as e:
                pass
            if exception:
                try:
                    self.driver.quit()
                except Exception as e:
                    pass
                raise Exception('TaskFailed')
        else:
            if query.get('profile',{}):
                if task.check_bot_request_limits():
                            self.max_crawl_attempts=task.calculate_fair_share()
                else:
                    print('Max Requests Exceeded for the bot for today for Scrape Task')
                  
                    
            add_data=query.get('add_data')
            queries=[]
            data_house=False
            if add_data.get('data_source'):
        
                data_source=add_data.get('data_source')
                data_house=True
                for source in data_source:
                    if source['type']=='data_house':
                        
                        from base.datahouse_client import DataHouseClient
                        d=DataHouseClient()
                        d.request_maker.task_id=query.get('uuid')
                        d.request_maker.run_id=query.get('run_id')
                        inputs=d.retrieve(object_type=source['object_type'],lock_results=source['lock_results'],filters=source['filters'],size=source['size'])
                        if inputs:
                            for profile in inputs['data']:                           
                                queries.append({'user_info':{'username':profile.get('username'),'rest_id':profile.get('rest_id')}}) 
                    elif source['type']=='task':
                            from base.storage_sense import Saver
                            s=Saver()
                            exclude_blocks=s.get_consumed_blocks(id=self.task.get('uuid'))
                            resp=s.read_task_outputs(exclude_blocks=exclude_blocks,uuid=source.get('identifier'),keys=True,block_name=source.get('block_name'))                            
                            queries=[]
                            for key, value in resp.items():
                                
                                for row in value:
                                    if not row.get('username'):
                                        continue
                                    if row.get('username') in exclude_blocks:
                                        continue
                                    queries.append(row)
                                if len(queries)>self.task.get('add_data',{}).get('max_size',10):
                                    break
            """             if query['data_point']=='condition_handler':
                query.update({'initialize':True})
                resp,data=self.end_point_handler.get_required_data_point(**query)
                if resp=='success':
                    if 'data_points' in data.keys():
                        for data_point in data.get('data_points',{}):
                            if data_point.get('payload_variations',[]):
                                for payload in data_point.get('payload_variations',[]):
                                    _={}
                                    _=query.copy()
                                    for variation in payload.get('variations'):
                                        _.update({variation['name']:variation['value']})
                                    _.update({'data_point':data_point['name'],'initialize':False,
                                              'response_key':payload.get('response_key'),'items':payload['items'],
                                              'max_crawls':payload.get('max_crawls')
                                              
                                              
                                      })
                                    queries.append(_)
            else:
                 """
            if not data_house:
                    queries.append(query)
            #for i in range(0,100):
             #   for q in query.get('username'):
               #     _.update({'username':q})
            data_inputs={}
            for _ in queries:
                if _.get('end_point')=='location':
                    if _.get('data_point')=='location_posts':
                        if _.get('input'):
                            _.update({'location_info':{'id':_.get('input')}})
                           
                        else:
                            if add_data.get('data_source')=='data_house':
                                _.update(self.task)
                            else:
                                return 'Input None'
                if _.get('end_point')=='search':
                    if _.get('data_point')=='search_keyword':
                        if _.get('input'):
                            _.update({'keyword':_.get('input')})
                           
                        else:
                          
                            if add_data.get('data_source')=='data_house':
                                _.update(self.task)
                            else:
                                return 'Input None'
                elif _.get('end_point')=='user':
                    if _.get('data_point')=='user_followers':
                        if _.get('input'):
                            _.update({'user_info':{'username':_.get('input'),'rest_id':add_data.get('rest_id')}})
                        else:
                            if add_data.get('data_source')=='data_house':
                                _.update(query)   
                    if _.get('data_point')=='user_info' or _.get('data_point')=='user_info_graphql':
                       
                        
                        if _.get('input'):
                            _.update({'user_info':{'username':_.get('input'),'rest_id':add_data.get('rest_id')}})
                        else:
                            if add_data.get('data_source')=='data_house':
                                _.update(query)
                          
                    if _.get('data_point')=='user_posts':
                        if _.get('input'):
                            _.update({'user_info':{'username':_.get('input')}})
                        else:
                            if add_data.get('data_source')=='data_house':
                                _.update(query)
                            
               
                if data_house:
                    
                    _.update(self.task)
                self.crawl_attempts=0
                if self.task.get('data_point')=='user_info_graphql':
                    from services.instagram.usabe_funcs_for_business_no_bs import get_bulk_user_info_with_browser
                    return get_bulk_user_info_with_browser(self.task,[_])
                if self.task.get('data_point')=='bulk_user_info_scraper':
                    from services.instagram.usabe_funcs_for_business_no_bs import get_single_user_info_with_browser
                    max_scrapes=0
                    x=0
              
                    num_threads=self.task.get('add_data',{}).get('max_threads',1)
                    while max_scrapes<50:
                        for i in range(0,num_threads):
                            if x>=len(queries):
                                return True
                            row=queries[x]
                            threading.Thread(target=get_single_user_info_with_browser,args=(row['username'],self.task)).start()
                            x+=1
                            max_scrapes+=1
                        time.sleep(60)


                    



                    
                    
                else:
                    try:
                        resp,data=self.serve_user_query(**_)
                    
                    except Exception as e:
                        import traceback
                        _['run_id']=str(_['run_id'])
                        self.reporter.report_performance(**{
                                                    'type':'exception','string':e,'traceback':traceback.format_exc(),
                                                    
                                                    'task':self.task.get('uuid'),
                                                    'is_error':True,
                                                    'query':_

                                                    })
                    else:
                        #print(data)
                        if query.get('data_point')=='condition_handler':
                            data_inputs.update({_['response_key']:data})
            if query.get('data_point')=='condition_handler':
                query.update(data_inputs)
                query['initialize']=False
                resp,data=self.end_point_handler.get_required_data_point(**query)      
                if resp:
                    if self.task:
                        from crawl.models import Task
                        task=Task.objects.all().filter(uuid=self.task['uuid'])
                        if task:
                            task=task[0]
                            task.status='completed'
                            task.save()
                            if len(task.dependents.all())>0:
                                for task in task.dependents.all():
                                    if not task.status=='running':
                                        task.status='pending'
                                        task.save()
                    return True
                            
                
        try:
            self.driver.quit()
        except Exception as e:
            pass
       
 
        
                    
            
            
            #_.update({'retrieve':True,'items':'users'})
            #resp,data=self.serve_user_query(retrieve=True,**_)




        # self.output.write('Storage Sense Initialized Successfully')
    
    def task_creation_logic(self,**job):
       
        if self.check_if_task_points_are_handled(job):
            input=job.get('input')
            job.update({'task_manager_info':True})
            info=self.end_point_handler.get_required_data_point(**job)
            required_keys=info
            
            #now figure out the required key for the task input
            for key,value in input.items():
                if key in required_keys:
                    required_keys.remove(key)
            if len(required_keys)!=0:
                return 'missing_required_keys'
            
            for key in info:
                _={}
                _.update({'key':input[key]})
        else:
            return 'error'
      
    def check_if_task_points_are_handled(self,job):
        implemented_task_points={
            'location':['search_location','get_details_about_location','country_directory',
                        'city_directory','location_directory','location_info','location_posts',
                        'get_conversation_details'
                        ],
            'hashtag':['search_hashtags'],
            'user':['search_user','user_info','user_followers','user_followings'],
            'interact':['login']


        }

        if job.get('end_point') in list(implemented_task_points.keys()):
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                  'type':'unhandled_end_point','end_point':job.get('end_point'),'job_service':job.get('service')
                                                                  ,'job':job
                                                                  
                                                                  })
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                  'type':'task_creation_failed_for_job','reason':'unhandled_end_point','job_service':job.get('service'),
                                                                  'job':job
                                                                  
                                                                  })
        else:
            return False
        if job.get('data_point') in list(implemented_task_points[job.get('end_point')]):
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                'type':'unhandled_google_data_point','end_point':job.get('end_point'),'job':job                                                            
                                                                })
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                'type':'task_creation_failed_for_job','reason':'unhandled_data_point','job_service':job.get('service'),
                                                'job':job
                                                
                                                })
            return True
        else:
            return False
        
import uuid         
query=    {
    "id":100,
        "service": "instagram",
        "os": "browser",
       
        "interact": False,
        "end_point": "interact",
        "data_point":"login",
        "targets":[],#["google_sheet__https://docs.google.com/spreadsheets/d/1DKc--qQiFvqJ0BT6A-HHI2tcORClZWO5Pk4V5LFLdUA/edit?gid=1464461431#gid=14644614310"],
 
  
       
        #"user_info":{"username":"juliancamarena"},
    
        "input":'sajid',
       
   
        "add_data":{"block_name": "users", #"data_source": [{"type": "task", "block_name": "users", "identifier": "a79064af-3291-11f0-b95b-b81ea4842696"}], "max_threads": 5, "use_proxies": "f2wSTy0:8CR2Iiyr2lbfM72:us4.4g.iproyal.com:7488","watch_story":True,#"follow_target":True,
                    #"send_reachout_message":True,
                    "reporting_house_url":"192.168.1.106:82/",
                    "messaging":{'values':['Congrats']},
                    "country_slug":"US",
                    "directory_code":"US",
                    "city_slug":"downtown-pennquarter-chinatown-united-states",
                    "city_code":"c2753900"
                    #"data_source": [{"size": 5, "type": "task", "identifier":"self"}], "save_to_storage_house": True
        },
    
        
        "profile":"edward_tiktok_ecomm_boom",
        
        "uuid": "cc523176-31ad-11f0-92b6-047c1611323a",
        "run_id":uuid.uuid1(),
        "last_state_changed_at": None,
        "status": "pending",
        "device": 'NMNA2J0191 ',
        'ref_id':1,
        #'sniffer_mode':True,
    }

i=Instagram()
i.task=query
""" i.run_bot(query)
dicto=query.copy()
from services.reports_manager.endpoints import EndPoints
e=EndPoints()
# e.Instagaram().create_run_report(**task)
e.Instagaram().create_run_log_report(**query)
if query.get('add_data',{}).get('reporting_house_url'):
    dicto['add_data'].update({'data_source':[{'type':'task','identifier':query['uuid'],'block_name':'reports'}
                                                                    
                                                                    
                                                                    ],'client_url': query.get('add_data',{}).get('reporting_house_url')})
    
    from services.datahouse.end_points import EndPoints
    e=EndPoints()
    e.update().send_update_to_client_latest(**dicto) """