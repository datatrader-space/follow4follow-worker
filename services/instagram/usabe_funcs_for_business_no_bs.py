import datetime as dt
def get_bulk_user_info_with_browser(task,queries,failed_count=0,success_count=0,retry=0,exclude_params=[],consumed_usernames=[],blacklisted_usernames=[],exclude_queries=[],time_started=dt.datetime.now()):
    
    from base.browser import Browser
    from base.basic_crawler import Crawler
    from base.request_maker import Request
    from services.reports_manager.manager import Manager
    from services.instagram.end_points import EndPoints as ep
    from services.instagram.recursion import Recursion
    from services.instagram.compatpatch import ClientCompatPatch
    import threading
    import json
    cc=ClientCompatPatch()
    r=Recursion()
    r.reporter=Manager()
    task=task
    c=Crawler()
    c.service_name='instagram'
    c.use_proxies=task.get('add_data',{}).get('use_proxies',{})
    c.reporter=Manager()
    c.reporter.run_id=task['run_id']
    rq=Request()
    c.task=task
    if not success_count>30:
        c.initialize_all_variables(**{'username':task.get('username'),'profile':task.get('profile'),**task})
        c.open_custom_browser(selenium_wire=True,headless=False
                              )
    browser=c.browser
    print('Success Count: '+ str(success_count))
    print('Failed Count: '+ str(failed_count))
    print(dt.datetime.now()-time_started)
    exclude_params=[]
    if len(exclude_queries)==0:
        from crawl.models import Task
        t=Task.objects.all().filter(uuid=task['uuid'])[0]
        if t.blacklisted_usernames:
            exclude_queries.extend(t.blacklisted_usernames.split(','))
        if t.consumed_usernames:
            exclude_queries.extend(t.consumed_usernames.split(','))
    
    for query in queries:
        if success_count>30:
            break
        user_info=query.get('user_info')
        if query in exclude_queries or user_info['username'] in exclude_queries:
            continue
        if retry>1:
            exclude_queries.append(query)
            blacklisted_usernames.append(user_info['username'])
            retry=0
            browser.driver.close()
            return get_bulk_user_info_with_browser(task=task,queries=queries,failed_count=failed_count,retry=retry,success_count=success_count,exclude_params=exclude_params,time_started=time_started,consumed_usernames=consumed_usernames,blacklisted_usernames=blacklisted_usernames)

        
        username=user_info['username']
 
        if rq.session:
            resp=c.make_request(url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+'')

            if resp['status']=='success':
                exclude_queries.append(query)
                info=resp['data']
                info={'data':info,'status':'success'}
                resp=ep.user().user_info(**{'response':info})
                success_count+=1
                th=threading.Thread(target=r.save_parsed_response,args=(resp,{}),kwargs=task)
                th.start()  
                consumed_usernames.append(user_info['username'])
                print('Success Count: '+ str(success_count))
                print('Failed Count: '+ str(failed_count))
                print(dt.datetime.now()-time_started)
            else:
                browser.driver.close()
                retry+=1
                return get_bulk_user_info_with_browser(task=task,queries=queries,exclude_queries=exclude_queries,failed_count=failed_count,retry=retry,success_count=success_count,exclude_params=exclude_params,time_started=time_started,consumed_usernames=consumed_usernames,blacklisted_usernames=blacklisted_usernames)

        else:
            
            browser.get('https://www.instagram.com/'+str(username)+'')
            try:
                web_profile_info=c.find_request(identifiers=['web_profile_info'],exclude_params=exclude_params,wait_time=60)
                
            except Exception as e:
                failed_count+=1
                browser.driver.close()
                retry+=1
                return get_bulk_user_info_with_browser(task=task,queries=queries,exclude_queries=exclude_queries,failed_count=failed_count,retry=retry,success_count=success_count,exclude_params=exclude_params,time_started=time_started,consumed_usernames=consumed_usernames,blacklisted_usernames=blacklisted_usernames)
            else:
                
                if web_profile_info:
                    exclude_params.append(web_profile_info[0].params)
                    try:
                        
                        info=json.loads(web_profile_info[0].response.body)
                    except Exception as e:
                        failed_count+=0
                        print('Exception occured while parsing the response body')
                    else:
                    
                        exclude_queries.append(query)
                        info={'data':info,'status':'success'}
                        
                        resp=ep.user().user_info(**{'response':info})
                        from services.reports_manager.manager import Manager
                        r=Manager()

                        consumed_usernames.append(user_info['username'])

                        success_count+=1
                        th=threading.Thread(target=r.save_parsed_response,args=(resp,{}),kwargs=task)
                        th.start()   
                        c.initialize_request_session(use_proxies=task.get('add_data').get('use_proxies'))                
                        c.copy_request_headers(web_profile_info[0])
                        rq.session=c.session
                        
                else:
                    
                    failed_count+=1
                    browser.driver.close()
                    retry+=1
                    return get_bulk_user_info_with_browser(task=task,queries=queries,exclude_queries=exclude_queries,failed_count=failed_count,retry=retry,success_count=success_count,exclude_params=exclude_params,time_started=time_started,consumed_usernames=consumed_usernames,blacklisted_usernames=blacklisted_usernames)

        print('Success Count: '+ str(success_count))
        print('Failed Count: '+ str(failed_count))
        print(dt.datetime.now()-time_started)
    from crawl.models import Task
    t=Task.objects.all().filter(uuid=task['uuid'])[0]
    t.success_count+=success_count
    t.failed_count+=failed_count

    t.consumed_usernames=','.join(list(set(consumed_usernames)))  
    t.blacklisted_usernames=','.join(list(set(blacklisted_usernames))) 
    t.save()
    return True

