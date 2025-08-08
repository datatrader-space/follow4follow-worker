import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import datetime as dt
import uuid
import traceback
import datetime
from django.utils import timezone
class Saver(object):
    def __init__(self):
        
        self.scraped_data=[]
        self.user_followers=[]
        self.user_posts=[]
        self.users=[]
        self.post_comments=[]
        self.follow_relations=[]
        self.parent_tweet=[]
        self.feed_tweets=[]
        self.t_lists=[]
        self.service='instagram'
        self.username=''
        self.end_point='user_posts'
        self.data_point=''
        self.object_identifer=''
        self.post_id='abcd1234'
        self.file_identifier=''
        self.data_blocks=[]
        self.cached_blocks=[]
        self.sectioned_data=None
        self.file_extension='.csv'
        self.empty_file=False
        self.overwrite=False
        self.block_address={}
        self.userId='hamza'
        self.drop_duplicates=False
    def create_crawler_directory(self):
        pth=os.path.join(os.getcwd(),'crawler')
        if not os.path.exists(pth):
           os.makedirs(pth)
        self.crawler_directory=pth
        return self
    def create_data_directory(self):
        pth=os.path.join(self.crawler_directory,'data')
        if not os.path.exists(pth):
           os.makedirs(pth)
        self.data_directory=pth
        return self
    def create_user_directory(self):
        self.create_crawler_directory().create_data_directory()
        pth=os.path.join(self.data_directory,self.userId)
        if not os.path.exists(pth):
           os.makedirs(pth)
        self.user_directory=pth
        return self

    def create_service_directory(self):

        self.service_directory=os.path.join(self.user_directory,self.service)
        if not os.path.exists(self.service_directory):
            os.makedirs(self.service_directory)    
        return self
    def load_resources(self):
        pth=os.path.join(os.getcwd(),'resources')
        block_address=self.block['address'].split('.')
        for module in block_address:
            if len(module.split(','))>1:
                for _ in module.split(','):
                    pth=os.path.join(pth,_)
               
            pth=os.path.join(pth,module)
        if os.path.exists(pth):
            pass
        else:
            os.makedirs(pth)
        self.block_address=pth
    def load_reports(self):
        pth=os.path.join(os.getcwd(),'reports')
        block_address=self.block['address'].split('.')
        for module in block_address:
            pth=os.path.join(pth,module)
        if os.path.exists(pth):
            pass
        else:
            try:
                os.makedirs(pth)
            except Exception as e:
                print(e)
                #print(e)
                #print('add report here')
            else:
                pass
        self.block_address=pth
    def load_deep_stuff(self):
        
        pth=os.path.join(os.getcwd(),'deep_stuff')
        block_address=self.block['address'].split('.')
        for module in block_address:
            pth=os.path.join(pth,module)
      
            if os.path.exists(pth):
                pass
            else:
                try:
                    os.makedirs(pth)
                except Exception as e:
                    pass
                    #self.create_report_dump({'service':'storage','end_point':'error','data_point':'makedirs_error',
                                        #'traceback':traceback.format_exc(),'datetime':str(dt.datetime.now()),'dir_path':pth
                                        
                                        
                                        #})
                else:
                    pass
                    #self.create_report_dump({'service':'storage_sense','end_point':'local_storage_sense','data_point':'load_deep_stuff',
                                          #   'type':'makedirs_success',
                                      #  'datetime':str(dt.datetime.now()),'dir_path':pth
                                        
                                        
                                       # })
        self.block_address=pth
    def load_screenshots(self):
        pth=os.path.join(os.getcwd(),'media','screenshots')
        self.block_address=pth
        if os.path.exists(pth):
            pass
        else:
            os.makedirs(pth)

    def load_block(self):
        self.create_user_directory()
        self.create_service_directory()
        block_address=self.block['address'].split('.')
        pth=self.service_directory
        if ',' in block_address:
            pass
            #print(block_address)
        
        for module in block_address:
            pth=os.path.join(pth,module)
        
        if os.path.exists(pth):
            pass
        else:
            os.makedirs(pth)
        self.block_address=pth
    def create_file_identifier(self):
        import uuid
        
        return str(uuid.uuid1())   
    def add_values_to_file(self,load_block=True):
    
        import uuid
        if load_block:
            self.load_block()

        self.open_file() 
                
        self.write_data_block_to_file()    
    def create_file(self):
        if not self.check_if_file_exists():
           open(self.file, 'w').close()
    def create_report_dump(self,output):
        from services.reports_manager.manager import Manager
        m=Manager()
        m.report_log(**output)
    def open_file(self):
        file_name=self.block.get('file_name')
         
        
        for file in os.listdir(self.block_address):
            if file.split('.')[0] == file_name:
                self.file_extension='.'+file.split('.')[1]
        pth=os.path.join(self.block_address,str(file_name)+self.file_extension)
        self.file_path=pth
        try:
            if os.path.exists(pth):
                self.empty_file=False
                if self.file_extension=='.csv':
                    self.file = pd.read_csv(pth)
                elif self.file_extension=='.xlsx':
                    self.file=pd.read_excel(pth,engine='openpyxl')
                elif self.file_extension=='.json':
                    self.file=pd.read_json(open(pth,'r'),dtype=False,encoding='utf-8')
                elif self.file_extension=='.html':
                    self.file=open(pth,'r',encoding='utf-8')
                elif self.file_extension=='.txt':
                    self.file=open(pth,'r',encoding='utf-8')
                    
                
            else:
                self.file = pd.DataFrame()
                self.empty_file=True
            self.data_frame=self.file
            return self
        except Exception as e:
            self.file=None
            self.empty_file=True
            
            _={'traceback':traceback.format_exc(),'service':'Storage','type':'error','error':'open_file_error','block_address':self.block_address,'file_path':self.file_path,'service':self.service,'datetime':dt.datetime.now()}
            from services.reports_manager.manager import Manager
            m=Manager()
            m.report_performance(**_)
                                                                                                             
                                                           
            #self.create_output(_)
            
   

    def write_data_block_to_file(self): 
         
        if self.file is None:
            _={'traceback':traceback.format_exc(),'service':'Storage','type':'error','error':'file_not_open_erro','block_address':self.block_address,'file_path':self.file_path,'service':self.service,'datetime':dt.datetime.now()}
            #print(_)
            raise ValueError("File is not open.")    
      
        if self.block.get('data'):
            data=self.block['data']
        else:
            data=self.block
        if type(data)==dict:
            data=[data]
        if self.file_extension=='.html':
            pass
        elif self.file_extension=='.txt':
            pass
        else:
            
            if self.overwrite:
                self.file=pd.DataFrame(data)
            else:          
                self.file = pd.concat([self.file, pd.DataFrame(data)], ignore_index=True)
                if self.drop_duplicates:

                    self.file.drop_duplicates(inplace=True)
        if self.file_extension =='.csv':
            self.file.to_csv(self.file_path)
        elif self.file_extension=='.json':
            self.file.to_json(self.file_path,orient='records',force_ascii=False)
        elif self.file_extension=='.html':
            
            self.file=open(self.file_path,'w',encoding='utf-8')
            self.file.write(data)
            self.file.close()
        elif self.file_extension =='.txt':
            self.file=open(self.file_path,'w',encoding='utf-8')
            self.file.write(data)
            self.file.close()

        else:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='w') as writer:       
              self.file.to_excel(writer, index=False)
    def create_new_data_blocks(self):
        ##Transforms to a 1d list data_block
        self.data_blocks=[] 
        if type(self.sectioned_data)==dict:
            self.sectioned_data=[self.sectioned_data]
        elif type(self.sectioned_data)==list:
            pass
        else:
            raise Exception("BadSectionedDataType")
        for data_row in self.sectioned_data:           
                self.data_blocks.append(data_row)     
        return self
    def cache_all_new_data_blocks(self):
        for block in self.data_blocks:
            if block.get('exclude_from_cache',True):
                continue
            self.cached_blocks.append(block.pop('data',None))
        return self
    def delete_file(self):
        if os.path.exists(self.file_path):
            try:
                self.file.close()
            except Exception:
                os.remove(self.file_path)
    def load_workflow_data(self):
        pass
    def load_workflow_jobs(self,workflow):
        _jobs={'active':[],'completed':[]}
        self.block={'address':'workflows.'+workflow+'.jobs'}
        self.load_deep_stuff()
        jobs=os.listdir(self.block_address)
        for job in jobs:
           
            self.block={'address':'workflows.'+workflow+'.jobs.'+job+'','file_name':'status'}
            self.load_deep_stuff()
            self.open_file()
            job_status=self.data_frame['status'].iloc[0]
            if job_status=='active':
                self.block={'address':'workflows.'+workflow+'.jobs.'+job+'','file_name':'settings'}
                self.load_deep_stuff()
                self.open_file()
                _jobs['active'].append(self.data_frame.to_dict(orient='records')[0])
        return _jobs
    def load_job_tasks(self,job,pop_keys=[]):
        tasks=[]
        s=Saver()
        s.block={'address':'workflows.'+job['workflow']+'.jobs.'+str(job['id'])+'','file_name':'status'}
        s.load_deep_stuff()
        s.open_file()
        job_status=s.data_frame['status'].iloc[0]
        if job_status=='active':
            s.block={'address':'workflows.'+job['workflow']+'.jobs.'+str(job['id'])+'.tasks'}
            s.load_deep_stuff()
            for task in os.listdir(s.block_address):
                s.block={'address':'workflows.'+job['workflow']+'.jobs.'+str(job['id'])+'.tasks.'+task+'','file_name':'settings'}
                s.load_deep_stuff()
                s.open_file()
                _=s.data_frame.to_dict(orient='records')
                if not len(_)>0:
                    continue
                tk=_[0]
                for key in pop_keys:
                    tk.pop(key,None)
               
                tasks.append(tk)
        return tasks
    def load_task_details(self,task,detail=None):
        address='workflows.'+task['workflow']+'.jobs.'+task['job']+'.tasks.'+task['id']+''
        self.block={'address':address,'file_name':'status'}
        self.load_deep_stuff()
        self.open_file()
        status=self.data_frame
        self.block={'address':address,'file_name':'settings'}
        self.load_deep_stuff()
        self.open_file()
        settings=self.data_frame.to_dict(orient='records')[0]
        #task_status=status.sort_values(by=['timestamp'],ascending=True)
        task_status=status['status'].iloc[len(status)-1]
        if detail:
            self.block={'address':address,'file_name':detail}
            self.load_deep_stuff()
            self.open_file()
            status=self.data_frame
        return {'status':task_status,'settings':settings,'detail':detail}     
    def change_state_of_task(self,task,state):
        """ address='WorkFlows.'+task['workflow']+'.jobs.'+str(task['job'])+'.tasks.'+task['id']+''
        self.block={'address':address,'file_name':'status','data':[{'status':state,'timestamp':dt.datetime.now(),'supply':[]}]}
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False) """
        from crawl.models import Task
        if not Task.objects.all().filter(uuid=task['uuid']):
            #print(task['uuid'])
            
            task=Task(**task)
            task.save()  
            task.status=state  
            task.last_state_changed_at=dt.datetime.now().timestamp()                                
        else:
             
            Task.objects.all().filter(uuid=task['uuid']).update(status=state)
            Task.objects.all().filter(uuid=task['uuid']).update(last_state_changed_at=dt.datetime.now().timestamp())
            dependent_uuid = task.get('dependent_on')
            if dependent_uuid:
                try:
                    dep_task = Task.objects.get(id=dependent_uuid)
                    Task.objects.filter(uuid=task['uuid']).update(dependent_on=dep_task)
                except Task.DoesNotExist:
                   
                    print(f"Dependent task not found yet: {dependent_uuid}")
                #address='WorkFlows.'+task['workflow']+'.jobs.'+str(task['job'])+'.tasks.'+task['id']+''
           # self.block={'address':address,'file_name':'settings','data':task}
   
                   



    def _create_dependents(self,task):
        import uuid
        import datetime as dt
        tasks=self.load_job_tasks(task,pop_keys=['id','job'])
        task_id=task.get('id')
        task.pop('id',None)
        task.pop('slug')
        task.pop('resources','')
        if task in tasks:
            index=tasks.index(task)
            ###print('Stopped creation of a duplicate task')
            ###print(task)
            ###print(tasks[index])
            return
        
        task_id=str(uuid.uuid1())
        address='WorkFlows.'+task['workflow']+'.jobs.'+str(task['job'])+'.tasks.'+task_id+''
        s=self
        task.update({'id':task_id})
        s.block={'address':address,'file_name':'settings','data':task}
        s.load_deep_stuff()
        s.add_values_to_file(load_block=False)
        s.block={'address':address,'file_name':'status','data':[{'status':'pending','supply':[],'timestamp':dt.datetime.now().timestamp()}]}
        s.load_deep_stuff()
        s.add_values_to_file(load_block=False)
        s.block={'address':address,'file_name':'output','data':[{}]}
        s.load_deep_stuff()
        s.add_values_to_file(load_block=False)  
        self.change_state_of_task(task,state='pending')

    def create_dependents_tasks(self,task):
        import threading
        th=threading.Thread(target=self._create_dependents,args=(task,))
        th.start()
        th.join()
    def get_dependents(self,task):
        pass
    def create_a_temporary_workflow(self,workflow):
        temporary_worflow={'workflow':[]}
        for i,job in enumerate(workflow):           
          
              temporary_worflow['workflow'].append(job)
        return temporary_worflow
    def search_dependents_of_job(self,task):
        
        self.block={'address':'workflows.'+task['workflow'],'file_name':'settings'}
        self.load_deep_stuff()
        self.open_file()
        workflow=self.data_frame.to_dict(orient='records')
        temporary_workflow=self.create_a_temporary_workflow(workflow)
        rep=[]        
        being_searched={'workflow':[{'flows':{'input':task.get('job',None)}}]}
    
        from base.purpose_helper import PurposeHelper
        p=PurposeHelper()
        p.data_block={'workflow':workflow}
        p.data_point=being_searched
        p.help(search=True)
        
        ###print(p.results)
        return p.results
    def create_task_dump(self,task,state):
        file_name=str(task['uuid'])
        self.block={'address':'workflows.dump.'+state+'','file_name':file_name,'data':[{'task':task,'state':state,'timestamp':dt.datetime.now().timestamp()}]}
        self.load_deep_stuff()
     
        self.add_values_to_file(load_block=False)
    def measure_time_elapsed(self):
        import time

    def measure_time_elapsed(self,start_time):
        import time
        end_time = time.perf_counter()
        return end_time - start_time
        elapsed_time = measure_time_elapsed(start_time)
    def calculate_time_elapsed(self,timestamp):
        current_time = dt.datetime.now()
        time_elapsed = current_time - pd.Timestamp(timestamp)
        time_elapsed_in_hours = pd.Timedelta(current_time-timestamp).ceil('H').total_seconds()/3600 
        return time_elapsed_in_hours
    def update_workflow_register(self,active_workflows):
        import time
        register_address={'address':'workflows','file_name':'register'}
        self.block=register_address
        self.load_deep_stuff()
        self.open_file()
        register=self.data_frame
        register_dict=register.to_dict(orient='records')
        if self.empty_file:
            task_ids=[]
        else:
            task_ids=register['id'].to_list()
        self.block={'address':'allocated'}
        self.load_resources()
        for resource in os.listdir(self.block_address):
            self.block={'address':'allocated','file_name':resource.split('.')[0]}
            self.load_resources()
            self.open_file()
            r=self.data_frame.to_dict(orient='records')[0]
            #print('found allocated resource, checking workflow register and updating now')
            t=register.loc[register['id']==r['task_id']]
            if len(t)>0:
                for index, row in t.iterrows():
                    if register_dict[index]['task'].get('resources'):
                        register_dict[index]['task']['resources'].update({r['type']:r})
                    else:
                        register_dict[index]['task'].update({'resources':{r['type']:r}})
                os.remove(self.file_path)
            else:
                pass
                #print('allocated resource task not found')
                
  
        statuses=['pendingg','pending','failed','completed']
        start_time = time.perf_counter()
        for status in statuses:
            self.block={'address':'workflows.dump.'+status+''}
            self.load_deep_stuff()
            for dump in os.listdir(self.block_address):
                self.block={'address':'workflows.dump.'+status+'','file_name':dump.split('.')[0]}
                self.load_deep_stuff()  
                file_path=os.path.join(self.block_address,dump)  

               
                self.open_file()
                row=self.data_frame.to_dict(orient='records')[0]    
                
                if len(task_ids)==0:
                    if row['task']['workflow'] not in active_workflows:
                        continue
                    task_ids.append(dump)  
                    register_dict.append({'status':status,'task':row['task'],'last_state_changed_at':row['timestamp'],'id':dump.split('.')[0]})                
                else:
                    if dump.split('.')[0] in task_ids:
                        record = register.loc[register['id'] == dump.split('.')[0]]
                        if len(record)==1:
                            counter=0
                            for index,row in record.iterrows():        
                                register_dict[index]['status']=status
                                register_dict[index]['last_state_changed_at']=dt.datetime.now()
                                counter+=1
                                if counter>1:
                                    del register_dict[index]
                    else:
   
                        self.open_file()
                        row=self.data_frame.to_dict(orient='records')[0]              
                        register_dict.append({'workflow':row['task']['workflow'],'job':row['task']['job'],'status':status,'task':row['task'],'last_state_changed_at':dt.datetime.now(),'id':dump.split('.')[0]})   
                        task_ids.append(dump)
                        if row['task']['workflow'] not in active_workflows:
                            continue
                os.remove(file_path)
                 
                    
                    
               
        ##print(self.measure_time_elapsed(start_time))
                
        if len(register_dict)>0:
            self.overwrite=True
            self.block={'address':register_address['address'],'data':register_dict,'file_name':'register'}
            self.load_deep_stuff()
            self.add_values_to_file(load_block=False)
            
            self.overwrite=False
    def create_proxy_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'proxies.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
    def create_request_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'requests.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        self.block={'address':'requests.records','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
    def create_profile_request_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'profiles.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        self.block={'address':'profiles.records','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)      
    def update_proxies_register(self):
        self.block={'address':'proxies.dump'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        for i,record in enumerate(records):
            self.block={'address':'proxies.dump','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            if self.data_frame.empty:
                continue
            row=self.data_frame.to_dict(orient='records')[0]
            records_.append(row)
            os.remove(self.file_path)
        if len(records_)>0:
            self.block={'address':'proxies','file_name':'requests_register','data':records_}
            self.load_resources()
            self.add_values_to_file(load_block=False)
    def read_proxies_requests_register(self):
  
        self.block={'address':'proxies','file_name':'requests_register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame
        if df.empty:
            return None, None
        df.loc[:, 'time_elapsed_in_hours']=df['timestamp'].apply(self.calculate_time_elapsed)
        groupby='proxy'
        if not 'proxy' in df.columns:
            groupby='ip_address'
        proxy_groups=df.groupby([groupby])
        output={}
        min_output={}
        time_record=[]
        for proxy in proxy_groups.groups:
            proxy_grouped_df=proxy_groups.get_group(proxy,)
            service_groups=proxy_grouped_df.groupby(['service'])
            output.update({proxy:{}})
            for service in service_groups.groups:
                service_grouped_df=service_groups.get_group(service,)
                time_record_groups=service_grouped_df.groupby(['time_elapsed_in_hours'])
                for i in range(0,24):
                    if i in time_record_groups.groups:

                            time_elapsed_grouped_df=time_record_groups.get_group(i,)
                            time_record.append({i:len(time_elapsed_grouped_df)})
                    else:
                        time_record.append({i:0}) 
                time_record_stats={}
                time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,24)})
                time_record_stats.update({'30h':self.get_workrecord_in_last_n_hours(time_record,30)})
                time_record_stats.update({'36h':self.get_workrecord_in_last_n_hours(time_record,36)})
                time_record_stats.update({'42h':self.get_workrecord_in_last_n_hours(time_record,42)})
                time_record_stats.update({'12h':self.get_workrecord_in_last_n_hours(time_record,12)})
                time_record_stats.update({'1h':self.get_workrecord_in_last_n_hours(time_record,1)})
                time_record_stats.update({'6h':self.get_workrecord_in_last_n_hours(time_record,6)})
                min_output.update({proxy:{service:{'time_record':time_record,'time_record_stats':time_record_stats,'total':len(service_grouped_df)}}})
        ##print(min_output)
        for proxy in proxy_groups.groups:
            proxy_grouped_df=proxy_groups.get_group(proxy,)
            service_groups=proxy_grouped_df.groupby(['service'])
            output.update({proxy:{}})
            for service in service_groups.groups:        
                service_grouped_df=service_groups.get_group(service,)
                output[proxy].update({service:[],'total':len(service_grouped_df)})
                end_point_groups=service_grouped_df.groupby(['end_point'])
                for end_point_index,end_point in enumerate(end_point_groups.groups):
                    output[proxy][service].append({end_point:{}})
                    end_point_grouped_df=end_point_groups.get_group(end_point,)
                    data_point_groups=end_point_grouped_df.groupby(['data_point'])
                    for data_point in data_point_groups.groups:
                        output[proxy][service][end_point_index][end_point].update({data_point:{}})
                        data_point_grouped_df=data_point_groups.get_group(data_point,)
                        status_code_groups=data_point_grouped_df.groupby(['status_code'])
                        for status_code in status_code_groups.groups:
                            status_code_grouped_df=status_code_groups.get_group(status_code,)
                            output[proxy][service][end_point_index][end_point][data_point].update({status_code:{'total':len(status_code_grouped_df)}})
                            time_elapsed_groups=status_code_grouped_df.groupby(['time_elapsed_in_hours'])
                            time_record=[]
                            for i in range(0,24):
                                if i in time_elapsed_groups.groups:

                                        time_elapsed_grouped_df=time_elapsed_groups.get_group(i,)
                                        time_record.append({i:len(time_elapsed_grouped_df)})
                                else:
                                    time_record.append({i:0})                          
                                output[proxy][service][end_point_index][end_point][data_point][status_code].update({'time_record':time_record})
        return min_output,output
    
    def update_profiles_request_register(self):
        return
        self.block={'address':'requests.records'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        time_start=dt.datetime.now()
        for i,record in enumerate(records):
            self.block={'address':'requests.records','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            if self.data_frame.empty:
                continue
            row=self.data_frame.to_dict(orient='records')[0]
            
            records_.append(row)
            from base.datetime_utils import parse_time_stamp_to_datetime_and_localize_to_timezone
            d=row['datetime']
                  
            row['task_id']=row['task']
            row.pop('task')
            
            from crawl.models import RequestRecord,Task
            t=Task.objects.all().filter(uuid=row['task_id'])
            if t:
                t=t[0]
                row['task_id']=t.id
            else:
                pass
            try:
                import json
                json.loads(row['data'])
            except Exception as e:
                row['data']={}
                row['text']=row['data']
            else:
                row['data']=json.loads(row['data'])
            try:
                if row.get('json'):
                    row['payload']=row['json']
                    row.pop('json')
                row.pop('object_type')
                data=row['data']
             
                if type(row.get('error'))==float:
                    row['error']={}

                datetime_string=row['datetime']
                
                aware_datetime = timezone.make_aware(datetime_string, timezone.get_default_timezone()) # Or a specific timezone if you know it
                row['datetime']=aware_datetime

                r=RequestRecord(**row)
                #r.save()
                

                r.data=json.dumps(data)
                os.remove(self.file_path)
            except Exception as e:
                pass
            
            """             r.save()
        if records:
            self.block={'address':'profiles','file_name':'requests_register','data':records_}
            self.load_resources()
            self.add_values_to_file(load_block=False) """
    def get_workrecord_in_last_n_hours(self,work_logs,n_hours):
        out=0
        for i,work_record in enumerate(work_logs):
       
            for key,value in work_record.items():
                if n_hours>=key:
                    
                    if value>0:
                        out+=value
        return out
    def update_reports_register(self):
        records=[]
        self.block={'address':'dump'}
        self.load_reports()
        for report in os.listdir(self.block_address):
            self.block={'address':'dump.','file_name':report.split('.')[0]}
            self.load_reports()
            self.open_file()
            df=self.data_frame
            record=df.to_dict(orient='records')[0]
            records.append(record)
        if len(records)>0:
            self.block={'address':'','file_name':'register','data':records}
            self.load_reports()
            self.add_values_to_file(load_block=False)
            def convert_timestamp_to_str(inp):
                try:
                    v=inp
                    __=str(v._short_repr)
                except Exception as e:
                    __=str(v)
                return
            

            self.file['datetime']=self.file['datetime'].map(convert_timestamp_to_str)
            self.file.fillna(' ',inplace=True)
            self.push_data_frame_to_google_sheet(self.file,**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1DBCUWwcjoA0GSB8IG1ihuCBVIMebxkLXaF5jIOvT5AQ/edit#gid=0'})
    def read_browser_profiles_request_register(self):        
        self.block={'address':'profiles','file_name':'requests_register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame
        if df.empty:
            return {},{}
        service_groups=df.groupby(['service'])
        df.loc[:, 'time_elapsed_in_hours']=df['timestamp'].apply(self.calculate_time_elapsed)   
        output={}
        min_output={}
        time_record=[]
        service_groups=df.groupby(['service'])
        for service in service_groups.groups:
            service_grouped_df=service_groups.get_group(service,)
            bot_groups=service_grouped_df.groupby(['bot_username'])
            min_output.update({service:[]})
            for bot in bot_groups.groups:
                bot_grouped_df=bot_groups.get_group(bot,)
                time_record_groups=bot_grouped_df.groupby(['time_elapsed_in_hours'])
        
                for i in range(0,48):
                    if i in time_record_groups.groups:

                            time_elapsed_grouped_df=time_record_groups.get_group(i,)
                            time_record.append({i:len(time_elapsed_grouped_df)})
                    else:
                        time_record.append({i:0}) 
                time_record_stats={}
                time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,24)})
                time_record_stats.update({'30h':self.get_workrecord_in_last_n_hours(time_record,30)})
                time_record_stats.update({'36h':self.get_workrecord_in_last_n_hours(time_record,36)})
                time_record_stats.update({'42h':self.get_workrecord_in_last_n_hours(time_record,42)})
                time_record_stats.update({'12h':self.get_workrecord_in_last_n_hours(time_record,12)})
                time_record_stats.update({'1h':self.get_workrecord_in_last_n_hours(time_record,1)})
                time_record_stats.update({'6h':self.get_workrecord_in_last_n_hours(time_record,6)})
                min_output[service].append({bot:{'time_record':time_record,'time_record_stats':time_record_stats,'total':len(service_grouped_df)}})
      
        time_record=[]
        for service in service_groups.groups:
            output.update({service:[]})
           
            service_grouped_df=service_groups.get_group(service,)
            bot_groups=service_grouped_df.groupby(['bot_username'])
           
            for bot_index,bot in enumerate(bot_groups.groups):
                bot_grouped_df=bot_groups.get_group(bot,)
                end_point_groups=bot_grouped_df.groupby(['end_point'])
                output[service].append({bot:[]})
               
                for end_point_index,end_point in enumerate(end_point_groups.groups):
                    output[service][bot_index][bot].append({end_point:{}})
                    end_point_grouped_df=end_point_groups.get_group(end_point,)
                    data_point_groups=end_point_grouped_df.groupby(['data_point'])
                    for data_point in data_point_groups.groups:
                        output[service][bot_index][bot][end_point_index][end_point].update({data_point:{}})
                        data_point_grouped_df=data_point_groups.get_group(data_point,)
                        status_code_groups=data_point_grouped_df.groupby(['status_code'])
                        for status_code in status_code_groups.groups:
                            status_code_grouped_df=status_code_groups.get_group(status_code,)
                            output[service][bot_index][bot][end_point_index][end_point][data_point].update({status_code:{'total':len(status_code_grouped_df)}})

                            time_elapsed_groups=status_code_grouped_df.groupby(['time_elapsed_in_hours'])
                            time_record=[]
                            for i in range(0,49):
                                if i in time_elapsed_groups.groups:
                                        time_elapsed_grouped_df=time_elapsed_groups.get_group(i,)
                                        time_record.append({i:len(time_elapsed_grouped_df)})
                                else:
                                    time_record.append({i:0})                          
                                output[service][bot_index][bot][end_point_index][end_point][data_point][status_code].update({'time_record':time_record})
                            
                            
                            time_record_stats={}

                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,24)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,30)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,36)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,42)})
                            time_record_stats.update({'12h':self.get_workrecord_in_last_n_hours(time_record,12)})
                            time_record_stats.update({'1h':self.get_workrecord_in_last_n_hours(time_record,1)})
                            time_record_stats.update({'6h':self.get_workrecord_in_last_n_hours(time_record,6)})
                            output[service][bot_index][bot][end_point_index][end_point][data_point][status_code].update({'time_record_stats':time_record_stats})
        return min_output,output
    def update_profiles_register(self):
        self.block={'address':'profiles.newbies'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        time_start=dt.datetime.now()
        for i,record in enumerate(records):
            self.block={'address':'profiles.newbies','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            if not self.data_frame.empty:
                row=self.data_frame.to_dict(orient='records')[0]
                records_.append(row)
                os.remove(self.file_path)
        if records_:
            self.block={'address':'profiles','file_name':'register','data':records_}
            self.load_resources()
            self.add_values_to_file(load_block=False)
             
        self.block={'address':'profiles','file_name':'register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame    
        if df.empty:
            return 
        """        self.block={'address':'profiles.allocated'}
        self.load_resources()
        a_s=[]
        for r in os.listdir(self.block_address):
            self.block={'address':'profiles.allocated','file_name':r.split('.')[0]}
            self.load_resources()       
            self.open_file()
            _row=self.data_frame.iloc[0]
            row=df.loc[(df['username']==_row['username'])&(df['service']==_row['service'])]
            if not row.empty:
                df.loc[row.index[0],'available']=_row['available']
                df.loc[row.index[0],'logged_in']=_row['logged_in']
                
            
        
                os.remove(self.file_path)
            else:
                os.remove(self.file_path)
        self.block={'address':'profiles.deallocated'}
        self.load_resources()
        a_s=[]
        for r in os.listdir(self.block_address):
            self.block={'address':'profiles.deallocated','file_name':r.split('.')[0]}
            self.load_resources()       
            self.open_file()
            _row=self.data_frame.iloc[0]
            row=df.loc[(df['username']==_row['username'])&(df['service']==_row['service'])]
            df.loc[row.index[0],'available']=_row['available']
            df.loc[row.index[0],'available']=_row['logged_in']

            os.remove(self.file_path) """
        """         if not df.empty:
            self.block={'address':'profiles','file_name':'register','data':df.to_dict(orient='records')}
            self.load_resources()
            self.overwrite=True
            self.add_values_to_file(load_block=False) """
    
    def read_profiles_register(self):
        block={'address':'profiles','file_name':'register'}
        self.block=block
        self.load_resources()
        self.open_file()
        return self.data_frame
    def read_proxies_register(self):
        block={'address':'proxies','file_name':'register'}
        self.block=block
        self.load_resources()
        self.open_file()
        return self.data_frame
        
    def get_profiles_stats(self,service='instagram',task={}):
        self.block={'address':'profiles','file_name':'settings'}
        self.load_resources()
        self.open_file()
        if not self.data_frame.empty:
            settings=self.data_frame.to_dict(orient='records')[0]
        else:
            return []
        min_output,output=self.read_browser_profiles_request_register()
        import os
        import django

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerserver.settings')
        django.setup()
        from crawl.models import ChildBot,Task
        c=list(ChildBot.objects.all().exclude(username__in=[Task.objects.all().filter(status='running').values_list('profile',flat=True)]).values())
        profiles_df=pd.DataFrame(c)

        
        if profiles_df.empty:
            return pd.DataFrame()
        good_bots=[]
        exclude_usernames=[]
        if min_output and output:    
            
            exclude_usernames=[]
            for _bot in min_output[service]:
                for key,value in _bot.items():
                    username=key
                    bot=_bot[username]
                    right_record=0
                    t_tests=0
                    time_record_stats=bot['time_record_stats']
                    for key, value in time_record_stats.items():
                        if key in settings[service]:
                            t_tests+=1
                            if value > settings[service][key]:
                                pass
                                #print('max requests exceeded for '+str(key))
                            else:
                                right_record+=1
                                ##print('good bot for'+str(key))
            
                    ##print('Goodness level is '+str(right_record))
                    ##print('ideal level is' +str(t_tests))
                    if right_record<4:
                         exclude_usernames.append(username)
                    else:
                        row=profiles_df.loc[(profiles_df['username']==username)]# & (profiles_df['available']==True)]
                    
                        if not row.empty:
                            good_bots.append(row.to_dict(orient='records')[0] )
                        else:
                            exclude_usernames.append(username)
            df=pd.DataFrame(good_bots)
            
        else:
            return profiles_df
        
        if df.empty:
            v=[]
          
            v=list(set(profiles_df['username'])-set(exclude_usernames))
            ##print(v)
        else:
            v=list(set(profiles_df['username'])-set(df['username']))
        idle_bots=[]
        for bot in v:
        
            buka=profiles_df.loc[(profiles_df['username']==bot)]# & profiles_df['available']==True]
            if len(buka)>0:
                buka=buka.to_dict(orient='records')[0]
                good_bots.insert(0,buka)
        df=pd.DataFrame(good_bots)
        return df
    def get_proxies_stats(self,service='instagram',task={}):
        
        self.block={'address':'proxies','file_name':'settings'}
        self.load_resources()
        self.open_file()
        if not self.data_frame.empty:
            settings=self.data_frame.to_dict(orient='records')
        else:
            return []
        
        intersect=[]
        min_output,output=self.read_proxies_requests_register()
        if not min_output:
            return []
        proxies_df=self.read_proxies_register()
        output_stats={}
        exclude_proxies=[]
        for key, value in settings.items():
            output_stats.update({key:[]})
        for key, value in min_output.items():
            proxy_url=key
            proxy_record=min_output[proxy_url]

            for service,_settings in settings.items():
                right_record=0
                t_tests=0
                service_proxy_record=proxy_record.get(service,{})
                time_record_stats=service_proxy_record.get('time_record_stats',{})
                for key, value in time_record_stats.items():
                    if key in _settings:
                        t_tests+=1
                        if value > _settings[key]:
                            pass
                            ##print('max requests exceeded for '+str(key))
                        else:
                            right_record+=1
                if t_tests==0:
                    ratio=0
                else:
                
                    ratio=right_record/t_tests

                if proxies_df.empty:
                    output_stats[service].append([])
                else:
                    if ratio==0 or ratio ==1 or ratio>0.5:
                        row=proxies_df.loc[proxies_df['url']==proxy_url]  
                        if row.empty:
                            pass
                        else:
                            
                            output_stats[service].append(row.to_dict(orient='records')[0])
                            exclude_proxies.append(proxy_url)
                    intersect=list(set(proxies_df['url'])-set(exclude_proxies))
      
        self.block={'address':'workflows','file_name':'register'}
        self.load_deep_stuff()
        self.open_file()
        df=self.data_frame
    
     
        for proxy_url in intersect:
            row=proxies_df.loc[proxies_df['url']==proxy_url]
            if not row.empty:
                for key,value in output_stats.items():
                    
                    if not type(row)==dict:
                        row=row.to_dict(orient='records')[0]
                    usage_counter=self.get_proxy_usage_stats(df,row['url'],service) 
                    row.update({'usage_counter':usage_counter})
                    output_stats[key].append(row)
                   
                    

        return output_stats
    def get_proxy_usage_stats(self,df,proxy_url,service):
        usage_counter=0 
        if df.empty:
            return usage_counter
        df=df.loc[(df['status']=='pendingg') | (df['status']=='pending') ]
        for index,row in df.iterrows():
            task=row
            if task['service']==service:
                if task.get('resources'):
                    resources=task.get('resources')
                    if resources.get('proxy',False):
                        proxy=resources.get('proxy')
                        if proxy.get('url')==proxy_url:
                            #print('Found One active Usage for proxy')
                            usage_counter+=1
        return usage_counter
    def allocate(self,resource,resource_type,task):
        
        #self.create_output(_)
        
        file_name=str(uuid.uuid1())
        resource.update({'task_id':task['uuid'],'type':resource_type})

        resource.update({'task_id':task['uuid']})
        self.block={'address':'allocated','file_name':file_name,'data':resource}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        if resource_type=='profile':
            resource.update({'available':False})
            self.block={'address':'profiles.allocated','file_name':file_name,'data':resource}
            __=resource['username']
        elif resource_type=='proxy':
            self.block={'address':'proxies.allocated','file_name':file_name,'data':resource}
            __=resource['url']
        _={'service':'resource_manager','end_point':'allocate','data_point':'create_allocation_entry',
           'log':'resource_allocation_entry','resource':__,'task':task,'resource_type':resource_type
           }
        self.load_resources()
        self.add_values_to_file(load_block=False)       
    def deallocate(self,resource,resource_type,task):
            file_name=str(uuid.uuid1())
            resource.update({'available':True})
            
            if resource_type=='profile:':
                self.block={'address':'profiles.deallocated','file_name':file_name,'data':resource}
                self.load_resources()
                self.add_values_to_file()
    def load_all_active_workflows(self):    
        s=Saver() 
        s.block={'address':'WorkFlows'}
        s.load_deep_stuff()
        names=[]
        active_workflows=[]
        workflows=os.listdir(s.block_address)
        wfs=[]
        for workflow in workflows:
            if  workflow=='__pycache__'or workflow =='drafts' or workflow=='register.json' or workflow=='dump' or workflow=='register' or '.py' in workflow:
                continue
            names.append(workflow)
            s.block={'address':'WorkFlows.'+workflow+'','file_name':'status'}
            s.load_deep_stuff()
            s.open_file()
            status=s.data_frame
            status=status['status'].iloc[len(status)-1]
            if status=='active':
                active_workflows.append(workflow)
            else:
                continue
            s.block={'address':'WorkFlows.'+workflow+'','file_name':'settings'}
            s.load_deep_stuff()
            s.open_file()
            _=s.data_frame.to_dict(orient='records')
            wfs.append(_)
            
                    

       
        
        return active_workflows   
    def push_data_frame_to_google_sheet(self,data,update=False,**kwargs):
        if kwargs.get('spreadsheet_url'):
            if kwargs.get('worksheet_name'):
                worksheet=kwargs.get('worksheet_name')
            if len(data)>0:
                from base.googlesheets import GoogleSheet
                g=GoogleSheet()
                g.initialize_connection()
                g.spreadsheet_url=kwargs.get('spreadsheet_url')    
                g.data=data             
                g.open_google_sheet().find_worksheet(worksheet).read_worksheet().update_worksheet(drop_duplicates=False,update=update)
    def save_screenshot(self,bin):
        self.block={'address':'screenshots'}
        self.load_screenshots()
        
        file_name=str(uuid.uuid1())+'.jpg'
        pth=os.path.join(self.block_address,file_name)
        open(pth, "wb").write(bin)
        return file_name
    def read_data_from_storage_block(self,address,service):
        self.service=service
        self.block={'address':address}
        self.load_block()
        data=[]
        for file in os.listdir(self.block_address):
            self.block={'address':address,'file_name':file.split('.')[0]}
            self.load_block()
            self.open_file() 
            data.append(self.data_frame.to_dict(orient='records')[0])
        return data
    def write_data_to_storage_block(self,address,service,data,file_name=None):
        self.service=service
        self.block={'address':address,'data':data}
        
        if not file_name:
            for row in data:
                id=uuid.uuid1()
                self.block={'address':address,'file_name':id,'data':row}
                self.load_block()
    def save_blocks_as_task_output(self,id,data,block_name=False):
        self.block={'address':'tasks.'+str(id)+'.outputs.blocks','file_name':str(uuid.uuid1()),'data':data,'file_name':self.block_id}
        self.load_deep_stuff()
        self.overwrite=False
        self.add_values_to_file(load_block=False)
    def open_blocks_from_task_output(self,id,exclude_blocks=[]):
        self.block={'address':'tasks.'+str(id)+'.outputs.blocks'}
        self.load_deep_stuff()
        output_blocks=self.block_address
        resp={}
        for output_block in os.listdir(output_blocks):
            output_block=output_block.split('.')[0]
            if output_block in exclude_blocks:
                continue
            else:
                self.block={'address':'tasks.'+str(id)+'.outputs.blocks','file_name':output_block}
                self.load_deep_stuff()
                self.open_file()
                if self.data_frame.empty:
                    pass
                else:
                    data=self.data_frame.to_dict(orient='records')
                    resp.update({output_block:[]})
                    for row in data:
                        block_address=row['block_address']
                        file_name=row['file_name']
                        self.block_address=block_address
                        self.block={'file_name':file_name}
                        self.open_file()
                        if not self.data_frame.empty:
                            resp[output_block].append(self.data_frame.to_dict(orient='records')[0])
                
                           
        return resp        

    def add_output_block_to_consumed(self,id,output_block):
        self.block={'address':'tasks.'+str(id)+'.inputs.consumed.blocks','file_name':output_block,'data':[{}]}
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False)
    def get_consumed_blocks(self,id):
        self.block={'address':'tasks.'+str(id)+'.inputs.consumed.blocks'}
        self.load_deep_stuff()
        resp=[]
        for block in os.listdir(self.block_address):
            resp.append(block.split('.json')[0])
        return resp
    def get_consumed_downloads(self,id):
        self.block={'address':'tasks.'+str(id)+'.inputs.consumed.downloads'}
        self.load_deep_stuff()
        resp=[]
        for block in os.listdir(self.block_address):
            resp.append(block.split('.')[0])
        return resp
    def add_output_block_to_consumed_blocks_for_audience_for_client(self,client_id,audience_id,output_block):
        self.block={'address':'audience.'+str(audience_id)+'.clients.'+str(client_id)+'.consumed.blocks','file_name':output_block}
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False)
    def get_consumed_blocks_for_audience_for_client(self,client_id,audience_id):
        self.block={'address':'audience.'+str(audience_id)+'.clients.'+str(client_id)+'.consumed.blocks'}
        self.load_deep_stuff()
        resp=[]
        for block in os.listdir(self.block_address):
            resp.append(block.split('.')[0])
        return resp
    def save_audience_outputs(self,id,data):
        self.block={'address':'audience.'+str(id),'file_name':str(uuid.uuid1()),'data':data}
        self.load_block()
        self.add_values_to_file(load_block=True)
    def retrieve_audience_outputs(self,id,exclude_blocks,keys=False,size=False):
        self.block={'address':'audience.'+str(id),'file_name':str(uuid.uuid1())}
        self.load_block()
        counter=0
        if keys:
            
            outputs={}
        else:
            outputs=[]
        for output in os.listdir(self.block_address):
            if output.split('.')[0] in exclude_blocks:
                continue
        
            self.block.update({'file_name':output.split('.')[0]})
            self.open_file()
            if not self.data_frame.empty:
                if keys:
                    counter+=len(self.data_frame.to_dict(orient='records'))
                    outputs.update({output.split('.')[0]:self.data_frame.to_dict(orient='records')})
                else:
                    counter+=len(self.data_frame.to_dict(orient='records'))
                    outputs.extend(self.data_frame.to_dict(orient='records'))
            if size:
                if counter>=size:
                    return outputs
        return outputs
    def create_task_outputs(self,id,data,block_name=False,medias=False,save_to_datahouse=False,file_name=False):
        if save_to_datahouse:
            data.update({'object_type':'output'})
        if not file_name:
            file_name=str(uuid.uuid1())
        
        if block_name:
            self.block={'address':'tasks.'+str(id)+'.outputs.'+str(block_name),'file_name':file_name,'data':data}
        else:
            self.block={'address':'tasks.'+str(id)+'.outputs','file_name':file_name,'data':data}
       
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False)
        if medias:
            for media in medias:
                if not media:
                    continue
                import shutil
                self.block={'address':os.path.join(self.block_address,'medias')}
                self.load_block()
                
                try:
                    shutil.copy2(media['file_path'],self.block_address)
                except Exception as e:
                    pass
    def create_task_inputs(self,id,data,block_name=False,file_name=False):
      
        if not file_name:
            file_name=str(uuid.uuid1())
        
        if block_name:
            self.block={'address':'tasks.'+str(id)+'.inputs.'+str(block_name),'file_name':file_name,'data':data}
        else:
            self.block={'address':'tasks.'+str(id)+'.inputs','file_name':file_name,'data':data}
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False)
        
    def create_task_failures(self,id,data=[{}],file_name=False):
        if not file_name:
            file_name=str(uuid.uuid1())
        self.block={'address':'tasks.'+str(id)+'.failures','file_name':file_name,'data':data}
        self.load_deep_stuff()
        self.add_values_to_file(load_block=False)
    def read_task_outputs(self,uuid,block_name=False,exclude_blocks=[],keys=False,size=False):
        
        if keys:
            outputs={}
        else:
            outputs=[]
        if block_name:
            self.block={'address':'tasks.'+str(uuid)+'.outputs.'+str(block_name)}
        else:
            self.block={'address':'tasks.'+str(uuid)+'.outputs'}
        self.load_deep_stuff()
        block_address=self.block_address

               
        self.load_deep_stuff()
        for output in os.listdir(self.block_address):
            if os.path.isdir(os.path.join(block_address,output)):
                continue
            if size:
                    if len(outputs)>size:
                        return outputs
            if output.split('.')[0] in exclude_blocks:
                continue
            self.block.update({'file_name':output.split('.')[0]})
            self.open_file()
            if not self.data_frame.empty:
                if keys:
                    outputs.update({output.split('.')[0]:self.data_frame.to_dict(orient='records')})
                else:
                    outputs.extend(self.data_frame.to_dict(orient='records'))
        return outputs
    
    def read_task_outputs_redundant(self,uuid,block_name=False,exclude_blocks=[],keys=False,size=False):
        
        if keys:
            outputs={}
        else:
            outputs=[]
        if block_name:
            self.block={'address':'tasks.'+str(uuid)+'.outputs.'+str(block_name)}
        else:
            self.block={'address':'tasks.'+str(uuid)+'.outputs'}
        self.load_deep_stuff()
        block_address=self.block_address
        if block_name:
            if len(os.listdir(self.block_address))>0:
                for obj in os.listdir(self.block_address):
                    #print(obj)
                    if os.path.isdir(os.path.join(block_address,obj)):
                        self.block={'address':block_address+'.'+str(obj)}
                        self.load_deep_stuff()
                        for output in os.listdir(os.path.join(self.block_address)):
                            if size:
                                if len(outputs)>size:
                                    return outputs
                            if output.split('.')[0] in exclude_blocks:
                                
                                continue
                            
                            self.block.update({'file_name':output.split('.')[0]})
                            self.open_file()
                    
                            if not self.data_frame.empty:
                                if keys:
                                    outputs.update({output.split('.')[0]:self.data_frame.to_dict(orient='records')})
                                else:
                                    outputs.extend(self.data_frame.to_dict(orient='records'))
                    else:
                        if obj.split('.')[0] in exclude_blocks:
                            continue
                        self.block.update({'file_name':obj.split('.')[0]})
                        self.open_file()
                        
                        if not self.data_frame.empty:
                            if keys:
                                outputs.update({obj.split('.')[0]:self.data_frame.to_dict(orient='records')})
                            else:
                                outputs.extend(self.data_frame.to_dict(orient='records'))        
            if not block_name:
               
                self.load_deep_stuff()
                for output in os.listdir(self.block_address):
                    if size:
                            if len(outputs)>size:
                                return outputs
                    if output.split('.')[0] in exclude_blocks:
                        continue
                    self.block.update({'file_name':output.split('.')[0]})
                    self.open_file()
                    if not self.data_frame.empty:
                        if keys:
                            outputs.update({output.split('.')[0]:self.data_frame.to_dict(orient='records')})
                        else:
                            outputs.extend(self.data_frame.to_dict(orient='records'))
        return outputs
    

    def read_task_outputs_for_run_id(self, uuid, run_id, exclude_blocks=None, keys=False, size=False):
        """
        Reads outputs for a specific run_id inside the logs block.
        Excludes blocks listed in exclude_blocks and optionally returns data as a dict (keys=True).
        """
        if exclude_blocks is None:
            exclude_blocks = []

        outputs = {} if keys else []

        # Point to: tasks.{uuid}.outputs.logs.{run_id}
        self.block = {'address': f'tasks.{uuid}.outputs.logs.{run_id}'}
        self.load_deep_stuff()
        
        try:
            for output_file in os.listdir(self.block_address):
                name = output_file.split('.')[0]

                if name in exclude_blocks:
                    continue

                if size and len(outputs) >= size:
                    break

                self.block.update({'file_name': name})
                self.open_file()

                if not self.data_frame.empty:
                    data = self.data_frame.to_dict(orient='records')
                    if keys:
                        outputs[name] = data
                    else:
                        outputs.extend(data)

        except FileNotFoundError:
            # Folder for run_id doesn't exist
            pass

        return outputs



    def read_task_inputs(self,uuid,block_name=False,exclude_blocks=[],keys=False,size=False):
        if keys:
            inputs={}
        else:
            inputs=[]
        if block_name:
            self.block={'address':'tasks.'+str(uuid)+'.inputs.'+str(block_name)}
        else:
            self.block={'address':'tasks.'+str(uuid)+'.inputs'}
        self.load_deep_stuff()
        block_address=self.block_address
        for input in os.listdir(self.block_address):
                if size:
                        if len(inputs)>size:
                            return inputs
                if input.split('.')[0] in exclude_blocks:
                    continue
                self.block.update({'file_name':input.split('.')[0]})
                self.open_file()
                if not self.data_frame.empty:
                    if keys:
                        inputs.update({input.split('.')[0]:self.data_frame.to_dict(orient='records')})
                    else:
                        inputs.extend(self.data_frame.to_dict(orient='records'))
        return inputs
    def read_task_output(self,uuid):
        self.block={'address':'tasks.'+uuid+'.outputs','file_name':uuid}
        self.load_deep_stuff()
        self.open_file()
        if not self.data_frame.empty:

            return self.data_frame.to_dict(orient='records')
        return False

        
    def get_payload_data(self,service,data_point):
        self.block={'address':'request_cache','file_name':data_point}
        self.load_block()
        self.open_file()
        if not self.data_frame.empty:
            if self.data_frame.to_dict(orient='records')[0].get('payload'):
                return self.data_frame.to_dict(orient='records')[0].get('payload')
        return False
    def get_next_cursor(self,identifier=False,service=False,data_point=False,block=False):
        
        pd.options.display.float_format = '{:.0f}'.format
        if not block:
            identifier=identifier.replace('.',',')
            if 'user' in data_point:
                if data_point=='user_posts':
                    dp='posts'
                elif data_point =='user_info_graphql':
                    dp='info'
                elif data_point=='user_followers':
                    dp='followers'
                elif data_point=='user_following':
                    dp='following'
                self.block={'address':'users.'+identifier+'.'+dp,'file_name':'register'}
            elif data_point=='location_posts':
                dp='location_posts'
            
                

            self.block={'address':'users.'+identifier+'.'+dp,'file_name':'register'}
        else:
            
            self.block=block
        self.load_block()
        self.open_file()     
        if self.empty_file:
            #print('FRegister dont exist')
            return {}
        else:
            df=self.data_frame
            df = df.where(pd.notnull(df), None)    
            sorted_df=df.sort_values(['last_scraped_at'],ascending=False)  
            row=sorted_df.iloc[0].to_dict()
     
            ##print(format(,'f'))

            if not row.get('has_next_page'):
                return {'has_next_page':False}
            return {'next_cursor':row.get('next_cursor') if type(row.get('next_cursor',''))==str or type(row.get('next_cursor'))==int or type(row.get('next_cursor'))==float else None,
                    'end_cursor':row.get('end_cursor') if type(row.get('end_cursor',''))==str or type(row.get('end_cursor'))==int else None,
                    
                    'has_next_page':row.get('has_next_page'),
                    'total_pages_crawled':len(sorted_df),
                    
                    'id':row.get('id'),
                    'name':row.get('name'),
                    'slug':row.get('slug'),
                    'next_max_id':row.get('next_max_id',None),
                    'next_media_ids':row.get('next_media_ids',None),
                    'next_page':row.get('next_page',None)
                    }
                   

    def get_logs_for_task(self,task):
        import datetime as dt
        if task:
          
            logs={}
            self.block={'address':'tasks.'+str(task)+'.logs'}
            self.load_deep_stuff()
            logs.update({task:[]})
            for log in os.listdir(self.block_address):

                self.block.update({'file_name':log.split('.')[0]})
                self.open_file()
                if not self.data_frame.empty:
                    row=self.data_frame.to_dict(orient='records')[0]
                    row.pop('task',False)
                    row.pop('end_point',False)
                    row.pop('data_point',False)
                    if row['type']=='task_preparation_failed':
                        continue
                    row.pop('_data_point')
                    row.update({'end_point':row['_end_point'],'message':row['type']})
                    row.pop('type')
                    row.pop('_end_point')
                    timestamp=row['datetime']
                    dt_obj = dt.datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S.%f')
                    formatted_str = dt_obj.strftime('%A, %B %d, %Y at %I:%M %p')
                    
                    row.update({"datetime":formatted_str})
                    row.pop('time_elapsed',False)
                    logs[task].append(row)
              
            return logs
        else:
            self.block={'address':'tasks'}
            self.load_deep_stuff()
            tasks=[]
            for task in os.listdir(self.block_address):
                tasks.append(task.split('.')[0])
            logs={}
            for task in tasks:
                
                self.block={'address':'tasks.'+str(task)+'.logs'}
                self.load_deep_stuff()
                logs.update({task:[]})
                for log in os.listdir(self.block_address):

                    self.block.update({'file_name':log.split('.')[0]})
                    self.open_file()
                    if not self.data_frame.empty:
                        row=self.data_frame.to_dict(orient='records')[0]
                        row.pop('task',False)
                        row.pop('end_point',False)
                        row.pop('data_point',False)
                        if row['type']=='task_preparation_failed':
                            continue
                        row.pop('_data_point')
                        row.update({'end_point':row['_end_point'],'message':row['type']})
                        row.pop('type')
                        row.pop('_end_point')
                        timestamp=row['datetime']
                        dt_obj = dt.datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S.%f')
                        formatted_str = dt_obj.strftime('%A, %B %d, %Y at %I:%M %p')
                        
                        row.update({"datetime":formatted_str})
                        row.pop('time_elapsed',False)
                        logs[task].append(row)
                break
               
        return logs