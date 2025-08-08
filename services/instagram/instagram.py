import requests

import random
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import pickle
#from django.conf import settings
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        InvalidSelectorException,
                                        JavascriptException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
import zipfile
import random as rd
import traceback
import json
from compatpatch import  ClientCompatPatch
from shopify_admin_api import ShopifyAPI
from googlesheets import GoogleSheet
from browser import Browser
from request_maker import Request
from recursion import Recursion
import logging
from parsers import Parser
class Crawler(object):

    def __init__(self):
        self.user_agent=None
        self.driver=None
        self.scraping_resources_created=False
        self.use_proxies=None
        self.sniffed_data=None
        self.scraped_data=[]
        self.followers_data=[]
        self.posts_data=[]
        self.profiles_data=[]
        self.make_request=Request.make_request
        self.base_path=r'E:\scraping_automation_scripts\twitter_api_scraper'
        self.parsers=Parser()
        self.max_scrape_count=500
        self.user_data_dir=''
    def create_headers(self):
        self.driver.get('https://www.instagram.com/camarena_artss/')
        time.sleep(4)
        patho=self.browser.save_cookies('test')
        
        for cookie in self.driver.get_cookies():
            print(cookie)
            if cookie['name']=='csrftoken':
                csrf_token=cookie.get('value')
        x_abs_id=''
        x_ig_app_id=''
        x_ig_www_claim='' 
        x_instagram_ajax='' 
        for request in self.driver.requests:
          
            if request.headers['x-asbd-id']:
                x_abs_id=request.headers['x-asbd-id']
            if request.headers['x-ig-app-id']:
                x_ig_app_id=request.headers['x-ig-app-id']
            if request.headers['x-ig-www-claim']:
                x_ig_www_claim=request.headers['x-ig-www-claim']
            if request.headers['x-instagram-ajax']:
                x_instagram_ajax=request.headers['x-instagram-ajax']
            if len(x_ig_www_claim)>1 & len(x_abs_id)>1 & len(x_ig_app_id)>1:
                break
        
        guest_token=None
        headers={
        

        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "x-csrftoken":csrf_token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1518.52",
        "scheme": "https",
        "x-ig-app-id": x_ig_app_id,
        "x-ig-www-claim":x_ig_www_claim,
        "x-absd-id":x_abs_id,
        "accept": "*/*",
        "x-instagram-ajax":x_instagram_ajax,
        "sec-ch-ua-platform": "Windows",
        "x-requested-with": "XMLHttpRequest",    
        }
        count=0
        print(headers)
        self.headers=headers
        self.session.headers.update(headers)
        self.scraping_resources_created=True
    def initialize_request_session(self,use_cookies=False,use_proxies=False):
        session=requests.session()     
        print(type(use_cookies))  
        if use_cookies:
            if not type(use_cookies)==list:

                cookie_path = use_cookies
                cookies = pickle.load(open(cookie_path, "rb"))
            else:
                cookies=use_cookies
            for cookie in cookies:
                if cookie['name']=='urlgen':
                    pass
                else:
                    session.cookies.set(name=cookie['name'],value=cookie['value'])
                
                  
        
        if self.use_proxies  and isinstance(self.use_proxies.get('proxy_url',None), str):
            if len(self.use_proxies['proxy_url'].split(':')) == 4:
                proxy_config = {
                    'http': 'http://%s:%s@%s:%s' % tuple(self.use_proxies['proxy_url'].split(':')),
                    #'https': 'https://%s:%s@%s:%s/' % tuple(self.use_proxies['proxy_url'].split(':')),
                }
                use_proxies = proxy_config
            else:
                 use_proxies = {'http': 'http://'+self.use_proxies['proxy_url']}
            session.proxies.update(use_proxies)
          
                
        
        
       
        self.session = session
        self.create_headers()         
    def create_scraping_resources(self):
        if not self.scraping_resources_created:
            browser=Browser()
            self.browser=browser
            browser.initialize_chrome_browser(mobile_emulation=False,user_data_dir=self.user_data_dir)
            self.driver=browser.driver
            self.driver.response_interceptor=self.intercept_post_request_and_change_caption
            self.driver.get('https://www.instagram.com/p/CUDXXtFrV1P/?img_index=1')
       
            self.initialize_request_session(use_cookies=self.driver.get_cookies())
          
            r=Request()
            r.initialize_logger()
            r.session=self.session
        
            self.make_request=r.make_request                   
    def get_conversation_data_instagram(self,url,data=None):  
        response=self.session.post(url,data)
        response=json.loads(response.text)
        print(response['content']['data']['user']['edge_followed_by']['page_info']) 
    def create_url_instagram(self,end_point,**kwargs):
        if end_point=='conversation':
            conversation_id=kwargs['conversation_id']
            if 'cursor' in kwargs.keys():
                cursor=kwargs['cursor']
                url='https://www.instagram.com/api/v1/direct_v2/threads/'+conversation_id+'/?cursor='+cursor+''
            else:
                url='https://www.instagram.com/api/v1/direct_v2/threads/'+conversation_id+''

        elif end_point=='followers':
            url='https://www.instagram.com/graphql/query/'    
        return url
    def get_media_info(self,short_code):
        queryhash='b3055c01b4b222b8a47dc12b090e4e64'
        params={"shortcode":short_code,"query_hash":queryhash} #,"child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}')
        try:
            info = self.session.get(
                'https://www.instagram.com/graphql/query/',params=params)
           
            if info.ok:
                info = info.json()
            else:
                return {
                    'error': info.reason
                }
        except Exception as exc:
            print(exc)
            return None
        print(info)
        media = ClientCompatPatch.media(info)
        print(media)
        return media
    def user_info(self,**kwargs):
        username=kwargs.get('username')
        url='https://www.instagram.com/api/v1/users/web_profile_info/?username='+username+''
        response=self.make_request('user_info',url)
        return self.parsers.parse_end_point('user_info',response,**kwargs)             
    def user_followers(self,**kwargs):
        url=self.create_url_instagram('followers')
        if kwargs.get('rest_id',None):
            rest_id=kwargs['rest_id']        
        variables = {'id':rest_id, 'first': 100}     
        if kwargs.get('next_cursor'):
            cursor=kwargs.get('next_cursor')
            variables.update({'after':cursor})  
        else:
            cursor=None
           
       
        query = {
                'query_hash': '7dd9a7e2160524fd85f50317462cff9f',
                'variables': json.dumps(variables, separators=(',', ':'))
            }
        response=self.make_request('user_followers',url,params=query)
        return self.parsers.parse_end_point('user_followers',response,**kwargs)      
    def type_post_caption(self, caption: str):
        import emoji
        """
        """
        try:
            has_emoji, value = len(emoji.emoji_lis(caption)) > 0, None
            caption_element = self.driver.find_element_by_xpath(
                '//div[@aria-label="Write a caption..."]/p'
            )
            #caption_element.send_keys('my darling')
            if has_emoji:
                '''try:
                    _caption_element=self.driver.find_element_by_xpath('//div[@aria-label="Write a caption..."]/p/span')
                except Exception as e:
                   
                    caption_element.send_keys(caption)'''
                    #return
                _js = """
                    var evt = new Event('input', {'bubbles': !0});
                    var input_field = arguments[0];
                    var message = arguments[1];
                    input_field.innerHTML=message;
                    input_field.outerHTML=input_field.outerHTML+' '+message
                    input_field.data=message;
                    input_field.textContent=message;
                    input_field.wholeText=message;
                    input_field.textContent='message;
                    input_field.outerText=message;
                    input_field.innerText=message;
                    input_field.text=message;
                    input_field.value=message;
                    input_field.dispatchEvent(evt);
                    return input_field.value
                    parentDiv=document.evaluate('//div[@aria-label="Write a caption..."]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    parent=parentDiv.parentElement
                   parentDivClone=parentDiv.cloneNode(true)
                    parentDivClone.children[0].firstChild.innerText='hammmy'
                    parent.replaceChild(parentDivClone,parent.children[0])

                """
                outer_html='<span data-lexical-text="true">'+caption+'</span>'

                value = self.driver.execute_script(
                    _js,
                    caption_element,
                    caption,
                    outer_html
                )
            else:
                ActionChains(
                    self.driver
                ).move_to_element(
                    caption_element
                ).send_keys_to_element(
                    caption_element,
                    caption,
                ).perform()

                value = caption_element.get_attribute('value')
            if value:
                return True, None
            return False, "Failed to type comment"

        except WebDriverException as exc:
            print(exc)
            return False, "Failed to Send Comment to the comment box. Error:%s" % (exc.msg)
    def create_feed_post(self, username: str, file_path: str, caption: str):
        """[summary]

        Args:
            username (str): [description]
            file_path (str): [description]
            caption (str): [description]

        Returns:
            [type]: [description]

        """
        try:
            self.driver.find_element_by_xpath('//div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]').click()           
            time.sleep(random.randint(3, 5))
            
            
            
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                        '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')))

            time.sleep(random.randint(3, 5))
            uploaded=False  
            for i,path in enumerate(file_path):
                if i==1:
                    WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                    'svg[aria-label="Open media gallery"]')))
                    
                    self.driver.find_element_by_css_selector('svg[aria-label="Open media gallery"]').click()
                    time.sleep(1)
                
                
                try:
                    self.driver.find_element_by_xpath(
                        '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]').send_keys(path)
                    
                    msg = "Success"
                except WebDriverException as exception:
                    print(exception)
                    
                    msg = exception
                else:
                    uploaded=True
                
            if not uploaded:
                return False, msg
            try:
                WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                        'svg[aria-label="Select crop"]')))
                self.driver.find_element_by_css_selector('svg[aria-label="Select crop"]').click()
            except Exception as e:
                pass
            else:
                time.sleep(random.randint(1,3))
                try:
                    self.driver.find_element_by_xpath('//button/div/div/div[text()="Original"]').click()
                except Exception as e:
                    print(e)
            try:
                WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                        '//span[contains(text()," shared as reels")]')))
            except Exception as e:
                pass
            else:
                try:
                    self.driver.find_element_by_xpath('//*[text()="OK"]').click()
                except Exception as e:
                    pass
                

            time.sleep(random.randint(3, 8))
            
            
            next_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[text()="Next"]')
            )
        )
            time.sleep(random.randint(3, 5))
            next_btn.click()
            
            try:
                WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located (
                (By.XPATH, '//div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div/div/form/input')
                )
                )
                self.driver.find_element_by_xpath('//div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div/div/form/input').send_keys(r'F:\darrxscale-dev-space-new\scraping_automation_scripts\twitter_api_scraper\media\342574e7-cfe9-11ed-bc82-0021ccb4ed18.jpg')
            except Exception as e:
                pass
            time.sleep(random.randint(3, 8))
            next_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[text()="Next"]')
            )
        )
            time.sleep(random.randint(3, 5))
            next_btn.click()
            if caption:
                self.type_post_caption(caption)
            time.sleep(random.randint(3,5))
            self.driver.find_element_by_xpath(
                '//*[text()="Share"]'
            ).click()

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'img[alt="Animated checkmark"]'
                    )
                )
            )
            time.sleep(10)
            

            return True, 'Posted image'
        except WebDriverException as exc:
        
            print(exc)
            return False, exc.msg
    def search_location(self,query=None,co_ords={},rank_token='720c9c6c-f407-4916-b8cf-18541b898b75'):
        params={'latitude':co_ords.get('latitude',0),'longitude':co_ords.get('longitude',0)}
        if query:
            params.update({'search_query':query})
        
        params.update({'rankToken':rank_token})
        params.update({'timestamp':str(round(time.time()*1000))})
        url='https://www.instagram.com/api/v1/location_search/'
        resp=self.session.get(url,params=params)
        location=resp.json()['venues'][0]
        return location
    def search_hashtags(self,query=None):
        url='https://www.instagram.com/api/v1/web/search/topsearch/'
        0.002777659144470812
        context = {
               "context":"hashtag",
                "query": query,
                "rank_token": 0.547015482035698,
                "include_reel": True,
                "search_surface": "web_top_search"
                    }
        resp=self.session.get(url,payload=context)
        print(resp.text)
    def search_user(self,query=None):
         context = {
            "context":"hashtag",
            "query": query,
            "rank_token": 0.547015482035698,
            "include_reel": True,
            "search_surface": "web_top_search"
                    }
    def get_details_about_location(self):
        resp=self.session.get('https://www.instagram.com/api/v1/locations/web_info/?location_id=c2511940')
        print(resp.text)
    def explore_city_directory(self):
        url='https://www.instagram.com/api/v1/locations/city/directory/?directory_code=c2728325&page=2'
        resp=self.session.get(url)
        print(resp.text)
    def explore_country_directory(self,directory_code=''):
        if not directory_code:
            url='https://www.instagram.com/api/v1/locations/directory/'
            resp=self.session.get(url)
            print(resp.text)
    
            url='https://www.instagram.com/api/v1/locations/country/directory/?directory_code=US'
            resp=self.session.get(url)
            print(resp.text)
    def post_photo(self,  photo_path, caption='',multiple=False,location=None):
        import mimetypes
        import time
        """
        Post a photo
        
        :param photo_data: byte string of the image
        :param caption: caption text
        """
        upload_ids=[]
        photo_paths=[photo_path]
        for path,thumbnail in photo_path:
            upload_id = str(round((time.time()*1000)))
            data = None
            content_type, _ = mimetypes.guess_type(path)
            with open(path, 'rb') as io:
                data = io.read() 
            headers = {
            
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate, br',
            
                'x-requested-with': 'XMLHttpRequest',
                #'x-instagram-ajax': hash_,
                'x-entity-length': str(len(data)),
                'x-entity-name': 'fb_uploader_%s' % upload_id,
                'x-entity-type': content_type,
            
            
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
                'Content-Type': content_type,
                'Offset': '0',
                'Content-Length': str(len(data))
            }
            if 'video' in content_type:
               
                _up={"client-passthrough":"1","is_clips_video":"1","is_sidecar":"0","media_type":2,"for_album":False,"video_format":"","upload_id":upload_id,"upload_media_height":1080,"upload_media_width":1080,"video_transform":None}#"video_edit_params":{"crop_height":360,"crop_width":360,"crop_x1":140,"crop_y1":0,"mute":False,"trim_end":17.461406,"trim_start":0}
                headers.update({'path':'rupload_igvideo/fb_uploader_'+str(upload_id)})
                endpoint = 'https://www.instagram.com/rupload_igvideo/fb_uploader_%s' % upload_id
                c_endpoint='https://www.instagram.com/api/v1/media/configure_to_clips/'
                _key='media_id'
            else:
                _up={"media_type": 1, "upload_id": upload_id, "upload_media_height": 1080, "upload_media_width": 1080}
                endpoint = 'https://www.instagram.com/rupload_igphoto/fb_uploader_%s' % upload_id
                c_endpoint='https://www.instagram.com/api/v1/media/configure/'
                _key='upload_id'
            headers.update({ "x-instagram-rupload-params": json.dumps(_up)})   
                              
            self.session.headers.update(headers)           
            upload_request = self.session.post(endpoint, data)
            if upload_request.ok:
                upload_res = upload_request.json()
            upload_id_ = upload_res[_key]
            upload_ids.append(upload_id)
            if 'video' in content_type:
                _up={"media_type": 2, "upload_id": upload_id, "upload_media_height": 798, "upload_media_width": 798}
                endpoint = 'https://www.instagram.com/rupload_igphoto/fb_uploader_%s' % upload_id
                
                _key='upload_id'
                if thumbnail:
                    
                    thumbnail_path=self.download_media(thumbnail,'image')
                    with open(thumbnail_path, 'rb') as io:
                        data = io.read() 
                self.session.headers.update({'x-entity-type': 'image/jpeg'})  
                self.session.headers.update({'x-entity-length': str(len(data))})        
                upload_request = self.session.post(endpoint, data)
                if upload_request.ok:
                    upload_res = upload_request.json()

            
        self.session.headers.clear()
        self.session.headers.update(self.headers)
        self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        
      
        endpoint = c_endpoint
        data = {
            'upload_id': upload_ids[0],
            'usertags': '',
            'source_type': 'library',
            'caption':caption,
            
            
            'disable_comments': 0,
            'like_and_view_counts_disabled': 0,
            'igtv_share_preview_to_feed': 1,
            'is_unified_video': 1,
            'video_subtitles_enabled': 0,
            'disable_oa_reuse': False
        }
        if location:
            data.update({'location':json.dumps(location)})
        if multiple:
            data={"source_type":"library","caption":'',"disable_comments":0,"like_and_view_counts_disabled":0}
            endpoint='https://www.instagram.com/api/v1/media/configure_sidecar/'
            import uuid
            data.update({'client_sidecar_id':str(round((time.time()*1000)))})
            data.update({'children_metadata':[]})
            '''self.session.headers.update({'content-type': 'application/json'})
            self.session.headers.update({'path': '/api/v1/media/configure_sidecar/'})
     
            self.session.headers.update({'scheme': 'https'})
            self.session.headers.update({"sec-fetch-dest": "empty"})
            self.session.headers.update({'sec-fetch-mode': 'cors'})
            self.session.headers.update({'sec-ch-prefers-color-scheme': 'light'})
            self.session.headers.update({'accept-language': 'en-US,en;q=0.9'})
            self.session.headers.update({'sec-fetch-site': 'same-origin'})
            self.session.headers.update({'authority': 'www.instagram.com'})
            self.session.headers.update({'accept-encoding': 'gzip, deflate, br'})
            self.session.headers.update({'content-length': '213'})'''
           
            h={
                'authority': 'www.instagram.com',
                'method': 'POST',
            
            'path': '/api/v1/media/configure_sidecar/',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': ';en-US,en;q=0.9',
            'content-length': '243',
            'content-type': 'application/json',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
          
           
            'x-requested-with': 'XMLHttpRequest'
            }
         
            self.session.headers.update(h)
 
            for upload_id in upload_ids:
                data['children_metadata'].append({'upload_id':str(upload_id)})
            print(data)
            _data={"source_type":"library","caption":"","disable_comments":"0","like_and_view_counts_disabled":0,"children_metadata":[{"upload_id":"1680575213562"},{"upload_id":"1680575213759"},{"upload_id":"1680575213567"}],"client_sidecar_id":"1680575284665"}
            print(_data)
            self.session.headers.update({'content-length': str(len(str(data)))})
        
        response=self.session.post(endpoint,data=data)
       
       
        print(response.text)
        return response
    def download_and_post(self,link=None,caption=None,location=None,tags=None):
        media_link=[]
        if 'shopify' in link:
            s=ShopifyAPI()
           
            data=s.get_data_for_purpose(**{'store':self.store,'product_id':self.product_id,'purpose':'social_media_posting','end_point':'product'})
            caption=data.get('caption')
            caption+='\n'+data.get('hashtags','')
            media_type='image'
        else:
            shortcode=link.split('/')[4]
            data=self.get_media_info(shortcode)
            media_type=data['type']
            if data.get('carousel_media',{}):
                if len(data.get('carousel_media'))>0:
                    media_type='carousel'
            
            caption=data.get('caption',{})
            if caption:
                caption=caption['text']

        if media_type=='video':
            print('Media Type is video')
            original_height=data.get('original_height','')
            original_width=data.get('original_width','')
            print('original height of media is:'+str(original_height))
            print('original width of media is:'+str(original_width))
            print('total video types are:'+str( len(data.get('videos'))))
            print('Using Original Widht and Height')
            
            for video in data.get('videos'):
                    _video=video.get('standard_resolution',{})
                    media_link.append({'media_type':'video','url':_video.get('url'),'thumbnail':data.get('images',[])[0].get('thumbnail',{}).get('url',None)})
        elif media_type=='image':
            print('Media Type is Image')
            original_height=data.get('original_height','')
            original_width=data.get('original_width','')
            print('original height of media is:'+str(original_height))
            print('original width of media is:'+str(original_width))
           
            print('Using Original Widht and Height')
            images=data.get('images',[])[0]
            media_link.append({'media_type':'image','url':img.get('url'),'thumbnail':''})       
           
        elif media_type=='carousel':
            print('Media Type is Carousel')
            print('Tota Carousel Objects are:'+str(len(data.get('carousel_media'))))
            for i,carousel in enumerate(data.get('carousel_media',[])):
                print('checking carousel '+str(i))
                media_type=carousel['type']
                if media_type=='video':
                    print('Media Type is video')
                    original_height=carousel.get('original_height')
                    original_width=carousel.get('original_width')
                    print('original height of media is:'+str(original_height))
                    print('original width of media is:'+str(original_width))
                  
              
                    print('Using Original Widht and Height')
                    videos=carousel.get('videos')
                    video=videos.get('standard_resolution',{})
                    media_link.append({'media_type':'video','url':video.get('url')})
                    

                elif media_type=='image':
                    print('Media Type is Image')
                    original_height=carousel.get('original_height')
                    original_width=carousel.get('original_width')
                    print('original height of media is:'+str(original_height))
                    print('original width of media is:'+str(original_width))
                    print('total image types are:'+str( len(carousel.get('images'))))
                    print('Using Original Widht and Height')
                    images=carousel.get('images',[])
                    img=images.get('standard_resolution',{})        
                    media_link.append({'media_type':'image','url':img.get('url')})
        print('media links acquired')   
        print(media_link)
        print(caption)
        print('Now downloading media')
        file_paths=[]
        for link in media_link:
            file_paths.append((self.download_media(link['url'],link['media_type']),link.get('thumbnail','')))
            
       
        #self.create_feed_post('art_camarena',file_paths,'')
        multiple=False
        if len(file_paths)>1:
            self.post_photo(photo_path=file_paths,caption=caption,location=location,multiple=multiple)
            self.create_feed_post('art_camarena',file_paths,'')
            time.sleep(10)
            if self.sniffed_data:
                media_id=self.sniffed_data.get('media',{}).get('pk')
                self.edit_media(media_id=media_id,caption=caption,location=location)
        else:
            self.post_photo(photo_path=file_paths,caption=caption,location=location,multiple=multiple)      
    def edit_media(self,media_id,caption=None,location=None):
        url='https://www.instagram.com/api/v1/media/'+str(media_id)+'/edit_media/'
        data={}
        if caption:
            data.update({'caption_text':caption})
        if location:
            data.update({'location':json.dumps(location)})
       
        print(data)
        resp=self.session.post(url,data=data)
        print(resp.text)
    def delete_media(self,media_id):
        url='https://www.instagram.com/api/v1/web/create/'+str(media_id)+'/delete/'
        resp=self.session.post(url)
        if resp.josn().get('did_delete',False):
            print('Media Deleted Successfully')
        else:
            print('Failed to Delete Media')
    def download_media(self,link,media_type):
        import uuid
        import requests
        if media_type=='image':
            file_path=os.path.join(r'F:\darrxscale-dev-space-new\scraping_automation_scripts\twitter_api_scraper\media',str(uuid.uuid1())+'.jpg')
        elif media_type=='video':
            file_path=os.path.join(r'F:\darrxscale-dev-space-new\scraping_automation_scripts\twitter_api_scraper\media',str(uuid.uuid1())+'.mp4')
        print ("Downloading file:%s"%file_path)
        r = requests.get(link, stream = True)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
    
        print ("%s downloaded!\n"%file_path)
        return file_path
    def intercept_post_request_and_change_caption(self,request,response):
        if request.url=='https://www.instagram.com/api/v1/media/configure_sidecar/' or request.url=='https://www.instagram.com/api/v1/media/configure/':
            if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
                from seleniumwire.utils import decode as sw_decode
                data = sw_decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
                self.sniffed_data=json.loads(data)               
    def save_to_google_sheet(self,**kwargs):
        share_with_emails=kwargs.get('share_with_emails',None)
        folder_name=kwargs.get('folder_name')
        spreadsheet_title=kwargs.get('spreadsheet_title',None)
        from googlesheets import GoogleSheet
        g=GoogleSheet()
        g.initialize_google_drive_api()
        resp=g.google_drive_api.get_files_in_folder(**{'folder_name':folder_name})
        g.share_with_email_addresses=share_with_emails
        g.folder_name=folder_name
        g.spreadsheet_title=spreadsheet_title
        g.initialize_connection().check_if_folder_exists().check_if_folder_has_been_shared_with_user()
        g.initialize_connection().check_if_file_exists_in_active_folder().open_google_sheet()
        if self.profiles_data:
            g.worksheet_title='profile'
            g.find_worksheet()
            g.data=self.profile_data
            g.update_worksheet()
        if self.posts_data:
            g.worksheet_title='posts'
            g.data=self.posts_data
            g.find_worksheet()
            g.update_worksheet()
        if self.followers_data:
            g.worksheet_title='followers'
            g.data=self.followers_data
            g.find_worksheet()
            g.update_worksheet()
    def run(self,**kwargs):    
        self.instagram_main(**kwargs)
        if kwargs.get('save_to_google_sheet',False):
            self.save_to_google_sheet(**{'folder_name':kwargs.get('folder_name','data-test21'),'share_with_emails':['metazon.inc@gmail.com'],'spreadsheet_title':'hamza-data'})            




c=Crawler()
r=Recursion()
r.session_id='asdasdasdasd'

r.crawler=c
c.create_scraping_resources()
#data=c.user_info(user_name='juliancamarena')
#if data and data.get('user') and data.get('user',{}).get('rest_id',''):
#rest_id=data.get('user',{}).get('rest_id',None)    
r.recursive_api_caller(end_point='user_info',username='juliancamarena')


""" if end_point=='user_info':
                data=self.crawler.user_info(**{'username':username})
            if end_point=='user_followers':
                data=self.crawler.user_followers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            if end_point=='list_followers':
                data=self.crawler.list_followers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point=='followings':
                data=self.crawler.user_followings(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'user_feed':
                data=self.crawler.user_feed(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'trends':
                data=self.crawler.trends(**{'next_cursor':next_cursor,'query':query,'query_type':'Top','query_url':query_url,'query_type':query_type})
            elif end_point == 'media_info':
                data=self.crawler.media_info(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'media_likers':
                data=self.crawler.media_likers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'place':
                data=self.crawler.place(**{'query':query,'query_url':query_url})
            elif end_point=='lists':
                data=self.crawler.lists(**{'query':query,'query_url':query_url}) """