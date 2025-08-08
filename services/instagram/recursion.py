import uuid
import logging
import os
from base.storage_sense import Saver
from services.instagram.end_points import EndPoints
from services.instagram.storage_sense import StorageSense
from services.reports_manager.manager import Manager
from base.purpose_helper import PurposeHelper
class Recursion(object):
    def __init__(self):
        self.crawler=None
        self.session_id='1231245'
        self.storage_sense=StorageSense
        self.scraped_so_far=0
        self.not_fine=0
        self.service=''
        self.next_cursors=[]
        self.used_nextos=[]
        self.end_point=''
        self.data_point=''
        self.crawler=EndPoints()
        self.used_nextos={'next_cursor':[],'previous_cursor':[],'next_max_id':[],'next_page':[],'end_cursor':[]}
        self.stop_condition_satisfied=False
        self.crawls=0
        self.reporter=Manager()
    
   
    def recursive_api_caller(self,move='forward',max_scrape_count=None,scraped_so_far=0,not_fine=0,**kwargs):
            self.reporter.report_performance(**{
                                                'type':'crawled','task':kwargs.get('uuid'),'service':'instagram'
                                                })
            self.crawler.end_point_handler.end_point=self.end_point
            self.crawler.end_point_handler.data_point=self.data_point          
            data=self.crawler.end_point_handler.get_required_data_point(**kwargs)    
            if data:
                payload=data.get('payload',[])
                print('Data Acquired for '+str(kwargs))

                
                
                next_page_info=self.next_recursion_status(data,**kwargs)
                import threading
                #threading.Thread(target=self.save_parsed_response,args=(data,next_page_info),kwargs=kwargs).start()
                self.save_parsed_response(data,next_page_info=next_page_info,**kwargs)
                if self.check_stop_condition(data,next_page_info,**kwargs):
                    return False
                if next_page_info:
                    self.reporter.report_performance(**{
                                                'type':'found_next_page_info','task':kwargs.get('uuid')
                                                })
                    
                    for key,value in next_page_info.items():
                        kwargs.update({key:value})
                    self.crawls+=1
                    
                    if self.should_recursion_continue():
                        self.reporter.report_performance(**{'service':'instagram',
                            'type':'continue_crawling','task':kwargs.get('uuid')
                            })
                        return self.recursive_api_caller(scraped_so_far=scraped_so_far,max_scrape_count=max_scrape_count,not_fine=not_fine,**kwargs) 
                else:
                    print('No Next Page Data Available')
                    self.reporter.report_performance(**{'service':'instagram',
                                                'type':'not_found_next_page_info','task':kwargs.get('uuid')
                                                })
                    return
            else:
                self.reporter.report_performance(**{'service':'instagram',
                                                'type':'error','string':{'args':'Expected Data from Data Point'},'data':data,'task':kwargs.get('uuid')
                                                })
                print('unexpected error occured')
    def save_parsed_response(self,data,next_page_info,**kwargs):
        import datetime as dt        
        comments_scraped=0
        users_scraped=0
        posts_scraped=0
        from base.downloader import Downloader
        d=Downloader()
        d.reporter=self.reporter
        d.request_maker
        d.storage_house_url=kwargs.get('add_data',{}).get('storage_house_url')
        s=Saver()
        s.file_extension='.csv'
        s.service='instagram'
        end_point=kwargs.get('end_point')
        data_point=kwargs.get('data_point')
        
       
        if end_point=='user':
  
            s.block={'block_address':''}           
            if data_point=='user_info' or data_point=='user_info_graphql' or data_point=='bulk_user_info_scraper':
                
                for u in data.get('users',[]):
                    u['profile_pic']=''
                    if '.' in u['username']:
                        username=u['username'].replace('.',',')
                    else:
                        username=u['username']
                    s.overwrite=True
                    s.block={'address':'users.'+username,'data':u,'file_name':'info'}
                    s.load_block()
                    
                    d.file_path=s.block_address
                    
                    fp=d.download_media('image',u.get('profile_pic_url_hd') if u.get('profile_pic_url_hd') else u.get('profile_pic_url'),save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'),bucket_name='instagram_profile_pic')
                    if fp:
                        u['profile_picture']=fp
                    
                    s.block.update({'data':u})
                    s.add_values_to_file()
                        
                    u['service']='instagram'
                    u.update({'object_type':'profile','task_uuid':kwargs.get('uuid')})
                    from services.instagram.compatpatch import ClientCompatPatch
                    c=ClientCompatPatch()
                    
                    u=c.user(u)
                    u['profile_picture']=fp
                    u.update({'object_type':'profile','service':'instagram'})
                    print('Scraped username: '+str(u['username']))
                    s.create_task_outputs(kwargs.get('uuid'),data=u,file_name=u['username'],block_name=kwargs.get('add_data',{}).get('block_name',''))
                    
                for p in data.get('posts',[]):
                    s.overwrite=False
                    s.block={'address':'users.'+username+'.posts.'+p['shortcode']+'','data':p,'file_name':'info'}
                    s.load_block()
                    post=p
                    d.file_path=s.block_address
                    downloaded_medias=False

                    if not downloaded_medias: 
                        post['downloaded_medias']=[]
                        out=d.download_media('image',post['display_url'],save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))
                        post['downloaded_medias'].append(out)                  
                        if post.get('media_type')==2 or post.get('is_video'):
                            media_type='video'
                            url=post['video_url']
                            out=d.download_media('video',url,save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))

                            
                            post['downloaded_medias'].append(out)
                    post['service']='instagram'
                    post['object_type']='post'
                    s.overwrite=True
                    s.load_block()       
                    s.add_values_to_file()
                    from services.instagram.compatpatch import ClientCompatPatch
                    c=ClientCompatPatch()
                    post=c.media(post)                
                    post.update({'object_type':'post','service':'instagram'})
                    s.create_task_outputs(kwargs.get('uuid'),data=post,block_name='posts')
                if data.get('next_page_info'):
                    _data={'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                    _data.update(next_page_info)
                    s.overwrite=False
                    s.block={'address':'users.'+username+'.posts','data':_data,'file_name':'register'}
                    s.load_block()
                    s.add_values_to_file()
                self.reporter.report_performance(**{
                                'type':'data_acquired','task':kwargs.get('uuid'),
                                'total_user_info_scraped':len(data.get('users')),'total_posts_scraped':len(data.get('posts'))
                                })
            elif data_point=='user_posts':
                for p in data.get('posts',[]):
                    post=p
                    post['downloaded_medias']=[]
                    username=data.get('username')
                    if '.' in username:
                        username=username.replace('.',',')
                    s.overwrite=False
                    s.block={'address':'users.'+username+'.posts.'+p['shortcode']+'','data':p,'file_name':'info'}
                    s.load_block()
                    s.overwrite=True
                    
                    d.file_path=s.block_address
                    fp=d.download_media('image',post['image_versions2']['candidates'][0]['url'],save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))
                    if fp:
                        post['downloaded_medias'].append(fp)
                    
                    
                    if post['media_type']==2:
                        media_type='video'
                        url=post['video_versions'][0]['url']
                        fp=d.download_media(media_type,url,save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))
                        if fp:
                            post['downloaded_medias'].append(fp)
                    s.add_values_to_file()   
                
                _data={'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                _data.update(next_page_info)
                s.overwrite=False
                s.block={'address':'users.'+username+'.posts','data':_data,'file_name':'register'}
                s.load_block()
                s.add_values_to_file()
                self.reporter.report_performance(**{
                                'type':'data_acquired','task':kwargs.get('uuid'),
                               'total_posts_scraped':len(data.get('posts'))
                                })
            elif data_point=='user_followers':
                self.reporter.report_performance(**{'service':'instagram',
                                                'type':'saving_user_followers','task':kwargs.get('uuid')
                                                })
     
                username=data.get('username').replace('.',',')
                s.block_id=str(uuid.uuid1())
                for u in data.get('users',[]):
                   
                    s.block={'address':'users.'+u['username'].replace('.',','),'data':u,'file_name':'info'}
                    
                    s.load_block()

                    if os.path.exists(os.path.join(s.block_address,'info.json')):
                        user_info=s.open_file()
                        user_info=s.data_frame.to_dict(orient='records')[0]
                        

                        d.file_path=s.block_address
                        fp=d.download_media('image',u['profile_picture'],'profile_picture',save_to_local_storage=kwargs.get('add_data',True).get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'),bucket_name='instagram_profile_pic')
                       
                        if fp:
                            
                            u['profile_picture']=fp
                            s.block.update({'data':user_info})
                            s.overwrite=True
                            s.add_values_to_file()
                    else:
                        d.file_path=s.block_address
                        
                        fp=d.download_media('image',u['profile_pic_url'],'profile_picture',save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'),bucket_name='instagram_profile_pic')
                        if fp:
                            u['profile_picture']=fp
                       
                        s.block.update({'data':u})
                        s.add_values_to_file()
                        
                    u['service']='instagram'
                    u.update({'object_type':'user_followers','follower_of':username})
                    s.overwrite=True
                    s.block={'address':'users.'+username+'.followers','data':u,'file_name':u['username'].replace('.',',')}
                    s.load_block()
                    
                    s.add_values_to_file()
                    s.create_task_outputs(kwargs.get('uuid'),data=u,block_name='users')
                _data={'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                _data.update(next_page_info)
                s.overwrite=False
                s.block={'address':'users.'+data.get('username').replace('.',',')+'.followers','data':_data,'file_name':'register'}
                s.load_block()
                s.add_values_to_file()
                self.reporter.report_performance(**{
                                'type':'data_acquired','task':kwargs.get('uuid'),
                               'total_users_scraped':len(data.get('users'))
                                }) 
         
        if end_point=='location':
           
            
  
            if self.data_point=='search_location':
                
                s.create_block(**{'end_point':'location','service':self.service,'enduser':'hamza@123', 'file_name':'register'}).\
                open_register().add_values_to_register(data.get('locations',[]))
                #s.data_block={'end_point':'location','service':self.service,'username':'', 'file_name':'register'}
                #s.open_register()
                #s.add_values_to_register()
            elif self.data_point=='country_directory':
               
                _data={'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                _data.update(next_page_info)
                s.block={'address':'location.countries','file_name':'register','data':_data}
                s.add_values_to_file()               
                for country in data.get('countries',[]):                          
                    country.update({'has_next_page':True,'next_cursor':None,'last_scraped_at':dt.datetime.now()})
                    s.block={'address':'location.countries.'+country['slug']+'','file_name':'register','data':country}
                    s.add_values_to_file()
                s.create_task_outputs(kwargs.get('uuid'),data=data.get('countries'),block_name='countries')
            elif self.data_point=='city_directory':
                dir=data.get('city_directory',{})
                
                country_slug=dir.get('country_info',{}).get('slug',None)
                country_name=dir.get('country_info',{}).get('name',None)
                id=dir.get('country_info',{}).get('id',None)
                _data={'id':id,'name':country_name,'slug':country_slug,'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                _data.update(next_page_info)
                block={'address':'location.countries.'+country_slug+'.cities','file_name':'register','data':_data}
                s.block=block
                s.add_values_to_file()
                #s.create_block(**{'end_point':'location','service':self.service,'enduser':'hamza@123','identifier':country_name,'file_name':'register'}).add_values_to_register(_data)
                for city in dir.get('cities',[]):
                   
                    
                    #s.create_block(**{'end_point':'location','service':self.service,'enduser':'hamza@123', 'identifier':country_name,'data_point':city['name'],'file_name':'register'})              
                    city.update({'has_next_page':True ,'last_scraped_at':dt.datetime.now()})
                    city.update({'next_cursor':None})
                    block={'address':'location.countries.'+country_slug+'.cities.'+city['slug']+'.locations','file_name':'register','data':city}
                    s.block=block
                    s.add_values_to_file()
                s.create_task_outputs(kwargs.get('uuid'),data=dir.get('cities'),block_name='cities')           
            elif self.data_point=='location_directory':
                dir=data.get('location_directory',{})
                country_name=dir.get('country_info',{}).get('slug','')
                country_slug=dir.get('country_info',{}).get('name','')

                city_slug=dir.get('city_info',{}).get('slug',' ')
                city_name=dir.get('city_info',{}).get('name','')
                city_id=dir.get('city_info',{}).get('id','')
                _data={'id':city_id,'name':city_name,'slug':city_slug,'has_next_page':True if next_page_info else False,'last_scraped_at':dt.datetime.now()}
                _data.update(next_page_info)
             
                block={'address':'location.countries.'+country_name+'.cities.'+city_id+'.locations','file_name':'register','data':_data}
                s.block=block
                s.add_values_to_file()
                for location in dir.get('locations',[]):
                    block={'address':'location.countries.'+country_name+'.cities.'+city_id+'.locations.'+location['slug']+'','file_name':'register','data':_data}              
                    location.update({'has_next_page':True ,'last_scraped_at':dt.datetime.now().timestamp()})
                    location.update({'next_cursor':None})
                    block.update({'data':location})
                    s.block=block
                    s.add_values_to_file()
                s.create_task_outputs(kwargs.get('uuid'),data=dir.get('locations'),block_name='locations')
            elif self.data_point=='info':
                recent_posts=data.get('recent_posts',[])
                recent_posts_next_page_info=data.get('recent_posts_next_page_info',{})
                ranked_posts=data.get('ranked_posts',[])
                ranked_posts_next_page_info=data.get('ranked_posts_next_page_info',{})
            elif self.data_point=='location_posts':
                location_posts=data.get('location_posts')
                next_page_info=data.get('next_page_info')
                location_info=kwargs.get('location_info')
                location_slug=location_info.get('slug',None)
                val=location_slug
                if not location_slug:
                    val=kwargs.get('location_info').get('id')

                country_info=kwargs.get('country_info',{})
                tab=kwargs.get('tab','recent')
                if not country_info:
                    location_block_address='location.places.'+val+''
            
                else:
                    country_slug=country_info.get('slug',None)
                    city_info=kwargs.get('city_info')
                    directory_code=city_info.get('id')
                    city_slug=city_info.get('slug')
                    location_block_address='location.countries.'+country_slug+'.cities.'+city_slug+'.locations.'+location_slug+'' 
                if next_page_info:                 
                
                    location_register={'has_next_page':True ,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                    location_register.update(next_page_info)
                else:
                    location_register={'has_next_page':False,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                    
                self.storage_sense.block={'address':location_block_address+'.'+tab+'','file_name':'register','data':location_register}
                self.storage_sense.load_block()       
                self.storage_sense.add_values_to_file()
                self.reporter.report_performance(**{'service':'instagram',
                                                'type':'saving_location_posts','task':kwargs.get('uuid')
                                                })
                user_count=0
                print(location_posts)
                for zem in location_posts:
                    user=zem.get('user',{})
                    if '.' in user['username']:
                        username=user['username'].replace('.',',')
                    else:
                        username=user['username']
                    
                    user_count+=1
                    block={'address':'users.'+username+'','data':user,'file_name':'info'}
                    s.block=block
                    s.load_block()
                    d.file_path=s.block_address
                    fp=d.download_media('image',user['profile_pic_url'],'profile_picture',save_to_local_storage=True,save_to_storage_house=True)
  
                    
                    if fp:
                        user['profile_pic']=fp
                    user['object_type']='user'
                    user['service']='instagram' 
                    s.add_values_to_file()
                   
                    s.block={'address':location_block_address+'.'+tab+'.users','file_name':username,'data':user}

                    s.overwrite=True
                    s.load_block()       
                    s.add_values_to_file()
                    s.overwrite=False
                    
                    s.create_task_outputs(kwargs.get('uuid'),data=user,block_name='users')
                    post=zem
                    block={'address':'users.'+username+'.posts.'+post['code']+'','data':post,'file_name':'info'}
                    s.block=block
                    s.load_block()
                    d.file_path=s.block_address
                    post['downloaded_medias']=[]
                    fp=d.download_media('image',post['image_versions2']['candidates'][0]['url'],save_to_local_storage=True,save_to_storage_house=True)
                    if fp:
                        post['downloaded_medias'].append(fp)
                    
                    
                    if post['media_type']==2:
                        media_type='video'
                        url=post['video_versions'][0]['url']
                        fp=d.download_media(media_type,url,save_to_local_storage=True,save_to_storage_house=True)
                        if fp:
                            post['downloaded_medias'].append(fp)
                    post['object_type']='post'
                    post['service']='instagram'
                    s.add_values_to_file()

                    
                    s.block={'address':location_block_address+'.'+tab+'.posts','file_name':post['code'],'data':post}
                    s.overwrite=True
                    s.load_block()
                    s.add_values_to_file()
                    s.overwrite=False
                    s.create_task_outputs(kwargs.get('uuid'),data=post,block_name='posts')
                self.reporter.report_performance(**{
                                'type':'data_acquired','task':kwargs.get('uuid'),
                                'total_users_scraped':len(location_posts),'total_posts_scraped':len(location_posts)
                                })
            elif self.data_point=='location_postss' or self.data_point=='location_info':
                recent_posts=data.get('recent_posts',[])
                recent_posts_next_page_info=data.get('recent_posts_next_page_info',{})
                ranked_posts=data.get('ranked_posts',[])
                ranked_posts_next_page_info=data.get('ranked_posts_next_page_info',{})
           
                location_info=kwargs.get('location_info')
                location_slug=location_info.get('slug',None)
                val=location_slug
                if not location_slug:
                    val=kwargs.get('location_info').get('id')

                country_info=kwargs.get('country_info',{})
                tab=kwargs.get('tab','recent')
                if not country_info:
                    location_block_address='location.places.'+val+''
            
                else:
                    country_slug=country_info.get('slug',None)
                    city_info=kwargs.get('city_info')
                    directory_code=city_info.get('id')
                    city_slug=city_info.get('slug')
                    location_block_address='location.countries.'+country_slug+'.cities.'+city_slug+'.locations.'+location_slug+''   
                if data.get('location_info'):

                    location_info.update(data.get('location_info'))  
                    self.storage_sense.block={'address':location_block_address,'file_name':'info','data':location_info}
                    self.storage_sense.load_block()       
                    self.storage_sense.add_values_to_file()           
                if recent_posts_next_page_info.get('next_max_id'):                 
                
                    location_register={'has_next_page':True ,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                    location_register.update(recent_posts_next_page_info)
                    self.storage_sense.block={'address':location_block_address+'.recent','file_name':'register','data':location_register}
                    self.storage_sense.load_block()       
                    self.storage_sense.add_values_to_file()
                else:
                    if kwargs.get('tab')=='recent':             
                        location_register={'has_next_page':False ,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                        location_register.update(recent_posts_next_page_info)
                        self.storage_sense.block={'address':location_block_address+'.'+tab+'','file_name':'register','data':location_register}
                        self.storage_sense.load_block()       
                        self.storage_sense.add_values_to_file()

                if ranked_posts_next_page_info.get('next_max_id'):              
                    location_register={'has_next_page':True ,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                    location_register.update(ranked_posts_next_page_info)
                    self.storage_sense.block={'address':location_block_address+'.ranked','file_name':'register','data':location_register}
                    self.storage_sense.load_block()       
                    self.storage_sense.add_values_to_file()                   
                else:
                    if kwargs.get('tab')=='ranked':
                        location_register={'has_next_page':False ,'last_scraped_at':dt.datetime.now(),'id':location_info['id']}
                        location_register.update(recent_posts_next_page_info)
                        self.storage_sense.block={'address':location_block_address+'.'+tab+'','file_name':'register','data':location_register}
                        self.storage_sense.load_block()       
                        self.storage_sense.add_values_to_file()
                    



                
                if tab=='recent':
                    posts=recent_posts[0]
                elif tab=='ranked':
                    posts=ranked_posts[0]
                self.reporter.report_performance(**{'service':'instagram','end_point':'recursion','data_point':'save_parsed_response',
                                                'type':'saving_location_posts','task':kwargs.get('uuid')
                                                })
                self.reporter.report_performance(**{'service':'instagram','end_point':'recursion','data_point':'save_parsed_response',
                                                'type':'scraped_'+str(len(posts)),'task':kwargs.get('uuid')
                                                })
                for zem in posts:
                    user=zem.get('user',{})
                    if '.' in user['username']:
                        username=user['username'].replace('.',',')
                    else:
                        username=user['username']
                    block={'address':'users.'+username+'','data':user,'file_name':'info'}
                    s.block=block
                    s.overwrite=True
                    s.add_values_to_file()
                    from base.downloader import Downloader
                    d=Downloader()
                    d.file_path=s.block_address
                    d.download_media('image',user['hd_profile_pic_url_info']['url'],'profile_picture')
                    s.block={'address':location_block_address+'.'+tab+'.users','file_name':username,'data':user}
                    s.overwrite=True
                    s.load_block()       
                    s.add_values_to_file()
                    s.overwrite=False
                    if not user['is_private']:
                        task={'service':self.service,
                            
                        'end_point':'user',
                        'data_point':'user_followers',
                        'input':user['username'],
                        'workflow':kwargs.get('workflow'),
                        'job':kwargs.get('job'),
                        'uuid':str(uuid.uuid1()),
                        'os':'browser',
                        'interact':False
                        }
                        #self.storage_sense.change_state_of_task(task=task,state='pending')

                    post=zem.get('post',{})
                    block={'address':'users.'+username+'.posts.'+post['code']+'','data':post,'file_name':'info'}
                    s.block=block
                    s.add_values_to_file()

                    d.file_path=s.block_address
                    if post['media_type']==2:
                        media_type='video'
                    else:
                        media_type='image'
                    s.block={'address':location_block_address+'.'+tab+'.posts','file_name':post['code'],'data':post}
                    s.overwrite=True
                    s.load_block()       
                    s.add_values_to_file()
                    s.overwrite=False
                    
                    d.download_media(media_type,post['image_versions2']['candidates'][0]['url'])
        if end_point=='search':
            if self.data_point=='search_keyword':
                search_keyword_posts=data.get('search_keyword_posts')
                next_page_info=data.get('next_page_info')
                
                keyword=kwargs.get('keyword')
                search_block={'address':'search.keywords.'+keyword,'file_name':'register'}
                search_block_address='search.keywords.'+keyword
                if next_page_info:                 
                
                    search_keyword_register={'has_next_page':True ,'last_scraped_at':dt.datetime.now(),'query':keyword}
                    search_keyword_register.update(next_page_info)
                else:
                    search_keyword_register={'has_next_page':True if next_page_info else False ,'last_scraped_at':dt.datetime.now(),'query':keyword}
                self.storage_sense.block={'address':'search.keywords.'+keyword,'file_name':'register','data':search_keyword_register}
                self.storage_sense.load_block()       
                self.storage_sense.add_values_to_file()
                self.reporter.report_performance(**{
                                                'type':'saving_search_keyword','task':kwargs.get('uuid')
                                                })
                
                posts=[]
                for zem in search_keyword_posts:
                    user=zem.get('user',{})
                    if '.' in user['username']:
                        username=user['username'].replace('.',',')
                    else:
                        username=user['username']
                    block={'address':'users.'+username+'','data':user,'file_name':'info'}
                    s.block=block
                    s.load_block()
                    d.file_path=s.block_address
                    out=d.download_media('image',user['hd_profile_pic_url_info']['url'],save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))
                    user['profile_picture']=out
                        
                            
                   
                    user['service']='instagram'
                    user['object_type']='user'
                    s.block={'address':search_block_address+'.users','file_name':username,'data':user}
                    s.overwrite=True
                    s.load_block() 
                    s.add_values_to_file()
                    s.create_task_outputs(kwargs.get('uuid'),data=user,block_name='users')                  
                    post=zem
                    block={'address':'users.'+username+'.posts.'+post['code']+'','data':post,'file_name':'info'}
                    s.block=block                  
                    
                    s.load_block()
                    d.file_path=s.block_address
                    downloaded_medias=False

                    if not downloaded_medias: 
                        post['downloaded_medias']=[]
                        out=d.download_media('image',post['image_versions2']['candidates'][0]['url'],save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))
                        post['downloaded_medias'].append(out)                  
                        if post['media_type']==2:
                            media_type='video'
                            url=post['video_versions'][0]['url']
                            out=d.download_media('video',url,save_to_local_storage=kwargs.get('add_data').get('save_to_local_storage'),save_to_storage_house=kwargs.get('add_data').get('save_to_storage_house'))

                            
                            post['downloaded_medias'].append(out)
                    s.add_values_to_file()
                    post['service']='instagram'
                    post['object_type']='post'
                    if kwargs.get('add_data').get('create_task_outputs',True):
                        s.create_task_outputs(kwargs.get('uuid'),data=post,block_name='posts')

                    s.block={'address':search_block_address+'.posts','file_name':post['code'],'data':post}
                    s.overwrite=True
                    s.load_block()       
                    s.add_values_to_file()
                    s.overwrite=False
                self.reporter.report_performance(**{
                                'type':'data_acquired','task':kwargs.get('uuid'),
                                'total_users_scraped':len(zem),'total_posts_scraped':len(zem)
                                })  
                        
        return data    
    def check_stop_condition(self,data,next_page_info,**kwargs):
        p=PurposeHelper()
        if 'next_page_info' in kwargs.get('stop_condition',{}).get('data_point',{}).keys():
            p.data_block={'next_page_info':next_page_info}
        else:
            p.data_block=data
        p.data_point={} 

        if kwargs.get('stop_condition'):
            p.data_point=kwargs.get('stop_condition',{}).get('data_point')
            p.help(search=False)
            stop_condition=kwargs.get('stop_condition',{})
            if stop_condition.get('filter')=='contains':
                value=stop_condition.get('value')

                if value in p.results:
                    print('stop condition found.Exiting Now')
                    self.stop_condition_satisfied=True
                    return True
            elif stop_condition.get('filter')=='equals':
                value=stop_condition.get('value')
                if value in p.results:
                    self.stop_condition_satisfied=True
                    return True
        return False     
    def next_recursion_status(self,data,**kwargs):
        found=0
        nextos=data.get('nextos')
        if nextos:
            pass
        else:
            nextos=['next_cursor']
        _next_page_info={}
        if self.data_point=='location_info':
            next_page_info={}
        elif self.data_point=='location_posts':
            next_page_info=data.get('next_page_info')
            if not next_page_info:
                if kwargs.get('tab','recent')=='recent':
                    next_page_info=data.get('recent_posts_next_page_info')
                elif kwargs.get('tab','ranked'):
                    next_page_info=data.get('ranked_posts_next_page_info')


        else:
            next_page_info=data.get('next_page_info')
        _next_page_info={}
        if next_page_info:
            for key,value in next_page_info.items():
                if key in nextos:
                    if not value:
                        self.not_fine+=1
                    elif value in self.used_nextos.get(key):
                        self.not_fine+=1
                    else:
                        print('new '+key)
                        self.used_nextos.get(key).append(value)
                        self.not_fine=0
                        _next_page_info.update({key:value})
                        found+=1
            if not found ==len(nextos):
                return {}
      
        return _next_page_info
    def should_recursion_continue(self):
        if self.data_point=='user_info' or self.data_point=='location_info':
            return False
        if self.crawls>=self.max_crawls:
            return False
        if self.crawler.max_scrape_count:
            if self.scraped_so_far>self.crawler.max_scrape_count:                
                return False
        return True
      

    
        
