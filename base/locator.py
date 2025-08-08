from services.instagram.xpaths import Xpaths
from services.instagram.run_bot import Crawler
import time
class Locator(Crawler):
    def __init__(self):
        super().__init__()
        self.driver=None
        self.xpath=None
        self.sub_page=''
        self.existing_content=[]
    def load_new_content_on_page(self,content_identifiers,method,retries=0,max_tries=5,sleep_time=0.1):
        if retries>max_tries:
            return False
        
       
        elems=self.locate(**content_identifiers)
        if elems:
            if not self.existing_content:
                self.existing_content=elems
            else:
                for elem in elems:
                    if not elem in self.existing_content:
                        self.existing_content.extend(elems)
                      
                        return True
        self.browser.scroll(kind='scrollHeight')
        
        retries+=1
        time.sleep(sleep_time)
        return self.load_new_content_on_page(content_identifiers=content_identifiers,method=method,retries=retries,max_tries=max_tries,sleep_time=sleep_time)
    def identify_current_page(self,retries=0,max_tries=3,refresh=False):
        if 'search' in self.browser.driver.current_url:
            self.page='search_page'
            return 
        x=Xpaths()
        tph=self.locate_by_xpath(xpath=x.LocationPosts().top_posts_heading(),retries=5)
        in_the_area=self.locate_by_xpath(xpath=x.LocationPosts().in_the_area_heading(),retries=5)
        if tph or in_the_area:
            self.page='location_posts_page'
            return
        if retries>=max_tries:
            return 
        self.page=None
        self.xpath=None
        count=0
        self.xpath=None
        
        home_page_touch_points=['click_notifications_button','click_inbox_button']   
        x=Xpaths()
    
        for tp in home_page_touch_points:
            elem=self.locato(**{'touch_point':tp,'page':'home_page'})
            if elem:
                count+=1
            else:
                pass
        if count>0:
            print('Current Page is Home Page')                    
            self.page='home_page'
            return
        else:
            self.xpath=None
        login_page_touch_points=['get_username_input','get_password_input']                
        for tp in login_page_touch_points:
            elem=self.locato(**{'touch_point':tp,'page':'login_page'})
            if elem:
                count+=1
            else:
                pass
        if count>0:
            print('Current Page is Login Page')                    
            self.page='login_page'
            return
        else:
            self.xpath=None
            self.page=None
            location_posts_page_touch_points=['most_recent_heading','top_posts_heading','in_the_area_heading']
            for tp in location_posts_page_touch_points:
                elem=self.locato(**{'touch_point':tp,'page':'location_posts_page'})
                if elem:
                    self.page='location_posts_page'
                    print('Current page is Locations Posts Page')
                    return
            self.xpath=None
            profile_page_touch_points=['get_followers','get_following','get_posts']
            for tp in profile_page_touch_points:
                elem=self.locato(**{'touch_point':tp,'page':'profile_page'})
                if elem:
                    count+=1
            if count>=2:
                print('Current page is Profile page')
                self.page='profile_page'
                return
            print('unknown page')
            if refresh:
                self.browser.driver.refresh()
            retries+=1
            return self.identify_current_page(retries=retries,max_tries=max_tries)
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
                
                    
                        
    



    def locate_by_xpath(self,xpath,elements=False,attr=False,click=False,retries=1):
        if type(xpath)==list:
            xpaths=xpath
        else:
            xpaths=[xpath]              
        for xpath in xpaths:
            if '//' in xpath:
                xpath=xpath
                css_selector=None
            else:
                print('CSS selector')
                css_selector=xpath
                xpath=None
            
            resp=self.browser.find_element(xpath=xpath,wait_time=0.1,elements=elements,max_retries=retries,css_selector=css_selector)
            if resp:
                try:
                    if click:
                        resp.click()
                except Exception as e:
                    return False
                if attr:
                 results=[]
                 for res in resp:
                     results.append(res.get_attribute(attr))
                 return results
               
       
        return False