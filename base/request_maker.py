import requests
import random
import time
import os
import pickle
#from django.conf import settings
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import zipfile
import random as rd
import traceback
from base.datetime_utils import parse_date_time_string_or_object_and_localize_to_timezone

import logging
import uuid
import json
from json.decoder import JSONDecodeError
from base.storage_sense import Saver
import datetime as dt
from django.utils import timezone
class Request(object):
     
    def __init__(self):
        self.logged_in=False
        self.cookies = None  # type: str
        self.request_record=[{}]
        self.banned_end_points=[]
        self.use_proxies = ''#{'proxy_url':'jcamar:hurley92:52.128.222.109:29842','proxy_type':'rotating'}
        self.browser_proxies=None#{'proxy_url':'jcamar:hurley92:52.128.222.109:29842','proxy_type':'rotating'} # type: str
        self.ip_info=None
        self.session = None  # type: requests.Sessions
        self.error = None  # type: str
        self.auto_patch=True
        self.session_id=str(uuid.uuid1())
        self.rate_limited=False
        self.bypass_rate_limit=False
        self.end_point_banned=False
        self.request_counter=0
        self.localstore=True
        self.task=''
        self.workflow=''
        self.job=''
        self.save_full_output_in_log=False
        self.data_point=''
        self.auto_task_uuid=self.session_id
        self.username=''
        self.users=[]
        self.comments=[]
        self.follow_relations=[]
        self.parent_tweet=[]
        self.feed_tweets=[]
        self.t_lists=[]
        self.end_point=''
        self.max_scrape_count=None
        self.task_id=False
        self.response='sniffer'
        self.bypass_rate_limit=False
        self.service=''
        self.storage_sense=Saver()
        self.payload={}
        self.params={}
        self.run_id=False
    def initialize_logger(self):
        filename=self.session_id+'.log'
        if not self.base_path:
            base_path=os.getcwd()
        else:
            base_path=self.base_path
        filepath=os.path.join(base_path,'logs',filename)
        print(filepath)
        #logging.basicConfig(filename=filepath,format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',filemode='w')
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO) 
    def make_request(self,url,retry=0,r_type='get',params={},payload={},_json={},data={},error=None,end_point='',data_point='',**kwargs):      
        if not self.bypass_rate_limit:
            if end_point in self.banned_end_points:
                self.end_point_banned=True
                return {'status':'error'}          
        request_record={'datetime':timezone.now(),'request_record_type':'log','service':self.service}
        request_record.update({'end_point':end_point,'data_point':data_point,'url':url,'r_type':r_type})
        
        request_record.update({'bot_username':self.username})
        request_record.update({'task':self.task_id})
        request_record.update({'run_id':str(self.run_id) or False})
        request_record.update({'object_type':'request_record'})
        request_record.update({'logged_in':self.logged_in})
        for key,value in kwargs.items():
            request_record.update({key:value})
      
        try:
            if r_type=='get':
                if params:
                    self.params=params
                    request_record.update({'params':params})
                    
                    resp=self.session.get(url,params=params)   
                    self.response=resp
                    
                
                    #s.add_values_to_file()
                else:
                    resp=self.session.get(url)    
                    #print(resp.text)
                    self.response=resp   
               
            elif r_type=='post':
                if payload:
                    self.payload=payload
                    request_record.update({'payload':payload})
                    resp=self.session.post(url,data=payload) 
                    self.response=resp
                elif _json:
                    request_record.update({'json':_json})
                    resp=self.session.post(url,json=_json)
                    ##print(resp.text)
                    self.response=resp
            
            #self.logger.info(json.dumps(request_record))
                    
        except ConnectionResetError as e:
            error=e
            
        except TimeoutError as e:
            error=e
        except requests.exceptions.TooManyRedirects as e:
            error=e
        except requests.exceptions.RequestException as e:
            e=str(e)
            e+=' exit'
            error=e

        
        else:
            ##print('text'+str(self.response.text))
            ##print(_json)
            if resp.headers.get('content-encoding')=='zstd':
                import pyzstd
                s=Saver()
 
                data=pyzstd.decompress(resp._content)
                self.response._content=data
                resp._content=data
            self.request_counter+=1
            headers=resp.headers
            if headers.get('x-rate-limit-limit'):
                rate_limit_assigned_for_end_point=headers.get('x-rate-limit-limit')
                if rate_limit_assigned_for_end_point:
                    if headers.get('x-rate-limit-remaining'):
                        rate_limit_remaining=headers.get('x-rate-limit-remaining')
                        requests_consumed=int(rate_limit_assigned_for_end_point)-int(rate_limit_remaining)
                        if int(rate_limit_assigned_for_end_point)-int(requests_consumed)<10:
                            self.banned_end_points.append(end_point)
                            request_record.update({'banned':True})
                        else:
                            request_record.update({'banned':False})
                        request_record.update({ 'requests_remaining':rate_limit_remaining,'rate_limit_reset_time':headers.get('x-rate-limit-reset')})
                    else:
                        request_record.update({'rate-limit-assigned':rate_limit_assigned_for_end_point})
        proxy_request_record={}
        proxy_request_record.update(request_record)
        if self.use_proxies:
           
            proxy_request_record.pop('bot_username')
            """             proxy_type=self.use_proxies.get('proxy_type')
            if proxy_type=='static':
                ip_address=self.use_proxies['proxy_url'].split(':')[2]
                proxy=self.use_proxies['proxy_url']
                
            else:
                ip_address=self.use_proxies['proxy_url']
                proxy=self.use_proxies['proxy_url']      """                 
            request_record.update({'ip_address':self.use_proxies,'proxy':self.use_proxies})
            proxy_request_record.update({'ip_address':self.use_proxies,'proxy':self.use_proxies})
            from base.proxy_utils import get_current_ip
            #get_current_ip(self.session)
            if self.ip_info:
                request_record.update({'ip_info':self.ip_info})
                proxy_request_record.update({'ip_info':self.ip_info})
        else:
            proxy_request_record.update({'ip_address':'local'})
        if error:
            retry+=1
            request_record.update({'error':error})
            proxy_request_record.update({'error':error})
            if self.localstore:
               
                self.storage_sense.create_request_dump(data=request_record)
                self.storage_sense.create_proxy_dump(proxy_request_record)
               
              #self.logger.info(json.dumps(request_record))               
            else:
                pass
                #self.commons.save_third_party_api_request_record(request_record)
            if retry>10:
                raise SystemExit(error)
            elif 'exit' in error:
                return False
            else:
                return self.make_request(r_type=r_type,retry=retry,end_point=end_point,url=url,params=params,payload=payload,data=data,kwargs=kwargs,error=error)

        
        if self.save_full_output_in_log:
             request_record.update({'data':json.loads(resp.text)})
        else:
             request_record.update({'data':resp.text})
        if resp.status_code==200 or resp.status_code==201 :
            try:
                data={'status':'success','data':json.loads(resp.text)}
                request_record.update({'status_code':resp.status_code})
                proxy_request_record.update({'status_code':resp.status_code})
                
                if self.localstore:
                    self.storage_sense.create_task_outputs(self.task_id,data=request_record,block_name='request_records') 
                    self.storage_sense.create_request_dump(data=request_record)
                    self.storage_sense.create_proxy_dump(proxy_request_record)
                    #self.logger.info(json.dumps(request_record))        
                else:
                    pass
                    #self.commons.save_third_party_api_request_record(request_record)
                return data
                
            except JSONDecodeError as error:
                data={'status':'error','data':data,'error':error}
                request_record.update({'error':error})
                proxy_request_record.update({'error':error})
                if self.localstore:
                    if self.username:
                        
                        self.storage_sense.create_request_dump(data=request_record)
                    self.storage_sense.create_task_outputs(self.task_id,data=request_record,block_name='request_records')
                    self.storage_sense.create_proxy_dump(proxy_request_record)
                          
                else:
                    pass
                    #self.commons.save_third_party_api_request_record(request_record)
                
                return data
        
        else:
            if resp.status_code==429:
                request_record.update({'rate_limited':True,'requests_made':self.request_counter})
                proxy_request_record.update({'rate_limited':True,'requests_made':self.request_counter})
                self.rate_limited=True
            request_record.update({'status_code':resp.status_code})
            request_record.update({'error':error})
            proxy_request_record.update({'status_code':resp.status_code})
            proxy_request_record.update({'error':error})
            data={'status':'error'}
           
            proxy_request_record.update({'request':str(resp.request.__dict__),'response':str(resp.__dict__)})
            if self.localstore:
                self.storage_sense.create_task_outputs(self.task_id,data=request_record,block_name='request_records')
                self.storage_sense.create_request_dump(data=request_record)
                self.storage_sense.create_proxy_dump(proxy_request_record)  
            else:
                pass
                #self.commons.save_third_party_api_request_record(request_record)
            
            return data
    def initialize_request_session(self,use_cookies=False,use_proxies=False):
        self.session=requests.session()      
        if self.use_proxies:
            if len(self.use_proxies.split(':')) == 4:
                proxy_config = {
                    'http': 'http://%s:%s@%s:%s/' % tuple(self.use_proxies.split(':')),
                    #'https': 'https://%s:%s@%s:%s/' % tuple(self.use_proxies.split(':')),
                }
                use_proxies = proxy_config
            else:
                 use_proxies = {'http': 'http://'+self.use_proxies}
           
            self.session.proxies.update(use_proxies)    