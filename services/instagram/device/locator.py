from services.instagram.device.xpaths import Xpaths
from uiautomator2 import Direction
from base.device import Device
class Locator():
    def __init__(self):
        self.device=Device()
        self.xpath=None
        self.sub_page=''
    def identify_current_page1(self):
        from services.instagram.device.xpaths import Xpaths
        m=Xpaths.Messenger()
        identifiers=m.get_required_xpath(**{'touch_point':'identifiers'})
        count=0
        for page in identifiers:
            for _xpath in page['identifiers']:
                for __xpath in _xpath:
                    print(__xpath)
                    if self.device.xpath(__xpath).exists:
                        _=self.device.xpath(__xpath).all()
                        count+=1
                        break                 
            if count==len(page['identifiers']):
                print('Curent sub-page is '+page['sub_page'])
                print('Current page is Messenger')
    def identify_current_page(self):
        
        self.page=None
        self.xpath=None
        count=0
        
        #self.device.swipe_ext(Direction.BACKWARD)
        inbox_page_touch_points=['click_create_new_message_button','click_primary_message_button']                
        for tp in inbox_page_touch_points:

            elem, info=self.locato(**{'touch_point':tp,'page':'messenger_page'})
            if elem:
                count+=1
            else:
                pass
        if count==2:
            print('Current Page is Inbox Page')                    
            self.page='messenger_page'
            self.sub_page='inbox_page'
            return
        search_recipient_page_touch_points=['new_message_title','search_recipient','create_group_chat']    
        count=0            
        for tp in search_recipient_page_touch_points:

            elem, info=self.locato(**{'touch_point':tp,'page':'messenger_page'})
            if elem:
                count+=1
            else:
                pass
        if count==3:
            print('Current Page is Search Recipients Page')                    
            self.page='messenger_page'
            self.sub_page='search_recipient_page'
            return
        compose_message_page=['click_media_selector','enter_message']     
        count=0           
        for tp in compose_message_page:

            elem, info=self.locato(**{'touch_point':tp,'page':'messenger_page'})
            if elem:
                return True
            else:
                pass
        if count==2:
            print('Current Page is Compose Message Page')                    
            self.page='messenger_page'
            self.sub_page='compose_message_page'
            return
        self.xpath=None
        self.page=None
        home_page_touch_points=['click_notifications_button','click_inbox_button'] 
        count=0               
        for tp in home_page_touch_points:

            elem, info=self.locato(**{'touch_point':tp,'page':'home_page'})
            if elem:
                count+=1
            else:
                pass
        if count>0:
            print('Current Page is Home Page')                    
            self.page='home_page'
            return
   
        self.xpath=None          
        elem, info=self.locato(**{'touch_point':'click_create_new_account_button','page':'create_new_account'})
        if elem:
            self.page='create_new_account'
            self.sub_page='login_page'
            return
        else:
            elem, info=self.locato(**{'touch_point':'click_none_of_the_above_accounts_screen_from_google','page':'create_new_account'})
            if elem:
                self.page='create_new_account'
                self.sub_page='login_page'
            
                return
            else:
                elem, info=self.locato(**{'touch_point':'enter_full_name_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='enter_full_name_page'              
                    return
                elem, info=self.locato(**{'touch_point':'enter_password_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='enter_password_page'              
                    return
                elem, info=self.locato(**{'touch_point':'save_login_info_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='save_login_info_page'              
                    return
                elem, info=self.locato(**{'touch_point':'set_birthday_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='set_birthday_page'              
                    return
                elem, info=self.locato(**{'touch_point':'create_username_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='create_username_page'              
                    return
                elem, info=self.locato(**{'touch_point':'choose_contact_method','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='choose_contact_method_page'              
                    return
                elem, info=self.locato(**{'touch_point':'whats_your_email_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='whats_your_email_page'              
                    return
                elem, info=self.locato(**{'touch_point':'confirmation_code_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='enter_confirmation_code_page'              
                    return
                elem, info=self.locato(**{'touch_point':'agree_to_instagram_page','page':'create_new_account'})
                if elem:
                    self.page='create_new_account'
                    self.sub_page='agree_to_instagram_page'              
                    return
        
        self.xpath=None
        
        elem, info=self.locato(**{'touch_point':'click_add_account','page':'add_switch_account_page'})
        if elem:
            self.page='add_switch_account_page'
            self.sub_page='add_account_menu'
            return
        else:
            elem, info=self.locato(**{'touch_point':'click_login_to_existing_account','page':'add_switch_account_page'})
            if elem:
                self.page='add_switch_account_page'
                self.sub_page='login_to_existing_account'
                return
            else:
                elem, info=self.locato(**{'touch_point':'click_switch_account','page':'add_switch_account_page'})
                if elem:
                    self.page='add_switch_account_page'
                    self.sub_page='switch_account'
                    return
                else:
                    elem, info=self.locato(**{'touch_point':'get_username_input','page':'add_switch_account_page'})
                    if elem:
                        self.page='add_switch_account_page'
                        self.sub_page='login'
                        return
                    else:
                        elem, info=self.locato(**{'touch_point':'get_password_input','page':'add_switch_account_page'})
                        if elem:
                            self.page='add_switch_account_page'
                            self.sub_page='login'
                            return
                        else:
                            elem, info=self.locato(**{'touch_point':'wrong_password','page':'add_switch_account_page'})
                            if elem:
                                self.page='add_switch_account_page'
                                self.sub_page='wrong_password'
                                return
                            else:
                                elem, info=self.locato(**{'touch_point':'incorrect_username','page':'add_switch_account_page'})
                                if elem:
                                    self.page='add_switch_account_page'
                                    self.sub_page='incorrect_username'
                                    return
                                else:
                                    elem, info=self.locato(**{'touch_point':'username_not_found','page':'add_switch_account_page'})
                                    if elem:
                                        self.page='add_switch_account_page'
                                        self.sub_page='incorrect_username'
                                        return
        
        self.xpath=None
        profile_page_touch_points=['get_followers','get_following','get_message_button','get_posts']
        for tp in profile_page_touch_points:
            elem, info=self.locato(**{'touch_point':tp,'page':'profile_page'})
            if elem:
                count+=1
        if count>=2:
            print('Current Page is Profile Page')
            self.page='profile_page'
            return
        else:
            self.xpath=None
            search_page_touch_points=['get_for_you_section','get_accounts_section','get_audio_section','get_tags_section','get_places_section']
            for tp in search_page_touch_points:
               
                elem, info=self.locato(**{'touch_point':tp,'page':'search_results_page'})
                if elem:
                    count+=1
            if count>=2:
                print('Current Page is Search Results Page')
                self.page='search_results_page'
                return
            else:
                #check whether its the Explore Page 
                search_page_touch_points=['get_posts','get_search_text']
                elem,info=self.locato(**{'touch_point':'get_posts','page':'explore_page'})
                if elem:
                    
                    elem,info=self.locato(**{'touch_point':'get_search_text','page':'explore_page'})
                    if elem and info and info.get('text')=='Search':
                        print('Current Page is Explore Page')
                        self.page='explore_page'
                        return
           
                
                self.xpath=None
                post_page_touch_points=['get_username','get_likes','get_caption','get_bookmark_button']
                for tp in post_page_touch_points:
                    elem, info=self.locato(**{'touch_point':tp,'page':'posts_page'})
                    if elem:
                        count+=1
                    else:
                        pass
                if count>=2:
                    print('Current Page is Post Page')                    
                    self.page='posts_page'
                    return
                else:
                    self.xpath=None
                    new_post_page_touch_points=[]
                    
                    
                    elem, info=self.locato(**{'touch_point':'click_see_all_albums_button','page':'new_post_page'})
                    if elem:
                        self.page='new_post_page'
                        self.sub_page='select_album_list'
                        return
                    
                    elem, info=self.locato(**{'touch_point':'click_select_mulitple_phots_button','page':'new_post_page'})
                    if elem:
                        self.page='new_post_page'
                        self.sub_page='select_media'
                        return
                    elem, info=self.locato(**{'touch_point':'click_next_button_from_filter_picker','page':'new_post_page'})
                    if elem:
                        self.page='new_post_page'
                        
                        return
                    for tp in ['choose_first_music_suggestion','focus_on_search_music_input','click_add_music_button','finish_music_addition']:
                        elem, info=self.locato(**{'touch_point':tp,'page':'new_post_page'})
                        if elem:
                            self.page='new_post_page'
                        
                            return
                    self.xpath=None
                    elem, info=self.locato(**{'touch_point':'recent_searches','page':'recent_searches_page'})
                    if elem:
                        self.page='recent_searches_page'
                        return

          
                
                    
                        
    def create_selector(self,xpath):
        if xpath.get('c'):
            
            self.device(className=xpath.get('c'))


    def get_xpath_object(self,**kwargs):
        if not self.page:
            page=kwargs.get('page')
        else:
            if kwargs.get('page'):
                page=kwargs.get('page')
            else:
                page=self.page
        if page =='create_new_account':
           _xpath=Xpaths.CreateAccount()
        elif page=='profile_page':
            _xpath=Xpaths.ProfilePage()
        elif page=='explore_page':
            _xpath=Xpaths.Search()
        elif page =='posts_page':
            _xpath=Xpaths.Posts()
        elif page =='search_results_page':
            _xpath=Xpaths.SearchResults()
        elif page=='home_page':
            _xpath=Xpaths.HomePage()
        elif page=='new_post_page':
            _xpath=Xpaths.NewPostPage()
        elif page=='recent_searches_page':
            _xpath=Xpaths.RecentSearches()
        elif page=='add_switch_account_page':
            _xpath=Xpaths.AddSwitchAccount()
        elif page=='messenger_page':
            _xpath=Xpaths.Messenger()
        elif page =='story_page':
            _xpath=Xpaths.StoryPage()
        else:
            return False
        self.xpath=_xpath
        return True
    def locate_by_xpath(self,xpath,elements=False,click=False,retries=1):
        if type(xpath)==list:
            xpaths=xpath
        else:
            xpaths=[xpath]
        while retries>0:
            for xpath in xpaths:
                if self.device.xpath(xpath).exists:
                        _=self.device.xpath(xpath).all()
                        
                        if _:
                            if elements:
                                return _
                            else:
                                if click:
                                    _[0].click()
                                    xpath='com.instagram.android:id/igds_promo_dialog_action_button'
                                    if self.device.xpath(xpath).exists:
                                        print('clikced prompo')
                                        self.device.xpath(xpath).all()[0].click()
                                    return True
                                else:
                                    return _[0]
                retries-=1
                import time
                time.sleep(0.3)
        
        return False
    def locato(self,**kwargs):
 
        if not self.xpath:
            self.get_xpath_object(**kwargs)

        
        xpaths=self.xpath.get_required_xpath(**kwargs)
        for xpath in xpaths:
        
            _=None
            if self.device.xpath(xpath).exists:
                _=self.device.xpath(xpath).all()
                
                if _:
                    if kwargs.get('elements',False):
                        return _,None
                    else:
                        return _[0],_[0].info
        
        return _,_
       
        return None, None
    def locate(self,**kwargs):
        self.xpath=None
        if kwargs.get('track'):

            self.identify_current_page()
            if not self.page:
                imagebin=self.device.screenshot(format='raw')
                self.storage_sense.save_screenshot(imagebin)
                raise Exception('Unknow page')
        else:
            pass
            
        if self.get_xpath_object():
            imagebin=self.device.screenshot(format='raw')
            #self.storage_sense.save_screenshot(imagebin)
            return self.locato(**kwargs)
        else:
            imagebin=self.device.screenshot(format='raw')
            #self.storage_sense.save_screenshot(imagebin)
            return None, None
                    
