from base.device import Device
from base.storage_sense import Saver
from uiautomator2 import Direction
from services.instagram.device.locator import Locator
from services.reports_manager.manager import Manager
from uiautomator2 import Direction
from services.instagram.run_bot import Instagram
from crawl.models import Interaction
from services.instagram.device.xpaths import Xpaths
import time
import random
class Search(Instagram):
    
    def __init__(self):
        super().__init__()
        self.current_page=None
       
        self.locator=Locator()
        self.xpaths=Xpaths()
        from services.reports_manager.manager import Manager
        self.reporter=Manager()
      
    def report(self,type,data_point,screenshot=False):
        report={'service':'instagram','end_point':'run_bot','data_point':data_point,
                                                    'type':type,'task':self.task['uuid']
                                                    }
        if screenshot:
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)  
            report.update({'screenshot':pth})
             
        self.reporter.report_performance(**report)   
        return pth
    def ensure_page_is_search_page(self,query):
      
        self.locator.identify_current_page()
        if self.locator.page=='search_results_page':
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'ensure_page_is_search_page',
                                            'type':'opened_search_page','screenshot':pth,'task':self.task['uuid'] })


            elem,_info=self.locator.locate(**{'touch_point':'get_search_text'})
            
            if elem.info:
                imagebin=self.device.screenshot(format='raw')
                s=Saver()
                pth=s.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'ensure_page_is_search_page',
                                                'type':'found_enter_search_text_field','screenshot':pth,'task':self.task['uuid'] })
                text=elem.info['text']
                if len(text)>0:
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'ensure_page_is_search_page',
                                                    'type':'search_text_field_already_filled','screenshot':pth })
                if text==query:
                    return 'search_results_page'

        
        else:
            elem,_info=self.locator.locate(**{'touch_point':'get_search_button'})
            if elem:
                elem.click()
        self.locator.page='explore_page'
        imagebin=self.device.screenshot(format='raw')
        s=Saver()
        pth=s.save_screenshot(imagebin)
        self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'ensure_page_is_search_page',
                                        'type':'opened_explore_page','screenshot':pth,'task':self.task.get('uuid') })
        """ elif page=='posts_page':
            self.device.swipe_ext(Direction.BACKWARD)
            elem,_info=self.locator.locate(**{'touch_point':'get_search_title'})
            text=_info['text']
            if text==query:
                return 'posts_page' """
    def make_search(self,**kwargs):
       
       
        query=kwargs.get('query')
        #self.ensure_page_is_search_page(query)
        imagebin=self.device.screenshot(format='raw')
        s=Saver()
        pth=s.save_screenshot(imagebin)
        self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                        'type':'find_search_text_field','screenshot':pth })
        if self.locator.locate_by_xpath(self.xpaths.Navigation().click_search_button(),click=True,retries=3):
            pass
        else:
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'not_found_search_button','screenshot':pth })
            
        
        if self.locator.locate_by_xpath(xpath=self.xpaths.Search().enter_search_query(),click=True):
            self.device.clear_text()
            self.device.send_keys(query)
            time.sleep(0.089)
            self.device.press('enter')
            
            self.current_page='search_results'
        else:
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'not_found_enter_search_text_field','screenshot':pth })
        self.current_page='search_page'
        return self
    def find_user_from_search_results(self,**kwargs):
        if not self.locator.locate_by_xpath(xpath=self.xpaths.Navigation().click_search_button(),retries=10):
            print('Navigation Not found')
            if self.locator.locate_by_xpath(self.xpaths.Posts().get_share_post_button(),click=True,retries=5):
                self.device.press('back')
            elif self.locator.locate_by_xpath(self.xpaths.Posts().click_your_story_button(),click=True,retries=5):
                self.device.press('back')
                if self.locator.locate_by_xpath(self.xpaths.Posts().click_discard_photo(),click=True,retries=5):
                    self.device.press('back')
                self.device.press('back')
        query=kwargs.get('query')
    
        if not self.locator.locate_by_xpath(self.xpaths.SearchResults().get_accounts_section(),retries=5):
            self.make_search(**kwargs)
            return self.find_user_from_search_results(**kwargs)
        else:
            elem=self.locator.locate_by_xpath(self.xpaths.SearchResults().get_search_text())
            if elem.text==query:
                pass
            else:
                self.make_search(**kwargs)
                return self.find_user_from_search_results(**kwargs)  
            if self.locator.locate_by_xpath(self.xpaths.SearchResults().get_accounts_section(),retries=5,click=True):        
                time.sleep(2)
                for i in range(0,2):
                    results=self.locator.locate_by_xpath(self.xpaths.SearchResults().accounts_section_results__username(),retries=10,elements=True)
                    if results:
                        for res in results:
                            info=res.info
                            username=info.get('text')
                            print(username)
                            if username==query:
                                
                                res.click()
                            
                            return True
                    return False
                #self.device.swipe_ext(Direction.FORWARD)

                
          
        return self

