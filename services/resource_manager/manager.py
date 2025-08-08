

from services.resource_manager.endpoints import EndPoints
class Manager:
    def __init__(self):
        self.task=None
        self.end_points_handler=EndPoints()
    def perform(self,task):
            self.task=task
            self.end_points_handler.task=self.task
            return self.end_points_handler.get_required_data_point(**task)
    def allocate(self,**kwargs):
         if kwargs.get('task'):
            
              kwargs.update({'end_point':'allocate','data_point':'allocate_resources_to_task_db'})
              return self.perform(kwargs)
    def update(self,**kwargs):
        if kwargs.get('register',False):
            kwargs.update({'end_point':'update','data_point':'register'})
            return self.perform(kwargs)
    def task_creation_logic(self,job):
        if self.check_if_task_points_are_handled(job):
            input=job.get('input')
            job.update({'task_manager_info':True})
            info=self.end_points_handler.get_required_data_point(**job)
            required_keys=info.copy()
            
            #now figure out the required key for the task input
            for key,value in input.items():
                if key in required_keys:
                    required_keys.remove(key)
            if len(required_keys)!=0:
                return 'missing_required_keys'
            
            for key in info:
                _={}
                _.update({key:input[key]})
            self.reports_manager.report_performance(**{'service':'resource_manager','end_point':job.get('end_point'),
                                                     'data_point':job.get('data_point'),'type':'assigned_input','job':job,
                                                     'input':_})
            return _
    def check_if_task_points_are_handled(self,job):
        implemented_task_points={
            'create':['profile','proxy','device',
                        'ec2instance','server','from_google_sheet'
                     ],
            'allocate':['allocate_resources_to_task'],
            'update':['register'],
            'assign':['proxy','device'],
            'sync':['with_google_sheet']


        }

        if not job.get('end_point') in list(implemented_task_points.keys()):
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                  'type':'unhandled_end_point','end_point':job.get('end_point'),'job_service':job.get('service')
                                                                  ,'job':job
                                                                  
                                                                  })
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                  'type':'task_creation_failed_for_job','reason':'unhandled_end_point','job_service':job.get('service'),
                                                                  'job':job
                                                                  
                                                                  })
            return False
        else:
            return True
        if not job.get('data_point') in list(implemented_task_points[job.get('end_point')]):
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                                'type':'unhandled_google_data_point','end_point':job.get('end_point')                                                            
                                                                })
            self.reports_manager.report_unhandled_scenario(**{'service':'workflow','end_point':'workflow_creator','data_point':'create_tasks_for_job',
                                                'type':'task_creation_failed_for_job','reason':'unhandled_data_point','job_service':job.get('service'),
                                                'job':job
                                                
                                                })
            return False
        else:
            return True

query= {
            "service": "instagram",
            "end_point": "location",
            "data_point": "location_posts",
            "max_interactions":5,
            "targets":[{'location':[{'slug':'cave-creek-arizona',"id":"213190018"}]}],
            "items":["users"],
            "search_query":"arizona",
            "username":["jwinterpa","juliancamarena"],
            "rest_id":"3771546820",
            "location_info":{"slug":"cave-creek-arizona","id":"213190018"},
            "os": "chrome",
            "bot": "camarena_artss",
            "job": "login_profiles_on_browsers",
            "workflow": "campaign_1",
            "resources": {
                "profile": {
                    "service": "instagram",
                    "username": "camarena_artss",
                    "status": "",
                    "password": "lofa@1",
                    "device_serial_number": "ZY22F82FWS",
                    "device_proxy": "",
                    "email_address": "",
                    "logged_in": False,
                    "available": False,
                    "task_id": "603d0f83-9f25-11ee-8e6c-74563c02f7f7",
                    "type": "profile"
                },
                "proxy": {
                    "usage_count_by_service": 0,
                    "ip": "154.13.200.125",
                    "port": 29842,
                    "username": "jcamar",
                    "password": "hurley92",
                    "country": "USA",
                    "area": "IL",
                    "location": "Chicago",
                    "plan_id": 361242,
                    "status": "online",
                    "url": "jcamar:hurley92:154.13.200.125:29842",
                    "type": "proxy",
                    "proxy_protocol": "http",
                    "max_intra_service_proxy_sharing": 3,
                    "max_concurrent_threads": 10,
                    "task_id": "603d0f83-9f25-11ee-8e6c-74563c02f7f7"
                }
            },
            "input": "login_profiles_on_browsers",
            "query": "juliancamarena",
            "id": "17094db5-9f31-11ee-948a-74563c02f7f7",
            "interact_with":"juliancamarena"
        }     
task= {
        "spreadsheet_url": "https://docs.google.com/spreadsheets/d/1DKc--qQiFvqJ0BT6A-HHI2tcORClZWO5Pk4V5LFLdUA/edit?gid=1464461431#gid=1464461431",
        "service": "resource_manager",
        "end_point": "create",
        "data_point": "from_google_sheet",
        "task":query,
        "input": {
            "spreadsheet_url": "https://docs.google.com/spreadsheets/d/11FBz_1nqDk3aN93R_sR6_chWvUb0DuggYsrVWZqViaA/edit#gid=1116455646"
        },
        "slug": "create_resources_from_google_sheet",
        "repeat": 30,
        "workflow": "campaign_1",
        "id": "bd4d0ddd-99e2-11ee-8466-74563c02f7f7"
    }
#im""" port json

#p=Manager()
#p.perform(task) 

""" task= {
        "spreadsheet_url": "https://docs.google.com/spreadsheets/d/11FBz_1nqDk3aN93R_sR6_chWvUb0DuggYsrVWZqViaA/edit#gid=1116455646",
        "service": "resource_manager",
        "end_point": "sync",
        "data_point": "with_google_sheet",
        "input": {
            "spreadsheet_url": "https://docs.google.com/spreadsheets/d/11FBz_1nqDk3aN93R_sR6_chWvUb0DuggYsrVWZqViaA/edit#gid=1116455646"
        },
        "slug": "create_resources_from_google_sheet",
        "repeat": 30,
        "workflow": "campaign_1",
        "id": "bd4d0ddd-99e2-11ee-8466-74563c02f7f7"
    }
 """
p=Manager()
#p.perform(task) 


'''if job.get('end_point')=='create':
                if job.get('data_point')=='from_google_sheet':
                    input=job.get('input')
                    required_keys=['spreadsheet_url']
                    for key,value in input.items():
                            if key in required_keys:
                                required_keys.remove(key)
                    if len(required_keys)!=0: 
                        print('Failed to Create Task.Missing Required Key')
                    else:
                        _={}                      
                        _.update({'spreadsheet_url':input.get('spreadsheet_url')})   
                        _.update(job)                
                        _tasks.append(_) 
            if job.get('end_point')=='sync':
                if job.get('data_point')=='with_google_sheet':
                    input=job.get('input')
                    required_keys=['spreadsheet_url']
                    for key,value in input.items():
                            if key in required_keys:
                                required_keys.remove(key)
                    if len(required_keys)!=0: 
                        print('Failed to Create Task.Missing Required Key')
                    else:
                        _={}                      
                        _.update({'spreadsheet_url':input.get('spreadsheet_url')})   
                        _.update(job)                
                        _tasks.append(_)'''