
from uiautomator2 import Direction
class Xpaths():

    class CreateAccount:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_none_of_the_above_accounts_screen_from_google(self,**kwargs):
            return [
                "//android.widget.Button[contains(@text,'NONE OF THE ABOVE')]"
            ]
        def click_create_new_account_button(self,**kwargs):
            return [
                "//android.view.View[contains(@text,'Create new account')]"
            ]
        def enter_full_name_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text, 'Full name') ]"

                ]
        def click_next_button(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text, 'Next') ]"

                ]
        def enter_full_name(self,**kwargs):
            return[  
                    "//android.view.View[contains(@content-desc, 'Full name') ]"

                ]
        def enter_password_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text, 'Create a password') ]"

                ]
        def enter_password(self,**kwargs):
            return[  
                    "//android.view.View[@text='Password']"

                ]
        def save_login_info_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text,'Save your login info')]"

                ]
        def click_save_login_info_button(self,**kwargs):
            return[  
                    "//android.view.View[@text='Save']"

                ]
        def click_not_now_button(self,**kwargs):
            return[  
                    "//android.view.View[@text='Not now']"

                ]
        def set_birthday_page(self,**kwargs):
            return[  
                    "//android.widget.TextView[@text='Set date']"

                ]
        def set_month(self,**kwargs):
            return[  
                    "//android.widget.EditText[@text='Feb']"

                ]
        def set_date(self,**kwargs):
            return[  
                    "//android.widget.EditText[@text='04']"

                ]
        def set_year(self,**kwargs):
            return[  
                    "//android.widget.EditText[@text='2023']"

                ]
        def click_set_button(self,**kwargs):
            return[  
                    "//android.widget.Button[@text='SET']"

                ]
        def create_username_page(self,**kwargs):
            return[  
                    "//android.view.View[@text='Create a username']"

                ]
        def choose_contact_method(self,**kwargs):
            return[  
                    "//android.view.View[@text='Sign up with email']"

                ]
        def whats_your_email_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text,'your email?')]"

                ]
        def enter_email_box(self,**kwargs):
            return[
                "//android.widget.EditText"
            ]
        def confirmation_code_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text,'enter the 6-digit code')]"

                ]
        def enter_confirmation_code_box(self,**kwargs):
            return[
                "//android.widget.EditText"
            ]
        def clear_confirmation_code_box(self,**kwargs):
            return[
                "//android.widget.Button[contains(@content-desc,'Clear Confirmation code text')]"
            ]
        def request_a_new_code(self,**kwargs):
            return[
                "//android.widget.Button[contains(@content-desc,'I didn’t get the code')]"
            ]
        def resend_confirmation_code(self,**kwargs):
            return[
                "//android.view.View[contains(@text,'Resend confirmation code')]"
            ]
        def agree_to_instagram_page(self,**kwargs):
            return[  
                    "//android.view.View[contains(@text,'Agree to Instagram')]"

                ]
        def click_i_agree_button(self,**kwargs):
            return[  
                    "//android.view.View[@text='I agree']"

                ]
      
    class AddSwitchAccount:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_add_account(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_user_textview'][contains(@text,'Add account')]"
            ]
        def click_login_to_existing_account(self,**kwargs):
            return [
               "//android.widget.Button[contains(@content-desc, 'Log ') ]"

            ]
        def click_none_of_the_above_accounts_screen_from_google(self,**kwargs):
            return [
                "//android.widget.Button[contains(@text,'NONE OF THE ABOVE')]"
            ]
        def click_switch_account(self,**kwargs):
            return [
               "//*[@resource-id='com.instagram.android:id/left_button'][contains(@text, 'Switch Accounts') ]"

            ]
        def get_logged_in_accounts(self,**kwargs):
            return [
               
               "//*[@resource-id='com.instagram.android:id/profile_header_barcelona_badge_text']"
               
               

            ]
           
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def get_username_input(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/login_username']"
                    ]
        def get_password_input(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/password']"
                    ]
        def get_login_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/next_button']"
                    ]
        def wrong_password(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/igds_headline_headline'][contains(@text, 'Forgotten password') ]"
                    ]
        def incorrect_username(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/igds_headline_headline'][contains(@text, 'Incorrect username') ]"
                    ]
        def username_not_found(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/igds_headline_headline'][contains(@text, 'Username Not Found') ]"
                    ]


    class ProfilePage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def click_account_switcher(self,**kwargs):
            return [
                    "//*[@resource-id='com.instagram.android:id/action_bar_title_chevron']"
                

            ]
        def accounts_list(self,**kwargs):
            return [
                "//*[@resource-id='android:id/list']"
                    ]
        def choose_account_from_list(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_user_textview'][contains(@text, '"+kwargs.get('text')+"')]"
            ]
        def has_unseen_story(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_profile_header_imageview'][contains(@content-desc,'unseen story')]"
            ]
        def get_username(self,**kwargs):
            
            return [
                  "//*[@resource-id='com.instagram.android:id/action_bar_large_title_auto_size']",
                  "//*[@resource-id='com.instagram.android:id/action_bar_title']"  
            ]
        def get_posts(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_post_count']"
            ]
        def get_followers(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_followers_count']"

            ]
        
        def get_following(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_following_count']"

            ]
        def get_count_of_followings(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_following_count']"

            ]
        def get_name(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_header_full_name']"

            ]
        def get_business_category(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_header_business_category']"

            ]
        def get_bio(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_header_bio_text']"

                
            ]
        def follow_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/profile_header_follow_button']"
            ]
        def get_highlights(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/highlights_reel_tray_recycler_view']/android.widget.LinearLayout"

            ]
        def get_first_post_of_user(self,**kwargs):
            return [
               "//android.widget.Button[contains(@content-desc, 'row 1') ]"

            ]
        def get_message_button(self,**kwargs):
            return [
               "//*[@resource-id='com.instagram.android:id/button_container'][contains(@text,'Message')]"

            ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def send_message_to_user_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/button_container'][contains(@content-desc, 'Message')]"
            ]
        def get_review_this_account_before_following_text(self,**kwargs):
            return [
                "//android.view.View[contains(@text,'Review this account before following')]"
            ]
        def click_follow_button_from_review_account(self,**kwargs):
            return [
                "//android.view.View[contains(@text,'Follow')]"
            ]
    
        def is_profile_page(self,retry=0,**kwargs):
            identifiers=[]
            identifiers.extend(self.get_username())
            identifiers.extend(self.follow_button())
            
            
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath):
                    return True
            if retry==1:
                return False
            else:
                
                return self.is_own_profile_page(retry=1) 
        def is_own_profile_page(self,retry=0,**kwargs):
            identifiers=[]
            identifiers.extend(self.click_account_switcher())            
          
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath):
                    elem=None
                    for xpath in self.get_username():
                        elem=self.locator.locate_by_xpath(xpath)
                        if elem:
                            pass
                    return elem
            if retry==1:
                return False
            else:
                self.device.swipe_ext(Direction.BACKWARD)
                return self.is_own_profile_page(retry=1) 
    class Challenges:
        def check_account_suspension_message(self,**kwargs):
            return[
                "//android.view.View[contains(@text, 'suspended your account')]"
            ]
        def click_meun_button_on_account_suspended_page(self,**kwargs):
            return[
                "//android.view.View[contains(@content-desc, 'Menu')]"
            ]
        def check_has_more_options_loaded_on_account_suspension_page(self,**kwargs):
            return[
                "//com.instagram.android:id/title_text_view[contains(@text, 'More options')]"
            ]
        def get_username_from_logout_text(self,**kwargs):
            return[
                "//android.view.View[contains(@text, 'Log out')]"
            ]
        def click_logout_button(self,**kwargs):
            return[
                "//android.view.View[contains(@text, 'Log out')]"
            ]
    class FollowingsPage:
        def click_sort_by_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/sorting_entry_row_icon']"
            ]  
        def click_following_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/follow_list_row_large_follow_button'][contains(@text, 'Following')]",
                "//*[@resource-id='com.instagram.android:id/follow_list_row_large_follow_button'][contains(@text, 'Message')]"

                
            ]
        def click_hashtag_creator_business_category(self):
            return [
                "//*[@resource-id='com.instagram.android:id/container'][contains(@content-desc, 'Hashtags, Creators and Businesses')]"

                
            ]
        def click_most_shown_in_feed(self):
            return [
                "//*[@resource-id='com.instagram.android:id/container'][contains(@content-desc, 'Most Shown in Feed')]"

                
            ]
        def click_least_interacted_with(self):
            return [
                "//*[@resource-id='com.instagram.android:id/container'][contains(@content-desc, 'Least Interacted With')]"

                
            ]
        def click_sort_by_date_followed_earliest(self):
            return [
                "//*[@resource-id='com.instagram.android:id/follow_list_sorting_option'][contains(@text, 'Date followed: Earliest')]"

                
            ]
        def click_sort_by_date_followed_latest(self):
            return [
                "//*[@resource-id='com.instagram.android:id/follow_list_sorting_option'][contains(@text, 'Date followed: Latest')]"

                
            ]
        def get_current_sorting_value(self):
            return [
                "//*[@resource-id='com.instagram.android:id/sorting_entry_row_option']"

                
            ]
        def click_more_options_icon(self):
            return ["//*[@resource-id='com.instagram.android:id/media_option_button']"]
        
        def click_unfollow_from_more_options(self):
            return ["//*[@resource-id='com.instagram.android:id/action_sheet_row_text_view'][contains(@text, 'Unfollow')]"]
        def click_unfollow_from_confirmation_dialog(self):
            return [
                "//*[@resource-id='com.instagram.android:id/primary_button'][contains(@text, 'Unfollow')]"

                
            ]
        def is_followings_page(self):
            identifiers=[]
            identifiers.extend(self.click_following_button())
            identifiers.extend(self.click_sort_by_button())
            
            count=0
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath):
                    return True
                    count+=1
            if count==len(identifiers):
                return True
            else: 
                return False 
    class Navigation:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def get_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def get_reels_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/clips_tab']"
            ]
        def get_profile_button(self,**kwargs):
           return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def click_profile_tab_button(self,**kwargs):
           return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
    class SearchResults:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def enter_search_query(self,**kwargs):
           return [
                "//*[@resource-id='com.instagram.android:id/action_bar_search_edit_text']"
                    ]
        def get_posts(self,**kwargs):
            return  ["//*[@resource-id='com.instagram.android:id/recycler_view']"
                    ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def get_search_text(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/action_bar_search_edit_text']"
                    ]
        def is_active_page(self):
            pass
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def get_for_you_section(self,**kwargs):
            return  ["//@android.widget.TabWidget[@text='For you']",
                     
                     
                     ]
        def get_accounts_section(self,**kwargs):
            return [ "//*[@text='Accounts']"
                    
                    ]
       
        def get_audio_section(self,**kwargs):
            return  ["//android.widget.TabWidget[@text='Audio']"
                    ]
        def get_tags_section(self,**kwargs):
            return  ["//android.widget.TabWidget[contains(@text, 'Tags')]"
                    ]
        def get_places_section(self,**kwargs):
            return  ["//android.widget.TabWidget[contains(@text, 'Places')]"
                    ]

        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def accounts_section_results__username(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_search_user_username']"
            ]
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def is_search_results_page(self):
            identifiers=[]
            identifiers.extend(self.get_accounts_section())
            identifiers.extend(self.get_for_you_section())
            
            count=0
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath,retries=2):
                    
                    count+=1
            if count==len(identifiers):
                return True
            else: 
                return False 
    class Search:
        def __init__(self):
            from services.instagram.device.locator import Locator
            self.locator=Locator()
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def enter_search_query(self,**kwargs):
           return [
                "//*[@resource-id='com.instagram.android:id/action_bar_search_edit_text']"
                    ]    
        def get_posts(self,**kwargs):
            return  ["//*[@resource-id='com.instagram.android:id/recycler_view']"
                    ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def get_search_text(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/action_bar_search_edit_text']"
                    ]
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def click_first_post(self,**kwargs):
            return [
                 "//android.widget.Button[contains(@content-desc, 'Reel')]"
                    ]
        def click_load_more_button(self,**kwargs):
            return [
                 "//*[@resource-id='com.instagram.android:id/row_load_more_button']"
                    ]
       
        def is_explore_page(self,retry=0):
            identifiers=[]
            identifiers.extend(self.get_posts())
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath=xpath):
                    return True

    class RecentSearches:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def recent_searches(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_search_keyword_title']"
            ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
         
    class Posts:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def get_explore_title(self,**kwargs):
            return[
                 "//*[@resource-id='com.instagram.android:id/action_bar_title'][contains(@text, 'Explore')]"  

            ]
        def get_search_title(self,**kwargs):
            return[
                 "//*[@resource-id='com.instagram.android:id/action_bar_title']"  

            ]
        def get_username(self,**kwargs):
            return [
                  "//*[@resource-id='com.instagram.android:id/row_feed_photo_profile_name']"  
            ]
        def get_likes(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_textview_likes']",
                "//android.widget.TextView[contains(@content-desc,'Like number')]"
            ]
        def get_comments(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_followers_count']",
                 "//android.widget.TextView[contains(@content-desc,'Comment number')]"

            ]
        
        def get_caption(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_comment_textview_layout']",
                "//*[@resource-id='com.instagram.android:id/caption_input_text_view']"
                

            ]
        def get_like_button(self,**kwargs):
            return [
                #"//*[@resource-id='com.instagram.android:id/row_feed_button_like']",
                "//*[@resource-id='com.instagram.android:id/like_button']",
                "//*[@resource-id='com.instagram.android:id/row_feed_button_like']"

            ]
        def get_comment_button(self,**kwargs):
            return [
                #"//*[@resource-id='com.instagram.android:id/row_feed_button_comment']",
                "//android.widget.ImageView[contains(@content-desc,'Comment')]"

            ]
        def get_share_post_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_button_share']"

                
            ]
        def click_your_story_button(self,**kwargs):
            return [
                "//android.widget.TextView[contains(@text,'Your story')]"
            ]
        def check_story_loading_status(self,**kwargs):
            return [
                "//android.widget.TextView[contains(@text,'loading')]"
            ]
        def click_discard_photo(self,**kwargs):
            return [
                "//android.widget.Button[contains(@text,'Discard')]"
            ]

        def get_bookmark_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_feed_view_group_buttons']"
            ]
        def get_time(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/highlights_reel_tray_recycler_view']"

            ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def is_posts_page(self,retry=1,**kwargs):
            identifiers=[]
            identifiers.extend(self.get_share_post_button())
            
          
            x=Xpaths()
            if self.locator.locate_by_xpath(x.HomePage().click_home_button()):

                for xpath in identifiers:
                    if self.locator.locate_by_xpath(xpath):
                        return True
                if retry==1:
                    return False
                else:

                    self.device.swipe_ext(Direction.BACKWARD)
                    return self.is_posts_page(retry=1)
            else:
                return False
    class SharePostPage:
        def __init__(self):
            from services.instagram.device.locator import Locator
            self.locator=Locator()

        def get_link_tracking_text(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/link_tracking_disclosure_text_view']"
            ]


        def click_search_users(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/search_edit_text']"
            ]
        def enter_search_text(self,**kwargs):
            return[
            "//android.widget.TextView[contains(@text,'Search')]"
            ]
        def click_add_note_button(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/label'][contains(@text,'Add note')]"
            ]
        def click_whatsapp_button(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/label'][contains(@text,'WhatsApp')]"
            ]
        def click_share_button(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/label'][contains(@text,'Share')]"
            ]
        def click_copy_link_button(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/label'][contains(@text,'Copy link')]"
            ]
        def click_messenger_button(self,**kwargs):
            return[
            "//*[@resource-id='com.instagram.android:id/label'][contains(@text,'Messenger')]"
            ]
    class HomePage:
        def __init__(self):
            from services.instagram.device.locator import Locator
            self.locator=Locator()
        
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def click_home_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/feed_tab']"
            ]
        def get_instagram_logo(self,**kwargs):
            return[
                 "//*[@resource-id='com.instagram.android:id/title_logo']"  

            ]
        def click_notifications_button(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/news_tab'][contains(@text, 'Activity')]" 

            ]
        def has_new_notifications(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/led_badge']" 

            ]
        def click_inbox_button(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/action_bar_inbox_button']" 

            ]
        def has_new_messages(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/action_bar_inbox_button'][contains(@text, 'unread')]" 

            ]
        def click_create_story_button(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/avatar_image_view']" 

            ]
        def click_create_story_button(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/avatar_image_view'][@index=1]" 

            ]
     
        def get_username(self,**kwargs):
            return [
                  "//*[@resource-id='com.instagram.android:id/row_feed_photo_profile_name']"  
            ]
        def get_likes(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_textview_likes']"
            ]
        def get_comments(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_profile_header_textview_followers_count']"

            ]
        
        def get_caption(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_comment_textview_layout']"

            ]
        def get_like_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_button_like']"

            ]
        def get_comment_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_button_comment']"

            ]
        def get_share_post_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_feed_button_share']"

                
            ]
        def get_bookmark_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_feed_view_group_buttons']"
            ]
        def get_time(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/highlights_reel_tray_recycler_view']"

            ]
        def get_search_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_tab']"
            ]
        def click_profile_tab(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/profile_tab']"
                    ]
        def is_home_page(self,retry=0,**kwargs):
            identifiers=[]
            identifiers.extend(self.click_notifications_button())
            identifiers.extend(self.click_inbox_button())
            identifiers.extend(self.get_instagram_logo())
            
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath):
                    return True
            if retry==1:
                return False
            else:

                return False
    class Comments:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def get_username(self,**kwargs):
            return [
                  "//android.widget.Button"  
            ]
        def get_likes(self,**kwargs):
            return [
                "com.instagram.android:id/row_comment_textview_like_count"
            ]
        def get_owner(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_comment_imageview']"

            ]
        
        def get_text(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_comment_textview_comment']"

            ]
        def get_reply_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_comment_textview_reply_button']"

            ]
        def get_write_comment_box(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/layout_comment_thread_edittext']"

            ]
        def get_post_comment_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/layout_comment_thread_post_button_click_area']"

                
            ]
      
        def get_time(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_comment_textview_time_ago']"

            ]
        def is_comments_page(self,retry=0,**kwargs):
            identifiers=[]
            identifiers.extend(self.get_write_comment_box())
            
          
            
            for xpath in identifiers:
                if self.locator.locate_by_xpath(xpath):
                    return True
            if retry==1:
                return False
            else:

                
                return self.is_comments_page(retry=1)
    class NewPostPage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
        def get_new_post_title(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/new_post_title']"

            ]
        def click_post_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/cam_dest_feed'][contains(@text,'POST')]"

            ]
        def open_gallery(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/gallery_folder_menu_tv']"

            ]
        def click_see_all_albums_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/button_see_all']"

            ]
        def get_albums_list_on_screen(self,**kwargs):
            return [
                    "//*[@resource-id='com.instagram.android:id/media_picker_grid_view']"

                ]
        def open_recents_album(self,**kwargs):
            return [
                "//android.widget.TextView[contains(@text,'Recents')]"

            ]
       
        def open_darrxscale_album(self,**kwargs):
            return [
                "//android.widget.TextView[contains(@text,'darrxscale')]"

            ]
        def click_select_mulitple_phots_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/multi_select_slide_button_alt']"

            ]
        def get_iterable_media_grid_of_album_photos(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/media_picker_grid_view']//android.view.ViewGroup"

            ]
        def click_next_button_from_media_picker(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/next_button_textview']",
                
                

            ]
        def click_next_button_from_filter_picker(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/next_button_textview']",
                "//*[@resource-id='com.instagram.android:id/creation_next_button']"

            ]
        def focus_on_caption_area(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/caption_text_view']"

            ]
        def click_on_add_location_option(self,**kwargs):
             return [
                "//*[@resource-id='com.instagram.android:id/location_label']"

            ]
        def focus_on_location_input(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_search_edit_text']"

            ]
        def choose_first_suggestion(self,**kwargs):
             return [
                "//*[@resource-id='com.instagram.android:id/row_venue_title']"

            ]
        def click_add_music_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/music_row_title']"

            ]
        def focus_on_search_music_input(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/row_search_edit_text']"

            ]
        def choose_first_music_suggestion(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/track_container']"

            ]
        def finish_music_addition(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/action_bar_button_action']"

            ]
        def share_to_facebook(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/share_switch']"

            ]
        def accept_search_settings(self,**kwargs):
          
            return [
                "//*[@resource-id='com.instagram.android:id/bb_primary_action'][contains(@text,'Share')]"

            ]
        def share_post_final(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/next_button_textview']",
                 "//*[@resource-id='com.instagram.android:id/share_footer_button']"

                

            ]
        def click_start_over_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/primary_button'][contains(@text,'Start over')]"

            ]

    class Share:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_add_to_story(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/button']/android.widget.TextView[contains(@text, 'Add to story')]",
            ]
        def click_add_to_your_story(self,**kwargs):
            return [
               "//android.widget.FrameLayout[contains(@description, 'Share to your story')]",
            ]
        def click_share_to(self,**kwargs):
            return [
               "//android.widget.FrameLayout[contains(@description, 'Share to')]",
            ]
        def click_message_option(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/message_row_container']",
            ]
        def focus_on_search_user_input(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/search_edit_text']",
            ]

    class Messenger:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_create_new_message_button(self,**kwargs):
             return[  
                    "//android.widget.Button[contains(@content-desc, 'New Message')]"
                ]
        def click_primary_message_button(self,**kwargs):
            return[  
                    "//android.widget.TextView[contains(@text, 'Primary')]"
                ]
        def new_message_title(self,**kwargs):
            return [           
                "//android.widget.TextView[contains(@text,'New message')]"      
                    ]
        def create_group_chat(self,**kwargs):
            return [
            
                "//*[@resource-id='com.instagram.android:id/direct_ff_group_chat_entry_point']"      
                ]
        def search_recipient(self,**kwargs):
            return [
            
                "//*[@resource-id='com.instagram.android:id/search_edit_text']"      
                ]

        def search_results__username(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_user_primary_name']"
            ]
        def enter_message(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_thread_composer_edittext']"
            ]
        def send_dm(self,**kwargs):
            return [
            
                "//android.widget.Button[contains(@text,'Send')]" , "//*[@resource-id='com.instagram.android:id/row_thread_composer_send_button_background']"     
                ]
        def click_media_selector(self,**kwargs):
             return [           
                "//*[@resource-id='com.instagram.android:id/row_thread_composer_button_gallery']",   
                    ]
        def get_messages_requests_are_changing_text(self,**kwargs):
            return [           
                "//android.widget.TextView[contains(@text,'Message requests are changing')]",   
                    ]
        def click_ok_button_on_message_request_change_box(self,**kwargs):
            return [           
                "//android.widget.TextView[contains(@text,'OK')]"
            ]
        def check_cant_message_text(self,**kwargs):
            return [           
                "//android.widget.TextView[contains(@text,'message this account unless they follow you.')]"
            ]
        def identifiers(self,**kwargs):
            return [{'sub_page':'inbox','identifiers':[self.click_create_new_message_button(),self.click_primary_message_button()]}
            ]
    class StoryPage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def like_story(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/toolbar_like_button']",
            ]
    class Reels:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def get_reels_title(self):
            pass
        def is_reels_page(self):
            return [
                "//*[@resource-id='com.instagram.android:id/root_clips_layout']",
                "//*[@resource-id='com.instagram.android:id/root_clips_layout']",
                
                    ]
        def clips_video_container(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/clips_video_container']",
            ]

        def get_username(self,**kwargs):
           return [
               "//*[@resource-id='android.widget.ImageView'][contains(@description, 'Profile picture')]",

           ]
        
        def get_follow_button(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/inline_follow_button']"

            ]
        def get_like_button(self,**kwargs):
            return [
                 "//*[@resource-id='com.instagram.android:id/like_button']"
            ]
        
        def get_comment_button(self,**kwargs):
            return [
                "//*[@resource-id='android.view.ViewGroup'][contains(@description, 'Comment')]"
            ]
        
        def get_share_button(self,**kwargs):
            return [
                    "//*[@resource-id='android.view.ViewGroup'][contains(@description, 'Share')]"

            ]
        def get_likes_count(self,**kwargs):
            return [
                    "//*[@resource-id='android.view.ViewGroup'][contains(@description, 'View likes')]"

            ]
        def get_comments_count(self,**kwargs):
            return [
                    "//*[@resource-id='android.view.ViewGroup'][contains(@description, 'View comments')]"

            ]
        
        def get_reshare_count(self,**kwargs):
            return [
                    "//*[@resource-id='android.view.ViewGroup'][contains(@description, 'Reshare number')]"

            ]
    


            
       

