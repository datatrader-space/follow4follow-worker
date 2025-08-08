import os
import json
import time
from base.storage_sense import Saver
from services.reports_manager.manager import Manager
import datetime as dt
import pandas as pd
from django.utils import timezone
import uuid
class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.resource_types=['servers','devices','proxies','profiles','targets']
        self.reporter=Manager()
        self.proxies_in_use=[]
        self.task_uuid=str(uuid.uuid1())
        self.collected_data=[]
   
        
    def get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    def internal_get_required_attribute(self,**kwargs):
        return getattr(self,kwargs.get('attr'))
    def set_required_attribute(self,**kwargs):
        return setattr(self,kwargs.get('attr'),kwargs.get('value'))
    
    

    class create:
        def __init__(self):
            super().__init__()   
            self.reporter=Manager()      
            self.collected_data=[]
        def profile(self,**kwargs):
            resp={}
            if kwargs.get('task_manager_info'):
                return['row']
            import os
            import django

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerserver.settings')
            django.setup()
            from crawl.models import ChildBot
            
            if kwargs.get('row'):
            
                profiles=[row]
            elif kwargs.get('input'):
                if type(kwargs.get('input'))==list:
                    profiles=kwargs.get('input')
                
                else:
                    profiles=[]
  
            objs=[]
            updated=0
            created=0
            for i,row in enumerate(profiles):
                row.pop('customer',None)
                p=ChildBot.objects.all().filter(username=row['username'])
                if p:
                    p=p[0]
                    #print('profile Exists')
                    updated+=1
                    p.save()
                    objs.append(p)
                    self.reporter.report_performance(**{'service':'resource_manager','end_point':'create','data_point':'profile',
                                    'uuid':self.task_uuid,'type':'updated_profile','id':p.id                                
                                        })
                else:
               
                    #profiles=row.pop('profiles')
                    row.pop('email_provider')
                    p=ChildBot(**row)
                    p.save()
                    self.reporter.report_performance(**{'service':'resource_manager','end_point':'create','data_point':'profile',
                            'uuid':self.task_uuid,'type':'created_profile','id':p.id                                   
                    })
                    created+=1
                    objs.append(p)
                    
            self.reporter.report_performance(**{'service':'resource_manager','end_point':'create','data_point':'profile',
                            'uuid':self.task_uuid,'profile_created':created,'profiles_updated':updated                                  
                    })
            return {'profiles':objs,'status':'success'}
            if assign_proxy:
                    proxy=self.internal_get_required_data_point(**{'end_point':'assign','data_point':'proxy','profile':profile})
                    
                    if proxy:
                        profile.update({'proxy':proxy})
                        """ _tasks.append({'service':profile.get('service'),
                            'end_point':'login',
                            'data_point':'login',
                            'os':'chrome',
                            'resources':{'profile':row,
                                        'proxy':{'url':profile['proxy']}
                                        
                                        }}) """
            if assign_device:
                    resp=self.internal_get_required_data_point(**{'end_point':'assign','data_point':'device','profile':profile})
                    if resp:    
                        profile=resp  
                        _tasks.append({'service':profile.get('service'),
                            'end_point':'login',
                            'data_point':'login',
                        
                            'bot':row['username']
                            #'resources':{'profile':profile,
                                        #'proxy':profile['proxy']}
                                        
                                        })
                        
                    else:
                            _tasks.append({'service':profile.get('service'),
                            'end_point':'login',
                            'data_point':'login',
                            
                            'bot':row['username'],
                            #'resources':
                                        #{'proxy':profile['proxy']}
                                        })

            p.create_newbie(**{'data':profile})
            p.update_profiles_register()
                    
            if not kwargs.get('create_login_task',True):
                return
            if create_login_task:
                from base.storage_sense import Saver
                s=Saver()
                for task in _tasks:
                    kwargs.update(task)
                    kwargs.pop('row',None)               
                    dependents = s.search_dependents_of_job(self.task)
                    for dependent in dependents:
                        _ = {}
                        _.update(task)
                        job=dependent.get('slug')
                    
                        
                        _.update(dependent)
                        _['job']=job
                        _["workflow"] = self.task["workflow"]
                        _.pop('input',None)

                    
                        s.create_dependents_tasks(_)
        def proxy(self,**kwargs):
            pass
        def device(self,**kwargs):     
            ds=[]
            if kwargs.get('task_manager_info'):
                return['row']
            from crawl.models import Device
            if kwargs.get('row'):
                devices=[kwargs.get('row')]
            elif kwargs.get('input'):
                if type(kwargs.get('input'))==list:
                    devices=kwargs.get('input')
                elif type(kwargs.get('input'))==dict:
                    devices=kwargs.get('input').get('devices',[])
                    

                else:
                    devices=[]
            for device in devices:
                 
                device.pop('connected_to_server')
                d=Device.objects.all().filter(serial_number=device['serial_number'])
                if d:
                    ds.append(d[0])
                    d=d[0]
                else:
                    d=Device(**device)
                    d.save() 
                    ds.append(d)             
                
            return {'status':'success','devices':ds}

                
                
            return
            

            d=Device()      
            d.update_device_info(**device)
            d.update_devices_register()
            def ec2instance(self,**kwargs):
                pass
        def server(self,**kwargs):
            pass
        def from_google_sheet(self,**kwargs):
            if kwargs.get('task_manager_info'):
                return['spreadsheet_url']
            from base.googlesheets import GoogleSheet
            g=GoogleSheet()
            g.initialize_connection()        
            if kwargs.get('spreadsheet_url'):
                g.spreadsheet_url=kwargs.get('spreadsheet_url')      
            resource_types=[kwargs.get('resource_type')]
            if not kwargs.get('resource_type'):
                resource_types=self.resource_types      
            for resource_type in resource_types:
                g.open_google_sheet().find_worksheet(resource_type).read_worksheet()  
                data=g.worksheet_data                                         
                kwargs.update({'data':data})
                if resource_type=='profiles':
                    kwargs.update({'resource_type':resource_type})
                    kwargs.update({'data_point':'profile'})                    
                elif resource_type=='devices':                 
                    kwargs.update({'resource_type':resource_type})
                    kwargs.update({'data_point':'device'})
                elif resource_type=='servers':
                    kwargs.update({'resource_type':resource_type})
                    kwargs.update({'data_point':'server'})
                elif resource_type=='proxies':
                    kwargs.update({'resource_type':resource_type})
                    kwargs.update({'data_point':'proxy'})
                elif resource_type=='targets':
                    kwargs.update({'resource_type':resource_type})
                    kwargs.update({'data_point':'create_targets'})

                return self.internal_get_required_data_point(**kwargs)
        def create_targets(self,**kwargs):
            data=kwargs.get('data')
            workflow=kwargs.get('task',{}).get('workflow','')
            for row in data:
                if 'username' in row.keys():
                    if len(row['username']) >1:
                        pass
                    else:
                        continue
                    entry={'type':'user','username':row['username']}
                    self.collected_data.append(entry)
            return self.collected_data
            
        def targets(self,**kwargs):
            #This data_point creates the Targets file. It checks the task assigned targets.
            #It loops over the blocks to create a single master sheet for the Workflow
            #The master sheet includes only the identifier, for example username, rest_id, shortcode.
            #It also includes the block address of target, to ease further information retrieval.
            #As input this function takes the target choices.
            targets=[]
            target_choices=kwargs.get('task',{}).get('targets')
            workflow=kwargs.get('task',{}).get('ref_id','')
            from services.instagram.end_points import EndPoints
            e=EndPoints()       
            for target in target_choices.split(','):
                if 'location' in target:
                    if 'post' in target:
                        slug=target.split('__')[1]
                        
                        e=EndPoints()
                        resp,data=e.get_required_data_point(**{'location_info':{'slug':slug},'retrieve':['users'],'output_type':list,'end_point':'location','data_point':'location_posts'})
                        if resp=='success':
                            #print(type(data))
                            targets.extend(data)
                if 'followers' in target:
                   
                        username=target.split('__')[1]
                        e=EndPoints()
                        resp,data=e.get_required_data_point(**{'user_info':{'username':username},'retrieve':True,'items':'usernames','output_type':list,'end_point':'user','data_point':'user_followers'})
                        if resp=='success':
                            #print(type(data))
                            targets.extend(data)
                if 'google_sheet' in target:
                    google_sheet_url=target.split('__')[1]
                    pl={'task':kwargs.get('task'),'end_point':'create','data_point':'from_google_sheet','resource_type':'targets','spreadsheet_url':google_sheet_url}
                    data=self.get_required_data_point(**pl)
                    targets.extend(data)
            s=Saver()
            s.block={'address':'workflows.'+workflow+'.targets','file_name':'targets','data':targets}
            s.overwrite=True
            s.load_deep_stuff()
            s.add_values_to_file(load_block=False)  
            #s.push_data_frame_to_google_sheet(targets,**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1eDSdU9MwQpIJ2xikOk0qg6KODkry0RIfI2FkB_ZhJt0/'})
    class allocate:
        def __init__(self):
            super.__init__()
           
            self.reporter.end_point='allocate'
           
            self.reporter.datetime=timezone.now()
        def allocate_resources_to_task_db(self,**kwargs): 
            s=Saver()
            service=kwargs.get('service')
            resources=kwargs.get('resources')
            task=kwargs.get('task')
           
            self.reporter.data_point='allocate_resources_to_task'
            if 'profile' in str(resources):
                if task.get('profile'):
                    profile=self.available_profiles.loc[(self.available_profiles['username']==task.get('bot'))&(self.available_profiles['service']==task.get('service'))]
                    if not profile.empty:
                        self.available_profiles.drop(profile.index[0],inplace=True)
                        profile=profile.to_dict(orient='records')[0]
                        proxy=profile.get('proxy')
                        profile.pop('proxy')
                    
                        
                        
                        
                        """ if task.get('os')=='android':
                            if profile['device_serial_number'] in self.currently_used_devices:
                                #print('Device in Use')
                                raise Exception('Device In Use')
                            else:
                                self.currently_used_devices.append(profile['device_serial_number']) """
                        
                        s.allocate(profile,'profile',task)
                        if type(proxy)==dict:
                            s.allocate(proxy,'proxy',task)
                            task['resources'].update({'proxy':proxy})
                            
                        else:
                            from services.resource_manager.proxy import Proxy
                            p=Proxy()
                            resp=p.get_proxy(proxy)
                            if resp.empty:
                                return task
                            else:
                                proxy=resp.to_dict(orient='records')[0]
                                s.allocate(proxy,'proxy',task)
                                task['resources'].update({'proxy':proxy})
     
                else:
                    available_profiles=self.available_profiles
                    #self.reporter.report_performance({'type':'profile_resource_stock_update','end_point':'allocate','data_point':'allocate_resources_to_task','task':task,'available_profiles':len(available_profiles),key:len(service_profiles)})
                    if len(available_profiles)==0:                
                        pass
                    else:
                        profile=pd.DataFrame()
                        service_profiles=available_profiles.loc[available_profiles['service']==service]
                        key=service+'_profiles'
                        import random
                        if len(service_profiles)==0:
                            pass
                        else:
                            if task.get('alloted_bots'):
                                for bot in task.get('alloted_bots').split(','):
                                  
                                        profile=self.available_profiles[(self.available_profiles['username'] == bot) & (self.available_profiles['service'] == task['service'])]
                                        if not profile.empty:
                                            profile=profile.to_dict(orient='records')
                                        else:
                                            pass
                            else:
                                profile=service_profiles.iloc[random.randint(0,len(service_profiles)-1)]
                                row=self.available_profiles[(self.available_profiles['username'] == profile['username']) & (self.available_profiles['service'] == profile['service'])]
                            
                                self.available_profiles.drop(row.index[0],inplace=True)
                            if type(profile)==list:
                                if len(profile)>0:
                                    profile=profile[0]
                            elif not profile.empty:
                                profile=profile.to_dict()
                            else:
                                return task
                            
                                
                            s.allocate(profile,'profile',task)
                            task.update({'profile':profile['username']})


               
                        if 'proxy' in str(resources):
                            if type(self.available_proxies)==list:
                                pass
                            service_proxies=self.available_proxies[service]
                            if len(self.available_proxies)==0:
                                self.reporter.report_performance({'type':'empty_proxies_database','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(available_profiles)})

                            else:
                                if 'static' in str(resources):
                                    proxy_type='static'
                                else:
                                    proxy_type='rotating'
                                df=pd.DataFrame(service_proxies)
                                df=df.loc[(df['usage_counter']<=1)]
                                if df.empty:
                                    self.reporter.report_performance({'type':'zero_proxy_usage','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df)})

                                else:
                                    self.reporter.report_performance(**{'type':'proxy_usage_count','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df)})

                                    df=df.loc[(df['type']==proxy_type)]
                                    if df.empty:
                                        key=proxy_type+'_'+proxy_type
                                        self.reporter.report_performance(**{'type':'no_'+str(proxy_type)+'_available','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df),'key':len(df)})        
                                    df=df[~df['url'].isin(self.proxies_in_use)]
                                    if len(df)>0:
                                        proxy=df.iloc[0].to_dict()
                                        self.proxies_in_use.append(proxy['url'])
                                        s.allocate(proxy,'proxy',task)  
                                        if task.get('resources'):
                                            task['resources'].update({'proxy':proxy or None})
                                        else:
                                            task.update({'resources':{'proxy':proxy or None}})
                                    else:
                                        self.reporter.report_performance(**{'type':'proxy_assignment_failure','end_point':'allocate','data_point':'allocate_resources_to_task','task':task,'available_proxies':len(available_profiles),'in_use_proxies':len(df),'key':len(df)})
            if 'device' in str(resources):
                from reports_manager.devices_report import report
                #from reports_manager manager import Device Report.
                #The Devices report includes the last use time,last used by service
                from crawl.models import Task,Device,ChildBot
                bot=task.get('profile')
                if not bot:
                    return task
                else:
                    bot=ChildBot.objects.all().filter(username=task.get('profile'))
                    if len(bot)>0:
                        bot=bot[0]
                        device=bot.device
                        if device:
                            pass
                        else:
                            return task
                        
                bots_on_device=ChildBot.objects.all().filter(device=device).filter(service=task['service']).values_list('username',flat=True)

                tasks=Task.objects.all().filter(profile_in=bots_on_device)
               
            if 'targets' in str(resources):
                _=self.internal_get_required_data_point(**{'end_point':'allocate','data_point':'targets','task':task})
                if _:
                    task.update(_)
                else:
                    pass
                    #print('Failed to Allocate Targets')
            return task
        def allocate_resources_to_task1(self,**kwargs): 
            s=Saver()
            service=kwargs.get('service')
            resources=kwargs.get('resources')
            task=kwargs.get('task')
           
            self.reporter.data_point='allocate_resources_to_task'
            if 'profile' in str(resources):
                if task.get('bot'):
                    profile=self.available_profiles.loc[(self.available_profiles['username']==task.get('bot'))&(self.available_profiles['service']==task.get('service'))]
                    if not profile.empty:
                        self.available_profiles.drop(profile.index[0],inplace=True)
                        profile=profile.to_dict(orient='records')[0]
                        proxy=profile.get('proxy')
                        profile.pop('proxy')
                    
                        task.update({'resources':{'profile':profile}})
                        
                        
                        """ if task.get('os')=='android':
                            if profile['device_serial_number'] in self.currently_used_devices:
                                #print('Device in Use')
                                raise Exception('Device In Use')
                            else:
                                self.currently_used_devices.append(profile['device_serial_number']) """
                        
                        s.allocate(profile,'profile',task)
                        if type(proxy)==dict:
                            s.allocate(proxy,'proxy',task)
                            task['resources'].update({'proxy':proxy})
                            
                        else:
                            from services.resource_manager.proxy import Proxy
                            p=Proxy()
                            resp=p.get_proxy(proxy)
                            if resp.empty:
                                return task
                            else:
                                proxy=resp.to_dict(orient='records')[0]
                                s.allocate(proxy,'proxy',task)
                                task['resources'].update({'proxy':proxy})
                          
                else:
                    available_profiles=self.available_profiles
                    #self.reporter.report_performance({'type':'profile_resource_stock_update','end_point':'allocate','data_point':'allocate_resources_to_task','task':task,'available_profiles':len(available_profiles),key:len(service_profiles)})
                    if len(available_profiles)==0:                
                        pass
                    else:
                        service_profiles=available_profiles.loc[available_profiles['service']==service]
                        key=service+'_profiles'
                        import random
                        if len(service_profiles)==0:
                            pass
                        else:
                            profile=service_profiles.iloc[random.randint(0,len(service_profiles)-1)]
                            row=self.available_profiles[(self.available_profiles['username'] == profile['username']) & (self.available_profiles['service'] == profile['service'])]
                        
                            self.available_profiles.drop(row.index[0],inplace=True)
                            
                            profile=profile.to_dict()
                            s.allocate(profile,'profile',task)
                            task.update({'profile':profile['username']})


               
                        if 'proxy' in str(resources):
                            if type(self.available_proxies)==list:
                                pass
                            service_proxies=self.available_proxies[service]
                            if len(self.available_proxies)==0:
                                self.reporter.report_performance({'type':'empty_proxies_database','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(available_profiles)})

                            else:
                                if 'static' in str(resources):
                                    proxy_type='static'
                                else:
                                    proxy_type='rotating'
                                df=pd.DataFrame(service_proxies)
                                df=df.loc[(df['usage_counter']<=1)]
                                if df.empty:
                                    self.reporter.report_performance({'type':'zero_proxy_usage','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df)})

                                else:
                                    self.reporter.report_performance(**{'type':'proxy_usage_count','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df)})

                                    df=df.loc[(df['type']==proxy_type)]
                                    if df.empty:
                                        key=proxy_type+'_'+proxy_type
                                        self.reporter.report_performance(**{'type':'no_'+str(proxy_type)+'_available','end_point':'allocate','data_point':'allocate_resources_to_task','available_proxies':len(self.available_profiles),'in_use_proxies':len(df),'key':len(df)})        
                                    df=df[~df['url'].isin(self.proxies_in_use)]
                                    if len(df)>0:
                                        proxy=df.iloc[0].to_dict()
                                        self.proxies_in_use.append(proxy['url'])
                                        s.allocate(proxy,'proxy',task)  
                                        if task.get('resources'):
                                            task['resources'].update({'proxy':proxy or None})
                                        else:
                                            task.update({'resources':{'proxy':proxy or None}})
                                    else:
                                        self.reporter.report_performance(**{'type':'proxy_assignment_failure','end_point':'allocate','data_point':'allocate_resources_to_task','task':task,'available_proxies':len(available_profiles),'in_use_proxies':len(df),'key':len(df)})
            if 'device' in str(resources):
                pass
            if 'targets' in str(resources):
                _=self.internal_get_required_data_point(**{'end_point':'allocate','data_point':'targets','task':task})
                if _:
                    task.update(_)
                else:
                    pass
                    #print('Failed to Allocate Targets')
            return task   
        def targets(self,**kwargs):
            s=Saver()
            task=kwargs.get('task')
            if task['add_data'].get('bulk_task'):
                if '__' in task.get('targets'):
                    pass
                else:
                    targets=[]
                    for entry in task.get('targets').split(','):
                        targets.append({'type':'user','username':entry})
                    task.update({'targets':targets})
                    return task
            max_size=5#kwargs.get('max_interactions')
            workflow=kwargs.get('task',{}).get('ref_id','')
            s.block={'address':'workflows.'+workflow+'.targets','file_name':'cursor'}
            s.load_deep_stuff()
            s.open_file()
            if s.data_frame.empty:
                cursor=0
            
                #print('Empty Cursors File')
            else:
                cursor=s.data_frame.loc[0]['cursor_index']
            max_index=cursor+max_size
            #print(len(s.data_frame))
            
            s.block={'address':'workflows.'+workflow+'.targets','file_name':'targets'}  
            s.load_deep_stuff()
            s.open_file()
            if s.empty_file or (max_index>len(s.data_frame)):
                if kwargs.get('retry'):
                    #print('Failed to Create Targets file for the workflow. Exiting')
                    return {}
                pl={'task':task,'end_point':'create','data_point':'targets'}
                self.get_required_data_point(**pl)
                pl.update({'end_point':'allocate','data_point':'targets','retry':True})
                return self.get_required_data_point(**pl)
            else:
                targets=s.data_frame
                _=targets.loc[cursor:max_index]
                data=[{'cursor_index':max_index}]
                s.block={'address':'workflows.'+workflow+'.targets','file_name':'cursor','data':data}  
                s.overwrite=True
                s.load_deep_stuff()
                s.add_values_to_file(load_block=False)
                _.to_dict()
                _=_.to_dict(orient='records')
                task.update({'targets':_})
                return task     
    class update:
        def __init__(self):
            pass
        def register(self,**kwargs):
            s=Saver()
            s.read_profiles_register()
            s.update_profiles_register()
            import threading
            
            s.update_profiles_request_register()
            #s.update_proxies_register()
            s.read_proxies_register()
            try:
                available_proxies=s.get_proxies_stats() 
            except Exception as e:
                available_proxies=[]
            s.read_profiles_register()
            available_profiles=s.get_profiles_stats()
            self.set_required_attribute(**{'attr':'available_profiles','value':available_profiles})
            self.set_required_attribute(**{'attr':'available_proxies','value':available_proxies})
            return available_profiles,available_proxies   
    class assign:
        def proxy(self,**kwargs):
            if kwargs.get('task_manager_info'):
                return['profile']
            from services.resource_manager.proxy import Proxy       
            if kwargs.get('profile'):
                profile=kwargs.get('profile')
                p=Proxy()
                proxies=p.get_proxy_usage_stats_by(**{'service':profile.get('service')})
                
                if profile.get('proxy'):
                    
                    is_proxy_in_db=proxies.loc[proxies['url']==profile.get('proxy')]
                    if is_proxy_in_db.empty:
                        pass
                       

                    else:
                        for i, row in is_proxy_in_db.iterrows():

                            current_=row['usage_count_by_service']
                            if current_>3:
                                pass
                                #print('Current Usage count of proxy is '+str(current_))
                            else:
                                return row.to_dict()
                proxies=proxies[proxies['usage_count_by_service']<3]
                if not proxies.empty:
                    proxy=proxies.iloc[0]
                
                    return proxy.to_dict()
                else:
                    pass
                    #print('No Proxies available for service. Add report')
        def device(self,**kwargs):
            if kwargs.get('task_manager_info'):
                return['profile']
            profile=kwargs.get('profile')
            from services.resource_manager.device import Device
            d=Device()
            stats=d.get_profiles_attached_stats(service=profile.get('service'))
            if len(stats)>0:
                for index,row in enumerate(stats):
                    
                    if row['service_profiles_attached']<7:
                        serial_number=row['serial_number']
                        if serial_number:
                            from services.resource_manager.device import Device
                            d=Device()
                            d.add_profile_to_device(**{'serial_number':serial_number,'profile':profile})
                            profile.update({'device_serial_number':serial_number})
                            return profile
            else:

                return False
            return False                 
    class sync:
        def with_google_sheet(self,**kwargs):    
            if kwargs.get('task_manager_info'):
                return['spreadsheet_url']
            if kwargs.get('spreadsheet_url'):
                from base.googlesheets import GoogleSheet
                g=GoogleSheet()
                g.initialize_connection()
                g.spreadsheet_url=kwargs.get('spreadsheet_url')
                for resource_type in self.resource_types:
                    sync=False
                    if resource_type=='profiles':
                        from services.resource_manager.profiles import Profile
                        p=Profile()
                        df=p.read_profiles_register()
                        if not df.empty:
                            sync=True
                            try:
                                df.drop(columns=['available','device','user_data_dir'],inplace=True)
                            except Exception as e:
                                #print('failed to dip columns')
                                pass
                        
                            def _prox(dicto):
                                return dicto.get('url')
                            df['proxy']=df['proxy'].map(_prox)
                            g.data=df  
                            g.open_google_sheet().find_worksheet(resource_type).update_worksheet()
                    elif resource_type=='devices':
                        sync=True
                        from services.resource_manager.device import Device
                        d=Device()
                        df=d.read_devices_register()
                        try:
                            df.drop(columns=['last_status_update_time'],inplace=True)
                        except Exception as e:
                            pass
                            #print('Failed to Dip Column')
                        df = df.loc[:,~df.columns.duplicated()].copy()
                        #print(df.columns.values)
                        df.fillna(' ',inplace=True)
                        df.drop(['hwaddr','udid','agentVersion','arch','usingBeganAt'],axis=1,inplace=True)                  
                        g.data=df                                     
                        g.open_google_sheet().find_worksheet(resource_type).update_worksheet()
                        #print(resource_type+' Sheet Synced')