from base.device import Device
from base.storage_sense import Saver
from uiautomator2 import Direction
from services.instagram.device.locator import Locator
from services.reports_manager.manager import Manager
from services.instagram.device.search import Search
from services.instagram.device.xpaths import Xpaths
from base.storage_sense import Saver
import time
import random
class Instagram(Device):
    def __init__(self):
        super().__init__()
        self.task={}
        self.locator=Locator()
        self.logged_in=False
        self.app_package='com.instagram.android'
        self.service='instagram'
        self.reporter=Manager()
        self.storage_sense=Saver()
        self.android_search=Search()
        x=Xpaths()
        self.homepage=x.HomePage()
        self.profilepage=x.ProfilePage()
        self.explorepage=x.Search()
        self.posts_page=x.Posts()
        self.comments_page=x.Comments()
        self.followings_page=x.FollowingsPage()
        self.new_post_page=x.NewPostPage()
        
    def create_device_object_and_start_app(self):
      
        
        try:
            self.connect_device().unlock_screen().start_app()
        except Exception as e:
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'create_device_object_and_start_app',
                                              'task':self.task['uuid'],'type':'device_connection_failure','reason':e,'device':self.serial_number})
            raise Exception('run_bot_launch_failure')
        else:
            
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'create_device_object_and_start_app',
                                                'task':self.task['uuid'],'type':'device_connected_successfully','device':self.serial_number})

        self.locator.device=self.device
        self.homepage.device=self.device
        self.homepage.locator=self.locator
        self.profilepage.device=self.device
        self.profilepage.locator=self.locator
        self.explorepage.device=self.device
        self.explorepage.locator=self.locator
        self.posts_page.device=self.device
        self.posts_page.locator=self.locator
        self.followings_page.locator=self.locator
        self.followings_page.device=self.device
        self.comments_page.locator=self.locator
        self.comments_page.device=self.device
        self.new_post_page.locator=self.locator
        self.new_post_page.device=self.device
        return self
    def perform_automation(self):
        self.create_device_object_and_start_target_app()   
    def start_scraping(self):
        self.create_device_object_and_start_target_app()
        for i in range(0,10):
            if self.device.xpath("//*[@resource-id='com.zhiliaoapp.musically:id/mfo']").exists:
                for elem in self.device.xpath("//*[@resource-id='com.zhiliaoapp.musically:id/mfo']").all():
                    print(elem.attrib.get('text'))
            self.device.swipe_ext(Direction.FORWARD)
    def open_profile_tab(self):
        elem,info=self.locator.locate(**{'touch_point':'profile_tab'})
        if elem:
            elem.click()
            print('clicked Profile Tab ')
            
        else:
            print('Failed to Open Profile Tab')
        return self
    def click_switch_account_button(self):
        elem,info=self.locator.locate(**{'touch_point':'account_switcher'})
        if elem:
            elem.click()
            print('clicked Account Switcher ')
            
        else:
            print('Failed to Open Account Switcher')
        return self
    def choose_account_from_accounts_list(self):
        elem,info=self.locator.locate(**{'touch_point':'choose_account_from_accounts_list','text':'camarena_artss'})
        if elem:
            elem.click()
            print('clicked Account Switcher ')
         
        else:
            print('Failed to Open Account Switcher')
        return self
    def get_profile_information(self):
        infos=['get_first_post_of_user','get_username','get_followers','get_posts','get_following',
               'get_name','get_business_category',
               'get_bio'
               
               ]
        for info in infos:
            elem,_info=self.locator.locate(**{'touch_point':info})
            if _info:
                if elem and info=='get_first_post_of_user':
                    elem.click()
                print(_info.get('text',))
            else:
                print(info+' not found')   
    def make_search(self,**kwargs):
        query=kwargs.get(query)
        page=self.locator.identify_current_page()
        if page=='search_results_page':
            elem,_info=self.locator.locate(**{'touch_point':'get_search_text'})
            if elem.info:
                text=elem.info['text']
                if text==query:
                    return 'search_results_page'
        elif page=='posts_page':
            self.device.swipe_ext(Direction.BACKWARD)
            elem,_info=self.locator.locate(**{'touch_point':'get_search_title'})
            text=_info['text']
            if text==query:
                return 'posts_page'
       
        elem,_info=self.locator.locate(**{'touch_point':'get_search_button'})
        if elem:
            elem.click()
        elem,_info=self.locator.locate(**{'touch_point':'enter_search_query'})
        if elem:
           
            elem.click()
            self.device.clear_text()
            self.device.send_keys(query)
            
            self.device.press('enter')
        return 'search_results_page'
    def explore_through_homepage(self,**kwargs):  
        add_data=kwargs.get('add_data') 

    
        
        
        
        if not self.homepage.is_home_page():
            if self.explorepage.is_explore_page():
                self.locator.locate_by_xpath(self.homepage.click_home_button(),click=True)
            if self.profilepage.is_profile_page():
                self.locator.locate_by_xpath(self.homepage.click_home_button(),click=True)
            elif self.comments_page.is_comments_page():
                self.device.press('back')
                if not self.homepage.is_home_page():
                    self.locator.locate_by_xpath(self.homepage.click_home_button(),click=True)
            else:
                self.locator.locate_by_xpath(self.homepage.click_home_button(),click=True)
                return self.explore_through_homepage(**kwargs)
        fail=0
        for i in range(0,10):#add_data.get('max_swipes',random.randint(1,8))):
            if fail>3:
                return
            self.device.swipe(10, 20, 30, random.randint(20,100))
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'explore_through_home_page',
                                              'task':self.task['uuid'],'type':'Performed Swipe','device':self.serial_number})
            self.device.swipe_ext(Direction.FORWARD)
            if self.comments_page.is_comments_page():
                self.device.press('back')
                time.sleep(0.3) 
                if not self.posts_page.is_posts_page():
                    self.device.press('back')
                 
               

            
            if random.randint(1,10) in [3,2,4]:
                self.locator.locate_by_xpath(self.homepage.get_like_button(),click=True)
                if add_data.get('open_comments_and_scroll',False):
                    self.locator.locate_by_xpath(self.homepage.get_comment_button(),click=True)
                    if self.comments_page.is_comments_page():              
                        for i in range(0,2):
                            time.sleep(random.randint(1,3))
                            self.device.swipe_ext(Direction.FORWARD)
                            
                    

                     
            #self.save_data()
    def save_data(self):
        d={}
        post_page_touch_points=['get_username','get_likes','get_caption','get_comments']
        attrs=['username','likes_count','caption','comments_count']
        for i,tp in enumerate(post_page_touch_points):
            
            
            elem,info=self.locator.locate(**{'touch_point':tp,'elements':False,'notrack':True})
            if not info:
                val=None
            else:
                if tp=='get_username':
                    username=''
                    val=info['text'].replace(' ','').strip(' ')
                   
                else:
                     val=info['text']
            print(val)
                

            d.update({attrs[i]:val})
    def explore_explore_page(self,**kwargs):
        if self.homepage.is_home_page():
            if self.locator.locate_by_xpath(self.homepage.get_search_button(),click=True):
                time.sleep(2)
        elif self.profilepage.is_profile_page():
            if self.locator.locate_by_xpath(self.homepage.get_search_button(),click=True):
                time.sleep(2)
        elif self.explorepage.is_explore_page():
            pass
        elif self.posts_page.is_posts_page():
            self.device.press('back')
        else:
            self.stop_app()
            self.start_app()
            return self.explore_explore_page(**kwargs)
        add_data=kwargs.get('add_data')    
        self.device.click(100,500)
        self.report(type='clicked_post_on_explore_page',data_point='explore_explore_page',screenshot=True)
        opened_posts_count=0
        for i in range(0,add_data.get('max_swipes')):
            self.device.swipe_ext(Direction.FORWARD)
            self.report(type='post_screenshot',data_point='explore_explore_page',screenshot=True)
            time.sleep(1)
            if random.randint(1,100) in [2,3,7,70,90,45]:
                self.device.click(100,400)
                
                if not opened_posts_count>=add_data.get('max_open_posts'):
                    if self.locator.locate_by_xpath(self.posts_page.get_comment_button(),click=True):
                        for z in range(0,add_data.get('max_swipes_in_open_posts',3)):
                            self.report(type='comments_screenshot',data_point='explore_explore_page',screenshot=True)
                            self.device.swipe_ext(Direction.FORWARD)
                            time.sleep(random.randint(1,5))
                            self.locator.page='posts_page'
                            self.locator.xpath=None
                            self.locator.locate_by_xpath(self.posts_page.get_like_button(),click=True)
                            self.report(type='liked_comment',data_point='explore_explore_page',screenshot=True)
                            opened_posts_count+=1

            if self.locator.locate_by_xpath(self.comments_page.get_write_comment_box()):
                self.device.press('back')

                time.sleep(2)
                self.report(type='went_back',data_point='explore_explore_page',screenshot=True)
           
           
            
            if random.randint(1,10) in [2,3,7]:
                self.locator.locate_by_xpath(self.posts_page.get_like_button(),click=True)
                self.report(type='liked_post',data_point='explore_explore_page',screenshot=True)
        
           
       
    
        
        
    def send_dm(self,step=0,bypass_step=False,**kwargs):
        self.start_app()           
        self.locator.identify_current_page()
        if self.locator.page=='home_page':            
            elem,_info=self.locator.locate(**{'touch_point':'click_inbox_button','notrack':True})
            if elem:
                elem.click()
                self.locator.page='messenger_page'
                return self.send_dm(**kwargs)
        elif self.locator.page=='messenger_page':
            
            if self.locator.sub_page=='inbox_page':
                elem,_info=self.locator.locate(**{'touch_point':'click_create_new_message_button','notrack':True})
                if elem:
                    elem.click()
                    return self.send_dm(step=1,**kwargs)
            elif self.locator.sub_page=='search_recipient_page':
                if not bypass_step:
                    if step==0:
                        self.device.press("back")
                        return self.send_dm(step=1,**kwargs)
                elem,_info=self.locator.locate(**{'touch_point':'search_recipient','notrack':True})
                if elem:
                    elem.click()
                    self.device.send_keys('camarena_artss')
                    time.sleep(2)
                    elems,_info=self.locator.locate(**{'touch_point':'search_results__username','notrack':True,'elements':True})
                    if elems:
                        for elem in elems:
                            elem.click()
                            time.sleep(1)
                            return self.send_dm(**kwargs)
            elif self.locator.sub_page=='compose_message_page':
                if not bypass_step:
                    if step==0:
                        self.device.press("back")
                        return self.send_dm(step=1,**kwargs)
                elem,_info=self.locator.locate(**{'touch_point':'enter_message','notrack':True})
                if elem:
                    elem.click()
                    self.device.send_keys("hi, we succeeded")
                    elem,_info=self.locator.locate(**{'touch_point':'send_dm','notrack':True})
                    if elem:
                        elem.click()

                    
        else:
            print('Not handled yet page')
    def watch_story(self,**kwargs):
        add_data=kwargs.get('add_data') 
        
        self.locator.identify_current_page()
        if self.locator.page=='home_page':            
            elem,_info=self.locator.locate(**{'touch_point':'click_create_story_button','notrack':True})
            if elem:
                elem.click()
    def ensure_page_is_new_post_page(self,retry=0):
        if retry>=3:
            return False
        retry+=1
        self.locator.identify_current_page()
        if  self.locator.page=='new_post_page':  
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'located_post_page','screenshot':pth,'task':self.task['uuid']
                                                })
            print('Current Page is New Post Creation Page')
            if self.locator.sub_page=='select_media':
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'located_select_media_page','screenshot':pth,'task':self.task['uuid']
                                                })
                return 
            elif self.locator.sub_page=='select_album_list':
                print('Sub-Page is Select Album. Going Back 1time')
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'located_select_album_list_page','screenshot':pth,'task':self.task['uuid']
                                                })
                self.device.press("back")
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                                })
            
            else:
                
                self.device.press("back")
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                                })
                print('Unknow Sub-Page.Going Back')
                elem,_info=self.locator.locate(**{'touch_point':'click_start_over_button','notrack':True})
                if elem:
                    print('Start over Button Found')
                    elem.click()
                print('Start over Button Not found.Checking if the current page is still New Post Page and active sub-page is Select Media')
        else:
            elem,_info=self.locator.locate(**{'touch_point':'click_camera_button','notrack':True})
            if elem:
                print('Clicked Camera Button. New post Creation Process Started')
                elem.click()
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'clicked_camera_button','screenshot':pth,'task':self.task['uuid']
                                                })
                self.page='new_post_page' 
            else:
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'not_found_camera_button','screenshot':pth,'task':self.task['uuid']
                                                })
                print('Camera Button Not Found. Exiting Post Creation')
        return self.ensure_page_is_new_post_page(retry=retry)
    def clear_posting_folder(self):
        output, exit_code=self.device.shell("ls sdcard/darrxscale", timeout=60)
        for file in output.split('\n'):
            file_path='sdcard/darrxscale/'+file
            command="rm "+file_path
            output, exit_code = self.device.shell(command, timeout=60)
            print(output)
        output, exit_code=self.device.shell("ls sdcard/darrxscale", timeout=60)
        print(output)
    def push_files_to_posting_folder(self,file_paths):
        import uuid

        for file_path in file_paths:
            extension=file_path.split('.')[1]
            file_name=str(uuid.uuid1())+'.'+extension
            android_file_path='sdcard/darrxscale/'+file_name
            file=open(file_path,'rb')
            self.device.push(file,android_file_path)
            print('pushed one file')
            output, exit_code=self.device.shell("am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///"+android_file_path+"", timeout=60)
            print(output)
            
            output, exit_code=self.device.shell("ls sdcard/darrxscale", timeout=60)
            print(output)
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
    def make_post(self,**kwargs):
        add_data=kwargs.get('add_data')
        self.ensure_page_is_new_post_page()
        self.report(type='opened_make_post_page',data_point='make_post',screenshot=True)
    
        if not self.locator.locate_by_xpath(self.new_post_page.open_gallery(),click=True):
            self.report(type='failed_to_open_gallery',screenshot=True,data_point='make_post')
            return
        else:
            self.report(type='opened_gallery',screenshot=True,data_point='make_post')   
            print('Successfully Opened gallery')
            try:

                self.device(text="darrxscale").click()
            except Exception as e:
                self.report(type='failed_to_click_darrxscale_album',screenshot=True,data_point='make_post')
                
            else:
                self.report(type='clicked_and_selected_darrxscale_album',screenshot=True,data_point='make_post')
                if not self.locator.locate_by_xpath(self.new_post_page.click_select_mulitple_phots_button(),click=True):
                    self.report(type='failed_to_click_select_multiple_photos',screenshot=True,data_point='make_post')
                else:
                    self.report(type='clicked_select_multiple_photos',screenshot=True,data_point='make_post')
                    elems=self.locator.locate_by_xpath(self.new_post_page.get_iterable_media_grid_of_album_photos(),elements=True)
                    
                    for i, elem in enumerate(elems):
                        if i==0:
                            continue
                        elem.click()
                    print('Selected '+str(i)+' Medias')
                    self.report(type='selected_photos',screenshot=True,data_point='make_post')
                    if not self.locator.locate_by_xpath(self.new_post_page.click_next_button_from_media_picker(),click=True):
                        self.report(type='failed_to_click_next_button_from_media_pickers',screenshot=True,data_point='make_post')
                    else:
                        self.report(type='clicked_next_button_from_media_pickers',screenshot=True,data_point='make_post')   
                        print('Clicked next button from media Picker')
                        time.sleep(2)
                        self.create_dump()
                        if not self.locator.locate_by_xpath(self.new_post_page.click_next_button_from_filter_picker(),click=True,retries=10):
                            self.report(type='failed_to_click_next_button_from_filter_picker',screenshot=True,data_point='make_post')
                        else:
                            self.report(type='clicked_next_button_from_filter_picker',screenshot=True,data_point='make_post')
                            time.sleep(4)
                            if not self.locator.locate_by_xpath(self.new_post_page.focus_on_caption_area(),click=True,retries=30):
                                self.report(type='not_found_caption_area',screenshot=True,data_point='make_post')
                            else:
                                if add_data.get('caption'):                      
                                    self.device.send_keys(add_data.get('caption'))
                                    self.report(type='sent_caption',screenshot=True,data_point='make_post')
                                else:
                                    print('Caption Not found in payload')
                                
                                if self.device(text="OK").exists:
                                    self.device(text="OK").click()
                                if add_data.get('location'):
                                    if not self.locator.locate_by_xpath(self.new_post_page.click_on_add_location_option(),click=True):
                                        self.report(type='failed_to_click_add_location_option',screenshot=True,data_point='make_post')
                                    else:
                                        self.report(type='clicked_add_location_option',screenshot=True,data_point='make_post')
                                        if not self.locator.locate_by_xpath(self.new_post_page.focus_on_location_input(),click=True):
                                            self.report(type='location_input_not_found',screenshot=True,data_point='make_post')
                                            self.device.press("back")
                                            self.report(type='went_back_from_location_input',screenshot=True,data_point='make_post')
                                        else:                                    
                                            print('Clicked and Focussed on the Location Input Area')
                                            self.device.send_keys(add_data.get('location'))
                                            self.report(type='entered_location_input',screenshot=True,data_point='make_post')
                                            if not self.locator.locate_by_xpath(self.new_post_page.choose_first_suggestion(),click=True,retries=5):
                                                self.report(type='no_suggestions_found_for_location_input',screenshot=True,data_point='make_post')
                                                self.device.press("back")
                                            else:
                                                self.report(type='clicked_first_suggestion',screenshot=True,data_point='make_post')
                                if add_data.get('music'):
                                    if not self.locator.locate_by_xpath(self.new_post_page.click_add_music_button(),click=True):
                                        self.report(type='not_found_add_music_button',screenshot=True,data_point='make_post')
                                    else:
                                        self.report(type='clicked_add_music_button',screenshot=True,data_point='make_post')
                                        if not self.locator.locate_by_xpath(self.new_post_page.focus_on_search_music_input(),click=True):
                                            self.report(type='not_found_music_input',screenshot=True,data_point='make_post')
                                            self.device.press('back')
                                        else:
                                            self.report(type='found_music_input',screenshot=True,data_point='make_post')
                                                          
                               
                                            self.device.send_keys(add_data.get('music'))
                                            if not self.locator.locate_by_xpath(self.new_post_page.choose_first_music_suggestion(),click=True):
                                                self.device.press("back")
                                                self.device.press("back")
                                                self.device.press("back")
                                            else:
                                                self.report(type='failed_to_add_Music',screenshot=True,data_point='make_post')
                                                self.locator.locate_by_xpath(self.new_post_page.finish_music_addition(),click=True)
                                
                                if self.locator.locate_by_xpath(self.new_post_page.share_post_final(),click=True):
                                    self.report(type='made_android_Feed_post',screenshot=True,data_point='make_post')

                                    time.sleep(20)
                                    
                                    self.storage_sense.block={'address':'profiles.'+self.task.get('profile')+'.consumed_gdrive_folder_names','file_name':self.task.get('google_drive_folder_name')}
                                    self.storage_sense.load_resources()
                                    self.storage_sense.add_values_to_file(load_block=False)
                                    return True               


            return False
    def search_user_and_interact(self,user):
        from services.instagram.device.search import Search,Profile,Post
        from base.storage_sense import Saver
        self.android_search.locator=self.locator
        self.android_search.device=self.device
        self.android_search.task=self.task
        add_data=self.task.get('add_data')
        interactions=[]
        messages=[]
        if add_data.get('send_reachout_message'):
            interactions.append('dm')
            messages=add_data.get('messaging').get('values')
        if add_data.get('like_latest_post'):
            interactions.append('open_lastest_post')  
            interactions.append('like_latest_post')
        if add_data.get('share_latest_post_as_story'):
            interactions.append('open_latest_post')
            interactions.append('share_as_story')
        if add_data.get('watch_story'):
            interactions.append('see_story')
        if add_data.get('watch_highlights'):
            interactions.append('watch_highlights')
        if add_data.get('follow_target'):
            interactions.append('follow')
        
        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'searching_and_interacting_with_user','task':self.task['uuid']
                                                })
        if self.android_search.find_user_from_search_results(**{'query':user}):
            imagebin=self.device.screenshot(format='raw')
            self.storage_sense.save_screenshot(imagebin)
            
            p=Profile()
            p.task=self.task
            p.locator=self.locator
            p.device=self.device
            p.storage_sense=self.storage_sense
            p.target_profile=user
            
            interaction_count=p.interact_with_profile(**{'interactions':interactions,'messages':messages})
            from base.storage_sense import Saver
            s=Saver()
            s.add_output_block_to_consumed(id=self.task['uuid'],output_block=user)
            imagebin=self.device.screenshot(format='raw')
            self.storage_sense.save_screenshot(imagebin)
            p=Post()
            p.target_profile=user
            p.task=self.task
            p.storage_sense=self.storage_sense
            p.locator=self.locator
            p.device=self.device
            p.interact_with_post(**{'interactions':interactions})
            imagebin=self.device.screenshot(format='raw')
            self.storage_sense.save_screenshot(imagebin)
            self.device.press("back")
            self.device.swipe_ext(Direction.BACKWARD)
            self.device.swipe_ext(Direction.BACKWARD)
            self.device.swipe_ext(Direction.BACKWARD)
            s=Saver()
            imagebin=self.device.screenshot(format='raw')
            pth=s.save_screenshot(imagebin)
            
            self.reporter.report_performance(**{'service':'instagram','end_point':'Profile','data_point':'interact_with_profile',
                                    'type':'clicked_follow_button','screenshot':pth, 'task':self.task['uuid'] })
    def get_all_posts(self):
        elems=self.locator.locate(**{'touch_point':'get_posts','elements':True})
        for elem in elems:
            elem.click()
    def get_post_info(self):
        d={}
        post_page_touch_points=['get_username','get_likes','get_caption','get_comments']
        attrs=['username','likes_count','caption','comments_count']
        for i,tp in enumerate(post_page_touch_points):
            
            
            elem,info=self.locator.locate(**{'touch_point':tp,'elements':False,'notrack':True})
            if not info:
                val=None
            else:
                if tp=='get_username':
                    username=''
                    val=info['text'].replace(' ','').strip(' ')
                   
                else:
                     val=info['text']
                

            d.update({attrs[i]:val})

        return d
    def push_files_to_posting_folder(self,file_paths):
        import uuid

        for i,file_path in enumerate(file_paths):
            extension=file_path.split('.')[1]
            file_name=str(i)+'.'+extension
            android_file_path='sdcard/darrxscale/'+file_name
            file=open(file_path,'rb')
            self.device.push(file,android_file_path)
            print('pushed one file')
            output, exit_code=self.device.shell("am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///"+android_file_path+"", timeout=60)
            print(output)
            
            output, exit_code=self.device.shell("ls sdcard/darrxscale", timeout=60)
            print(output)
    def ensure_page_is_home_page(self,count=0):
        
        self.locator.identify_current_page()
        if self.locator.page=='home_page': 
            return True
        else:
            if self.locator.page in ['post_page','profile_page','search_results_page','explore_page']:
                elem,info=self.locator.locate(**{'touch_point':'click_home_button','notrack':True})
                if elem:
                    elem.click()
                    count+=1
                    return self.ensure_page_is_home_page(count)
            if count>=10:
                return False
            self.device.press("back") 
            time.sleep(1)
            self.start_app()
            count+=1
            return self.ensure_page_is_home_page(count)
    def ensure_all_is_set(self,count=0):
        count+=1
        if count==3:
            self.stop_app()
            
            return self.ensure_all_is_set(count=count)
        if count>4:
            
            return False
        self.start_app()
        time.sleep(2)

        self.locator.identify_current_page()
        if self.locator.page=='profile_page':  
            return True
        elif self.locator.page=='home_page' or self.locator.page=='posts_page':
            elem,_info=self.locator.locate(**{'touch_point':'click_profile_tab','notrack':True})
            if elem:
                elem.click()
            else:
                self.device.press("back")
            
            return self.ensure_all_is_set(count)
        else:
           
            self.ensure_page_is_home_page()
            return self.ensure_all_is_set(count) 
    def test_progrmatic_code_creation(self,**kwargs):
        command='''Click  Get Profile button.
                    Click on Sort By default.
                    Get count of followings. 
                    If 
                        count greater than 60
                            exit
                    else
                        click followings table, then iterate through each row for 5 times, click unfollow button, take screenshot, save
                '''
        commands=command.split('.')
        for command in commands:
            output=execute_command(command)
            convey_output(output)

        def execute_command(command):
            if 'click' in command.lower():
                text=command.split('click')
                match=find_nearest_neighbor(text)
                xpaths=get_data_point(match.split('.')[1],match.split('.')[0])
                self.locator.locate_by_xpath(xpaths,click=True)
        def convey_output():
            pass
        def find_nearest_neighbor(text):
            data=create_json_rep_of_xpaths()
            sub=text
            #sub=''.join(ch for ch in sub if ch.isalnum())
            x=list(s for s in data['xpaths'] if sub in s)
            return x[0]
            #file=services.instagram.xpaths import Xpaths
        def create_json_rep_of_xpaths():
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
            j_rep={'pages':[]}
            pages=j_rep['pages']
            xpaths=[]
            import inspect
            from xpaths import Xpaths
            x=Xpaths()
            
            members = [attr for attr in dir(x) if callable(getattr(x, attr)) and not attr.startswith("__")]
            for member in members:
                xx=getattr(x,member)
                print(xx)
                

                members__ = [attr for attr in dir(xx) if callable(getattr(xx, attr)) and not attr.startswith("__")]
                pages.append({'name':member,'xpaths':members__})
                for member__ in members__:
                    xpaths.append(member__+'.'+member)
            print(xpaths)
            return {'xpaths':xpaths,'pages':j_rep}
        def get_data_point(end_point,data_point):
            from xpaths import Xpaths
            x=Xpaths()
            endpoint=getattr(x, end_point)
            datapoint=getattr(endpoint,data_point)
            return (datapoint(endpoint))
    def switch_account(self,retry=0,**kwargs):
        if retry>3:
            return False
        retry+=1
        if self.homepage.is_home_page():
            elem=self.locator.locate_by_xpath(self.homepage.click_profile_tab())
            if elem:
                elem.click()
                time.sleep(1)
                return self.switch_account(retry,**kwargs)
        elif self.explorepage.is_explore_page():
            elem=self.locator.locate_by_xpath(self.homepage.click_profile_tab())
            if elem:
                elem.click()
                time.sleep(1)
                return self.switch_account(retry,**kwargs)
        elif self.comments_page.is_comments_page():
            self.device.press("back")
            time.sleep(1)
            return self.switch_account(retry,**kwargs)
        elif self.posts_page.is_posts_page():
            elem=self.locator.locate_by_xpath(self.homepage.click_profile_tab())
            if elem:
                elem.click()
                return self.switch_account(retry,**kwargs)
        
        
            

        
            
        elif self.profilepage.is_profile_page():
           
            elem=self.locator.locate_by_xpath(self.profilepage.get_username(),retries=2)
            if elem:
                print(elem.text.lower())
                if elem.text.lower().strip(' ')==kwargs.get('username').lower():
                    return True
          
            if self.locator.locate_by_xpath(self.profilepage.click_account_switcher(),click=True):
                if self.device(text=kwargs.get('username').lower()).exists:
                    print('Account Already logged in')
                    self.device(text=kwargs.get('username').lower()).click()
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                            'type':'clicked_choose_account', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                            'screenshot':pth
                                            })
                    time.sleep(1)
                    
                    return True #self.switch_account(**kwargs)
                else:
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                            'type':'account_not_logged_in', 'username':kwargs.get('username'),'task':self.task['uuid'],
                                            'screenshot':pth
                                            }) 
                    return False
                         
                
        
        if self.locator.locate_by_xpath(self.profilepage.click_profile_tab(),click=True):
            return self.switch_account(**kwargs)
        else:
            self.stop_app()
            self.start_app()
            time.sleep(3)
            retry+=1
            return self.switch_account(**kwargs,retry=retry)
                    
    def add_account(self,retry=0,**kwargs):

        self.locator.identify_current_page()
        if self.locator.page=='profile_page':  
            elem,_info=self.locator.locate(**{'touch_point':'click_profile_tab','notrack':True})
            if elem:
                elem.click()

                
                elem,_info=self.locator.locate(**{'touch_point':'click_account_switcher','notrack':True})
                if elem:
                    elem.click()
                    time.sleep(2)
                    self.locator.page='add_switch_account_page'
                    self.locator.sub_page='add_account'
                    elem,_info=self.locator.locate(**{'touch_point':'get_logged_in_accounts','notrack':True,'elements':True})
                    if elem:
                       for username in elem:
                           if username.info.get('text')==kwargs.get('username'):
                                self.logged_in=True
                                self.device.press("back")
                                print('profile already logged in')
                                return
                    elem,_info=self.locator.locate(**{'touch_point':'click_add_account','notrack':True})
                    if elem:
                        elem.click()
                        time.sleep(2)
                        elem,_info=self.locator.locate(**{'touch_point':'click_login_to_existing_account','notrack':True})
                        if elem:
                            elem.click()
                            try:
                                self.device(text="NONE OF THE ABOVE").click()
                            except Exception as e:
                            
                                print(e)

                            elem,_info=self.locator.locate(**{'touch_point':'click_switch_account','notrack':True})
                            if elem:
                                elem.click()
                            return self.add_account(**kwargs)
            
        elif self.locator.page=='add_switch_account_page':  
            if self.locator.sub_page=='switch_account':
                elem,_info=self.locator.locate(**{'touch_point':'click_switch_account','notrack':True})
                if elem:
                    elem.click()
                    self.locator.sub_page=='login'
            if self.locator.sub_page=='login':                
                elem,_info=self.locator.locate(**{'touch_point':'get_username_input','notrack':True})
                if elem:
                    elem.click()
                    self.device.clear_text()
                    self.device.send_keys(kwargs.get('username'))
                    elem,_info=self.locator.locate(**{'touch_point':'get_password_input','notrack':True})
                    if elem:
                        elem.click()
                        self.device.clear_text()
                        self.device.send_keys(kwargs.get('password'))
                        elem,_info=self.locator.locate(**{'touch_point':'get_login_button','notrack':True})
                        if elem:
                            elem.click()
                            time.sleep(3)
                            elem,_info=self.locator.locate(**{'touch_point':'wrong_password','notrack':True})
                            if elem:
                                print('Wrong Password')
                                elem.click()   
                            elem,_info=self.locator.locate(**{'touch_point':'incorrect_username','notrack':True})
                            if elem:
                                print('Incorrect Username')
                                elem.click()  
                            elem,_info=self.locator.locate(**{'touch_point':'username_not_found','notrack':True})
                            if elem:
                                print('Incorrect Username')
                                elem.click() 
                            time.sleep(10)
                            self.locator.identify_current_page()
                            if self.locator.page=='home_page':
                                self.logged_in=False                             
                            
            else:
                self.device.press("back")
                return self.add_account(**kwargs)
        else:
            self.ensure_all_is_set()
            return self.add_account(**kwargs)         
    def create_new_account(self,retry=0,**kwargs):

        #1st check which page
        if retry>3:
            return False
        
        time.sleep(2)
        self.locator.page='create_new_account'
        
        elem,info=self.locator.locate(**{'touch_point':'click_none_of_the_above_accounts_screen_from_google','notrack':True})
        if elem:
            print('None of the ABove Account Button CLicked')
            elem.click()
            time.sleep(1)
        self.locator.identify_current_page()
        if self.locator.page=='create_new_account':

            if self.locator.sub_page=='login_page':
                elem,_info=self.locator.locate(**{'touch_point':'click_create_new_account_button','notrack':True})
                if elem:
                    print('Incorrect Username')
                    elem.click()  
                    return self.create_new_account()
            elif self.locator.sub_page=='enter_full_name_page':
                elem,_info=self.locator.locate(**{'touch_point':'enter_full_name_page','notrack':True})
                if elem:
                    print('Full Name Page Entered') 
                    elem.click()
                    self.device.clear_text()
                    time.sleep(0.1)
                    elem,_info=self.locator.locate(**{'touch_point':'enter_full_name','notrack':True})
                    if elem:
                        elem.click()
                        
                        self.device.send_keys(self.full_name)
                        elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                        if elem:
                            elem.click()
                            return self.create_new_account()
            elif self.locator.sub_page=='enter_password_page':
                elem,_info=self.locator.locate(**{'touch_point':'enter_password_page','notrack':True})
                if elem:
                    print('Password Page Entered') 
                    elem,_info=self.locator.locate(**{'touch_point':'enter_password','notrack':True})
                    if elem:
                        elem.click()  
                                            
                        self.device.send_keys(self.password)
                        elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                        if elem:
                            elem.click()
                            return self.create_new_account()
            elif self.locator.sub_page=='save_login_info_page':
                elem,_info=self.locator.locate(**{'touch_point':'save_login_info_page','notrack':True})
                if elem:
                    print('Save Login Info Page Entered') 
                    elem,_info=self.locator.locate(**{'touch_point':'click_not_now_button','notrack':True})
                    if elem:
                        elem.click()  
                        return self.create_new_account()
            elif self.locator.sub_page=='set_birthday_page':
                for i in range(0,random.randint(3,10)):
                    self.device(className='android.widget.NumberPicker',instance=1).swipe("down", steps=0)
                for i in range(0,random.randint(3,20)):
                    self.device(className='android.widget.NumberPicker',instance=1).swipe("down", steps=0)
                for i in range(0,random.randint(3,20)):
                    self.device(className='android.widget.NumberPicker',instance=2).swipe("down", steps=0)
                
                elem,_info=self.locator.locate(**{'touch_point':'click_set_button','notrack':True})
                if elem:

                    elem.click()
                    print('SET BUTTON CLICKED')
                time.sleep(1)
                elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                if elem:
                    elem.click()
                    return self.create_new_account()
            elif self.locator.sub_page=='create_username_page':
                elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                if elem:
                    elem.click()
                    return self.create_new_account()
            elif self.locator.sub_page=='choose_contact_method_page':
                elem,_info=self.locator.locate(**{'touch_point':'choose_contact_method','notrack':True})
                if elem:
                    elem.click()
                    time.sleep(2)
                    
                   
                    
                    return self.create_new_account()
            elif self.locator.sub_page=='whats_your_email_page':
                self.device(text="Email").click()
                elem,_info=self.locator.locate(**{'touch_point':'enter_email_box','notrack':True})
                if elem:
                    elem.click()   
                    self.device.clear_text()     
                    self.device(text="Email").click()           
                    self.device(className='android.widget.EditText',instance=0).send_keys(self.email_address)
                    elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                    if elem:
                        elem.click()
                        return self.create_new_account()
            elif self.locator.sub_page=='enter_confirmation_code_page':
                elem,_info=self.locator.locate(**{'touch_point':'clear_confirmation_code_box','notrack':True})
                if elem:
                        elem.click()
                        elem,_info=self.locator.locate(**{'touch_point':'request_a_new_code','notrack':True})
                        if elem:
                            elem.click()
                            time.sleep(1)
                            elem,_info=self.locator.locate(**{'touch_point':'resend_confirmation_code','notrack':True})
                            if elem:
                                elem.click()
                                time.sleep(10)
                            
                from base.emails import DefaultClient
                d=DefaultClient('EMAIL_CONFIRMATION')
                d.email_address=self.email_address
                d.init()
                d.get_code()
                if len(d._codes)>0:
                    _code=''
                    code=d._codes[0]
                    for char in code:
                        print(char.isalpha())
                        if char.isnumeric():
                            _code+=char
                else:
                    elem,_info=self.locator.locate(**{'touch_point':'request_a_new_code','notrack':True})
                    if elem:
                        elem.click()
                        time.sleep(1)
                        elem,_info=self.locator.locate(**{'touch_point':'resend_confirmation_code','notrack':True})
                        if elem:
                            elem.click()
                            time.sleep(10)
                            return self.create_new_account()
                
                elem,_info=self.locator.locate(**{'touch_point':'enter_confirmation_code_box','notrack':True})
                if elem:
                    elem.click()   
                    self.device.clear_text()                
                    self.device(className='android.widget.EditText',instance=0).send_keys(_code)
                    elem,_info=self.locator.locate(**{'touch_point':'click_next_button','notrack':True})
                    if elem:
                        elem.click()
                        return self.create_new_account()
            elif self.locator.sub_page=='agree_to_instagram_page':
                elem,_info=self.locator.locate(**{'touch_point':'click_i_agree_button','notrack':True})
                if elem:
                    elem.click()
                    time.sleep(2)
                    return self.create_new_account()
            else:
                retry+=1
                return self.create_new_account(retry=retry)
    def post_story(self,**kwargs):
        
        self.ensure_page_is_new_post_page() 
        imagebin=self.device.screenshot(format='raw')
        pth=self.storage_sense.save_screenshot(imagebin)  
        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'opened_make_post_page','screenshot':pth,'task':self.task['uuid']
                                                })   
        elem,_info=self.locator.locate(**{'touch_point':'open_gallery','notrack':True})
        if not elem:
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)  
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                    'type':'failed_to_open_gallery','screenshot':pth,'task':self.task['uuid']
                                                    })   
        else:
            elem.click()
            imagebin=self.device.screenshot(format='raw')
            pth=self.storage_sense.save_screenshot(imagebin)  
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                    'type':'opened_gallery','screenshot':pth,'task':self.task['uuid']
                                                    })   
            print('Successfully Opened gallery')
            try:

                self.device(text="darrxscale").click()
            except Exception as e:
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)  
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                        'type':'failed_to_click_darrxscale_album','screenshot':pth,'task':self.task['uuid']
                                                        })   
                print('Failed to Click DarrxScale Album')
            else:
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)  
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                        'type':'clicked_and_selected_darrxscale_album','screenshot':pth,'task':self.task['uuid']
                                                        })   
                print('Clicked and Selected DarrxScale Album')
                elem,_info=self.locator.locate(**{'touch_point':'click_select_mulitple_phots_button','notrack':True})
                if not elem:
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                        'type':'failed_to_click_select_multiple_photos','screenshot':pth,'task':self.task['uuid']
                                                        })   
                    print('Failed to Click the Select Multiple photos button')
                else:
                    
                    elem.click()
                    imagebin=self.device.screenshot(format='raw')
                    pth=self.storage_sense.save_screenshot(imagebin)  
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                        'type':'clicked_select_multiple_photos','screenshot':pth,'task':self.task['uuid']
                                                        })   
                    print('Clicked Select multiple Photos Option')
                    print('Selecting All photos in Album')
                    elem,_info=self.locator.locate(**{'touch_point':'get_iterable_media_grid_of_album_photos','notrack':True,'elements':True})
                    for i, elem in enumerate(elem):
                        if i==0:
                            continue
                        elem.long_click()
                    print('Selected '+str(i)+' Medias')
                    imagebin=self.device.screenshot(format='raw')
                    pth=self.storage_sense.save_screenshot(imagebin)  
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                        'type':'selected_photos','screenshot':pth,'task':self.task['uuid']
                                                        })   
                    elem,_info=self.locator.locate(**{'touch_point':'click_next_button_from_media_picker','notrack':True})
                    if not elem:
                        imagebin=self.device.screenshot(format='raw')
                        pth=self.storage_sense.save_screenshot(imagebin)  
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                            'type':'failed_to_click_next_button_from_media_picker','screenshot':pth,'task':self.task['uuid']
                                                            })   
                        print('Failed to Click Next button from Media Picker')
                    else:
                        elem.click()
                        imagebin=self.device.screenshot(format='raw')
                        pth=self.storage_sense.save_screenshot(imagebin)  
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                            'type':'clicked_next_button_from_media_picker','screenshot':pth,'task':self.task['uuid']
                                                            })   
                        print('Clicked next button from media Picker')
                        time.sleep(2)
                        elem,_info=self.locator.locate(**{'touch_point':'click_next_button_from_filter_picker','notrack':True})
                        if not elem:
                            print('Failed to click next button from filter Picker')
                            imagebin=self.device.screenshot(format='raw')
                            pth=self.storage_sense.save_screenshot(imagebin)  
                            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                                'type':'failed_to_click_next_button_from_filter_picker','screenshot':pth,'task':self.task['uuid']
                                                                })   
                        else:
                           
                            self.device(text="Next").click()
                            imagebin=self.device.screenshot(format='raw')
                            pth=self.storage_sense.save_screenshot(imagebin)  
                            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                                'type':'clicked_next_button_from_filter_picker','screenshot':pth,'task':self.task['uuid']
                                                                })  
                            print('Clicked next button from filter picker')
                            time.sleep(2)
                            elem,_info=self.locator.locate(**{'touch_point':'focus_on_caption_area','notrack':True})
                            if not elem:
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                                    'type':'not_found_caption_area','screenshot':pth,'task':self.task['uuid']
                                                                    }) 
                                print('Failed to Focus on Caption Area')
                            else:
                                
                                elem.click()
                                
                                print('Clicked and Focused on Caption Caption Area')
                                
                                self.device.send_keys(kwargs.get('caption'))
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                                    'type':'sent_caption','screenshot':pth,'task':self.task['uuid']
                                                                    }) 
                                print('Sent caption to the Caption Area')
                                if self.device(text="OK").exists:
                                    self.device(text="OK").click()
                            elem,_info=self.locator.locate(**{'touch_point':'click_on_add_location_option','notrack':True})
                            if not elem:
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                                    'type':'failed_to_click_add_location_option','screenshot':pth,'task':self.task['uuid']
                                                                    }) 
                                print('Failed to Click on Add Location option')
                            else:
                                elem.click()
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'clicked_add_location_option','screenshot':pth,'task':self.task['uuid']
                                    }) 
                                print('Clicked on Add Location Option')

                                elem,_info=self.locator.locate(**{'touch_point':'focus_on_location_input','notrack':True})
                                if not elem:
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'location_input_not_found','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                    print('Failed to Focus on Location Input.Going back')
                                    
                                    self.device.press("back")
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                else:
                                    elem.click()
                                    
                                    print('Clicked and Focussed on the Location Input Area')
                                    self.device.send_keys(kwargs.get('location'))
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'entered_location_input','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                    print('Sent Location to the Input')
                                    time.sleep(2)
                                    elem,_info=self.locator.locate(**{'touch_point':'choose_first_suggestion','notrack':True})
                                    if not elem:
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'no_suggestions_found_for_location_input','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        self.device.press("back")
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        print('Waited 2s for the First Suggestion to Appear.None Found. Going back now')
                                    else:
                                        print('Clicked 1st suggestion after 2s wait')
                                        elem.click()
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'clicked_first_suggestion','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        
                            elem,_info=self.locator.locate(**{'touch_point':'click_add_music_button','notrack':True})
                            if not elem:
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'not_found_add_music_button','screenshot':pth,'task':self.task['uuid']
                                    }) 
                                print('Failed to find Add Music button')
                            else:

                                elem.click()
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'clicked_add_music_button','screenshot':pth,'task':self.task['uuid']
                                    }) 
                                print('Clicked Add  Music Button')
                                elem,_info=self.locator.locate(**{'touch_point':'focus_on_search_music_input','notrack':True})
                                if not elem:
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'not_found_music_input','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                   
                                else:
                                    elem.click()
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'found_music_input','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                    print('Clicked and Focused on Search Music Input')
                                    self.device.press("back")
                                    imagebin=self.device.screenshot(format='raw')
                                    pth=self.storage_sense.save_screenshot(imagebin)  
                                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                        'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                        }) 
                                    time.sleep(1)
                                    self.device.send_keys(kwargs.get('music'))
                                    print('Entered Music Search after 1s Wait')
                                    time.sleep(2)
                                    elem,_info=self.locator.locate(**{'touch_point':'choose_first_music_suggestion','notrack':True})
                                    if not elem:
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'failed_to_choose_first_music_suggestion','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        print('Failed to Choose First Music Suggestion.Going back now ')
                                        self.device.press("back")
                                        self.device.press("back")
                                        self.device.press("back")
                                    else:
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'found_first_music_suggestion','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        elem.click()
                                        imagebin=self.device.screenshot(format='raw')
                                        pth=self.storage_sense.save_screenshot(imagebin)  
                                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                            'type':'clicked_first_music_suggestion','screenshot':pth,'task':self.task['uuid']
                                            }) 
                                        elem,_info=self.locator.locate(**{'touch_point':'finish_music_addition','notrack':True})
                                        if not elem:
                                            imagebin=self.device.screenshot(format='raw')
                                            pth=self.storage_sense.save_screenshot(imagebin)  
                                            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'not_found_finish_music_add_button','screenshot':pth,'task':self.task['uuid']
                                                })
                                            print('Failed to Find Finish Music Additon Button.Going back now')
                                            self.device.press("back")
                                            imagebin=self.device.screenshot(format='raw')
                                            pth=self.storage_sense.save_screenshot(imagebin)  
                                            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'went_back','screenshot':pth,'task':self.task['uuid']
                                                })
                                        else:
                                            
                                            elem.click()
                                            imagebin=self.device.screenshot(format='raw')
                                            pth=self.storage_sense.save_screenshot(imagebin)  
                                            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                                'type':'clicked_finish_music_add_button','screenshot':pth,'task':self.task['uuid']
                                                })
                                            print('Clicked Finish Music Addition Button')
                            time.sleep(2)
                            elem,_info=self.locator.locate(**{'touch_point':'share_post_final','notrack':True})
                            if elem:
   
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'found_share_post_button','screenshot':pth,'task':self.task['uuid']
                                    })
                                elem.click()
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'clicked_share_post_button','screenshot':pth,'task':self.task['uuid']
                                    })
                                print('Successfully Shared the Post')
                            else:
                                imagebin=self.device.screenshot(format='raw')
                                pth=self.storage_sense.save_screenshot(imagebin)  
                                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'ensure_page_is_new_post_page',
                                    'type':'not_found_share_post_button','screenshot':pth,'task':self.task['uuid']
                                    })
                                print('Finalize and Share Post Button Not found')
                                                


            print(elem)
    def search_user_and_share_latest_post(self,user,**kwargs):
        from services.instagram.device.search import Search,Profile,Post
        self.stop_app()
        self.start_app()
        self.android_search.locator=self.locator
        self.android_search.device=self.device
        self.android_search.task=self.task
        
        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'searching_and_interacting_with_user','task':self.task['uuid']
                                                })
        if self.android_search.find_user_from_search_results(**{'query':user}):
            imagebin=self.device.screenshot(format='raw')
            self.storage_sense.save_screenshot(imagebin)
            
            p=Profile()
            p.task=self.task
            p.locator=self.locator
            p.device=self.device
            p.storage_sense=self.storage_sense
            p.interact_with_profile(**{'interactions':['open_first_post_of_user']})
            imagebin=self.device.screenshot(format='raw')
            self.storage_sense.save_screenshot(imagebin)
            p=Post()
            p.task=self.task
            p.storage_sense=self.storage_sense
            p.locator=self.locator
            p.device=self.device
            interactions=[]
            if 'story' in kwargs.get('share_post_as'):
                interactions.append('share_as_story')
            p.interact_with_post(**{'interactions':interactions})
    def unfollow_users(self):
        add_items=self.task.get('add_data')
        if add_items and add_items.get('unfollow_after'):
            unfollow_after=add_items.get('unfollow_after')
        else:
            unfollow_after=1
        if self.homepage.is_home_page():
            if self.locator.locate_by_xpath(self.profilepage.click_profile_tab(),click=True):
                return self.unfollow_users()
        elif self.profilepage.is_own_profile_page():
            elem=self.profilepage.is_own_profile_page()
            if elem:
                if elem.text==self.task.get('profile'):
                    count=self.locator.locate_by_xpath(self.profilepage.get_count_of_followings())
                    if not count:
                        self.locator.locate_by_xpath(self.profilepage.click_profile_tab(),click=True)
                        return self.unfollow_users()
                    if int(count.text)>unfollow_after:
                        pass
                    else:
                        return True
                    elem=self.locator.locate_by_xpath(self.profilepage.get_following(),click=True)
                    return self.unfollow_users()
        elif self.followings_page.is_followings_page():
            elem=self.locator.locate_by_xpath(self.followings_page.get_current_sorting_value())
            if 'earliest' in elem.text:
                print('Earliest')
            else:

                if self.locator.locate_by_xpath(self.followings_page.click_sort_by_button(),click=True):
                    if self.locator.locate_by_xpath(self.followings_page.click_sort_by_date_followed_earliest(),click=True):
                        print('Sorted by Earliest')
            unfollowed_users=[]
            while True:
                users=self.locator.locate_by_xpath(self.followings_page.click_following_button(),elements=True)
                if users:
                    for i in range(0,add_items.get('max_unfollows_per_run')):
                        user=self.locator.locate_by_xpath(self.followings_page.click_following_button(),elements=False)
                        if len(unfollowed_users)>=add_items.get('max_unfollows_per_run'):
                            return True

                        if user.attrib.get('content-desc') in unfollowed_users:
                            continue
                        else:
                            unfollowed_users.append(user.attrib.get('content-desc'))
                        if user.text=='Message':
                            self.locator.locate_by_xpath(self.followings_page.click_more_options_icon(),click=True)
                            self.locator.locate_by_xpath(self.followings_page.click_unfollow_from_more_options(),click=True)
                        else:
                            user.click()
                            time.sleep(1)
                            self.locator.locate_by_xpath(self.followings_page.click_unfollow_from_confirmation_dialog(),click=True)
                    self.device.swipe_ext(Direction.FORWARD)

    def run(self):
        import subprocess
        import time
        import psutil
        try:
            self.start()
        except Exception as e:
            print(e)
        self.stop_app()
        self.device.screen_off()   

    def start(self):
        #self.locator.storage_sense=self.storage_sense
        from crawl.models import Task
        task=Task.objects.all().filter(uuid=self.task['uuid'])
        if task:
            self.task_obj=task[0]
        else:
            self.task_obj=False
        from django.forms import model_to_dict
        profile=self.task.get('profile')
        if not profile:
          return 'No Login Profile Found'
        from crawl.models import ChildBot
        p=ChildBot.objects.all().filter(username=profile)
        if len(p)>0:
            p=p[0]
            self.serial_number=p.device.serial_number
            profile=model_to_dict(p)
        else:
            return
        
        self.create_device_object_and_start_app()
        self.reporter.task=self.task_obj
        #self.test_progrmatic_code_creation()
        self.device.uiautomator.start()
        

        from services.instagram.device.xpaths import Xpaths
        x=Xpaths()
        if self.locator.locate_by_xpath(x.ProfilePage().get_username(),retries=5):
                        print('yo')   
        if self.task.get('data_point')=='feed_post':
            if self.switch_account(**profile):
                self.clear_posting_folder()
                add_data=self.task.get('add_data')
                if add_data.get('google_drive_root_folder_name'):
                    self.storage_sense.block={'address':'tasks.'+self.task.get('uuid'),'file_name':'downloads'}
                    self.storage_sense.load_deep_stuff()
                    self.storage_sense.open_file()
                    if self.storage_sense.file.empty:                       
                        from base.googlesheets import GoogleSheet
                        from base.google_api import GoogleAPI
                        _g=GoogleAPI()

                        _g.service_account_from_dict()
                        ks={'folder_name':add_data.get('google_drive_root_folder_name')}
                        out=_g.find_folder(select_first=True,**ks) 
                        pth={add_data.get('google_drive_root_folder_name'):{}}
                        active_dict=pth[add_data.get('google_drive_root_folder_name')]
                        if not add_data.get('bypass_profile',True):              
                            ks.update({'folder_name':self.task.get('profile')})
                        resp=_g.get_files_in_folder(**ks)

                        if not add_data.get('bypass_profile',True): 
                            resp=sorted(resp, key=lambda d: int(d['name']))
                        
                            caption_pth=None
                            active_dict.update({self.task.get('profile')})
                            active_dict=active_dict[self.task.get('profile')]
                        else:
                            pth[add_data.get('google_drive_root_folder_name')].update({'media':[],'caption':''})
                        active_dict={add_data.get('google_drive_root_folder_name'):{'posts':[]}}
                        posts=[]
                        for media in resp:  
                            post={'number':media['name'],'medias':[],'caption':''}                                          
                            if media['mimeType']=='application/vnd.google-apps.folder':
                                
                                if not add_data.get('bypass_profile'):                                     
                                    ks.update({'folder_name':media['name']})
                                    resp_=_g.get_files_in_folder(**ks)
                                    #resp_=sorted(resp_, key=lambda d: int(d['name'].split('.')[0]))                                
                                    for media_ in resp_:
                                        try:
                                            _=_g.download_file(media_)['file_path']
                                            if media_['mimeType']=='text/plain':
                                                caption_pth=_
                                                with open (caption_pth,'r',encoding='utf-8') as file:
                                                    caption=file.read()
                                                    post['caption']=caption     
                                            else:
                                                post['medias'].append(_)
                                        except Exception as e:
                                            continue
                                    posts.append(post)
                                           
                            else:
                                
                                self.active_google_folder_name=add_data.get('google_drive_root_folder_name')       
                                try:

                                    _=_g.download_file(media)['file_path']                              
                                    if media['mimeType']=='text/plain':
                                        caption_pth=_
                                        with open (caption_pth,'r',encoding='utf-8') as file:
                                            caption=file.read()
                                            print(caption)      
                                            pth[add_data.get('google_drive_root_folder_name')]['caption']=caption
                                    else:
                                        pth[add_data.get('google_drive_root_folder_name')]['media'].append({'path':_,'name':media['name']})
                                except Exception as e:
                                    time.sleep(1)
                                    continue
                        active_dict.update({'posts':posts})
                        if len(pth)>0:
                           
                            self.storage_sense.block={'address':'tasks.'+self.task.get('uuid'),'data':pth,'file_name':'downloads'}
                            self.storage_sense.load_deep_stuff()
                            self.storage_sense.add_values_to_file(load_block=False)
                            return self.start()
                                
                    else:
                        pths=[]
                        file_names=[]
                        data=self.storage_sense.data_frame.to_dict(orient='records')[0]
                        consumed_blocks=self.storage_sense.get_consumed_blocks(self.task.get('uuid'))
                        medias=data[add_data.get('google_drive_root_folder_name')]['media']
                        for media in medias:
                            if media['name'].split('.')[0] in consumed_blocks:
                                pass
                            else:
                                pths.append(media['path'])
                                file_names.append(media['name'])
                            if len(pths)>add_data.get('max_media',2):
                                break
                        caption=data[add_data.get('google_drive_root_folder_name')]['caption']
                        caption=random.choice(caption.split(';'))
                          
                        self.task['add_data'].update({
                                          'caption':caption
                                          })


                    
                else:
                    from base.downloader import Downloader
                    d=Downloader()
                    link='http://localhost'+self.task.get('media_link')
                    if '.png' or '.jpg' or '.jpeg' in link:
                        media_type='image'
                    elif '.mp4' in link:
                        media_type='video'
                    pth=d.download_media(media_type=media_type,link=link)
                    pth=[pth]
               
                self.push_files_to_posting_folder(pths)
                
                    
                self.stop_app()
                self.start_app()
                if self.make_post(**self.task):
                    for file_name in file_names:
                        self.storage_sense.add_output_block_to_consumed(self.task.get('uuid'),file_name)
                        print('File Names added to consumed input')
                                        
        if self.task.get('data_point')=='search_user_and_interact':
            if self.switch_account(**profile):
                print('Account Switched')
                """ try:
                    self.make_post()
                except Exception as e:
                    print(e)
                else:
                    pass
                self.stop_app()
                self.start_app() """
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                            'type':'account_switched', 'query':self.task.get('username'),'task':self.task['uuid'],
                                            'screenshot':pth
                                            })
                targets=self.task.get('targets')

                if targets:

                    if len(targets)<1:
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'no_targets_found', 'query':self.task.get('username'),'task':self.task['uuid']
                                                })
                    
                    for target in targets:
                        target=target['username'] 
                        if ',' in target:
                            target=target.replace(',','.')
                        try:
                            #self.exp
                            self.search_user_and_interact(target)
                        except Exception as e:
                            print(e)
                else:
                    self.explore_through_homepage(**self.task)
                            #self.start_app()
            else:
                print('Account switching failed')             
        if self.task.get('data_point')=='search_location_and_create_database_of_users':
            if self.switch_account(**profile):
                self.make_search()
        if self.task.get('data_point')=='explore_home_page':
            if self.switch_account(**profile):
                self.explore_through_homepage(**self.task)
        if self.task.get('data_point')=='explore_explore_page':
            if self.switch_account(**profile):
                self.explore_explore_page(**self.task)
        if self.task.get('data_point')=='send_dm':
            self.stop_app()
            self.start_app()
            time.sleep(2)
            for i in range(0,3):
                self.send_dm()
        if self.task.get('data_point')=='unfollow_users':
            if self.switch_account(**profile):
                self.unfollow_users()
            else:
                print('no')
                            
                
        if self.task.get('data_point')=='watch_story':
            from services.instagram.device.xpaths import Xpaths
            x=Xpaths()
            self.stop_app()
            self.start_app()
            time.sleep(2)
            self.locator.locate_by_xpath(x.HomePage().click_create_story_button(),click=True,retries=5)
            for i in range(0,self.task.get('add_data').get('max_swipes',20)):
                if self.locator.locate_by_xpath(x.StoryPage().like_story(),retries=5):
                    self.locator.locate_by_xpath(x.StoryPage().like_story(),click=True,retries=3)
                else:
                    if self.locator.locate_by_xpath(x.HomePage().click_profile_tab(),retries=3):
                        self.locator.locate_by_xpath(x.HomePage().click_create_story_button(),click=True,retries=5)
                self.device.swipe_ext(Direction.HORIZ_FORWARD,scale=1)
                
        if self.task.get('data_point')=='search_user_and_share_latest_post':
            if self.switch_account(**profile):
                print('Account Switched')
                """ try:
                    self.make_post()
                except Exception as e:
                    print(e)
                else:
                    pass
                self.stop_app()
                self.start_app() """
                imagebin=self.device.screenshot(format='raw')
                pth=self.storage_sense.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                            'type':'account_switched', 'query':self.task.get('username'),'task':self.task['uuid'],
                                            'screenshot':pth
                                            })
                targets=self.task.get('targets')

                if targets:

                    if len(targets)<1:
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'no_targets_found', 'query':self.task.get('username'),'task':self.task['uuid']
                                                })
                        
                    for target in targets:
                        target=target['username'] 
                        try:
                            #self.exp
                            self.search_user_and_share_latest_post(target,**self.task)
                        except Exception as e:
                            print(e)
                else:
                    self.explore_through_homepage()
                            #self.start_app()
            else:
                print('Account switching failed')
        
  
  
  
  
  
  
  #return
        #import names
        """ self.full_name=names.get_full_name()
        self.email_address=names.get_first_name()+'@datatrader.space'
        import uuid
        self.password=str(uuid.uuid1())
      
        from services.proxy.device.run_bot import SuperProxy
        #s=SuperProxy()
        #https://work3.zo8g.com:18222/jpg_proxy_reset?api_key=28d35f6d-cb95-4217-ac3f-22ec68a2daf7
        proxy={'username':'jk_proxy_user ',
                'password':'giaos89^!^',
                'port':'21719',
                'ip':'175.209.193.57',
                'proxy_protocol':'http'}
        
        #s.device=self.device
        #s.start()
        #self.start_app() """
        """         self.create_new_account()
        if self.task.get('proxy',{}):
            from services.proxy.device.run_bot import SuperProxy
            s=SuperProxy()
            s.proxy=self.task.get('proxy',{})
            s.device=self.device
            #s.start()
        if self.task.get('data_point')=='login':
            self.add_account(**profile) """