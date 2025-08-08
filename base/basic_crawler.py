from base.parsers import Parser
import zipfile
import random as rd
import traceback
import json


from base.browser import Browser
from base.request_maker import Request
from base.recursion import Recursion
import logging

import time
import os
import pickle
import requests
import uuid
class Crawler:
    def __init__(self) -> None:
        self.user_agent=None
        self.driver=None
        self.scraping_resources_created=False
        self.use_proxies=None
        self.sniffed_data=None
        self.scraped_data=[]
        self.followers_data=[]
        self.posts_data=[]
        self.profiles_data=[]
      
        self.base_path=r'E:\scraping_automation_scripts\twitter_api_scraper'
     
        self.max_scrape_count=500
        self.user_data_dir=''
        self.scraping_resources_created=False
        self.use_cookies=False
    def initialize_logger(self):
        filename=self.session_id+'.log'
        if not self.base_path:
            base_path=os.getcwd()
        else:
            base_path=self.base_path
        filepath=os.path.join(base_path,'logs',filename)
        print(filepath)
        logging.basicConfig(filename=filepath,format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',filemode='w')
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO) 
    def initialize_request_session(self,use_cookies=False,use_proxies=False):
        self.session=requests.session()      
        if self.use_proxies:
            if len(self.use_proxies.split(':')) == 4:
                proxy_config = {
                    'http': 'http://%s:%s@%s:%s' % tuple(self.use_proxies.split(':')),
                    #'https': 'https://%s:%s@%s:%s/' % tuple(self.use_proxies.split(':')),
                }
                use_proxies = proxy_config
            else:
                 use_proxies = {'http': 'http://'+self.use_proxies}
        r=Request()
        r.use_proxies=self.use_proxies
        r.service=self.service_name
        r.task_id=self.task['id']
        r.run_id=self.task.get('run_id')
        self.session.proxies=use_proxies
        r.session=self.session   
     
        self.request_maker=r 
        self.make_request=r.make_request 
            #self.session.proxies.update(use_proxies)   
    def initialize_all_variables(self,**kwargs):
        from crawl.models import ChildBot
        c=ChildBot.objects.all().filter(username=kwargs.get('username'))
        if len(c)>0:
            c=c[0]
            self.use_proxies=c.proxy_url
        elif kwargs.get('add_data',{}).get('use_proxies'):
            self.use_proxies=kwargs.get('add_data',{}).get('use_proxies')
        if not self.scraping_resources_created:
            if self.driver:
                self.driver.close()
            browser=Browser()
            self.browser=browser
            self.browser.task=self.task
            self.browser.reporter=self.reporter
            if not self.use_proxies:
                
                self.browser.browser_proxies=self.use_proxies
            if c:
                if not self.user_data_dir:
                        from base.storage_sense import Saver
                        s=Saver()
                        
                        s.block={'address':'profiles.'+kwargs.get('profile')+'.browser'}
                        s.load_resources()
                        self.user_data_dir=os.path.join(s.block_address)
                if os.path.exists(self.user_data_dir):
                    pass
                else:
                    os.makedirs(self.user_data_dir)

                

    def create_scraping_resources(self,selenium_wire=False,url_to_capture_requests_from='',headers_dict={},request_identifier='',use_proxies=None,create_request_session=False):
        if not self.scraping_resources_created:
            browser=Browser()
            self.browser=browser
            
            if use_proxies:
                pass
                self.browser.browser_proxies=use_proxies
            if os.path.exists(self.user_data_dir):
                pass
            else:
                if not self.user_data_dir:
                    pass
                else:
                    os.makedirs(self.user_data_dir)
            browser.initialize_chrome_browser(mobile_emulation=False,user_data_dir=self.user_data_dir,selenium_wire=selenium_wire)
            self.driver=browser.driver
            #self.driver.response_interceptor=self.intercept_post_request_and_change_caption       
            
            if create_request_session:
                self.initialize_request_session(use_cookies=self.driver.get_cookies())      
                self.create_headers_and_cookies(headers_dict=headers_dict,request_identifiers=request_identifier,url_to_capture_requests_from=url_to_capture_requests_from)   
                r=Request()
                r.service=self.service_name
               
                r.session=self.session   
                self.request_maker=r 
                self.make_request=r.make_request
            
    def open_custom_browser(self,selenium_wire=False,headers_dict={},mobile_emulation=False,headless=False,incognito=False):
            self.browser.browser_proxies=self.use_proxies
            self.browser.initialize_chrome_browser(mobile_emulation=mobile_emulation,user_data_dir=self.user_data_dir,selenium_wire=selenium_wire,headless=headless,incognito=incognito)
            self.driver=self.browser.driver       
    def open_requests_session(self,headers_dict={}):

        self.initialize_request_session(use_cookies=self.driver.get_cookies())      
        
        r=Request()
        r.service=self.service_name
        
        r.session=self.session   
        self.request_maker=r 
        self.make_request=r.make_request
    def create_headers_and_cookies(self,url_to_capture_requests_from,headers_dict=[],request_identifiers=None):
        self.driver.get('https://www.instagram.com/explore/locations/212918601/grand-central-terminal/')
        time.sleep(5)
        self.headers=self.session.headers
        if headers_dict:
            self.create_headers(url_to_capture_requests_from,headers_dict)
        elif request_identifiers:
            self.copy_request_headers(request_identifiers)
        ##set a log over here
        if self.use_cookies:
            self.load_cookies()
        else:
            self.copy_cookies()
        self.scraping_resources_created=True
    def find_request_and_copy_headers(self,identifiers):
        for request in self.driver.requests:
            for identifier in identifiers:
                if identifier in request.url:
                    
                    for header in request.headers:
                      
                            self.session.headers.update({header:request.headers[header]})
                    return
    def find_request_and_return_response(self,identifiers):
        for request in self.driver.requests:
            for identifier in identifiers:
                if identifier in request.url:
                    
                   return request.response
    def find_request(self,identifiers,exclude_requests=[],exclude_params=[],wait_time=40):
        
        requests=[]
        if wait_time<=0:
            return requests
        while True:
            
            for request in self.driver.requests:
                for identifier in identifiers:
                    if identifier in request.url:
                        if request in requests:
                            pass
                        else:
                            if exclude_requests:
                                if request in exclude_requests:
                                    continue
                            if exclude_params:
                                if request.params in exclude_params:
                                    continue
                            elif request.response:
                                if request.response.body:
                                    requests.append(request)
    
            if len(requests)<=0:
                wait_time-=1
                time.sleep(1)

                return self.find_request(identifiers=identifiers,wait_time=wait_time,exclude_params=exclude_params,exclude_requests=exclude_requests)
            else:
            
                return requests
    def find_request_by_payload_variable(self,identifiers,variable_name,variable_value,use_latest=True,snifT=False,wait_time=40):
        try:
            requests=[]
            if wait_time<=0:
                return requests
            for request in self.driver.requests:
                for identifier in identifiers:
                    if identifier in request.url:
                       
                        if request.params.get(variable_name)==variable_value:
                            requests.append(request)
                            if snifT:
                                return request
                            break
            if len(requests)<=0:
                wait_time-=1
                time.sleep(1)
                return self.find_request_by_payload_variable(identifiers=identifiers,wait_time=wait_time,variable_name=variable_name,snifT=snifT,variable_value=variable_value)
            if len(requests)>0:
            
                if use_latest:
                    return requests[len(requests)-1]
                else:
                    return requests
        except Exception as e:
            return False

        return False
        
    def copy_request(self,request,**kwargs):
        from base.storage_sense import Saver
        payload=request.params
        headers=dict(request.headers)
        try:
            cookies=self.driver.get_cookies()  
        except Exception as e:
            print(e)
            cookies={}  
        data={'headers':dict(headers),'cookies':cookies,'payload':payload}
       
        s=Saver()
        s.service=self.service
        if kwargs.get('profile'):
            s.block={'address':'request_cache.'+str(kwargs.get('profile').replace('.',',')),'file_name':kwargs.get('data_point'),'data':data}
            s.overwrite=True
            s.add_values_to_file()
        
        
        s.block={'address':'request_cache','file_name':kwargs.get('data_point'),'data':data}
        s.overwrite=True
        s.add_values_to_file()          
    def copy_request_headers(self,request):
        for header in request.headers:

            self.session.headers.update({header:request.headers[header]})
        
        self.reporter.report_performance(**{
                                        'type':'create_request_headers_from_sniffed_request','task':self.task.get('uuid')
                                        })
        try:
            pass
            #self.copy_cookies()
        except Exception as e:
            print('failed to copy cokkies')
            pass
    def find_and_copy_request_headers(self,identifiers):
        for request in self.driver.requests:
            for identifier in identifiers:
                if identifier in request.url:
                    
                    for header in request.headers:

                            self.session.headers.update({header:request.headers[header]})
                    
        self.copy_cookies()


        
     
            
    def copy_cookies(self):   
         for cookie in self.driver.get_cookies():
                if cookie['name']=='urlgen':
                    pass
                else:
                    self.session.cookies.set(name=cookie['name'],value=cookie['value'])   
    def load_cookies(self):
        cookies = pickle.load(open(self.use_cookies, "rb"))
        for cookie in cookies:
            self.session.cookies.set(name=cookie['name'],value=cookie['value'])
    def create_headers(self,headers_dict):      
        extract_from_cookies={}
        acquire_headers=[]
        headers={

        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "scheme": "https",       
        "accept": "*/*",   
        "sec-ch-ua-platform": "Windows",
        "x-requested-with": "XMLHttpRequest",    
        }
        count=0
      
        self.scraping_resources_created=True

        for key, value in headers_dict.items():
           
            acquire_headers.append(key)
            
       
    
        for cookie in self.driver.get_cookies():
           
                    headers.update({key:cookie.get('value')})
      
        for request in self.driver.requests:
            for _header in acquire_headers:
                
                if request.headers.get(_header,False):
                    headers.update({_header:str(request.headers[_header])})
           #add breaking when all values have been acquired
           # if len(x_ig_www_claim)>1 & len(x_abs_id)>1 & len(x_ig_app_id)>1:
            #    break
        self.headers=headers
        self.session.headers.update(headers)
  
    def create_request_cache(self,**kwargs):
        
            if kwargs.get('from_request',False):
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'creating_request_cache','task':kwargs.get('uuid')
                                                })
            from base.storage_sense import Saver
            s=Saver()
            s.block={'address':'request_cache','file_name':kwargs.get('data_point')}
            s.load_block()
            s.open_file()

           
            self.create_headers(s.data_frame.to_dict(orient='records')[0]['headers'])
       
            for key,value in s.data_frame.to_dict(orient='records')[0].items():
                if key in self.session.headers:
                    pass
                else:
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                                                'type':'creating_request_cache_failed_headers_not_found','task':kwargs.get('uuid')
                                                })
            data={'headers':self.headers} 
            s.block={'address':'request_cache.'+str(kwargs.get('profile')).replace('.',','),'file_name':kwargs.get('data_point'),'data':data}
            s.load_block()
            s.open_file()
            s.overwrite=True
            s.add_values_to_file()  

            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'start',
                            'type':'created_request_cache','task':kwargs.get('uuid')
                            })
            return True
                

        
        