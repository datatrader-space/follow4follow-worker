#from celery import shared_task
#from celery.utils.log import get_task_logger
#from django_celery_results.models import TaskResult
#from deep_stuff.workflow_creator import WorkFlow
import os
import time
from django.forms import model_to_dict
import datetime as dt
import uuid
#@shared_task()
def get_logs():

    from base.storage_sense import Saver
    s=Saver()
    s.block={'address':'performance'}
    report_logs_type=['clicked_follow_button','run_bot_launch_success','run_bot_launch_failure','saving_user_followers']
    
    """ 'located_profile_page','account_switched','user_already_logged_in','clicked_choose_account',
        'clicked_camera_button','selected_photos','clicked_next_button_from_media_picker','sent_caption',
                      'clicked_add_location_option','entered_location_input','clicked_first_suggestion','found_share_post_button','not_found_share_post_button',
                      'clicked_share_post_button' """
    
    logs=[]
    
    for l_type in report_logs_type:
         print(l_type)
         s.block={'address':'performance.'+l_type}
         s.load_reports()
         for i,log in enumerate(os.listdir(s.block_address)):

        
            s.block={'address':'performance.'+l_type,'file_name':log.split('.')[0]}
            s.load_reports()
            s.open_file()
            if not s.data_frame.empty:
                try:
                    data=s.data_frame.to_dict(orient='records')
                    if len(data)>0:
                        data=data[0]
                        if data.get('screenshot',False):
                            pth=data['screenshot']
                    
                            pth=pth.split('vivid_mind_panel')[1]
                            data['pth']=pth
                            data.pop('screenshot')
                        
                            #print("last modified: %s" % time.ctime(os.path.getmtime(file)))
                        datetime=time.ctime(os.path.getctime(s.file_path))
                        data['datetime']=datetime
                        
                except Exception as e:
                    print(e)

                else:
                    logs.append(data)
    
    import pandas as pd
    df=pd.DataFrame(data=logs)
    if not df.empty:
        df.sort_values(by=['datetime'],inplace=True,ascending=True)
        logs=df.to_dict(orient='records')
        return logs
    return[]


##@shared_task()
def create_hourly_report():
    import pandas as pd
    from base.storage_sense import Saver
    s=Saver()
    from pathlib import Path
    import datetime as dt
    s.block={'address':'performance'}
    reports_dict={'task_manager':['task_run_started','task_run_failed','task_run_completed','bot_started_successfully','run_bot_launch_success','run_bot_launch_failure'],
              'login':['failed_login','user_already_logged_in','switching_profile','target_profile_is_active','account_switched'],
             'sniffing':['target_request_sniffed','create_request_headers_from_sniffed_request','acquired_data','crawl_count_incremented','saving_user_info',
                         'saving_location_posts'],
              'activity':['not_found_follow_button','clicked_follow_button','located_home_page','located_login_page']
            
             
             
             }
    
    for report_type,logs_type in reports_dict.items(): 
        reports=[{}]
        for l_type in logs_type:

            count=0
            s.block={'address':'performance.'+l_type}     
            s.load_reports()
            paths = sorted(Path(s.block_address).iterdir(), key=os.path.getctime,reverse=True)
          
            modification_times = [dt.datetime.fromtimestamp(os.path.getmtime(path)) for path in paths]
          
            count = sum(1 for _ in modification_times if (dt.datetime.now() - _).total_seconds() <= 3600 * 48)
            reports[0].update({l_type:count})
           
   
            import pandas as pd
            df=pd.DataFrame(data=reports)

            from base.googlesheets import GoogleSheet
            from base.google_api import GoogleAPI
            g=GoogleSheet()
            g.initialize_google_drive_api()
            g.initialize_connection()
            g.folder_name='gary_automates'
            g.spreadsheet_title='hourly_report'
            worksheet=report_type
            g.check_if_folder_exists()
            g.check_if_file_exists_in_active_folder()
            g.open_google_sheet()
            g.data=df
            df.fillna(0,inplace=True)
            g.find_worksheet(worksheet).update_worksheet(drop_duplicates=False)
            file_id=g.active_file['id']
            print(g.spreadsheet.url)
    _g=GoogleAPI()

    _g.service_account_from_dict()
    _g.share_with_user(**{'email_address':'hamza@northrays.com','type':'user','role':'writer','msg':'Your Hourly Report for Gary Autoamtes','id':file_id})
   
    