class Profile:
    def __init__(self):
        self.current_page=None
     
        self.xpaths=Xpaths()
        self.profile_page=self.xpaths.ProfilePage()
        self.locator=Locator()
        from services.reports_manager.manager import Manager
        self.reporter=Manager()
      
    def report(self,type,data_point,screenshot=False):
        report={'service':'instagram','end_point':'run_bot','data_point':data_point,
                                                    'type':type,'task':self.task['uuid']
                                                    }
        if screenshot:
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)  
            report.update({'screenshot':pth})
             
        self.reporter.report_performance(**report)   
        return pth
    def ensure_page_is_profile_page(self):
        
        
        
       
        gfo=self.locator.locate_by_xpath(self.profile_page.get_followers(),retries=2)
        gfl=self.locator.locate_by_xpath(self.profile_page.get_following(),retries=2)
        gusr=self.locator.locate_by_xpath(self.profile_page.get_username(),retries=2)
        if gfo or gusr or gfl:
            return True
        else:
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'Profile','data_point':'ensure_page_is_profile_page',
                                            'type':'located_page','screenshot':pth,'task':self.task['uuid'] })
            return False
    def interact_with_profile(self,**kwargs):
        
        interactions=[]
        self.ensure_page_is_profile_page()
        for interaction in kwargs.get('interactions'):
            interactions.append(interaction)

       
        
        interaction_count=0
        if 'follow' in interactions:
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            
            elem=self.locator.locate_by_xpath(self.profile_page.follow_button(),retries=2)
            if elem:
                imagebin=self.device.screenshot(format='raw')
                s=Saver()
                pth=s.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'Profile','data_point':'interact_with_profile',
                                            'type':'found_follow_button','screenshot':pth,'task':self.task['uuid'] })
                if elem.info.get('text')=='Following':
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    self.reporter.report_performance(**{'service':'instagram','end_point':'Profile','data_point':'interact_with_profile',
                                                    'type':'following_user','screenshot':pth,'task':self.task['uuid'] })
                    print('Already Following user')
                else:
                    
                    
                    elem.click()
                    if self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_review_this_account_before_following_text(),retries=4):
                        if self.locator.locate_by_xpath(self.xpaths.ProfilePage().click_follow_button_from_review_account(),retries=4,click=True):
                            time.sleep(1)
                        else:
                            return False
                    
                    self.device.screen_off()
                    self.device.screen_on()
                    time.sleep(1)
                    self.device.screen_on()
                    self.device.screen_on()
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    interaction_count+=1
                    i=Interaction(**{'bot_username':self.task['profile'],'target_profile':self.target_profile,'activity':'follow','screenshot':pth,'ref_id':self.task.get('ref_id')})
                    i.save()
                    time.sleep(2)

                    
            else:   
                imagebin=self.device.screenshot(format='raw')
                s=Saver()
                pth=s.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'Profile','data_point':'interact_with_profile',
                                            'type':'not_found_follow_button','screenshot':pth,'task':self.task['uuid'] })
        
        if 'dm' in interactions:
            messages=kwargs.get('messages')
            if len(messages)>0:
                message=random.choice(messages) 
                kwargs.update({'message':message})       
                if self.send_dm(**kwargs):
                    interaction_count+=1
                    i=Interaction(**{'bot_username':self.task['profile'],'target_profile':self.target_profile,'activity':'dm','screenshot':pth,'ref_id':str(self.task.get('ref_id',''))})
                    i.save()
                    self.device.press('back')
                    if not self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_username(),retries=5):
                        self.device.press('back')
                    self.locator.page=None
                    self.locator.sub_page=None
        if 'open_latest_post' in interactions or 'like_latest_post' in interactions:   
                 
            elems=self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_first_post_of_user(),elements=True,retries=3)
            if elems:
                elems[0].click()
                if 'like_latest_post' in interactions:
                    self.locator.locate_by_xpath(self.xpaths.Posts().get_like_button(),elements=False,click=True,retries=3)
                    imagebin=self.device.screenshot(format='raw')
                    file_name=self.storage_sense.save_screenshot(imagebin)
                    interaction_count+=1
                    i=Interaction(**{'ref_id':str(self.task.get('ref_id','')),'activity':'like',
                                        'target_profile':self.target_profile,'screenshot':file_name,'bot_username':self.task['profile'],
                                        
                                        })
                    i.save()
                
            else:
                self.device.swipe_ext(Direction.FORWARD)
                
                if self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_first_post_of_user(),click=True):


                    pass
                else:
                    return
            self.device.swipe_ext(Direction.BACKWARD)
        if 'go_through_posts' in interactions:
            for i in range(0,3):
                self.device.swipe_ext(Direction.FORWARD)
                imagebin=self.device.screenshot(format='raw')
                self.storage_sense.save_screenshot(imagebin)
        if 'see_story' in interactions:
            if self.locator.locate_by_xpath(self.xpaths.ProfilePage().has_unseen_story(),retries=5):
                pass
            self.locator.locate_by_xpath(self.xpaths.ProfilePage().has_unseen_story(),retries=5,click=True)
            time.sleep(2)
            if not self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_username(),retries=5):
                self.locator.locate_by_xpath(self.xpaths.StoryPage().like_story(),retries=5,click=True)
                time.sleep(1)
                 
                imagebin=self.device.screenshot(format='raw')
                file_name=self.storage_sense.save_screenshot(imagebin)
                interaction_count+=1
                i=Interaction(**{'bot_username':self.task['profile'],'target_profile':self.target_profile,'activity':'watch_story','screenshot':file_name,'ref_id':str(self.task.get('ref_id',''))})
                i.save()
                self.device.press('back') 
        if 'watch_highlights' in interactions:
            highlights= self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_highlights(),elements=True,retries=5)
            print(highlights)
            for highlight in highlights:
                highlight.click()
                time.sleep(random.ranint(1,5))
                if not self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_username(),retries=5):
                    self.device.press('back') 
                interaction_count+=1 
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                i=Interaction(**{'bot_username':self.task['profile'],'target_profile':self.target_profile,'activity':'watch_highlight','screenshot':pth,'ref_id':str(self.task.get('ref_id',''))})
                i.save()
        return interaction_count        
    def send_dm(self,step=0,bypass_step=False,**kwargs):
               
        elem=self.locator.locate_by_xpath(self.xpaths.ProfilePage().get_username(),retries=4)
        if elem and elem.text==self.target_profile:
            pass
        else:
            return False
        if self.locator.locate_by_xpath(self.xpaths.ProfilePage().send_message_to_user_button(),click=True,retries=5):           
        
            if self.locator.locate_by_xpath(self.xpaths.Messenger().get_messages_requests_are_changing_text(),retries=3):
                if self.locator.locate_by_xpath(self.xpaths.Messenger().click_ok_button_on_message_request_change_box(),retries=5,click=True):
                    pass
                else:
                    return False
            if self.locator.locate_by_xpath(self.xpaths.Messenger().check_cant_message_text(),retries=3):
                return False
            if self.locator.locate_by_xpath(self.xpaths.Messenger().enter_message(),retries=5,click=True):
                    self.device.send_keys(kwargs.get('message'))
                    if self.locator.locate_by_xpath(self.xpaths.Messenger().send_dm(),retries=6,click=True):
                
                        self.device.screen_off()
                        self.device.screen_on()
                        time.sleep(1)
                        self.device.screen_on()
                        time.sleep(2)
                        imagebin=self.device.screenshot(format='raw')
                        file_name=self.storage_sense.save_screenshot(imagebin)
                        i=Interaction(**{'ref_id':str(self.task.get('ref_id','')),'activity':'dm','dm_type':'reachout_message',
                                        'target_profile':self.target_profile,'screenshot':file_name,'bot_username':self.task['profile'],
                                        'data':{'message':kwargs.get('message')}
                                        })
                        i.save()
                        
                        return True
                        
                        
            else:
                return False
                print('Not handled yet page')   

