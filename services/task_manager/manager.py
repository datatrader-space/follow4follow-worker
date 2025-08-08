

from services.task_manager.endpoints import EndPoints
class TaskManager:
    def __init__(self):
        self.task=None
    def perform(self,**kwargs):
        
            e=EndPoints()
            e.get_required_data_point(**kwargs)
    
        
task={
        "spreadsheet_url": "https://docs.google.com/spreadsheets/d/11FBz_1nqDk3aN93R_sR6_chWvUb0DuggYsrVWZqViaA/edit#gid=1116455646",
        "id": "dddb7647-8d5c-11ee-803b-74563c02f7f7",
        "slug": "obtain_and_sync_resources_from_google_sheet",
        "workflow": "campaign_1",
        "end_point": "CreateResource",
        "data_point": "sync_resources_info_with_google_sheets",
        "service": "resource_manager"
    }


#im""" port json

#p=Perform()
#p.perform(**task) """

