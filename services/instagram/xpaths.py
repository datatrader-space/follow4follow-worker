class Xpaths():
    class LoginPage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def get_username_input(self,**kwargs):
            return ['//input[@aria-label= "Phone number, username, or email"]','//label[text()="Mobile number, username or email"]']
        def get_password_input(self,**kwargs):
            return ['//input[@aria-label="Password"]']
        def click_login_button(self,**kwargs):
            return ['//button[@type="submit"]']
        def incorrect_password_text(self,**kwargs):
            return ['//div[contains(text(),"your password was incorrect")]']
        def get_security_code_input_field(self, **kwargs):
            return [
                "//input[@aria-label='Security Code']"
            ]
        def get_confirm_button(self, **kwargs):
      
            return [
                
                "//button[normalize-space()='Confirm']",
                # "//button[@type='button' and normalize-space()='Confirm']"
            ]
        def get_instagram_login_error(self, **kwargs):

            return '//div[contains(text(), "connected to the internet and try again.")]'
        def get_allow_all_cookies_banner(self,**kwargs):
            return["//*[contains(text(),'all cookies')]"]
    class ProfilePage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def get_username(self,**kwargs):
            return [
                  "//*/div/div/div[2]/div/div/div[1]/div[2]/div[1]/section/main/div/header/section/div[1]/div[1]/h2"
            ]
        def get_posts(self,**kwargs):
            return [
                "//div[contains(text(),'posts')]/span/span|//span[contains(text(),'posts')]"
            ]
        def get_followers(self,**kwargs):
            return [
                "//a[contains(text(),'followers')]/span/span|//span[contains(text(),'followers')]"
            ]
        
        def get_following(self,**kwargs):
            return [
                "//a[contains(text(),'following')]/span/span|//span[contains(text(),'following')]"
            ]
        def get_name(self,**kwargs):
            return [
                "//section/main/div/header/section/div[4]/div/span"

            ]
        def get_business_category(self,**kwargs):
            return [
                "//section/main/div/header/section/div[4]/div[3]/div"

            ]
        def get_bio(self,**kwargs):
            return [
                "//section/main/div/header/section/div[4]/h1"

                
            ]
        def get_external_links(self,**kwargs):
            return [
                "//section/main/div/header/section/div[4]/button/div"
            ]
        def follow_button(self,**kwargs):
            return[
                "//section/main/div/header/section/div[1]/div//button//*[text()='Follow']|//section/main/div/header/section/div[1]/div//button//*[text()='Following']"
            ]
        def get_message_button(self,**kwargs):
            return [
               "//section/main/div/header/section/div[1]/div//*[text()='Message']"

            ]
        def get_suggested_users(self,**kwargs):
            return [
                "//section/main/div/header/section/div[1]/div[2]/div/div[3]"
            ]
        def get_highlights(self,**kwargs):
            return [
                "//section/main/div/header/following-sibling::div/div/div//ul/li"

            ]
        def get_posts_of_user(self,**kwargs):
            return [
               "//section/main/div/header/following-sibling::div[3]/article/div/div/div/div"

            ]
        
    
    class ChallengePage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def automated_behavior_warning_page(self,**kwargs):
            return ['//*[contains(text(),"automated behavior")]']
        def click_dismiss_button(self,**kwargs):
            return['//*[text()="Dismiss"]']
        

    class Navigation:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def click_search_button(self,**kwargs):
            return  [            
                "svg[aria-label='Search']",
                "svg[aria-label='Search & Explore']",               
                "//span[text()='Search']"
                ]
        def click_home_button(self,**kwargs):
            return  [            
                "svg[aria-label='Home']"
                ]
        def click_new_post_button(self,**kwargs):
            return[
               "svg[aria-label='New post']"
            ]
        def click_explore_button(self,**kwargs):
            return  [            
                "svg[aria-label='Home']"
                ]
        def click_reels_button(self,**kwargs):
            return  [            
                '//a[@href="/reels/"]'
                ]
        def click_messenger_button(self,**kwargs):
            return [
                "//a[@href='/direct/inbox/']"
            ]
        def click_notifications_button(self,**kwargs):
            return [
                "svg[aria-label='Notifications']"
            ]
        def click_profile_button(self,**kwargs):
           return [
                "svg[aria-label='Notifications']"
                    ]
        def click_settings_button(self,**kwargs):
            return [
                "svg[aria-label='Settings']"
                    ]
        def check_has_new_messages(self,**kwargs):
            return[
                "//a[contains(@aria-label,'notification')]"
            ]
    class Messenger:
        def iterate_through_chats(self,**kwargs):
            return [
                "//div[@aria-label='Chats']/div/div/div/div[2]/div/div"
                ]
        def is_chat_unread(self,**kwargs):
            return [
                "//div[@role='listitem']/div/div[3]//span"]
        def focus_on_chat_area(self,**kwargs):
            return [
                "//div[contains(@aria-label,'Conversation')]"
            ]
        def get_username_of_recipient(self,**kwargs):
            return [
                "//a/div/div/div/div/div/div/span"
            ]
        def click_conversation_details_button(self,**kwargs):
            return [
                'svg[aria-label="Conversation information"]'
                ]
        def get_new_requests(self,**kwargs):
            return [
                "//span[contains(text(),'Request')]"
            ]
        def focus_on_message_text_area(self,**kwargs):
            return [
                "//div[contains(@aria-placeholder,'Message')]"
            ]
        def click_send_button(self,**kwargs):
            return [
                "//div[text()='Send']"
            ]
        def click_compose_new_message_button(self,**kwargs):
            return [
                'svg[aria-label="New message"]'
                ]
        def focus_on_messenger_recipient_search_text_box(self,**kwargs):
            return [
                "//input[@placeholder='Search...']"
            ]
        def iterate_over_search_results(self,**kwargs):
            return [
                '//div[@role="dialog"]//span[@style="----base-line-clamp-line-height: 18px; --lineHeight: 18px;"]/span'
            ]
        def click_chat_button(self,**kwargs):
            return [
                "//div[text()='Chat']"
            ]
    class LocationPosts:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def most_recent_heading(self,**kwargs):
            return [
                '//*[text()="Most recent"]',
                '//span[text()="Recent"]'
                ]
        def top_posts_heading(self,**kwargs):
            return [
                '//*[text()="Top posts"]'
                ]
        def in_the_area_heading(self,**kwargs):
            return [
                '//span[text()="In the area"]'
            ]
        
        def get_posts(self,**kwargs):
            return  [
                "//a[contains(@href,'/p')]"
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
            return [
                'svg[aria-label="Home"]'
                ]
        def click_search_button(self,**kwargs):
            return [
                'svg[aria-label="Home"]'
                ]
        def click_explore_button(self,**kwargs):
            return [
                'svg[aria-label="Explore"]'
                ]
        def click_reels_button(self,**kwargs):
            return [
                'svg[aria-label="Reels"]'
                ]
        def click_messenger_button(self,**kwargs):
            return [
                'svg[aria-label="Messenger"]'
                ]
        def click_notifications_button(self,**kwargs):
            return [
                'svg[aria-label="Notifications"]'
                ]
        def click_create_post_button(self,**kwargs):
            return [
                'svg[aria-label="New post"]'
                ]
        def click_profile_button(self,**kwargs):
            return [
                'svg[aria-label="Profile"]'
                ]
        
        def accounts_section_results__username(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/row_search_user_username']"
            ]
        
    class Search:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def enter_search_query(self,**kwargs):
           return [
                "//input[@aria-label='Search input']"
           ]
        def click_clear_all_searches(self,**kwargs):
            return [
                "//div[text()='Clear all']"
                    ]
        def remove_search(self,**kwargs):
            return [
                "svg[aria-label='Close']"
            ]
        def iterate_through_search_links(self,**kwargs):
            return [
                "//ul//a"
                    ]
        def iterate_through_search_results(self,**kwargs):
            return[
                "//div[div/span/text()='Search']/following-sibling::div/div/div/div[2]/div/a"
            ]
     
       
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
        def click_camera_button(self,**kwargs):
            return[
                "//*[@resource-id='com.instagram.android:id/creation_tab']"
            ]
    class StoryPage:
        def click_next_story_button(self,**kwargs):
            return [
                "//button[@aria-label='Next']"
                ]
        def click_on_reply_to_story_text_area(self,**kwargs):
            return [
                    "//textarea[contains(@placeholder,'Reply')]"
                    ]
        def click_share_story_button(self,**kwargs):
            return [
                "//div/button[@type='button']"
            ]
        def click_send_reply_button(self,**kwargs):
            return [
                "//div[text()='Send']"
                ]
        def click_like_story_button(self,**kwargs):
            return ["//span/div/div/span"]
        def iterate_through_stories(self,**kwargs):
            return [
                "//section/div/div/div"
                ]
        def close_story_section(self,**kwargs):
            return [
                "svg[aria-label='Close']"
            ]
        def get_sponsored_text(self,**kwargs):
            return [
                "//header//*[text()='Sponsored']"
            ]
    class HomePage:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        
        def iterate_through_posts(self,**kwargs):
            return [
                    "//div/article"
                    ]
        def get_stories_button(self):
            return [
                "//ul//li//button[contains(@aria-label,'Story by')]"
                    ]
        def get_username_from_post(self):
            return [
                "div/div[1]//span//div//a//div/div/span"
            ]
        def click_like_button(self,**kwargs):
            return [
                "svg[aria-label='Like']"
              
            ]
        def click_comment_button(self,**kwargs):
            return [
                '//section[1]/div/span[2]/div/div'
                    ]
        def click_share_post_button(self,**kwargs):
            return [
                '//section[1]/div/button'
                    ]
        def click_instagram_button(self,**kwargs):
            return [
                'svg[aria-label="Instagram"]'
                
            ]
        def click_bookmark_button(self,**kwargs):
            return [
                '//section[1]/div[2]'
                ]
        
        def click_next_media_button(self,**kwargs):
            return [
                '//button[@aria-label="Next"]'
                ]
        def click_add_a_comment_text_area(self,**kwargs):
            return [
                '//textarea[@aria-label="Add a comment…"]'
                ]
        def click_post_comment_button(self,**kwargs):
            return [
                '//div[text()="Post"]'
                ]
        def post_dialog_box(self,**kwargs):
            return [
                '//div[@role="dialog"]//article'
                ]
        
        def click_home_button(self,**kwargs):
            return[
                "//svg[aria-label='Home']"
            ]
        def click_explore_button(self,**kwargs):
            return[
                "//svg[aria-label='Explore']"
            ]
        
        def click_notifications_button(self,**kwargs):
            return[
               'svg[aria-label="Notifications"]'
            ]
        def has_new_notifications(self,**kwargs):
            return[
                "//div[@class='x14vhib7 xnwf7zb x40j3uw x1s7lred x15gyhx8 xdk7pt x1xc55vz x1yhmmig xeqyd3i xyb01ml xdn568n x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x5see2y x8ebbdf x1pzews7 x1r61nuk']"
            ]
        def click_inbox_button(self,**kwargs):
             return[
               'svg[aria-label="Direct"]'
            ]
        def has_new_messages(self,**kwargs):
            return[
                  "//*[@resource-id='com.instagram.android:id/action_bar_inbox_button'][contains(@text, 'unread')]" 

            ]
        def click_reels_button(self,**kwargs):
             return[
                "//svg[aria-label='Reels']"
            ]
        def click_create_new_post_button(self,**kwargs):
            return[
                "//svg[aria-label='New post']"
            ]
        def get_stories(self,**kwargs):
            return[
                  "//button[contains(@aria-label,'Story')]" 

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
    class PostDialogBox:
        def post_dialog_box(self,**kwargs):
            return [
                '//div[@role="dialog"]//article'
                ]
        def focus_on_comments_section(self,**kwargs):
            return [
                '//div[@role="dialog"]//article/div/div[2]'
                    ]
        def click_add_comment_text_area(self,**kwargs):
            return [
                '//div[@role="dialog"]//textarea'
            ]
        def click_post_comment_button(self,**kwargs):
            return [
                '//div[@role="dialog"]//div[text()="Post"]'
                ]
        def click_load_more_comments(self,**kwargs):
            return [
                'svg[aria-label="Load more comments"]'
                ]
        
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
        def is_comments_page(self,**kwargs):
            self.locat
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
                "//*[@resource-id='com.instagram.android:id/next_button_textview']"

            ]
        def click_next_button_from_filter_picker(self,**kwargs):
            return [
                "//*[@resource-id='com.instagram.android:id/next_button_textview']"

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
                "//*[@resource-id='com.instagram.android:id/next_button_textview']"

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


    class Reels:
        def get_required_xpath(self,**kwargs):
            
            touch_point=getattr(self,kwargs.get('touch_point'))
            return touch_point(**kwargs)
        def get_reels_title(self):
            pass
        def is_reels_page(self):
            return [
                "//div[@id='mount_0_0_aD']//section/main/div/div"
               
                
                    ]
        def iterate_through_posts(self,**kwargs):
            return [
                 "//div[contains(@id,'mount')]//section/main/div/div",
            ]

        def get_username(self,**kwargs):
           return [
               "//a[contains(@href,'reels')]",

           ]
        
        def get_follow_button(self,**kwargs):
            return [
                "//div[text()='Follow']"

            ]
        def get_like_button(self,**kwargs):
            return [
                "/div/div[2]/div[1]/span"
            ]
        
        def click_comment_button(self,**kwargs):
            return [
                "/div/div[2]/div[2]"
            ]
        
        def get_comment_title(self,**kwargs):
            return [
                    "//div[contains(@id,'mount')]//*[contains(text(),'Comments')]"

            ]
        def click_add_comment_text_area(self,**kwargs):
            return [
                "//input[@placeholder='Add a comment…']"
            ]
        def click_post_comment_button(self,**kwargs):
                        return [
                    "//div[contains(@id,'mount')]//div[text()='Post']"
                        ]
        def click_comment_container(self,**kwargs):
            return [
                "//div[@role='dialog']"
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
    


            
       

