import requests
import json
import uuid
from django.conf import settings
from base.request_maker import Request
class DataHouseClient:
    def __init__(self):
        self.base_url = settings.DATA_HOUSE_URL
        self.request_maker=Request()
        self.request_maker.initialize_request_session()
      
        self.session = requests.Session()  # Use a session for efficiency

    def retrieve(self, object_type, filters=[],size=30, provide_for_profile_analysis=False,lock_results=False,lock_type=False, ref_id=None, **kwargs):
        url = f"{self.base_url}datahouse/api/provide/"  # Construct the URL

        payload = {
            "filters":filters,
            "size":size,
            "lock_type": lock_type,
            "provide_for_profile_analysis":provide_for_profile_analysis,
            "lock_results": lock_results,
            "object_type":object_type,
            "uuid": kwargs.get("uuid")
            
        }
        payload.update(kwargs) # Add any additional kwargs to the payload.
        print(payload)
        try:
            response = self.request_maker.make_request(end_point='api',data_point='provide',url=url,r_type='post',retry=3,_json=payload) 
            if response['status']=='success':
                return response['data']
            else:
                return False
            

        except Exception as e:
            print(f"Error in provide: {e}")
            return None  # Or raise the exception if you prefer

    def consume(self, payload):
        url = f"{self.base_url}/datahouse/api/consume"

       
        try:
            response = self.request_maker.make_request(end_point='api',data_point='consume',url=url,r_type='post',retry=3,_json=payload) 
            if response['status']=='success':
                return response['data']
            else:
                return False
            

        except Exception as e:
            print(f"Error in provide: {e}")
            return None  # Or raise the exception if you prefer