def communicate_todo_with_worker(todo):
    for bot in todo.bots.all():    
        if bot.device==None:       
            continue
        else:
            print(bot.device.connected_to_server)

            worker=bot.device.connected_to_server.public_ip
            worker+='crawl/api/workflow/'
            _bot=model_to_dict(bot)
            _bot.pop('created_on')
            _bot.pop('cookie')
            _bot['device']=bot.device.__str__()

            name=bot.campaign.name
            data={'id': todo.id,'name':b.name,'service': bot.service,'childbots':[_bot],'os':'android','activity_to_perform':'feed_post',
                  'todo':{'action':'create', 'name': todo.name, 
            'media':todo.file.url,
            'caption':todo.caption,'location':todo.location, 
            'music':todo.music}
            }   
#@shared_task()
def handle_scrape_task_delete(scrapetask):
    from crawl.models import Task   
    st_tasks=Task.objects.all().filter(ref_id=scrapetask.id).delete()
def handle_scrape_task_update(scrapetask):

  
    from crawl.models import ScrapeTask,Task
    st_tasks=Task.objects.all().filter(ref_id=scrapetask.id)
    s=ScrapeTask.objects.all().filter(id=scrapetask.id)
    s=s[0]
    if s.repeat and scrapetask.repeat:
        if s.repeat_duration==scrapetask.repeat_duration:
            pass
        else:
            st_tasks.update(repeat_duration=scrapetask.repeat_duration)
    
    print(scrapetask.internal_state)
    if scrapetask.internal_state=='active':
        pass
    else:
        print(scrapetask.internal_state)
        st_tasks.update(state='in-active')
        return
    


        #check if input has been removed
    removed_inputs=[]
    print(s.input)
    for input in s.input.split(','):

        if input in scrapetask.input.split(','):
            pass
        else:
            removed_inputs.append(input)

    for removed_input in removed_inputs:
        st_tasks.filter(input=removed_input).delete()
    #we have deleted the tasks with removed input
    #now we need to add tasks for new input
    for input in scrapetask.input.split(','):
        tasks_with_input=st_tasks.filter(input=input)
        print(tasks_with_input)
        if len(tasks_with_input)==0:
            if 'location' in input:
                end_point='location'
                if 'posts' in input:
                    data_point='location_posts'
            elif 'follower' in input:
                end_point='user'
                data_point='user_followers'
                print(data_point)
            elif 'marketplace' in input:
                end_point='marketplace'
                data_point='search'
            else:
                continue
            task={'service':scrapetask.service,
                'interact':False,
                'end_point':end_point,
                'data_point':data_point,
                'os':scrapetask.os,
                'input':input.split('__')[1],
                'repeat':scrapetask.repeat,
                'repeat_duration':scrapetask.repeat_duration,
            
                'uuid':str(uuid.uuid1()),
             
                'ref_id':scrapetask.id
                            }
            dup_check=Task.objects.all().filter(ref_id=scrapetask.id).filter(end_point=end_point).filter(data_point=data_point).filter(input=input)
            
            if len(dup_check)>0:
                
                print('Excluding Duplicate Scrape Task Creation')
                continue
            t=Task(**task)
            t.save()
            #tasks need to be created
        else:
            pass
    alloted_bots=scrapetask.childbots.all()
    _=[]
    for bot in alloted_bots:
        _.append(bot.username)
    st_tasks.update(alloted_bots=','.join(_))
            #tasks already present


       #the new update has the value of scrape task input changed, so we will update it for all existing tasks
        #if new input has been added, new tasks will be created.
        #if input has been removed, tasks with the input will be deleted or marked in active as well.

