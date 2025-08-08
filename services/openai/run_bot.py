
from base.storage_sense import Saver
from services.reports_manager.manager import Manager
import json
import time
import threading
import concurrent.futures


class OpenAi():
    def __init__(self):
        super().__init__()

        
        self.end_point = "user_info"
        self.data_point = ""
        self.task = {}
        self.reporter=Manager()
        self.storage_sense = Saver()
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
        
        from services.openai.end_points import EndPoints
        e=EndPoints()
        e.reporter=self.reporter
        resp=e.get_required_data_point(**task)
        return resp

       






