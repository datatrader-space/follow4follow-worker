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
from services.data_enricher.end_points import EndPoints

class DataEnricher():
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
    
    
    def run_bot(self, task):
        
        from services.data_enricher.end_points import EndPoints
        e=EndPoints()
        resp=e.get_required_data_point(**task)
        print(resp)

       

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
      

task=_={'service':'enricher',
                    'ref_id':1,
                    'end_point':"Enrich",
                    'data_point':'enrich',
                    'add_data':{'data_source':[{'type':'task','identifier':'0db96f37-c838-11ef-bc28-047c1611323a'}],
                                'service':'openai',
                                'columns':['nickname','uniqueId'],
                                'prompt': "For the name {nickname} and username {uniqueId}, provide the following details:\n" \
                 "1. Type (e.g., Person, Brand, etc.)\n" \
                 "2. Gender (if it's a person's name)\n" \
                 "3. Country of origin or association\n\n\
                and follow this strictly."\
                "Try to provide the details based on their names and also don't focus on any special characters or icons in the name"\
                "Try to provide the details regarding country and gender while focusing on the name and not focusing on icons in the name."\
                "If you don't have any information, just keep the fields empty, please.",
                                'output_column_names':['country','gender','type'],

                        'save_to_googlesheet':True,
                        'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1lTmrDMt4Z5HR7-zK2crpke71FQ81EZOZpua-vNsi23g/edit?gid=1586039951#gid=1586039951'
                        ,'worksheet_name':'test'
                                                    

                    },
                    'uuid':str(1)
}
task=_={'service':'enricher',
                    'ref_id':1,
                    'end_point':"enrich",
                    'data_point':'enrich_social_media_profile',
                    'add_data':{"block_name": "users", "data_source": [{"type": "data_house",
                                                                         "filters": {"service": "instagram", "gender.exact": "Female",
                                                                                      "task_uuid.in": "c04630e7-29c0-11f0-865c-047c1611323a",
                                                                                        "country.exact": "France", "post_count.gte": 10, "followers_count.lte": 3000,
                                                                                          "followings_count.lte": 1000}, 
                                                                                          "object_type": "profile", "lock_results": False}]},

                    'uuid':'64dd591f-2b55-11f0-9bbf-047c1611323a',
}
d=DataEnricher()
#d.run_bot(task)
""" prompt = f"For the name'{item['name']}', provide the following details:\n" \
                 "1. Type (e.g., Person, Brand, etc.)\n" \
                 "2. Gender (if it's a person's name)\n" \
                 "3. Country of origin or association\n\n" \
                 "Return the response in this format: {'Type': '...', 'Gender': '...', 'Country': '...'} and follow this strictly."\
                "Try to provide the details based on their names and also don't focus on any special characters or icons in the name"\
                "Try to provide the details regarding country and gender while focusing on the name and not focusing on icons in the name."\
                "If you don't have any information, just keep the fields empty, please."
                # gender = random.choice(genders)
                # type_ = random.choice(types)
                # country = random.choice(countries) """