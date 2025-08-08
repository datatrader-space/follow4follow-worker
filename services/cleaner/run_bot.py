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


class Cleaner():
    def __init__(self):
        super().__init__()

        self.seo_extractors = SeoExtractors()
        self.end_point = "user_info"
        self.data_point = ""
        self.task = {}
        self.reporter=Manager()
        self.storage_sense = StorageSense()
        self.storage_sense.service = "instagram"
        self.storage_sense.userId = "hamza"
    
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
                print(type(resp))
                if status == "success":  ##if file is empty
                    if type(resp) == list:   #if response is dict, i.e. some additonal request keys has been passed from end -point, update 
                        
                        #query["retrieve"] = False
                        query.update({'retrieve':False,'items':False})
                        #th=threading.Thread(self.crawl(**query))
                        #th.start()
                        return status,resp
                    
                
        else:
           
            self.crawl(**query)
            #query.pop('scrape',)
            return self.serve_user_query(**query)

    def run_bot(self, task):
        
        from services.cleaner.end_points import EndPoints
        e=EndPoints()
        resp=e.get_required_data_point(**task)
        return resp

       

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
      
task={'service':'cleaner',
      'end_point':'Instagram',
      'data_point':'clean_user_followers',
    'uuid':'799f6c6e-bf91-11ef-9a3e-047c1611323a',
    'add_data':{"data_source": [{"type": "task", "identifier": "af1516cc-bf90-11ef-a9c9-047c1611323a"}],
                "save_to_googlesheet":True,
                   "fields_to_compare": [{"key": "username", "value": "str"}, 
                                        
                                         {"key": "is_private", "value": False}], 
                                         "check_for_presence_of": [{"key": "check_profile_picture", "value": "1232131231"}, {"key": "check_bio", "value": "fan"}]}}

c=Cleaner()
c.run_bot(task)
""" task={'service':'cleaner',
      'end_point':'Instagram',
      'data_point':'clean_user_followers',
      'add_data':{'data_source':[{'type':'task','identifier':'7b27e47f-6c48-11ef-9d8b-74563c02f7f7'},
                                #{'type':'storage_block','identifier':'dancingtheearth','service':'instagram'},
                                #{'type':'data_point','service':'instagram','identifier':'user_followers','end_point':'user',
                                 # 'input':'dancingtheearth'},
                                #{'type':'google_sheet','link':'somelink'}                         
                                 ],
        'fields_to_compare':[{'key':'is_private','value':False},
                                    {'key':'rest_id','value':int}
                                    
                            ],
        'check_for_presence_of':[
                        {
                            "key":"profile_picture",
                            "value":"44884218_345707102882519",

                           
                        }],
        'save_to_googlesheet':False#'https://docs.google.com/spreadsheets/d/1wTVLDWlmfTTnkrltx1iBUppJ5J_9EBYuCVXa59mhaVM/edit?gid=0#gid=0'
        
                                    

      },
      'uuid':123123
      }
 """

