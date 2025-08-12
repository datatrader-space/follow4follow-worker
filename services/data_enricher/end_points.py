import os
import json
import time

from base.storage_sense import Saver
from services.reports_manager.manager import Manager as reports_manager

import random
class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.reports_manager=reports_manager()
        self.reports_manager.service='data_enricher'
     
       
        self.storage_sense=Saver()
    
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
       
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
    
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    class enrich:
        def __init__(self):
            self.reports_manager=reports_manager()
            self.reports_manager.service='data_enricher'
            pass
        def enrich(self,**kwargs):
                self.reports_manager.task_id=kwargs.get('uuid')
                self.reports_manager.run_id=kwargs.get('run_id')
                
                add_data=kwargs.get('add_data')
                service=add_data.get('service')
                data_point=kwargs.get('data_point')
                
                              
                add_data=kwargs.get('add_data')
                if add_data.get('data_source'):
                    data_source=add_data.get('data_source')
                    if add_data.get('service')=='openai':
                        from services.openai.run_bot import OpenAi
                        client=OpenAi()
                        client.reporter=self.reports_manager
                    gpt_responses_count=0
                    partial_responses_count=0
                    complete_responses_count=0
                    exception_in_openai_api_count=0
                    empty_responses_count=0
                    missing_column_rows=0
                    total_rows=0

                    for source in data_source:
                        if source['type']=='data_house':
                            from base.datahouse_client import DataHouseClient
                            d=DataHouseClient()
                            d.request_maker.task_id=kwargs.get('uuid')
                            d.request_maker.run_id=kwargs.get('run_id')
                            inputs=d.retrieve(object_type=source['object_type'],lock_results=source['lock_results'],size=source['size'],filters=source['filters'],**{'uuid':kwargs.get('uuid')})
                            total_rows=len(inputs)
                            if inputs:
                                for row in inputs:
                                    try:
                                        resp=client.run_bot({'end_point':'Text_Generation','data_point':'names_and_generated_data',
                                                        'add_data':{'api_key':add_data.get('api_key'),
                                                                    'prompt':_prompt
                                                                    }
                                                                                                    
                                                        })
                                    except Exception as e:
                                        self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'error','task':str(kwargs['uuid']),'error':e, 
                                        }) 
                                        raise Exception('Insufficient Funds')
                                        
                                    if resp:
                                        _=row.copy()
                                        _.update(resp)
                                
                                        results.append(_)
                                    else:
                                        s.create_task_failures(kwargs.get('uuid'),data=[row])
                                        
                                s.create_task_outputs(kwargs.get('uuid'),data=results,block_name=kwargs.get('add_data').get('block_name'))
                                #s.add_output_block_to_consumed(kwargs.get('uuid'),key)
                                      

                        else:
                            s=Saver()                       
                            if source['type']=='task':
                                exclude_blocks=s.get_consumed_blocks(id=kwargs.get('uuid'))
                                resp=s.read_task_outputs(exclude_blocks=exclude_blocks,uuid=source.get('identifier'),keys=True,block_name=source.get('block_name'))                            
                                
                                prompt=add_data.get('prompt')
                                prompt+='\n Return the output as dict with following keys '+','.join(add_data.get('output_column_names'))+' . Dont comment anything. Not even python'
                                
                                for key, value in resp.items():
                                    total_rows+=1
                                    results=[]
                                    
                                    for row in value:
                                        column_found=0
                                        _prompt=prompt
                                        for column in add_data.get('columns'):
                                            if '|' in column:
                                                names=column.split('|')
                                                for name in names:
                                                    if row.get(name):
                                                        _prompt=_prompt.replace('{'+column+'}', row.get(name))
                                        
                                            elif row.get(column):
                                                column_found+=1
                                                _prompt=_prompt.replace('{'+column+'}', row.get(column))
                                            else:
                                               pass
                                        if not column_found==len(add_data.get('columns')):
                                            self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                                    'type':'row_missing_required_columns','task':str(kwargs['uuid']),'row':row, 
                                                    })    
                                            missing_column_rows+=1 
                                            continue

                                        try:
                                            resp=client.run_bot({'end_point':'Text_Generation','data_point':'names_and_generated_data',
                                                            'add_data':{'api_key':add_data.get('api_key'),
                                                                        'prompt':_prompt
                                                                        }
                                                                                                        
                                                            })
                                        except Exception as e:
                                            import traceback
                                            self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                                    'type':'error','task':str(kwargs['uuid']),'error':e,'traceback':traceback.format_exc() 
                                                    })   
                                            
                                           
                                        if resp:
                                            _=row.copy()
                                            _.update(resp)
                                    
                                            results.append(_)
                                            gpt_responses_count+=1
                                            count=0
                                            for column in add_data.get('output_column_names'):
                                                if resp.get(column):
                                                    count+=1
                                            if count==0:
                                                empty_responses_count+=1
                                            if count%len(add_data.get('output_column_names'))==0:
                                                complete_responses_count+=1
                                           
                                            else:
                                                partial_responses_count+=1

                                            
                                                
                                            
                                        else:
                                            self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                                    'type':'failed_to_enrich','task':str(kwargs['uuid'])
                                                    }) 
                                            exception_in_openai_api_count+=1
                                            s.create_task_failures(kwargs.get('uuid'),data=[row])
                                            
                                    s.create_task_outputs(kwargs.get('uuid'),data=results,block_name=kwargs.get('add_data').get('block_name'))
                                    s.add_output_block_to_consumed(kwargs.get('uuid'),key)
                                      

                self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                                                        'type':'data_acquired','task':str(kwargs['uuid']),
                                                                        'total_rows':total_rows,
                                                                        'total_rows_with_missing_column':missing_column_rows,
                                                                        'total_responses_from_gpt':gpt_responses_count,
                                                                        'total_empty_responses':empty_responses_count,'total_partial_responses':partial_responses_count,
                                                                        'total_complete_responses':complete_responses_count,'exception_in_openai_api':exception_in_openai_api_count

                                                                        })   
                if kwargs.get('add_data',{}).get('save_to_googlesheet',False):
                    print('pushing to google sheet')
                    s=Saver()
                    block_name=''
                    if kwargs.get('add_data',{}).get('block_name'):
                        block_name=kwargs.get('add_data',{}).get('block_name','')
                    outputs=s.read_task_outputs(kwargs.get('uuid'),keys=False,block_name=block_name)
                    print('outputs read: total size:'+str(len(outputs)))
                    print('pushing to')
                    print(add_data.get('spreadsheet_url'))
                    s.push_data_frame_to_google_sheet(update=True,**{'spreadsheet_url':add_data.get('spreadsheet_url'),
                                                        'worksheet_name':add_data.get('worksheet_name'),
                                                        'data':outputs
                                                        
                                                        })
        def enrich_social_media_profile(self,**kwargs):
            add_data=kwargs.get('add_data')
            service=add_data.get('service')
            data_point=kwargs.get('data_point')
            
                            
            add_data=kwargs.get('add_data')
            if add_data.get('data_source'):
                data_source=add_data.get('data_source')
                if add_data.get('service')=='openai':
                    from services.openai.run_bot import OpenAi
                    client=OpenAi()
                for source in data_source:
                    if source['type']=='data_house':
                        self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'source_type_is_datahouse','task':str(kwargs['uuid'])
                                        }) 
                        from base.datahouse_client import DataHouseClient
                        import urllib
                        import re
                        from base.downloader import Downloader
                        downloader=Downloader()
                        d=DataHouseClient()
                        d.request_maker.task_id=kwargs.get('uuid')
                        d.request_maker.run_id=kwargs.get('run_id')
                        self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'making_request_to_datahouse','task':str(kwargs['uuid']) 
                                        }) 
                        inputs=d.retrieve(object_type=source['object_type'],lock_type=source.get('lock_type'),lock_results=source.get('lock_results',False),filters=source['filters'],size=source.get('size',None),provide_for_profile_analysis=True,**{'uuid':kwargs.get('uuid')})
                        self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'request_finished_inputs_retrieved','task':str(kwargs['uuid']) 
                                        }) 
                        self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'length_of_inputs__'+str(len(inputs['data'])),'task':str(kwargs['uuid']) 
                                        }) 
                        if inputs:
                            self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'length_of_inputs__'+str(len(inputs['data'])),'task':str(kwargs['uuid']) 
                                        })
                            self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'checking_inputs_that_meet_profile_analysis_criterion','task':str(kwargs['uuid']) 
                                        }) 
                            for profile in inputs['data']:
                                medias=[]
                                texts=[]
                                posts=profile['posts']
                                if not posts:
                                    print('profile doesnt have posts')
                                    continue
                                for post in profile.get('posts',[])[0:5]:
                                    if len(post['text'])>0:

                                        texts.append(post['text'])
                                    updated_medias = []
                                 
                                    for url in post.get('medias', []):
                                        cleaned_url = url.replace("\\", "/")
                                        parsed_url = urllib.parse.urlparse(cleaned_url)
                                                            
                                        cleaned_url = urllib.parse.urlunparse(parsed_url)
                                        cleaned_url = re.sub(r"(?<!:)/{2,}", "/", cleaned_url)
                                        local_path = downloader.download_media(media_type='image', link=cleaned_url,save_to_local_storage=True)
                                        if local_path:
                                            medias.append(local_path['local_storage_file_path'])
                                    post.pop('medias')
                                        #post['medias'] = updated_medias 
                                if not texts and not medias:
                                    print('neither text nor media found')
                                    continue
                                if profile.get('profile_info',{}).get('profile_picture'):
                                    url=profile.get('profile_info',{}).get('profile_picture')
                                    cleaned_url = url.replace("\\", "/")
                                    parsed_url = urllib.parse.urlparse(cleaned_url)
                                                        
                                    cleaned_url = urllib.parse.urlunparse(parsed_url)
                                    cleaned_url = re.sub(r"(?<!:)/{2,}", "/", cleaned_url)
                                    local_path = downloader.download_media(media_type='image', link=cleaned_url,save_to_local_storage=True)
                                    if local_path:
                                        profile['profile_info']['profile_picture']=local_path
                                
                                task = {
                                'service':"openai_",
                                'end_point':'MultiModalAnalysis',
                                'data_point':'analyze_content',
                                "uuid":kwargs.get('uuid'),
                                "add_data":{
                                    "text":f"""Understand what is in the images. Try to extract the details from the images. 
                                    Predict the gender, country, interests, profile analysis, age, possible buying interests, religion from the image, Profile information: {profile.get('profile_info')}, Posts text: {posts} as well
                                    while predicting the gender, country, city, interests, and profile analysis.
                                    Predict the keywords from Posts text.
                                    Also, try to extract any contact information(Number, Address, email) if present in the image, Profile information and post text.
                                    The 'Gender' field should represent the gender of the profile owner, not necessarily the gender of individuals mentioned in the posts. Determine the gender of the profile owner based on the true context of the username and full name like if username and full name are "dhamis.collection" and "Dhami's by Sharmeen Lakhani". It doesn't mean the profile's gender is female because the profile is simply a business account. Do not simply rely on individual names within the full name. 
                                    Extract type of profile as well. It should always be on of:"Business","Personal","Fan","Spam".
                                    Extract any external accounts mentioned as well.
                                    Religion should be predicted keeping in mind the username and full name of the person. It should be None if the name and full name suggests that the profile is not associated to a person.
                                    Based on the text in Posts text and images provided, determine the Age by considering the following:
                                    - Language complexity, slang, and writing style.
                                    - Topics discussed 
                                    - Emojis and internet trends commonly associated with specific age groups.
                                    - If images contain faces, analyze visible aging features.
                                    - If the gender is not specified, set Age as "None" or "Null".
                                    - If the profile is not associated with a person, set Age as 'None' or 'Null'
                                    - If the gender is specified, you are strongly advised to determine the Age.
                                    Extract as well infer the keywords that might help marketing team filter through dataset to identify, find profiles for advertising
                                    Extract or predict "Interests & Lifestyle Patterns", "Possible Buying Intent" and "Financial and Economic Status" strongly and these three attributes should have simple words, not sentences.
                                    Return only a dictionary with keys:
                                    gender,country,city, interests ,profile_analysis,keywords,phone_number,email,external_accounts,type,age,possible_buying_interests,interests_and_lifestyle_patterns,possible_buying_intent,financial_and_economic_status,religion
                                    You are instructed to give all information strictly.
                                    Any information that is not present, keep it "Null" or "None". It should never be "Not Applicable" or "Not specified".
                                    Only generate a dictionary and nothing else, not even a single word or a line break or whitespaces.
                                    Dont mention reasoning.
                                    Follow the above given instructions, strictly.""",
                                    "image_paths":medias,
                                    "api_key":kwargs.get('add_data',{}).get('api_key','')
                                }
                            }
                                from services.openai.run_bot import OpenAi
                                client=OpenAi()
                                s=Saver()
                                self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'starting_openai_bot','task':str(kwargs['uuid']),
                                        }) 
                                resp=client.run_bot(task)
                                self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'parsing_bot_response','task':str(kwargs['uuid']),
                                        }) 
                                try:
                                    resp_dict = json.loads(resp)
                                    print(resp_dict)
                                except Exception as e:
                                    self.reports_manager.report_performance(**{'service':'data_enricher','end_point':'enrich','data_point':'enrich',
                                        'type':'error_in_parsing_bot_response','task':str(kwargs['uuid']),'error':e, 
                                        }) 
                                    dp_output= {
                                    'object_type':'output',
                                    'data':{
                                    'inputs':[{
                                        'profile_info':profile.get('profile_info'),
                                        'posts':profile.get('posts')
                                    }],
                                    'output':resp_dict
                                }}
                                    
                                    s.create_task_outputs(kwargs.get('uuid'),block_name='dp_output',data=dp_output)
                                    continue
                                profile_dict=resp_dict
                                profile_dict.update({'username':profile.get('profile_info')['username'],'object_type':'profile','service':profile.get('profile_info').get('service')})
                                dp_output= {
                                    'object_type':'output',
                                    'data':{
                                    'inputs':[{
                                        'profile_info':profile.get('profile_info'),
                                        'posts':profile.get('posts')
                                    }],
                                    'output':resp_dict
                                }}
                                s.create_task_outputs(kwargs.get('uuid'),data=profile_dict,block_name=kwargs.get('add_data').get('block_name'))
                                s.create_task_outputs(kwargs.get('uuid'),block_name='dp_output',data=dp_output)

        def compare(self,**kwargs):
            cleaned_data=[]
            data=kwargs.get('data')
            fields_to_compare=kwargs.get('add_data').get('fields_to_compare')
            for row in data:
                append=0
                for field in fields_to_compare:
                
                    if field['key'] in row.keys():
                        if field['value']==int:
                            if type(row[field['key']])==int:
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
                       
                if append==len(fields_to_compare):
                   
                    cleaned_data.append(row)
            return cleaned_data
        def remove_columns(self,**kwargs):
            data=kwargs.get('data')
            after_removal_data=[]
            columns_to_remove=kwargs.get('add_data').get('columns_to_remove',[])
            for row in data:
                for column in columns_to_remove:
                    row.pop(column,None)
                after_removal_data.append(row)
            return after_removal_data
        def remove_duplicates(self,**kwargs):
            data=kwargs.get('data')
            
            import pandas as pd
            df=pd.DataFrame.from_records(data).fillna(0)
            df.drop_duplicates(keep='last',inplace=True)
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
                    
                        


    class Instagram:
        def __init__(self):
            pass
        def clean_user_followers(self,**kwargs):
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
                        k.update({'data_point':'remove_columns','end_point':'Clean','data':data,'add_data':{'columns_to_remove':['last_scraped_at']}})
                        after_removed_column_data=self.internal_get_required_data_point(**k)
                        
                        outputs.append({'name':'uncleaned_data','data':data})
                        outputs.append({'name':'after_removed_columns','data':after_removed_column_data})
                        k=kwargs.copy()
                        k.update({'data_point':'check_for_presence_of_and_remove','end_point':'Clean','data':data})
                        check_for_presence_of=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'check_for_presence_of','data':check_for_presence_of})
                        k=kwargs.copy()
                        k.update({'data_point':'compare','end_point':'Clean','data':check_for_presence_of})
                        compared_data=self.internal_get_required_data_point(**k)
                        k=kwargs.copy()
                        k.update({'data_point':'remove_duplicates','end_point':'Clean','data':compared_data})
                        duplicates_removed_data=self.internal_get_required_data_point(**k)
                        outputs.append({'name':'removed_duplicates','data':duplicates_removed_data})
                        
                        outputs.append({'name':'cleaned_data','data':duplicates_removed_data})
                        if kwargs.get('add_data',{}).get('save_to_googlesheet',False):
                            for output in outputs:

                                s.push_data_frame_to_google_sheet(**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1wTVLDWlmfTTnkrltx1iBUppJ5J_9EBYuCVXa59mhaVM/edit?gid=0#gid=0',
                                                                'worksheet_name':output['name'],
                                                                'data':output['data']
                                                                
                                                                })
                        else:
                            address='.tasks.'+str(kwargs.get('uuid'))+'.outputs'
                            service='deep_stuff'
                            s.create_task_outputs(kwargs.get('uuid'),data=duplicates_removed_data)
                            
                        s.add_output_block_to_consumed(kwargs.get('uuid'),key)
                        #s.write_data_to_storage_block(address,service,duplicates_removed_data)
           
            
        