def communicate_bulk_campaign_update_with(bulkcampaign):
    print(model_to_dict(bulkcampaign))

    bots=[]
    for bot in bulkcampaign.childbots.all():
        print
        if bulkcampaign.os=='android':
     
             if bot.device==None:
                
                continue
        print(bot.device)
        _bot=model_to_dict(bot)
        _bot.pop('created_on')
        _bot.pop('cookie')
        _bot['device']=bot.device.__str__()
        bots.append(_bot)
    print(bots)
    devices=[]
    for device in bulkcampaign.devices.all():
        device=(model_to_dict(device))
        """ profiles=[]
        for profile in device['profiles']:
            profile=(model_to_dict(profile))
            profile.pop('created_on')
            profile.pop('cookie')
            profiles.append(profile)

        device['profiles']=profiles """
        devices.append(device)
    scrape_tasks=[]
    for task in bulkcampaign.scrape_tasks.all():
        #bots=[]
        scrape_task=model_to_dict(task)
        _=[]
        for bot in scrape_task['childbots']:
            bot=model_to_dict(bot)
            bot.pop('created_on')
            bot.pop('cookie')
            _.append(bot)
        scrape_task['childbots']=bots
        scrape_tasks.append(scrape_task)


    messaging=[]
    for messag in bulkcampaign.messaging.all():
        messaging.append(model_to_dict(messag))
    sharing=[]
    for shar in bulkcampaign.sharing.all():
        sharing.append(model_to_dict(shar))
    settings=[]
    for sett in bulkcampaign.settings.all():
        sett=(model_to_dict(sett))
        sett.pop('created_on')
        settings.append(sett)
    data={'action':'create','id': bulkcampaign.id, 'name': bulkcampaign.name, 
    'service': bulkcampaign.service, 'activity_to_perform': bulkcampaign.activity_to_perform, 
    'os': bulkcampaign.os, 'localstore': bulkcampaign.localstore, 'proxy_disable': bulkcampaign.proxy_disable,  'blacklist': '', 
    'required_interactions': 10000, 'launch_datetime': None, 'stop_datetime': None,
   'internal_state': 'active', 'campaign_state': 'launched', 'is_completed': False,
     'is_deleted': False, 'media_id': None, 'comment_id': None, 'childbots':bots,
     'devices':devices,'scrape_tasks':scrape_tasks,'messaging':messaging,
     'sharing':sharing,'settings':settings}     
    queue_vivid_mind_payload(data)        
#@shared_task()
    
