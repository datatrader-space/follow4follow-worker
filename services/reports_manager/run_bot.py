
from services.instagram.storage_sense import StorageSense

from services.reports_manager.manager import Manager
import json



class ReportsManager():
    def __init__(self):
        super().__init__()

       
        self.reporter=Manager()
        self.storage_sense = StorageSense()
        self.storage_sense.service = "instagram"
        self.storage_sense.userId = "hamza"
    


    def run_bot(self, task):
        
        from services.reports_manager.endpoints import EndPoints
        e=EndPoints()
        resp=e.get_required_data_point(**task)
        print(resp)

       

    