def get_single_user_info_with_browser(username,task={},retry=0,):
    
    from base.browser import Browser
    from base.basic_crawler import Crawler
    from base.request_maker import Request
    from services.reports_manager.manager import Manager
    from services.instagram.end_points import EndPoints as ep
    from services.instagram.recursion import Recursion
    from services.instagram.compatpatch import ClientCompatPatch
    from base.storage_sense import Saver
    import threading
    import json
    cc=ClientCompatPatch()
    r=Recursion()
    r.reporter=Manager()
    task=task
    c=Crawler()
    c.service_name='isntagram'
    c.use_proxies=task.get('add_data',{}).get('use_proxies',{})
    c.reporter=Manager()
    c.reporter.run_id=task['run_id']
    c.reporter.task_id=task['uuid']
    c.reporter.service='instagram'
    r.reporter=c.reporter
    rq=Request()
    c.task=task
    exclude_params=[]
    browser=Browser()
    s=Saver()
    if username in s.get_consumed_blocks(task.get('uuid')):
        return False
    if retry>3:
        s.create_task_failures(task.get('uuid'),file_name=username,data=[])
        s.add_output_block_to_consumed(task.get('uuid'),username)
        c.reporter.report_performance(**{'type':'failed_to_acquire_use_info','message':'Failed to Scrape User info'})
        return False
    if rq.session:
        resp=c.make_request(url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+'')

        if resp['status']=='success':
          
            info=resp['data']
            info={'data':info,'status':'success'}
            resp=ep.user().user_info(**{'response':info})
            success_count+=1
            th=threading.Thread(target=r.save_parsed_response,args=(resp,{}),kwargs=task)
            th.start()  
            return True
        else:
            browser.driver.close()
            retry+=1
            return get_single_user_info_with_browser(username=username,retry=retry,task=task)

    else:
        c.initialize_all_variables(**{'username':task.get('username'),'profile':task.get('profile'),**task})
        c.open_custom_browser(selenium_wire=True,headless=True)
        browser=c.browser
        browser.get('https://www.instagram.com/'+str(username)+'')
        try:
            web_profile_info=c.find_request(identifiers=['web_profile_info'],exclude_params=exclude_params,wait_time=60)
                
        except Exception as e:
         
            browser.driver.close()
            retry+=1
            return get_single_user_info_with_browser(username=username,retry=retry,task=task)
        else:
            
            if web_profile_info:
                exclude_params.append(web_profile_info[0].params)
                try:
                    
                    info=json.loads(web_profile_info[0].response.body)
                except Exception as e:
                    failed_count+=0
                    print('Exception occured while parsing the response body')
                else:
                    info={'data':info,'status':'success'}
                    resp=ep.user().user_info(**{'response':info})
                    th=threading.Thread(target=r.save_parsed_response,args=(resp,{}),kwargs=task)
                    th.start()   
                    print('Scraped user info for'+str(username))
                    s=Saver()
                   
                    s.add_output_block_to_consumed(task.get('uuid'),username)
                    return True
                    
            else:
                
                try:
                    browser.driver.close()
                except Exception as e:
                    pass
                retry+=1
                return get_single_user_info_with_browser(username=username,retry=retry,task=task)






def generate_session_id():
  import random
  """Generates a random session ID in the format xxxxxxx:xxxxxxx:xxxxxxx."""
  part1 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
  part2 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
  part3 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
  print(f"{part1}:{part2}:{part3}")
  return f"{part1}:{part2}:{part3}"
import random

def generate_random_integer_with_same_length(example_integer):
  """Generates a random integer with the same number of digits as the example."""
  example_str = str(example_integer)
  length = len(example_str)

  if length <= 0:
    return 0
  lower_bound = 10**(length - 1)
  upper_bound = (10**length) - 1
  return str(random.randint(lower_bound, upper_bound))