def handle_automation_task_creation(automation_task):
    from django.forms import model_to_dict
    
    scrape_tasks=automation_task.scrape_tasks.all()
    _targets=[]
    jobs=[]
    for scrape_task in scrape_tasks:
        _targets.append(scrape_task.input)
    _targets=','.join(_targets)
  
    print(automation_task.monitor)
    for i,activity in enumerate(automation_task.activity_to_perform):
        task={'service':automation_task.service,
          'ref_id':automation_task.id,
          'os':automation_task.os
                        
        }
      
        repeat=False
        repeat_duration=None
        inp=activity['Page']
        if inp.get('repeat_after'):
            repeat=True
            repeat_duration=str(inp.get('repeat_after'))+'h'
            inp.pop('repeat_after')
         
        task.update({'end_point':inp['end_point'],'data_point':inp['data_point']})  
        inp.pop('end_point')
        inp.pop('data_point')
        task.update({'add_data':inp})
        if task['data_point']=='search_user_and_interact':
            task.update({'targets':_targets})
            task['add_data'].update({'messaging':model_to_dict(automation_task.messaging)})
        if task['data_point']=='bulk_task':
            
            activity_to_perform=inp['activity_to_perform'].split(',')
            print(activity_to_perform)
            for act in activity_to_perform:
                print(activity)
                if act=='follow':
                    t=task.copy()
                    t['data_point']='search_user_and_interact'
                    t['bulkaction']=True
                    t['targets']=inp['target_profile']
                    t['os']=inp['os']
                    t['activity_to_perform']='follow'
                    task=t
                elif act=='like':
                    t=task.copy()
                    t['data_point']='search_post_and_interact'
                    t['bulkaction']=True
                    t['targets']=inp['target_profile']
                    t['os']=inp['os']
                    t['activity_to_perform']='like'
                    task=t
                elif act=='dm':
                    t=task.copy()
                    t['data_point']='send_dm'
                    t['bulkaction']=True
                    t['targets']=inp['target_profile']
                    t['os']=inp['os']
                    t['activity_to_perform']='like'
                    task=t
                elif act=='share_post_as_story':
                    t=task.copy()
                    t['data_point']='share_post_as_story'
                    t['bulkaction']=True
                    t['targets']=inp['target_profile']
                    t['os']=inp['os']
                    t['activity_to_perform']='like'
                    task=t

        
                        
                        
                            

            
    
             

        if repeat:
            task.update({'repeat':True,'repeat_duration':repeat_duration})
        jobs.append(task)


    
     
    behavior=model_to_dict(automation_task.behavior)              
    """     job={'service':automation_task.service,
            'interact':True,
            'end_point':'interact',
            'data_point':'check_notification',

            'add_data':behavior,
            
            'os':automation_task.os,           
            'repeat':True,
            'repeat_duration':'2h',
            'ref_id':automation_task.id
                                                        
                }
    jobs.append(job) """
    from crawl.models import Task
    if automation_task.monitor:
        for monitor_dict in automation_task.monitor:
          
            for event in monitor_dict['onEvent']:
                if event['event']=='on_new_post':
                    condition='has_new_post'
                    for username in monitor_dict['usernames'].split(','):
                        exstn_task=Task.objects.all().filter(end_point=monitor_dict['type'],data_point='condition_handler',condition=condition,input=username,ref_id=automation_task.id)
                        if len(exstn_task)>=1:
                            monitor_task=exstn_task[0]
                        else:
                            
                            task={'service':automation_task.service,
                                'interact':False,
                                'end_point':monitor_dict['type'],
                                'data_point':'condition_handler',
                                'condition':condition,
                                'os':'browser',
                                'input':username,
                                'repeat':True if event['monitor_after'] else False,
                                'repeat_duration':event['monitor_after'],
                                'uuid':str(uuid.uuid1()),
                                'ref_id':automation_task.id
                            }
                            monitor_task=Task(**task)
                            monitor_task.save()
                        if event['share_as_story']:
                            share_latest_post_as_story=True
                        like=False
                        if event['like']:
                            like=True
                        comment=False
                        if event.get('comment'):
                            comment=event.get('comments')
                        task={'service':automation_task.service,
                            'interact':False,
                            'end_point':'interact',
                            'data_point':'search_user_and_interact',                               
                            'os':'android',                              
                            'repeat':False,
                            'repeat_duration':event['monitor_after'],
                            'uuid':str(uuid.uuid1()),
                            'add_data':{'messaging':{'type':'reachout_message','values':[]},
                                        'follow':True,
                                        'open_latest_post':True,
                                        'share_latest_post_as_story':share_latest_post_as_story,
                                        'like':like,
                                        'comment':comment

                                        },
                            'dependent_on_id':monitor_task.id,                               
                            'targets':{'type':'user','username':username},
                            'ref_id':automation_task.id,
                            'status':'completed',
                        }
                        jobs.append(task)
                        
    
    for bot in automation_task.childbots.all():
        for job in jobs:
            print(job)
            exstn_tasks=Task.objects.all().filter(ref_id=automation_task.id).filter(end_point='interact').filter(data_point=job['data_point']).filter(profile=bot.username).filter(add_data=task['add_data'])
            if len(exstn_tasks)>0:
                if task.get('dependent_on_id'):
                    if exstn_tasks.filter(dependent_on=task['dependent_on_id']):
                        continue
                else:
                    continue

            if job['data_point']=='search_user_and_interact':
                if not _targets:
                    dup_check=exstn_tasks.filter(targets='')
                else:
                    dup_check=exstn_tasks.filter(targets=_targets)
                if len(dup_check)>0:
                    
                    print('Excluding Duplicate Task Creation')
                    continue
            else:
                if len(exstn_tasks)>0:
                    continue

            job.update({'profile':bot.username,'uuid':str(uuid.uuid1()),'device':bot.device.serial_number})
            
            t=Task(**job)
            t.save()
    