class Post:
    def __init__(self):
        self.current_page=None
        self.xpaths=Xpaths()
        self.locator=Locator()
        from services.reports_manager.manager import Manager
        self.reporter=Manager()
      
    def report(self,type,data_point,screenshot=False):
        report={'service':'instagram','end_point':'run_bot','data_point':data_point,
                                                    'type':type,'task':self.task['uuid']
                                                    }
        if screenshot:
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)  
            report.update({'screenshot':pth})
             
        self.reporter.report_performance(**report)   
        return pth
    def ensure_page_is_posts_page(self):
      
        self.locator.identify_current_page()
        if self.locator.page=='posts_page':
            return True
        else:
            return False

    def interact_with_post(self,**kwargs):
        """         if not self.ensure_page_is_posts_page():
            return False """
        interactions=[]
        for interaction in kwargs.get('interactions'):
            interactions.append(interaction)
       
       
        if 'share_as_story' in interactions:
            
            self.locator.locate_by_xpath(self.xpaths.Posts().get_like_button(),click=True,retries=5)
            time.sleep(2)
            if self.locator.locate_by_xpath(self.xpaths.Posts().get_share_post_button(),click=True,retries=5):#_(**{'touch_point':'get_share_post_button'})
                elem=self.locator.locate_by_xpath(self.xpaths.SharePostPage().click_share_button())
                bounds=elem.info.get('bounds')            
                x1,x2,y1,y2=bounds.get('left'),bounds.get('right'),bounds.get('top'),bounds.get('bottom')
                for i in range(0,3):
                    self.device.swipe_ext(Direction.HORIZ_FORWARD,box=(x1,y1,1000,y2))
                    time.sleep(1)
                    try:
                        
                        self.device(text="Add to story").click()
                    except Exception as e:
                        clicked=False
                    else:
                        clicked=True
                        break
                if clicked:
                    loading=True
                    time_start=time.time()
                    while loading:

                        if self.locator.locate_by_xpath(self.xpaths.Posts().check_story_loading_status(),retries=4):
                            pass
                        else:
                            loading=False
                        if time.time()-time_start>180:
                            print('time xceeded')
                            loading=False
                        
                        print('still loading')
                        print(time.time()-time_start)
                    if self.locator.locate_by_xpath(self.xpaths.Posts().click_your_story_button(),click=True,retries=4):
                        time.sleep(2)
                        self.device.press("back")
                        self.locator.locate_by_xpath(self.xpaths.HomePage().click_home_button(),click=True)
                        
                        time.sleep(2)
                        self.device(text="Your story").click()
                        time.sleep(2)
                        pth=self.report(type='shared_post_as_story',screenshot=True,data_point='interact_with_post')
                        i=Interaction(**{'bot_username':self.task['profile'],'target_profile':self.target_profile,'activity':'shared_latest_post_as_story','screenshot':pth,'ref_id':self.task.get('ref_id')})
                        i.save()
             

    