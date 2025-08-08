from services.instagram.xpaths import Xpaths
from services.instagram.run_bot import Crawler
from services.reports_manager.manager import Manager as reports_manager

import time
import random
class Locator(Crawler):
    def __init__(self):
        super().__init__()
        self.driver=None
        self.xpath=None
        self.sub_page=''
        self.existing_content=[]
        self.reporter = reports_manager()  # ✅ Create reporter
    def load_new_content_on_page(self,content_identifiers,method,retries=0,max_tries=5,sleep_time=0.1):
        if retries>max_tries:
            return False
        from services.instagram.locator import Locator
       
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
                            
    


    def get_xpath_object(self,**kwargs):
        if not self.page:
            page=kwargs.get('page')
        else:
            page=self.page
        if page=='login_page':
            _xpath=Xpaths.LoginPage()
        if page=='profile_page':
            _xpath=Xpaths.ProfilePage()
        elif page=='explore_page':
            _xpath=Xpaths.Search()
        elif page =='posts_page':
            _xpath=Xpaths.Posts()
        elif page =='location_posts_page':
            _xpath=Xpaths.LocationPosts()
        elif page =='search_page':
            _xpath=Xpaths.LocationPosts()
        elif page=='home_page':
            _xpath=Xpaths.HomePage()
        elif page=='new_post_page':
            _xpath=Xpaths.NewPostPage()
        elif page=='recent_searches_page':
            _xpath=Xpaths.RecentSearches()
        self.xpath=_xpath
      
    def locato(self,**kwargs):
 
        if not self.xpath:
            self.get_xpath_object(**kwargs)


        xpaths=self.xpath.get_required_xpath(**kwargs)
        for xpath in xpaths:
            if '//' in xpath:
                xpath=xpath
                css_selector=None
            else:
                print('CSS selector')
                css_selector=xpath
                xpath=None
            elements=kwargs.get('elements',False)
            resp=self.browser.find_element(xpath=xpath,wait_time=0.1,elements=elements,max_retries=1,css_selector=css_selector)
            if resp:
                return resp
       
            return False
    def locate(self,**kwargs):
        self.xpath=None
        if kwargs.get('track'):

            self.identify_current_page()
            if not self.page:
                raise Exception('Unknow page')
        else:
            pass
            
        self.get_xpath_object()
        return self.locato(**kwargs)
    
    def locate_by_xpath(self, xpath, elements=False, attr=False, click=False, retries=1, **kwargs):
        import time, traceback
        task = kwargs.get('uuid')
        run_id = kwargs.get('run_id')

        start_time = time.time()

        # Normalize xpath list
        xpaths = xpath if isinstance(xpath, list) else [xpath]

        for xpath in xpaths:
            self.reporter.report_performance(**{
                'service': 'instagram',
                'end_point': 'locate_element',
                'data_point': 'start',
                'type': 'xpath_locate_attempt_start',
                'page': self.browser.driver.current_url,
                'x_path': xpath,
                'task': task,
                'run_id': run_id,
                'timestamp': start_time,
                'max_attempts': retries,

                })

        for xpath in xpaths:
            try:
                css_selector = None
                if '//' not in xpath:
                    css_selector = xpath
                    xpath = None

                resp = self.browser.find_element(
                    xpath=xpath,
                    wait_time=0.1,
                    elements=elements,
                    max_retries=retries,
                    css_selector=css_selector
                )

                if resp:
                    if click:
                        try:
                            resp.click()
                            # self.browser.wait_until_page_loaded(wait_timeout=50, max_retries=3, **kwargs)
                            self.reporter.report_performance(**{
                                'service': 'instagram',
                                'end_point': 'locate_element',
                                'data_point': 'success',
                                'page': self.browser.driver.current_url,
                                'x_path': xpath ,
                                'type': 'clicked_xpath',
                                'task': task,
                                'run_id': run_id,
                                'timestamp': time.time(),
                                
                            })
                            return resp
                        except Exception as e:
                            self.reporter.report_performance(**{
                                'service': 'instagram',
                                'end_point': 'locate_element',
                                'data_point': 'exception',
                                'type': 'click_failed',
                                'x_path': xpath ,
                                'task': task,
                                'run_id': run_id,
                                'critical': True,
                                'timestamp': time.time(),
                                'string': {'name': type(e).__name__, 'args': str(e)},
                                'traceback': traceback.format_exc()
                            })
                            return False

                    if attr:
                        if not isinstance(resp, list):
                            resp = [resp]
                        results = []
                        for res in resp:
                            results.append(res.get_attribute(attr) if attr != 'text' else res.text)
                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'locate_element',
                            'data_point': 'success',
                            'type': 'xpath_attr_fetched',
                            'x_path': xpath ,
                            'page': self.browser.driver.current_url,
                            'task': task,
                            'run_id': run_id,
                            'timestamp': time.time(),
                            
                        })
                        return results[0] if not elements else results
                    else:
                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'locate_element',
                            'data_point': 'success',
                            'page': self.browser.driver.current_url,
                            'x_path': css_selector or xpath,
                            'type': 'xpath_found',
                            'task': task,
                            'run_id': run_id,
                            'timestamp': time.time(),
                            
                        })
                        return resp

            except Exception as e:
                self.reporter.report_performance(**{
                    'service': 'instagram',
                    'end_point': 'locate_element',
                    'data_point': 'exception',
                    'type': 'xpath_exception',
                    'x_path': xpath ,
                    'task': task,
                    'run_id': run_id,
                    'critical': True,
                    'timestamp': time.time(),
                    'string': {'name': type(e).__name__, 'args': str(e)},
                    'traceback': traceback.format_exc()
                })
                continue

        # Final failure log if no element found
        self.reporter.report_performance(**{
            'service': 'instagram',
            'end_point': 'locate_element',
            'data_point': 'failure',
            'page': self.browser.driver.current_url,
            'x_path': xpath ,
            'type': 'xpath_not_found',
            'task': task,
            'run_id': run_id,
            'timestamp': time.time(),
            
        })

        return False

    


    def identify_active_page(self, page_locators_dict, max_retries=50, retries=0, random_order=False, **kwargs):
        import random, time, traceback
        task = kwargs.get('uuid')
        run_id = kwargs.get('run_id')
        pages_to_check = list(page_locators_dict.keys())

        print("Attempting to identify active page...")

        try:
            while not retries >= max_retries:
                if random_order:
                    random.shuffle(pages_to_check)
                

                for page_name in pages_to_check:
                    locators_for_page = page_locators_dict.get(page_name, [])

                    if not locators_for_page:
                        print(f"Warning: No locators defined for page: '{page_name}'. Skipping.")
                        continue

                    # Log detection start
                    start_time = time.time()
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'page_detect',
                        'page': self.browser.driver.current_url,
                        'data_point': 'start',
                        'type': 'page_detection_started',
                        'xpath': locators_for_page,
                        'task': task,
                        'run_id': run_id,
                        'critical': False,
                        'timestamp': start_time,
                    })

                    # Attempt to detect
                    if self.locate_by_xpath(xpath=locators_for_page, retries=1, **kwargs):
                        print(f"Successfully identified active page: '{page_name}'")

                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'page_detect',
                            'data_point': 'success',
                            'type': 'page_identified',
                            'xpath': locators_for_page,
                            'page': self.browser.driver.current_url,
                            'task': task,
                            'run_id': run_id,
                            'critical': False,
                            'timestamp': time.time(),
                            'max_attempts': retries,
                        })
                        return page_name

                    # ❗️Per-attempt failure log (moved inside loop)
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'page_detect',
                        'data_point': 'failure',
                        'type': 'page_not_identified',
                        'xpath': locators_for_page,
                        'page': self.browser.driver.current_url,
                        'task': task,
                        'run_id': run_id,
                        'critical': False,
                        'timestamp': time.time(),
                        'max_attempts': retries
                    })

                    retries += 1

            # All retries exhausted
            print("Could not identify any active page from the provided locators.")
            return None

        except Exception as e:
            print("Exception during page detection:", e)
            self.reporter.report_performance(**{
                'service': 'instagram',
                'end_point': 'page_detect',
                'data_point': 'exception',
                'type': 'page_detection_exception',
                'task': task,
                'run_id': run_id,
                'critical': True,
                'timestamp': time.time(),
                'max_attempts': retries,
                'string': {
                    'name': type(e).__name__,
                    'args': str(e)
                },
                'traceback': traceback.format_exc()
            })
            return None