def handle_todo_creation(todo):
    from crawl.models import Task
    for bot in todo.bots.all():
        task={'ref_id': todo.id,'service': bot.service,'profile':bot.username,'os':'android','end_point':'interact','data_point':'feed_post',             
                'media_link':todo.file.url,
                'caption':todo.caption,'location':todo.location, 
                'google_drive_root_folder_name':todo.google_drive_root_folder_name,
                'music':todo.music,
                'device':bot.device.serial_number,
                'uuid':str(uuid.uuid1())
                }   
        exstn_tasks=Task.objects.all().filter(service=bot.service).filter(profile=bot.username).filter(end_point='interact').filter(data_point='feed_post').filter(media_link='http://localhost'+todo.file.url)
        print(exstn_tasks)
        add_data={'target_location':{},"music_info":[]}
       
        if todo.target_location:
            location=todo.target_location
            add_data['target_location'].update({'city_info':{'id':location['city_id']},'country_info':{'slug':location['country_slug']}})
       
        task.update({'add_data':add_data})      
        if not todo.caption:
            dup_check=exstn_tasks.filter(caption='')
        else:
            dup_check=exstn_tasks.filter(caption=todo.caption)
        if len(dup_check)>0:
            
            print('Excluding Duplicate Todo Task Creation')
            continue
        if todo.repeat:
            if todo.repeat_after:
                repeat_duration=todo.repeat_after*60*60
                task.update({'repeat':True,'repeat_duration':repeat_duration})
        t=Task(**task)
        t.save()
''' 
def create_workflow_from_payload():
    import os
    import uuid
    uuid=str(uuid.uuid1())
    from base.storage_sense import Saver
    #from services.reports_manager.manager import Manager
    reports_manager=Manager()
    s=Saver()
    s.block={'address':'payloads.pending'}
    s.load_deep_stuff()
    addr=s.block_address
    print(addr)
    print(os.listdir(addr))
    
    for file in os.listdir(addr):
        reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                                              'task':'system','type':'central_request','status':'pending','uuid':uuid                                             
                                              
                                              })
        print(file)
        file_name=file.split('.')[0]
        s.block={'address':'payloads.pending','file_name':file_name}
        s.load_deep_stuff()
       
        s.open_file()
        if not s.file:
            reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                                        'task':'system','type':'central_request','status':'file_open_error','uuid':uuid                                               
                                        
                                        })
        elif s.empty_file:
            reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                            'task':'system','type':'central_request','status':'empty_file_error','uuid':uuid                                               
                            
                            })
        payload=s.data_frame.to_dict(orient='records')
        if not type(payload)==list:
            payloads=[payload]
        else:
            payloads=payload
        if len(payloads)>1:
            reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                'task':'system','type':'central_request','status':'multiple_payloads_found','uuid':uuid                                               
                
                })
        for payload in payloads:

            w=WorkFlow()
            name=payload.get('name')

            print(payload)
            action=payload.get('action')
            if action=='create':
                reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                'task':'system','type':'central_request','request_type':'create','status':'started_workflow_manager','uuid':uuid                                               
                
                })
                w.task_uuid=uuid
                w.start_workflow_manager()
            
            os.remove(s.file_path)
            reports_manager.report_performance(**{'service':'external_party_communication_facilitator','end_point':'create_workflow_from_payload','data_point':'create_workflow_from_payload',
                'task':'system','type':'central_request','request_type':'create','status':'started_workflow_manager','uuid':uuid                                               
                
                })
            _=w.convert_vivid_mind_payload_to_workflow(payload)
            print(_)
            s.block={'address':'payloads.handled','file_name':file_name,'data':payload}
            s.load_deep_stuff()
            s.add_values_to_file(load_block=False)
       
    
def queue_vivid_mind_payload(payload):
        print(payload)
        file_name=payload['name']
        from base.storage_sense import Saver
        s=Saver()
        s.block={'address':'payloads.pending','file_name':file_name,'data':payload}
        s.load_deep_stuff() 
        s.add_values_to_file(load_block=False) 
'''
