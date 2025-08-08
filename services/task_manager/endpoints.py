import os
import json
import time
import threading
from base.storage_sense import Saver
from services.resource_manager.manager import Manager as resource_manager
from services.reports_manager.manager import Manager as reports_manager
import datetime as dt
from django.utils import timezone
import traceback
class EndPoints:
    def __init__(self):
        self.resource_manager=resource_manager()
        self.reports_manager=reports_manager()
        self.reports_manager.datetime=timezone.now()
        self.reports_manager.service='task_manager'
        self.currently_used_devices=[] 
        self.currently_active_profiles=[]
       

        
    def get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    def internal_get_required_data_point_func(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point,self
    
    class Check:
        def service_check(self,**kwargs):
            self.reports_manager.data_point='service_check'               
            task=kwargs.get('task')
            if not task['service'] in ['instagram','google','tiktok','twitter','daraz','threads','resource_manager','facebook','cleaner','reports_manager','data_enricher','audience','datahouse']:
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FireUp','data_point':'fire_up_task',
                                            'type':'unkown_service','task':task['uuid']
                                            })   
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FireUp','data_point':'fire_up_task',
                                            'type':'task_execution_failed','reason':'unkown_task_service','task':task['uuid']
                                            })   
                
                print('Service not Recognized Error')
                s=Saver()
                s.change_state_of_task(task=task,state='completed')
                return False
            return True
        def has_profile_check_for_android_device(self,**kwargs):
            task=kwargs.get('task')
            if task.get('os')=='android':
                if task.get('profile',{}):              
                    return True
                elif task.get('profile',''):
                    print('bot found, now checking if profile exists with username')
                    return True
                else:
                    s=Saver()
                    s.change_state_of_task(task=task,state='completed')
                    return False
            return True
    class FireUp:
        def __init__(self):
            super().__init__()         
            self.reports_manager.end_point='FireUp'
        def prepare_task(self,**kwargs):
            task=kwargs.get('task')
            if task['service']=='google':            
                argo={'end_point':'RunTask','data_point':'run_google_task'}
            elif task['service']=='openweb':
                argo={'end_point':'RunTask','data_point':'run_openweb_task'}
            elif task['service']=='extractor':
                argo={'end_point':'RunTask','data_point':'run_extractor_task'}
            elif task['service']=='instagram':
                argo={'end_point':'RunTask','data_point':'run_instagram_task'}
            elif task['service']=='facebook':
                argo={'end_point':'RunTask','data_point':'run_facebook_task'}
            elif task['service']=='tiktok':
                argo={'end_point':'RunTask','data_point':'run_tiktok_task'}
            elif task['service']=='threads':
                argo={'end_point':'RunTask','data_point':'run_threads_task'}
            elif task['service']=='twitter':
                argo={'end_point':'RunTask','data_point':'run_twitter_task'}
            elif task['service']=='google_api':
                argo={'end_point':'RunTask','data_point':'run_google_api_task'}
            elif task['service']=='slack':
                argo={'end_point':'RunTask','data_point':'run_slack_task'}      
            elif task['service']=='resource_manager':
                argo={'end_point':'RunTask','data_point':'run_resource_manager_task'}
            elif task['service']=='reports_manager':
                argo={'end_point':'RunTask','data_point':'run_reports_manager_task'}
            elif task['service']=='cleaner':
                argo={'end_point':'RunTask','data_point':'run_cleaner_task'}
            elif task['service']=='data_enricher':
                argo={'end_point':'RunTask','data_point':'run_data_enricher_task'}
            elif task['service']=='audience':
                argo={'end_point':'RunTask','data_point':'run_audience_task'}
            elif task['service']=='datahouse':
                argo={'end_point':'RunTask','data_point':'run_datahouse_task'}
            elif task['service']=='daraz':
                argo={'end_point':'RunTask','data_point':'run_daraz_task'}
            if argo:
                    argo.update({'task':task})
                    
                    func,task=self.internal_get_required_data_point(**argo)
                    if task:

                        return {'func':func,'task':task}
                    else:
                        return False
        
        def fire_up_task(self,**kwargs): 
            self.reports_manager.data_point='fire_up_task'       
            self.pause=True
            task=kwargs.get('task')
            func=kwargs.get('func')
            s=Saver()     
            import uuid
            
            try:
                
                time_started=time.time()  
                from crawl.models import Task
                _task = Task.objects.filter(uuid=task['uuid']).first()

                if _task:
                    _task.status = 'running'
                    _task.save()

                    self.reports_manager.task = _task  # ✅ Assign the actual Task object here
                else:
                    raise Exception(f"Task with UUID {task['uuid']} not found.")
                task['run_id']=str(uuid.uuid1())  
                self.reports_manager.run_id=task['run_id']   
                self.reports_manager.task_id=task['uuid']
                self.reports_manager.service=task['service']  
                s.change_state_of_task(task=task,state='running')
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FireUp','data_point':'fire_up_task',
                                        'type':'task_run_started','task':str(task['uuid']),'run_id':task['run_id']
                                        })  
                from services.resource_manager.profiles import Profile
                
                func(task)
            except Exception as e:          
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FireUp','data_point':'fire_up_task',
                                        'type':'task_run_failed','task':str(task['uuid']), 'traceback':traceback.format_exc(),'run_id':task['run_id']
                                        })   
                if 'NoProfileResourceProvided' in str(e):
                    
                    s.change_state_of_task(task=task,state='completed')
                else:
                    s.change_state_of_task(task=task,state='failed')          
            else:
                time_stopped=time.time()-time_started
                self.reports_manager.report_performance(**{'end_point':'FireUp','data_point':'fire_up_task','service':'task_manager',
                                                            'type':'task_run_completed','task':task['uuid'],
                                                            'time_elapsed':time_stopped
                                                            }) 
                           
                s.change_state_of_task(task=task,state='completed')

            from services.reports_manager.endpoints import EndPoints
            e=EndPoints()
            # e.Instagaram().create_run_report(**task)
            e.Instagaram().create_run_log_report(**task)
            from services.datahouse.end_points import EndPoints
            e=EndPoints()
            dicto=task.copy()
            if  task.get('add_data',{}).get('datahouse_url',False):
                if task.get('add_data',{}).get('datahouse_blocks',False):
                    
                    for block_name in task.get('add_data',{}).get('datahouse_blocks',[]):
                        
                        dicto['add_data'].update({'data_source':[{'type':'task','identifier':task['uuid'],'block_name':block_name}
                                                                                    
                                                                                
                                                                                ],'client_url': task.get('add_data',{}).get('datahouse_url')})
                        e.update().send_update_to_client_latest(**dicto)
                else:
                    dicto['add_data'].update({'data_source':[{'type':'task','identifier':task['uuid'],'block_name':False}
                                                                                    
                                                                                
                                                                                ],'client_url': task.get('add_data',{}).get('datahouse_url')})
                    e.update().send_update_to_client_latest(**dicto)
            if task.get('add_data',{}).get('reporting_house_url'):
                dicto['add_data'].update({'data_source':[{'type':'task','identifier':task['uuid'],'block_name':'reports'}
                                                                                
                                                                               
                                                                               ],'client_url': task.get('add_data',{}).get('reporting_house_url')})
                e.update().send_update_to_client_latest(**dicto)
            task=Task.objects.all().filter(uuid=task['uuid'])[0]
            
            if task.dependents:
                task.dependents.all().update(status='pending')
        def fire_up_pending_task_runner(self,**kwargs):
            self.reports_manager.data_point='fire_up_pending_task_runner'
            pending_queue=kwargs.get('pending_queue',[])


            monitor_queue=kwargs.get('monitor_queue',[])
            self.currently_used_devices=kwargs.get('currently_used_devices')
            self.currently_active_profiles=kwargs.get('currently_active_profiles')
            self.available_profiles=kwargs.get('available_profiles')
            self.available_proxies=kwargs.get('available_proxies')
            max_allowed_tasks= kwargs.get('max_allowed_tasks',[])

            #print(self.resource_manager.end_points_handler.available_profiles)
            
            
            for i,task in enumerate(pending_queue):
                if  task['data_point']=='feed_post':

                    pass
                
                self.pause=True
                if max_allowed_tasks:

                    if len(monitor_queue)>=max_allowed_tasks:
                        break
                
                   
                if self.internal_get_required_data_point(**{'task':task,'end_point':'Check','data_point':'service_check'}):
                    if self.internal_get_required_data_point(**{'task':task,'end_point':'Check','data_point':'has_profile_check_for_android_device'}):
                        resp=self.internal_get_required_data_point(**{'task':task,'end_point':'FireUp','data_point':'prepare_task'})
                        if resp:
                            func,task=resp.get('func'),resp.get('task')           
                            
                            
                            kwargs.update({'task':task,'func':func,'end_point':'FireUp','data_point':'fire_up_task'})
                            th=threading.Thread(target=self.internal_get_required_data_point,kwargs=kwargs)                               
                            monitor_queue.append(task)
                            th.start()
            self.pause=False
              
    class FetchTasks:
        def __init__(self):
            self.reports_manager.end_point='FetchTasks'
       



        def fetch_active_workflow_and_their_tasks_from_db(self,**kwargs):
            
            self.reports_manager.data_point='fetch_active_workflow_and_their_tasks'
            pending_queue=[]
            monitor_queue=[]
            completed_queue=[]
            failed_queue=[]
            pending_recurring_queue=[]
            currently_used_devices=[]
            currently_active_profiles=[]
            #Updates Queues in the Parent Process

            s=Saver()
            locked_inputs=[]
            from crawl.models import Task
            from django.forms import model_to_dict
            import pandas as pd
            import pytz
            pending_tasks=Task.objects.all().filter(status='pending').filter(paused=False)
            recurring_tasks=Task.objects.all().filter(repeat=True).filter(paused=False)
            tasks=list(pending_tasks)
            tasks.extend(list(recurring_tasks))
           
            tasks.extend(list(Task.objects.all().filter(status='running')))
            tasks.extend(list(Task.objects.all().filter(status='failed').filter(retries_count__lte=11).filter(paused=False)))
            tasks=list(set(tasks))
            for task in tasks:  
                #workflow=task['workflow'] 

                task_obj=task
                task=model_to_dict(task)
       
                task.pop('state_changed_at',None)
                if task.get('last_state_changed_at',None):
                    pass
                else:
                    task.update({'last_state_changed_at':dt.datetime.now()}) 
                if not task['status']:
                    task['status']='pending'
                if task.get('repeat',False):

                    repeat_duration=task.get('repeat_duration')
                    if not repeat_duration:
                        repeat_duration='10m'
                    r=''
                    for ch in repeat_duration:
                        if ch.isnumeric():
                            r+=ch
                    try:
                        r=int(r)
                    except Exception as e:
                      
                        r=30
                        repeat_duration='30m'
                    else:
                        pass
                    if task['os']=='android':
                        pass
                    if task['status']=='failed' or (task['status']=='completed'):
                        
                        for _ in ['days','h','m','s']:

                            if 'h' in repeat_duration:
                                r*=3600
                                break
                            elif 'm' in repeat_duration:
                                r*=60
                                break
                            elif 'days' in repeat_duration:
                                r*=24*60*60
                                break
                            else:
                                pass
                        datetime1=task['last_state_changed_at']
                        if not isinstance(datetime1,dt.datetime):
                       
                            datetime1 = dt.datetime.fromtimestamp(task['last_state_changed_at'])
                        
                        datetime2 = dt.datetime.now()
                        time_difference = datetime2 -datetime1
                      
                        if time_difference.total_seconds()>int(r):
                           
                            pending_recurring_queue.append(task)
                            #task.update({'status':'pending','last_state_changed_at':datetime2})
                        else:
                            pass
                    
                if task['status']=='running':
                    if not type(task['last_state_changed_at'])==dt.datetime:
                        datetime1 =dt.datetime.fromtimestamp(task['last_state_changed_at'])
                    else:
                        datetime1=task['last_state_changed_at']
                    datetime2 = dt.datetime.now()

                    # Calculate the time difference.
                    time_difference = datetime2 - datetime1

                    # Return the time difference in seconds.
                    if task['input']:
                        locked_inputs.append(task['input'])
                    
                    if task.get('os')=='android':
                        currently_used_devices.append(task.get('device'))
                        currently_active_profiles.append(task.get('profile'))
                        """ self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks',
                                                                        'type':'device_in_use','device_serial_number':task.get('device'),
                                                                        'task':task}) """
                    if (task.get('os')=='chrome' or task.get('os')=='browser') :
                        currently_active_profiles.append(task.get('profile',{}))
                        """ self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks',
                                                                        'type':'profile_in_use','username':task.get('profile',{}),
                                                                        'task':task})
"""
                #active_workflows=s.load_all_active_workflows()
                if task['service']=='instagram':
                    #print(task)
                    pass
                #if not workflow in active_workflows:
                
                    #continue       
               
                 
                    #add task to the queue
                
                if task['status']=='running':
                    monitor_queue.append(task)
                    #add task to the monitor queue
                if task['status']=='pending':
                    if task['input'] in locked_inputs:
                        continue
                    else:
                        pending_queue.append(task)
                if task['status']=='failed':
                    #add task to the failed queue
                    if task_obj.retries_count>10:
                        continue
                    else:
                        task_obj.retries_count+=1                        
                        pending_queue.append(task)
                        task_obj.retries_count=0
                        task_obj.save()
                        
                    #pending_queue.append(task)
            p_r_q_stats=[]
            for item in pending_recurring_queue:
                task=item
                resp=self.internal_get_required_data_point(**{'end_point':'Stats','data_point':'task_execution_details','task':task})
                resp.update({'task':task})
                p_r_q_stats.append(resp)
            import pandas as pd
            df=pd.DataFrame(p_r_q_stats)
            if not df.empty:
                df=df.sort_values(by=['run_bot_launch_success'],ascending=True)
                p_r_q_stats=df.to_dict(orient='records')
                for stats in p_r_q_stats:
                    task=stats['task']
                    s.change_state_of_task(task=task,state='pending')
                    pending_queue.append(task)
             
            return monitor_queue,pending_queue,completed_queue,failed_queue,currently_used_devices,currently_active_profiles
        
        def fetch_active_workflow_and_their_tasks(self,**kwargs):
            self.reports_manager.data_point='fetch_active_workflow_and_their_tasks'
            pending_queue=[]
            monitor_queue=[]
            completed_queue=[]
            failed_queue=[]
            pending_recurring_queue=[]
            currently_used_devices=[]
            currently_active_profiles=[]
            #Updates Queues in the Parent Process
            s=Saver()
        
            register_address={'address':'workflows','file_name':'register'}
            s.block=register_address
            s.load_deep_stuff()
            s.open_file()
            import datetime as dt
            import pandas as pd
            self.register=s.data_frame
            register=self.register


            if register.empty:
                return [],[],[],[],[],[]
            register['last_state_changed_at'] = pd.to_datetime(register['last_state_changed_at'], unit='s')
            register_dict=register.to_dict(orient='records')
        
            locked_inputs=[]
            for task in register_dict:  
                #workflow=task['workflow'] 
                task.pop('state_changed_at',None)
                if task.get('last_state_changed_at',None):
                    pass
                else:
                    task.update({'last_state_changed_at':dt.datetime.now()}) 
                if not task['status']:
                    task['status']='pending'
                if task.get('repeat',False):

                    repeat_duration=str(task.get('repeat'))
                    r=''
                    for ch in repeat_duration:
                        if ch.isnumeric():
                            r+=ch
                    r=int(r)


                    if task['status']=='failed' or (task['status']=='completed'):
                        
                        for _ in ['days','h','m','s']:

                            if 'h' in repeat_duration:
                                r*=3600
                                break
                            elif 'm' in repeat_duration:
                                r*=60
                                break
                            elif 'days' in repeat_duration:
                                r*=24*60*60
                                break
                            else:
                                pass
                        datetime1 =task['last_state_changed_at']
                        datetime2 = dt.datetime.now()
                        time_difference = datetime2 - datetime1
                        if time_difference.total_seconds()>int(r):
                           
                            pending_recurring_queue.append(task)
                            #task.update({'status':'pending','last_state_changed_at':datetime2})
                        else:
                            pass
                
                if task['status']=='running':
                    datetime1 =task['last_state_changed_at']
                    datetime2 = dt.datetime.now()

                    # Calculate the time difference.
                    time_difference = datetime2 - datetime1

                    # Return the time difference in seconds.
                    if task['input']:
                        locked_inputs.append(task['input'])
                    if time_difference.total_seconds()>900:
                        self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks',
                                                                           'type':'changed_state_of_running_task','from_state':task['status'],'to_state':'completed',
                                                                           'time_difference':time_difference.total_seconds(),'task':task['uuid']})
                        s.change_state_of_task(task,'completed')
                        
                    else:
                        if task.get('os')=='android':
                            currently_used_devices.append(task.get('device'))
                            currently_active_profiles.append(task.get('profile'))
                            """ self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks',
                                                                           'type':'device_in_use','device_serial_number':task.get('device'),
                                                                           'task':task}) """
                        if (task.get('os')=='chrome' or task.get('os')=='browser') :
                            currently_active_profiles.append(task.get('profile',{}))
                            """ self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks',
                                                                           'type':'profile_in_use','username':task.get('profile',{}),
                                                                           'task':task})
 """
                #active_workflows=s.load_all_active_workflows()
                if task['service']=='instagram':
                    #print(task)
                    pass
                #if not workflow in active_workflows:
                
                    #continue       
                if task['status']=='pending':
                    
                   if task['input'] and task['input'] in locked_inputs:
                        pass
                   else:
                        pending_queue.append(task)
                    #add task to the queue
                if task['status']=='completed':
                    completed_queue.append(task)  
                if task['status']=='running':
                    monitor_queue.append(task)
                    #add task to the monitor queue
                
                if task['status']=='failed':
                    #add task to the failed queue
                    pending_queue.append(task)

                
                    #pending_queue.append(task)
            p_r_q_stats=[]
            for item in pending_recurring_queue:
                task=item
             
                resp=self.internal_get_required_data_point(**{'end_point':'Stats','data_point':'task_execution_details','task':task})
                resp.update({'task':task})
                p_r_q_stats.append(resp)
            df=pd.DataFrame(p_r_q_stats)
            if not df.empty:
                df=df.sort_values(by=['run_bot_launch_success'],ascending=True)
                p_r_q_stats=df.to_dict(orient='records')
                for stats in p_r_q_stats:
                    task=stats['task']
                    s.change_state_of_task(task=task,state='pending')
                    pending_queue.append(task)
            register_address={'address':'workflows','file_name':'register','data':register_dict}
            s.block=register_address
            s.overwrite=True
            s.load_deep_stuff()
            s.add_values_to_file(load_block=False)         
            return monitor_queue,pending_queue,completed_queue,failed_queue,currently_used_devices,currently_active_profiles
     
        def create_workflow_from_pending_payloads(self,**kwargs):
            import os
        
            from base.storage_sense import Saver
           
            s=Saver()
            s.block={'address':'payloads.pending'}
            s.load_deep_stuff()
            addr=s.block_address
      
         
            for file in os.listdir(addr):
              
                file_name=file.split('.')[0]
                s.block={'address':'payloads.pending','file_name':file_name}
                s.load_deep_stuff()
                s.open_file()
                payload=s.data_frame.to_dict(orient='records')
                if not type(payload)==list:
                    payloads=[payload]
                else:
                    payloads=payload
                for payload in payloads:
                    w=WorkFlow()
                    name=payload.get('name')
          
                    action=payload.get('action')
                    if action=='create':
                        w.start_workflow_manager()
                    
                    
                    _=w.convert_vivid_mind_payload_to_workflow(payload)
               
                    s.block={'address':'payloads.handled','file_name':file_name,'data':payload}
                    s.load_deep_stuff()
                    s.add_values_to_file(load_block=False)
        def update_workflow_register_db(self,**kwargs):
            import os
            import django

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerserver.settings')
            django.setup()

            from crawl.models import Task
            
            s=Saver()  
            statuses=['running','pending','failed','completed','inactive']
            start_time = time.perf_counter()
            for status in statuses:                   
                s.block={'address':'workflows.dump.'+status+''}
                s.load_deep_stuff()
                for _dump in os.listdir(s.block_address):
                    uuid=_dump.split('.json')[0]
                   
                    task=Task.objects.all().filter(uuid=uuid)
                    if len(task)>0:
                        task=task[0]
                        create=False
                    else:
                        create=True
    
                    s.block={'address':'workflows.dump.'+status+'','file_name':_dump.split('.')[0]}
                    s.load_deep_stuff()  
                    file_path=os.path.join(s.block_address,_dump)                               
                    s.open_file()                      
                    if s.empty_file:
                        self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                        'type':'empty_task_dump',  
                                                        'file_path':s.file_path,
                                                                                                            
                                                        })
                        
                        if not s.file:
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                            'type':'task_dump_not_opened',  
                                                            'file_path':s.file_path,
                                                                                                                
                                                            })
                            continue
                    if create:
                        _=s.data_frame.to_dict(orient='records')[0]['task']
                        
                        _.pop('job',None)
                        _.pop('workflow',None)
                        if _.get('repeat'):
                            _.update({'repeat_duration':_['repeat'],'repeat':True})
                        else:
                            _.update({'repeat':False})
                        _.pop('dependent',None)
                        try:

                            task=Task(**_)
                        except Exception as e:
                            pass
                    
                    row=s.data_frame.to_dict(orient='records')[0]    
                    _task=row['task']
                   
                    task.last_state_changed_at=row['timestamp'].timestamp()
                    task.status=status
                    task.profile=_task.get('profile')
                    self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                            'type':'task_state_changed',  
                                            'to':status,
                                            'task':_dump
                                            })
                    
                    task.save()
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        pass
                    
         

        def update_workflow_register(self,**kwargs):
            s=Saver()
            #active_workflows=s.load_all_active_workflows()
            register_address={'address':'workflows','file_name':'register'}
            s.block=register_address
            s.load_deep_stuff()
            s.open_file()
            register=s.data_frame
            if register.empty:
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'empty_task_manager_register',                                                          
                                                           })
            register_dict=register.to_dict(orient='records')
            if s.empty_file:
                task_ids=[]
            else:
                task_ids=register['uuid'].to_list()
            s.block={'address':'allocated'}
            s.load_resources()
            if len(os.listdir(s.block_address))==0:
                pass
                #self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                         #  'type':'no_allocated_resources_found',                                                          
                  #                                         })

            for resource in os.listdir(s.block_address):
                break
                s.block={'address':'allocated','file_name':resource.split('.')[0]}
                s.load_resources()
                s.open_file()
                r=s.data_frame.to_dict(orient='records')[0]
                print('found allocated resource, checking workflow register and updating now')
                t=register.loc[register['id']==r['task_id']]
                if len(t)>0:
                    for index, row in t.iterrows():
                        if register_dict[index].get('resources'):
                            register_dict[index]['task']['resources'].update({r['type']:r})
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'updated_task_with_allocated_resource',  
                                                           'resource':r,
                                                            'task':  register_dict[index]['task']                                                     
                                                           })
                        else:
                            register_dict[index].update({'resources':{r['type']:r}})

                    os.remove(s.file_path)
                else:
                    self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'allocated_resource_task_not_found',  
                                                           'resource':r                                                        
                                                           })
                    print('allocated resource task not found')
                    
    
            statuses=['running','pending','failed','completed','inactive']
            start_time = time.perf_counter()
            for status in statuses:
                s.block={'address':'workflows.dump.'+status+''}
                s.load_deep_stuff()
                for _dump in os.listdir(s.block_address):
                    dump=_dump.split('.')[0]
                    s.block={'address':'workflows.dump.'+status+'','file_name':_dump.split('.')[0]}
                    s.load_deep_stuff()  
                    file_path=os.path.join(s.block_address,_dump)    
                              
                    s.open_file()
                    
                      
                    if s.empty_file:
                        self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'empty_task_dump',  
                                                           'file_path':s.file_path,
                                                                                                             
                                                           })
                        
                        if not s.file:
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                            'type':'task_dump_not_opened',  
                                                            'file_path':s.file_path,
                                                                                                                
                                                            })
                            continue
                        
                    row=s.data_frame.to_dict(orient='records')[0]    
                    task=row['task']
                    task['job']=str(task['job'])
                    if len(task_ids)==0:
                        """  if task['workflow'] not in active_workflows:
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'skipped_inactive_workflow_task',  
                                                           'task':row['task'],
                                                           'workflow':row['task']['workflow']
                                                                                                             
                                                           })
                            continue """
                        task_ids.append(dump)  
                        task.update({'profile':task['profile']})
                        task.update({'last_state_changed_at':row['timestamp'],'status':status})
                        register_dict.append(task)
                        #register_dict.append({'status':status,'task':row['task'],'last_state_changed_at':row['timestamp'],'id':dump})                
                    else:
                        if dump in task_ids:
                            if register.empty:
                                continue
                            record = register.loc[register['uuid'] == dump]
                            if len(record)==1:
                                counter=0
                                for index,row in record.iterrows():        
                                    register_dict[index]['status']=status
                                    register_dict[index]['profile']=task['profile']
                                    register_dict[index]['last_state_changed_at']=dt.datetime.now()
                                    self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'task_state_changed',  
                                                           'to':status,
                                                           'from':register_dict[index]['status'],
                                                           'task':register_dict[index]['uuid']
                                                           })
                                    counter+=1
                                    if counter>1:
                                        self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'deleted_duplicate_task_entry',  
                                                           'task':row['task'],
                                                           'workflow':row['task']['workflow']
                                                                                                             
                                                           })
                                        del register_dict[index]
                        else:
    
                            s.open_file()
                            row=s.data_frame.to_dict(orient='records')[0]              
                            register_dict.append(row['task'])
                            task_ids.append(dump)
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'new_task_entry',  
                                                           'task':row['task']['uuid'],
                                                           'workflow':row['task'],
                                                           'job':row['task']})
                    os.remove(file_path)
                    
                        
                        
                
            #print(self.measure_time_elapsed(start_time))
                    
            if len(register_dict)>0:
                s.overwrite=True
                s.block={'address':register_address['address'],'data':register_dict,'file_name':'register'}
                s.load_deep_stuff()
                s.add_values_to_file(load_block=False)

               
                _=[]
                for row in register_dict:
                    break
                    task=row
                    task.update({'input':str(task.get('input',''))})
                    task.update(({'status':row['status']}))
                    task.update({'allocated_profile':task.get('resources',{}).get('profile',{}).get('username','')})
                    task.update({'allocated_proxy':task.get('resources',{}).get('proxy',{}).get('url','')})
                    task.update({'allocated_device':task.get('resources',{}).get('profile',{}).get('device_serial_number','')})
                    task.pop('resources','')
                    task.pop('proxy','')
                    
                    v=row['last_state_changed_at']
                   
                    __=str(v)
                    task.update(({'last_state_changed_at':__}))
                    _.append(task)
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'task_manager_register_updated',  
                                                           'count_of_tasks':len(register_dict)
                                                           
                                                                                                             
                                                           })
                #s.push_data_frame_to_google_sheet(_,**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1VoE9aZH7VEey6065LYPe8Zu_06FQQdUu0B4GzjSTL7w/edit#gid=0'})
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'FetchTasks','data_point':'update_workflow_register',
                                                           'type':'pushed_task_manager_register_to_google_sheets',  
                                                           'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1VoE9aZH7VEey6065LYPe8Zu_06FQQdUu0B4GzjSTL7w/edit#gid=0'
                                                           
                                                                                                             
                                                           })            
    class Start:
        def __init__(self):
             super().__init__()   
             self.reports_manager.end_point='task_manager' 
        def start_task_manager(self,**kwargs):
            self.reports_manager.data_point='start_task_manager'
            available_profiles,available_proxies=self.resource_manager.update(**{'register':True})

            
            if kwargs.get('fetch_tasks'):
                pass
            else:
                

                self.internal_get_required_data_point(**{'end_point':'FetchTasks','data_point':'create_workflow_from_pending_payloads'})
                #self.internal_get_required_data_point(**{'end_point':'FetchTasks','data_point':'update_workflow_register_db'})
                monitor_queue,pending_queue,completed_queue,failed_queue,currently_used_devices,currently_active_profiles=self.internal_get_required_data_point(**{'end_point':'FetchTasks','data_point':'fetch_active_workflow_and_their_tasks_from_db'}) 
                s=Saver()
                s.update_reports_register()
                self.internal_get_required_data_point(**{'end_point':'FireUp','data_point':'fire_up_pending_task_runner',
                                                       'pending_queue':pending_queue,
                                                       'monitor_queue':monitor_queue,
                                                       'max_allowed_tasks':1,
                                                       'completed_queue':completed_queue,
                                                       'failed_queue':failed_queue,
                                                       'currently_used_devices':currently_used_devices,
                                                       'currently_active_profiles':currently_active_profiles,
                                                       'available_proxies':available_proxies,
                                                       'available_profiles':available_profiles
                                                       })
    class RunTask:
        def __init__(self):
            
            self.reports_manager.end_point='RunTask'
        def verify_allocation(self,**kwargs):
            task=kwargs.get('task')
            resources=kwargs.get('resources')
            self.reports_manager.data_point='verify_allocation'   
            if task.get('resources',False):
                for resource in resources:
                    """                     if 'proxy' in resource:
                        if task.get('resources',{}).get('proxy',False):
                            if type(task.get('resources',{}).get('proxy',False))==dict:
                                pass
                            else:
                                return False
                        else:
                            return False
                    if 'profile' in resource:
                        if task.get('resources',{}).get('profile',False):
                            pass
                        else:
                            return False """
                    if 'targets' in resource:
                        if type(task.get('targets'))==dict:
                            return False
            else:
                return False
                
            return True
        def run_google_task(self,**kwargs):
            task=kwargs.get('task')
            self.reports_manager.data_point='run_google_task'
            from services.google_cloud.run_bot import Google
            self.resource_manager.allocate(service='google',resources=['proxy__static'],task=task)         
            if not self.internal_get_required_data_point(**{'end_point':'RunTask','data_point':'verify_allocation','service':'google','resources':['proxy__static'],'task':task}):
                self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_instagram_task',
                    'task':task, 'type':'resource_allocation_failure','reason':'verification_failed',
                    'required_resources':['proxy__static']
                                })
                return
            g=Google()
            g.task=task
            self.reports_manager.pending(**{'end_point':'log','data_point':'task_run_started','service':'google','task':task,
                                                       })
            g.run_bot(task)
        def run_threads_task(self,**kwargs):
            task=kwargs.get('task')
            if task['status']=='failed' and task['end_point']=='interact':
                return False,False
            self.reports_manager.data_point='run_instagram_task'
            from services.threads.run_bot import Threads
            req_resources=[]#['proxy_static','profile']      
            if not task['end_point']=='interact':
                if not task['profile']:
                    req_resources.append('profile')
                #req_resources.append('proxy')
            else:
                if  task['data_point'] == 'search_user_and_interact':
                    import ast
                    if 'type' in task['targets']:
                        targets=ast.literal_eval(task['targets'])
                        task['targets']=[targets]
                    else:

                        req_resources.append('targets')

            task=self.resource_manager.allocate(**{'service':'instagram','resources':req_resources,'end_point':'allocate','data_point':'allocate_resources_to_task_db','task':task})         
            if task['end_point']=='interact'and not task['profile']:
             
                return 'failed',{}
            if task.get('os')=='android':
                if task.get('device',{}) in self.currently_used_devices:
                #print('Device in Use. Add pending')
                   
                     return 'failed',{}
                else:
                    self.currently_used_devices.append(task.get('device',''))
                
            if self.currently_active_profiles:
                if (task.get('os')=='chrome' or task.get('os')=='browser') and len(task.get('profile'))>1 and task.get('profile',{}) in self.currently_active_profiles:
                    
                    
                    return 'failed',{}
                else:
                    self.currently_active_profiles.append(task.get('profile',{}))  
                    self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_instagram_task',
                    'task':task['uuid'], 'type':'allocated_resource'})
            else:
                self.currently_active_profiles.append(task.get('profile',{}))  
               #if not self.internal_get_required_data_point(**{'service':'instagram','resources':req_resources,'end_point':'RunTask','data_point':'verify_allocation','task':task}):       
                    
                  # raise Exception('AllocationFailure')              

            i=Threads()
            i.task=task
                    
            return i.run_bot,task
        def run_instagram_task(self,**kwargs):
            task=kwargs.get('task')
            if task['status']=='failed' and task['end_point']=='interact':
                return False,False
            self.reports_manager.data_point='run_instagram_task'
            from services.instagram.run_bot import Instagram
            req_resources=[]#['proxy_static','profile']      
            if not task['end_point']=='interact':
                if not task['profile']:
                    req_resources.append('profile')
                #req_resources.append('proxy')
            else:
                if  task['data_point'] == 'search_user_and_interact':
                    import ast
                    if 'type' in task['targets']:
                        targets=ast.literal_eval(task['targets'])
                        task['targets']=[targets]
                    else:

                        req_resources.append('targets')

            task=self.resource_manager.allocate(**{'service':'instagram','resources':req_resources,'end_point':'allocate','data_point':'allocate_resources_to_task_db','task':task})         
            if task['end_point']=='interact'and not task['profile']:
             
                return 'failed',{}
            if task.get('os')=='android':
                if task.get('device',{}) in self.currently_used_devices:
                #print('Device in Use. Add pending')
                   
                     return 'failed',{}
                else:
                    self.currently_used_devices.append(task.get('device',''))
            if task.get('profile'):   
                if self.currently_active_profiles:
                    
                        if (task.get('os')=='chrome' or task.get('os')=='browser') and len(task.get('profile'))>1 and task.get('profile',{}) in self.currently_active_profiles:
                            
                            #print('failed, profile active')
                            return 'failed',{}
                        else:
                            self.currently_active_profiles.append(task.get('profile',{}))  
                            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_instagram_task',
                            'task':task['uuid'], 'type':'allocated_resource'})
                else:
                    self.currently_active_profiles.append(task.get('profile',{}))  
               #if not self.internal_get_required_data_point(**{'service':'instagram','resources':req_resources,'end_point':'RunTask','data_point':'verify_allocation','task':task}):       
                    
                  # raise Exception('AllocationFailure')              

            i=Instagram()
            i.task=task
            #print('task created')    
            return i.run_bot,task
        def run_tiktok_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_tiktok_task'
            from services.tiktok.run_bot import TikTok
            req_resources=[]#['proxy_static','profile']      
            if not task['end_point']=='interact':
                if not task['profile']:
                    req_resources.append('profile')
                #req_resources.append('proxy')
            else:
                if  task['data_point'] == 'search_user_and_interact':
                    import ast
                    if 'type' in task['targets']:
                        targets=ast.literal_eval(task['targets'])
                        task['targets']=[targets]
                    else:

                        req_resources.append('targets')

            task=self.resource_manager.allocate(**{'service':'instagram','resources':req_resources,'end_point':'allocate','data_point':'allocate_resources_to_task_db','task':task})         
            if task.get('end_point')=='interact':
                if not task['profile']:
                   
                    return 'failed',{}
                if task.get('os')=='android':
                    if task.get('device',{}) in self.currently_used_devices:
                    #print('Device in Use. Add pending')
                    
                        return 'failed',{}
                    else:
                        self.currently_used_devices.append(task.get('device',''))
                    
                if self.currently_active_profiles:
                    if (task.get('os')=='chrome' or task.get('os')=='browser') and task.get('profile',{}) in self.currently_active_profiles:
                        
                        
                        return 'failed',{}
                    else:
                        self.currently_active_profiles.append(task.get('profile',{}))  
                        self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_tiktok_task',
                        'task':task['uuid'], 'type':'allocated_resource'})
                else:
                    self.currently_active_profiles.append(task.get('profile',{}))  
               #if not self.internal_get_required_data_point(**{'service':'instagram','resources':req_resources,'end_point':'RunTask','data_point':'verify_allocation','task':task}):       
                    
                  # raise Exception('AllocationFailure')              

            i=TikTok()
            i.task=task
                    
            return i.run_bot,task
        def run_facebook_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_instagram_task'
            from services.facebook.run_bot import Facebook
            print('passed')
            req_resources=[]#['proxy_static','profile']      
            if not task['end_point']=='interact':
                req_resources.append('profile')
                #req_resources.append('proxy')

            task=self.resource_manager.allocate(**{'service':'facebook','resources':req_resources,'end_point':'allocate','data_point':'allocate_resources_to_task','task':task})         
            if not task['profile']:
                
                return
            if task.get('os')=='android':
                if task.get('device',{}) in self.currently_used_devices:
                #print('Device in Use. Add pending')
          
                    return
                else:
                    self.currently_used_devices.append(task.get('device',''))
                
            if self.currently_active_profiles:
                if (task.get('os')=='chrome' or task.get('os')=='browser') and task.get('profile',{}) in self.currently_active_profiles:
                    
                    
                    return
                else:
                    self.currently_active_profiles.append(task.get('profile',{}))  
                    self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_instagram_task',
                    'task':task['uuid'], 'type':'allocated_resource'})
            else:
                self.currently_active_profiles.append(task.get('profile',{}))  
               #if not self.internal_get_required_data_point(**{'service':'instagram','resources':req_resources,'end_point':'RunTask','data_point':'verify_allocation','task':task}):       
                    
                  # raise Exception('AllocationFailure')              

            i=Facebook()
            i.task=task
                    
            return i.run_bot,task    
        def run_openweb_task(self,**kwargs):
            task=kwargs.get('task')
            self.reports_manager.data_point='run_openweb_task'
            from services.open_web.run_bot import OpenWeb
            #resource_manager.allocate(service='openweb',resources=['proxy__static'],task=task)         
            #if not self.verify_allocation(service='openweb',resources=['proxy__static'],task=task):
             #   self.reports_manager.pending(**{'end_point':'log','data_point':'resource_allocation_failure','task':task})
              #  return
            w=OpenWeb()
            w.task=task    
            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_openweb_task',
                                           'task':task, 'type':'task_run_started'
                                                       })
            w.run_bot(task)
        def run_resource_manager_task(self,**kwargs):
            task=kwargs.get('task')
            self.reports_manager.data_point='run_resource_manager_task'
            from services.resource_manager.manager import Manager
            #resource_manager.allocate(service='openweb',resources=['proxy__static'],task=task)         
            #if not self.verify_allocation(service='openweb',resources=['proxy__static'],task=task):
             #   self.reports_manager.pending(**{'end_point':'log','data_point':'resource_allocation_failure','task':task})
              #  return
            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_resource_manager_task',
                                'task':task, 'type':'task_run_started'
                                           })
            r=Manager()
            #r.perform(**task)
            return r.perform, task
            
        def run_extractor_task(self,**kwargs):
            task=kwargs.get('task')
            self.reports_manager.data_point='run_extractor_task'
            from services.extractor.run_bot import Extractor
            #resource_manager.allocate(service='openweb',resources=['proxy__static'],task=task)         
            #if not self.verify_allocation(service='openweb',resources=['proxy__static'],task=task):
             #   self.reports_manager.pending(**{'end_point':'log','data_point':'resource_allocation_failure','task':task})
              #  return
            self.reports_manager.report_performance(**{'service':'task_manager','end_point':'RunTask','data_point':'run_extractor_task',
                    'task':task, 'type':'task_run_started'
                                })
            e=Extractor()
            e.run_bot(task)
        def run_cleaner_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_cleaner_task'
            from services.cleaner.run_bot import Cleaner
            req_resources=[]#['proxy_static','profile']      
                      

            c=Cleaner()              
            return c.run_bot,task
        def run_data_enricher_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_data_enricher_task'
            from services.data_enricher.run_bot import DataEnricher
            req_resources=[]#['proxy_static','profile']      
                      

            d=DataEnricher()              
            return d.run_bot,task
        def run_daraz_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_data_enricher_task'
            from services.daraz.run_bot import Daraz
            req_resources=[]#['proxy_static','profile']      
                      

            d=Daraz()              
            return d.run_bot,task
        def run_reports_manager_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_reports_manager_task'
            from services.reports_manager.run_bot import ReportsManager
            req_resources=[]#['proxy_static','profile']      
                      

            r=ReportsManager()

            return r.run_bot,task
        def run_audience_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_data_enricher_task'
            from services.audience.run_bot import Audience
            req_resources=[]#['proxy_static','profile']      
                      

            a=Audience()              
            return a.run_bot,task
        def run_datahouse_task(self,**kwargs):
            task=kwargs.get('task')
            
            self.reports_manager.data_point='run_data_enricher_task'
            from services.datahouse.run_bot import DataHouse
            req_resources=[]#['proxy_static','profile']      
                      

            d=DataHouse()
            return d.run_bot, task            
            
    class Stats:
        def task_execution_details(self,**kwargs):
            task_id=kwargs['task'].get('uuid')
            s=Saver()
            s.block={'address':'output.tasks.'+task_id+''}
            s.load_reports()      
            task_run_started=0
            run_bot_launch_success=0
            task_run_completed=0
            task_run_failed=0
            for output in os.listdir(s.block_address):
                if 'task_run_started' in output:
                    task_run_started+=1
                elif 'task_run_failed' in output:
                    task_run_failed+=1
                elif 'task_run_completed' in output:
                    task_run_completed+=1
                elif 'run_bot_launch_success' in output:
                    run_bot_launch_success+=1

            return {'task_run_started':task_run_started,'task_run_failed':task_run_failed,'task_run_completed':task_run_completed,
                    'run_bot_launch_success':run_bot_launch_success
                    }
import traceback
while True:
    e=EndPoints()
    try:
        e.get_required_data_point(**{'end_point':'Start','data_point':'start_task_manager'})    
    except Exception as e:
        print(e)   
        print(traceback.format_exc()) 
    else:
        time.sleep(3)

            
            

