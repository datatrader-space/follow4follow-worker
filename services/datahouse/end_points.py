import os
import json
import time
from services.instagram.parsers import Parser
from base.storage_sense import Saver
from base.request_maker import Request
from django.conf import settings
from base.datahouse_client import DataHouseClient
import random
class EndPoints:
    def __init__(self):
       
        self.make_request=''
        self.request_maker=Request()
        self.retrieve = self.retrieve(self)  # pass reference to parent
 
        self.storage_sense=Saver()
      
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
       
        return data_point(**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
    
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(**kwargs)

    class update: 
        def __init__(self):
            self.request_maker=Request()                                                  
        def send_update_to_client(self,**kwargs):
                add_data=kwargs.get('add_data')                              
                add_data=kwargs.get('add_data')
                if add_data.get('data_source'):
                    data_source=add_data.get('data_source')
                    for source in data_source:
                        results=[]
                        s=Saver()   
                        keys=[]                    
                        if source['type']=='task':
                            exclude_blocks=s.get_consumed_blocks(id=kwargs.get('uuid'))
                            resp=s.read_task_outputs(exclude_blocks=exclude_blocks,uuid=source.get('identifier'),keys=True,block_name=source.get('block_name'),size=1000)                                                 
                            for key, value in resp.items():
                                
                                for row in value:
                                    if row.get('service')=='task_manager':
                                         print('tm log out ign')
                                         continue
                                    row.update({'task_uuid':source.get('identifier')})
                                    
                                    results.append(row)   
                                keys.append(key) 
                            if len(results)>1:
                                from base.request_maker import Request
                                r=Request()
                                r.task_id=kwargs.get('uuid')
                                r.run_id=kwargs.get('run_id')
                                import uuid
                            
                                r.initialize_request_session()
                                import pandas as pd
                                df=pd.DataFrame(results)
                                df.fillna(False,inplace=True)
                                
                                url=settings.DATA_HOUSE_URL+'datahouse/api/consume/'
                                results=EndPoints.update().convert_timestamps(df)
                                results=df.to_dict(orient='records')
                                for row in results:
                                    try:
                                          json.dumps(row)
                                    except Exception as e:
                                         print(e)
                                         print(row.keys())
                                resp=r.make_request(end_point='audience',data_point='send_update_to_client',url=url,r_type='post',payload=json.dumps({'method':'create','data':results,'task_uuid':source.get('identifier')}))
                                if resp['status']=='error':
                                    print('Failed to send update to client. Client is Offline Most Likely or wrong url')
                                else:
                                    for key in keys:
                                        s.add_output_block_to_consumed(kwargs.get('uuid'),key)
        def send_update_to_client_latest(self,**kwargs):
                add_data=kwargs.get('add_data')                              
                add_data=kwargs.get('add_data')
                if add_data.get('data_source'):
                    data_source=add_data.get('data_source')
                    for source in data_source:
                        results=[]
                        s=Saver()   
                        keys=[]                    
                        if source['type']=='task':
                            exclude_blocks=s.get_consumed_blocks(id=kwargs.get('uuid'))
                            resp=s.read_task_outputs(exclude_blocks=exclude_blocks,uuid=source.get('identifier'),keys=True,block_name=source.get('block_name'),size=1000)                                                 
                            for key, value in resp.items():
                                
                                for row in value:
                                    if row.get('service')=='task_manager':
                                         print('tm log out ign')
                                         continue
                                    row.update({'task_uuid':source.get('identifier')})
                                    
                                    results.append(row)   
                                keys.append(key) 
                            if len(results)>=1:
                                from base.request_maker import Request
                                r=Request()
                                r.task_id=kwargs.get('uuid')
                                r.run_id=kwargs.get('run_id')
                                import uuid
                            
                                r.initialize_request_session()
                                r.session.headers.update({"Content-Type": "application/json"})
                              
                                import pandas as pd
                                df=pd.DataFrame(results)
                                df.fillna(False,inplace=True)
                                url=kwargs.get('add_data',{}).get('client_url',False)
                                if not kwargs.get('add_data',{}.get('client_url')):
                                     
                                   return False
                                results=EndPoints.update().convert_timestamps(df)
                                results=df.to_dict(orient='records')
                                for row in results:
                                    try:
                                          json.dumps(row)
                                    except Exception as e:
                                         print(e)
                                         print(row.keys())
                            
                                resp=r.make_request(end_point='audience',data_point='send_update_to_client',url=url,r_type='post',payload=json.dumps({'method':'create','data':results,'task_uuid':source.get('identifier')}))
                                if resp:
                                    if resp['status']=='error':
                                        print('Failed to send update to client. Client is Offline Most Likely or wrong url')
                                    else:
                                        for key in keys:
                                            s.add_output_block_to_consumed(kwargs.get('uuid'),key)

        def convert_timestamps(self,df):
                        import pandas as pd
                        import numpy as np
                        """
                        Converts timestamp columns in a pandas DataFrame to datetime format.

                        Args:
                            df (pd.DataFrame): The input DataFrame.

                        Returns:
                            pd.DataFrame: The DataFrame with timestamp columns converted to datetime.
                        """
                        for col in df.columns:
                                if col=='datetime' or col=='taken_at' or col=='device_timestamp' or col=='carousel_last_edited_at' or col =='created_time':
                                
                                    df[col] = df[col].astype(str) # Convert datetime to string in a vectorized manner

                        return df

    class retrieve: # Renamed from 'retr' for clarity and consistency
        def __init__(self,parent):
            # Initialize once in constructor
            self.client = DataHouseClient()
            self.parent = parent  # Can be used if needed


        def retrieve_from_datahouse1(self,**kwargs):

            add_data = kwargs.get('add_data', {})
            data_source = add_data.get('data_source', [])
            source = data_source[0]
            object_type = source.get('object_type')
            filter = source.get("filters")
            


        def retrieve_from_datahouse(self, **kwargs):



            """
            Retrieves data from the Aadml Data House using the DataHouseClient.
            Expected kwargs:
                - add_data: dictionary containing 'data_source' with 'object_type' and 'filters'.
            """
            add_data = kwargs.get('add_data', {})
            data_source = add_data.get('data_source', [])
            uuid = kwargs.get('uuid')
          
            self.client.base_url=add_data.get('datahouse_url')
            if not data_source:
                print("Error: No data_source provided for retrieve_from_datahouse.")
                return False

            # Assuming data_source is a list, and we're interested in the first item for now
            source_config = data_source[0]
            object_type = source_config.get('object_type')
            filters = source_config.get('filters', [])
            size = source_config.get('size', 30)
            lock_results = source_config.get('lock_results', False)
            lock_type = source_config.get('lock_type', False)
            provide_for_profile_analysis = source_config.get('provide_for_profile_analysis', False)

            if not object_type:
                print("Error: 'object_type' missing in data_source for retrieve_from_datahouse.")
                return False

            # Use the DataHouseClient instance from the parent EndPoints class
            retrieved_data = self.client.retrieve(
                object_type=object_type,
                filters=filters,
                size=size,
                lock_results=lock_results,
                lock_type=lock_type,
                provide_for_profile_analysis=provide_for_profile_analysis,
                ref_id=kwargs.get('ref_id'),
                uuid = kwargs.get("uuid")

            )

            if retrieved_data is not None:
                print(f"Successfully retrieved data from Data House for object_type: {object_type}")
                return retrieved_data
            else:
                print(f"Failed to retrieve data from Data House for object_type: {object_type}")
                return False                                            
                                            
