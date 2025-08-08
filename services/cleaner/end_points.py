import os
import json
import time
from services.instagram.parsers import Parser
from base.storage_sense import Saver
from services.instagram.register_assistant import RegisterAssistant
from services.instagram.run_bot import Instagram
from base.browser import Browser
import random
class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.parsers=Parser() 
        self.register_assistant=RegisterAssistant()
        self.storage_sense=Saver()
        self.browser=Browser()
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
       
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
    
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    class clean:
        def __init__(self):
            pass
        def compare(self,**kwargs):
            cleaned_data=[]
            data=kwargs.get('data')
            fields_to_compare=kwargs.get('add_data').get('fields_to_compare')
            for row in data:
                append=0
                for field in fields_to_compare:
                    if '.' in field['value']:
                        field['value']=field['value'].split('.')[0]
                        operator=field['value'].split('.')[1]

                    if field['key'] in row.keys():
                        if field['value']==int or field['value']=='int':
                            if type(row[field['key']])==int:
                                append+=1
                                continue
                        elif field['value']==str or field['value']=='str':
                            

                            if type(row[field['key']])==str and len(row[field['key']])>1:
                                append+=1
                                continue
                        elif type(field['value'])==bool:
                            if type(row[field['key']])==bool:
                                
                                if row[field['key']] ==field['value']:
                                    append+=1
                                    continue
                            elif len(row[field['key']])>0:
                                append+=1
                                continue
                        elif type(field['value'])==str:
                            if type(row[field['key']])==str and row[field['key']].lower()==field['value'].lower():
                                append+=1
                                continue
                       
                if append==len(fields_to_compare):
                   
                    cleaned_data.append(row)
            return cleaned_data
        def remove_columns(self,**kwargs):

            data=kwargs.get('data')
            after_removal_data=[]
            columns_to_remove=kwargs.get('add_data').get('columns_to_remove',[])
            columns_to_keep=kwargs.get('add_data').get('columns_to_keep')
            if columns_to_keep:
                import pandas as pd
                df=pd.DataFrame(data)
                return df[columns_to_keep].to_dict(orient='records')
            else:
                for row in data:
                    if columns_to_keep:
                        return df
                    for column in columns_to_remove:
                        row.pop(column,None)
                    
                    after_removal_data.append(row)
                return after_removal_data
        def remove_duplicates(self,**kwargs):
            data=kwargs.get('data')
            
            import pandas as pd
            df=pd.DataFrame.from_records(data).fillna(0)
            columns_to_remove_by=kwargs.get('add_data').get('remove_duplicates_by_column')
            if columns_to_remove_by:

                df.drop_duplicates(subset=columns_to_remove_by,keep='last',inplace=True)
            return df.to_dict(orient='records')
        def check_for_presence_of_and_remove(self,**kwargs):
            final_data=[]
            data=kwargs.get('data')
            after_removal_data=[]
            check_for_presence_of=kwargs.get('add_data').get('check_for_presence_of',[])
            remove=False
            for row in data:             
                for check in check_for_presence_of:
                    key=check['key']
                    value=check['value']
                   
                    if value in row.get(key,''):
                        remove=True
                        break
                    else:
                        remove=False
                if remove:
                    pass
                else:
                    final_data.append(row)
            return final_data
        def clean_data(self,**kwargs):
            data_source=kwargs.get('add_data').get('data_source')
            outputs=[]
            add_data=kwargs.get('add_data')
            for source in data_source:
                s=Saver()
                if source['type']=='storage_block':
                    
                    data=s.read_data_from_storage_block('users.'+source['identifier']+'.followers','instagram')
                elif source['type']=='task':
                    exclude_blocks=s.get_consumed_blocks(id=kwargs.get('uuid'))

                    resp=s.read_task_outputs(uuid=source['identifier'],exclude_blocks=exclude_blocks,keys=True,block_name=source.get('block_name',False))
                    for key, value in resp.items():

                        k=kwargs.copy()
                        data=value
                        k.update({'data_point':'remove_columns','end_point':'clean','data':data})
                        after_removed_column_data=self.internal_get_required_data_point(**k)
                        
                        outputs.append({'name':'uncleaned_data','data':after_removed_column_data})
                        outputs.append({'name':'after_removed_columns','data':after_removed_column_data})
                        k=kwargs.copy()
                        k.update({'data_point':'check_for_presence_of_and_remove','end_point':'clean','data':after_removed_column_data})
                        check_for_presence_of=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'check_for_presence_of','data':check_for_presence_of})
                        k=kwargs.copy()
                        k.update({'data_point':'compare','end_point':'clean','data':check_for_presence_of})
                        compared_data=self.internal_get_required_data_point(**k)
                        k=kwargs.copy()
                        k.update({'data_point':'remove_duplicates','end_point':'clean','data':compared_data})
                        duplicates_removed_data=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'removed_duplicates','data':duplicates_removed_data})
                        
                        outputs.append({'name':'cleaned_data','data':duplicates_removed_data})
                        
                        
                        address='.tasks.'+str(kwargs.get('uuid'))+'.outputs'
                        service='deep_stuff'
                        print(duplicates_removed_data)
                        if len(duplicates_removed_data)>0:
                            s.create_task_outputs(kwargs.get('uuid'),data=duplicates_removed_data,block_name=kwargs.get('add_data',{}).get('block_name',False))
                            
                        s.add_output_block_to_consumed(kwargs.get('uuid'),key)
                        #s.write_data_to_storage_block(address,service,duplicates_removed_data)
                        
            if kwargs.get('add_data',{}).get('save_to_googlesheet',False):
                            return
                            add_data=kwargs.get('add_data')
                            s=Saver()
                            data={}
                            for output in outputs:
                                if not output['name'] in list(data.keys()):
                                    data.update({output['name']:[]})
                                data[output['name']].extend(output['data'])
                            try:
                                for key,value in data.items():
                                    s.push_data_frame_to_google_sheet(**{'spreadsheet_url':add_data.get('spreadsheet_url'),
                                                                    'worksheet_name':key,
                                                                    'data':value
                                                                    
                                                                    })
                            except Exception as e:
                                pass
                            try:
                                outputs=s.read_task_outputs(kwargs.get('uuid'))
                                s.push_data_frame_to_google_sheet(**{'spreadsheet_url':add_data.get('spreadsheet_url'),
                                                                    'worksheet_name':add_data.get('worksheet_name'),
                                                                    'data':outputs
                                                                    
                                                                    })      
                            except Exception as e:
                                pass   
                        


    class Instagram:
        def __init__(self):
            pass
        def clean_data(self,**kwargs):
            data_source=kwargs.get('add_data').get('data_source')
            outputs=[]
            
            for source in data_source:
                s=Saver()
                if source['type']=='storage_block':
                    
                    data=s.read_data_from_storage_block('users.'+source['identifier']+'.followers','instagram')
                elif source['type']=='task':
                    exclude_blocks=s.get_consumed_blocks(id=kwargs.get('uuid'))

                    resp=s.open_blocks_from_task_output(source['identifier'],exclude_blocks)
                    for key, value in resp.items():

                        k=kwargs.copy()
                        data=value
                        k.update({'data_point':'remove_columns','end_point':'clean','data':data,'add_data':{'columns_to_remove':['last_scraped_at']}})
                        after_removed_column_data=self.internal_get_required_data_point(**k)
                        
                        outputs.append({'name':'uncleaned_data','data':data})
                        outputs.append({'name':'after_removed_columns','data':after_removed_column_data})
                        k=kwargs.copy()
                        k.update({'data_point':'check_for_presence_of_and_remove','end_point':'clean','data':data})
                        check_for_presence_of=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'check_for_presence_of','data':check_for_presence_of})
                        k=kwargs.copy()
                        k.update({'data_point':'compare','end_point':'clean','data':check_for_presence_of})
                        compared_data=self.internal_get_required_data_point(**k)
                        k=kwargs.copy()
                        k.update({'data_point':'remove_duplicates','end_point':'clean','data':compared_data})
                        duplicates_removed_data=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'removed_duplicates','data':duplicates_removed_data})
                        
                        outputs.append({'name':'cleaned_data','data':duplicates_removed_data})
                        
                        
                        address='.tasks.'+str(kwargs.get('uuid'))+'.outputs'
                        service='deep_stuff'
                        s.create_task_outputs(kwargs.get('uuid'),data=duplicates_removed_data)
                            
                        s.add_output_block_to_consumed(kwargs.get('uuid'),key)
                        #s.write_data_to_storage_block(address,service,duplicates_removed_data)
                        
            if kwargs.get('add_data',{}).get('save_to_googlesheet',False):
                            s=Saver()
                            data={}
                            for output in outputs:
                                if not output['name'] in list(data.keys()):
                                    data.update({output['name']:[]})
                                data[output['name']].extend(output['data'])
                            for key,value in data.items():
                                s.push_data_frame_to_google_sheet(**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1lTmrDMt4Z5HR7-zK2crpke71FQ81EZOZpua-vNsi23g/edit?gid=0#gid=0',
                                                                'worksheet_name':key,
                                                                'data':value
                                                                
                                                                })
                            outputs=s.read_task_outputs(kwargs.get('uuid'))
                            s.push_data_frame_to_google_sheet(**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1lTmrDMt4Z5HR7-zK2crpke71FQ81EZOZpua-vNsi23g/edit?gid=0#gid=0',
                                                                'worksheet_name':'task_data',
                                                                'data':outputs
                                                                
                                                                })