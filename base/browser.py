from json.decoder import JSONDecodeError

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
import time
import random as rd
import pickle
import os
class Browser(object):
    def __init__(self):
       
        self.logged_in=True
        self.cookies = None  # type: str
      

        self.use_proxies = ''#{'proxy_url':'jcamar:hurley92:52.128.222.109:29842','proxy_type':'rotating'}
        self.browser_proxies=None#{'proxy_url':'jcamar:hurley92:52.128.222.109:29842','proxy_type':'rotating'} # type: str
        self.ip_info=None
   
        self.error = None  # type: str
        self.auto_patch=True
 
        self.rate_limited=False
        self.bypass_rate_limit=False
        self.end_point_banned=False
        self.request_counter=0
        self.localstore=True
        self.base_path=r'E:\scraping_automation_scripts\twitter_api_scraper'
        self.service='twitter'
        self.user_agent=None
        self.task=None
        self.reproter=None
    def handle_password_protected_proxy(self,proxy):
        proxy=proxy.split(':')
        PROXY_HOST = proxy[2]  # rotating proxy or host
        PROXY_PORT = proxy[3] # port
        PROXY_USER = proxy[0] # username
        PROXY_PASS = proxy[1]
        manifest_json = """
            {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
            }
            """

        background_js = f"""
    // Function to set the proxy
    function setProxy() {{
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{PROXY_HOST}",
                    port: parseInt("{PROXY_PORT}")
                }},
                bypassList: ["localhost"]
            }}
        }};
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    }}
    setProxy();
    // Function to clear the proxy
    function clearProxy() {{
        chrome.proxy.settings.clear({{scope: "regular"}}, function() {{}});
    }}

    // Check if proxy has been set in this *session*.  If not, set it.
    

        // Clear the proxy settings when the *browser* closes (all windows)
    chrome.runtime.onSuspend.addListener(function() {{
    clearProxy();
    }});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{PROXY_USER}",
                password: "{PROXY_PASS}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );"""
        return manifest_json,background_js
    def initialize_chrome_browser(self,headless=False,refresh_profile=False,profile=False,incognito=False,selenium_wire=False,mobile_emulation=False,enable_geolocation=False,user_data_dir=False,use_cookies=False,use_proxies=False):
         from base.browser_utils import ChromeDriverCheckerandDownloader
         c=ChromeDriverCheckerandDownloader()
         c.reporter=self.reporter
         c.task=self.task['uuid']
         c.check_and_download_chromedriver()
         if not self.browser_proxies:
             if not use_proxies:
                 self.browser_proxies=''
             else:
                 self.browser_proxies=use_proxies
         if profile:
            user_data_dir=os.path.join(os.getcwd(),'resources',profile,'browser')
            if refresh_profile:
               
                try:
                     import shutil
                     shutil.rmtree(user_data_dir)
                    
                except Exception as e:
                    pass
             
            if not user_data_dir:
                 os.makedirs(user_data_dir)
            


         import pickle
         self.chrome_options = webdriver.ChromeOptions()
         if headless:
              self.chrome_options.add_argument("--headless")   
         if incognito:
             self.chrome_options.add_argument("--incognito ")           
         if mobile_emulation:             
             user_agents={'user_agents':[{'MotoG4':'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'},
                         {'Nexus5':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'},
                         {'Pixel2Xl':'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'},
                         {'Iphone5':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'},
                         {'Iphone6':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'},
                         {'Iphone6Plus':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'},
                         {'IphoneX':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'},
                         {'Galaxy S5':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'},
                         {'Pixel2':'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'},
                         #{'Ipad':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'},
                         #{'IpadPro':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'},
                         ]}
             width=rd.randint(400,800)
             height=rd.randint(500,700)
             user_agent=rd.sample(user_agents['user_agents'],1)
             if self.user_agent:
               if user_agent==self.user_agent:
                  self.user_agent=rd.choice(user_agents['user_agents'])
                  
             else:
                self.user_agent=user_agent
                
             for key,value in self.user_agent[0].items():
                self.user_agent=value
             mobile_emulation = {
            "deviceMetrics": { "width": width, "height": height, "pixelRatio": 8.0 },
            "userAgent": self.user_agent }            
            #mobile_emulation = { "deviceName": device_name }                 
             self.chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
         if enable_geolocation:
              self.chrome_options.add_argument("enable-geolocation");     
         if user_data_dir:
              self.chrome_options.add_argument("user-data-dir="+user_data_dir+"") #Path to your chrome profile

         self.chrome_options.add_argument("--disable-notifications");
      
         self.chrome_options.add_argument("--start-maximized")
       
         self.chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled"
                )
         self.chrome_options.add_experimental_option("useAutomationExtension", False)
         self.chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
         preference = {
                'disk-cache-size': 4096,
                "exit_type": "normal"
            }
         #self.chrome_options.add_experimental_option('prefs', preference)
         self.chrome_options.add_argument("--disable-gpu")
         self.chrome_options.page_load_strategy='none'
         self.chrome_options.add_argument("log-level=3")
         self.chrome_options.add_argument("--disable-notifications")
            
         self.chrome_options.add_argument("ignore-certificate-errors")
         self.chrome_options.add_argument("--disable-infobars")
         self.chrome_options.add_argument("--disable-blink-features")
         self.chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled"
    )  
         capabilities = self.chrome_options.to_capabilities() 
         options = {
                'suppress_connection_errors': True,
                'debug':False,  # Show full tracebacks for any connection errors
                    }        
         if self.browser_proxies:
            use_proxies=self.browser_proxies
            url=self.browser_proxies
            if len(url.split(':'))>2:
                
                if not selenium_wire:
                    manifest_json, background_js = self.handle_password_protected_proxy(
                                use_proxies
                            )
                    proxy = use_proxies.split(':')
                    username, password, host, port = proxy[0], proxy[1], proxy[2], proxy[3]
                    file_name = 'proxy_auth_plugin.zip'
                    if profile:
                        file_location=user_data_dir
                    else:
                        file_location = os.path.join(os.getcwd(),'resources','profiles',self.service,self.bot_username,'extensions')
                    if not os.path.exists(file_location):
                        os.makedirs(file_location)
                    with zipfile.ZipFile(os.path.join(file_location,file_name), 'w') as zp:
                        zp.writestr("manifest.json", manifest_json)
                        zp.writestr("background.js", background_js)
                    self.chrome_options.add_extension(os.path.join(file_location,file_name))
                else:
                    
                    
                    
                    ip_address=url.split(":")[2]
                    passw=url.split(":")[1]
                    port=str(url.split(":")[3])
                    user=url.split(":")[0]
                    url='https://'+user+':'+passw+'@'+ip_address+':'+port
                    options.update({'proxy':{ 'https': url}})
            else:
                ip_address,port=url.split(':')
                url='https://'+ip_address+':'+port
                options.update({'proxy':{ 'https': url}})
                
            
           
                  
         print(options)
         print(capabilities)
         executable_path=os.path.join(os.getcwd(),'assets','chromedriver.exe')
         from selenium.webdriver.chrome.service import Service
         s=Service(executable_path=executable_path)
         print('selenium_wire:'+str(selenium_wire))
         #executable_path=os.path.join(settings.BASE_DIR,'chromedriver\chromedriver.exe')##############################
         if selenium_wire:
            from seleniumwire import webdriver as selenium_wire_web_driver
            self.driver =selenium_wire_web_driver.Chrome( service=s,options=self.chrome_options,seleniumwire_options=options)
#seleniumwire_options=options,
         
         else:
        
            s=Service(executable_path=executable_path)
            self.driver =webdriver.Chrome(service=s,options=self.chrome_options)


         if use_cookies:
              cookie_path=use_cookies
              self.driver.get('https://www.google.com/')
              time.sleep(5)              
              cookies = pickle.load(open(cookie_path, "rb"))
              for cookie in cookies:
                   self.driver.add_cookie(cookie) 
         if mobile_emulation==False:
            pass
              
            
         return self.driver    
    def save_cookies(self,identifier):       
          file_name=identifier+'.pk1'
          file_path=os.path.join(os.getcwd(),file_name)
          pickle.dump(self.driver.get_cookies() , open(file_path,"wb"))
          return file_path
    def scroll(self,kind='',x=0,y=0,element=False):
        if kind=='scrollHeight':            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-600)")
        elif kind=='page_down_key':                    
            webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
        elif kind=='custom':
            self.driver.execute_script("window.scrollTo("+str(x)+", "+str(y)+")")
        elif kind=='page_up_key':
            webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
        elif element:
            webdriver.ActionChains(self.driver).move_to_element(element).perform()
        else:
             webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
    def move_slider(self,slider_xpath):
        en=self.driver.find_element_by_xpath(slider_xpath)
        move = ActionChains(self.driver)
        move.click_and_hold(en).move_by_offset(30, 0).release().perform()
        print('mved')
        time.sleep(5)
        move.click_and_hold(en).move_by_offset(60, 0).release().perform()
        print('mved')
        time.sleep(5)
        move.click_and_hold(en).move_by_offset(90, 0).release().perform()
    def send_command_key(self,key,element=False):
        try:
            if element:
                if key=='enter':
                    ActionChains(self.driver).move_to_element(element).send_keys(Keys.ENTER).perform()
                elif key=='escape':
                    ActionChains(self.driver).move_to_element(element).send_keys(Keys.ESCAPE).perform()
                elif key=='page_down':
                    ActionChains(self.driver).move_to_element(element).send_keys(Keys.PAGE_DOWN).perform()
                elif key=='arrow_down':
                    ActionChains(self.driver).move_to_element(element).send_keys(Keys.ARROW_DOWN).perform()
            else:
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        except Exception as e:
            print('Error while sending command key'+str(e))

    def find_element(self,element=None,xpath=None,css_selector=None,wait_time=1,check_method='presence',elements=False,retry=0,max_retries=1):
    
        if retry>=max_retries:
            return False
        
        if element:
            pass
        else:
            element=self.driver
        if check_method=='presence' and not elements:
            check_method=EC.presence_of_element_located
        elif check_method=='presence' and elements:
            check_method=EC.presence_of_all_elements_located
        if xpath:
            find_method=element.find_elements_by_xpath
            locator=xpath
            check=check_method((By.XPATH,xpath))
        elif css_selector:
            find_method=element.find_elements_by_css_selector
            check=check_method((By.CSS_SELECTOR,css_selector))
            locator=css_selector
        else:
            return False ##raise exception and save log
        try:
            WebDriverWait(self.driver,wait_time).until(check)
        except Exception as e:
            if 'no such window' in str(e):
                raise Exception('DriverClosed')
            
            time.sleep(3)
            retry+=1
            return self.find_element(element=element,xpath=xpath,css_selector=css_selector,wait_time=wait_time,check_method=check_method,elements=elements,retry=retry,max_retries=max_retries)
             ##return an exception save log
        else:
            res=find_method(locator)
            if not elements:
                if res:
                    res=res[0]
                else:
                    return False
        return res
    
    
    def click_element(self,element,nature='fatal'):
        try:
            ActionChains(self.driver).move_to_element(element).click().perform()
        except ElementNotInteractableException:
            if nature=='fatal':
                return ElementNotInteractableException
    def get(self,url):
        if 'http' in url or 'https' in url:
            pass
        else:
            url='https://'+url
        self.driver.get(url)

    def wait_until_page_loaded(self, wait_timeout=50, max_retries=5, **kwargs):
        """
        Waits until a web page is fully loaded and has at least one of:
        <input>, <button>, or <form>. This ensures the page is not stuck
        on a loader or blank shell, and is ready for user interaction.
        """
        from selenium.common.exceptions import WebDriverException
        import time
        import traceback

        for attempt in range(max_retries):
            print(f"\n⏳ Waiting for full page load (Attempt {attempt + 1})")

            start_time = time.time()

            # Log start
            self.reporter.report_performance(**{
                'service': 'instagram',
                'end_point': 'page_load',
                'data_point': 'start',
                'page': self.driver.current_url,
                'type': 'page_loading_start',  # ✅ Corrected from 'page_loading_started'
                'task': kwargs.get('uuid'),
                'run_id': kwargs.get('run_id'),
                'critical': False,
                'timestamp': start_time,
                'max_attempts': attempt + 1,
            })

            while time.time() - start_time < wait_timeout:
                try:
                    page_state = self.driver.execute_script("return document.readyState;")
                    if page_state != 'complete':
                        print(f"   → Waiting: readyState = {page_state}")
                        time.sleep(5)
                        continue

                    has_required_elements = self.driver.execute_script("""
                        return (
                            document.getElementsByTagName('input').length > 0 ||
                            document.getElementsByTagName('button').length > 0 ||
                           
                            document.getElementsByTagName('form').length > 0
                        );
                    """)
                    if has_required_elements:
                        end_time = time.time()
                        latency = round(end_time - start_time, 2)
                        print(f"✅ Page fully loaded in {latency} seconds with interactive elements.")

                        self.reporter.report_performance(**{
                            'service': 'instagram',
                            'end_point': 'page_load',
                            'data_point': 'page_loaded',
                            'page': self.driver.current_url,
                            'type': 'page_loaded_successfully',
                            'task': kwargs.get('uuid'),
                            'run_id': kwargs.get('run_id'),
                            'critical': False,
                            'timestamp': end_time,
                            'max_attempts': attempt + 1,
                            'latency': latency,  # ✅ Include latency
                        })
                        return

                    print("⚠️ No <input>, <button>, or <form> found — page may not be ready.")
                    time.sleep(1)

                except WebDriverException as e:
                    print(f"[!] WebDriver error: {e}")
                    time.sleep(2)

            return 
            if attempt < max_retries - 1:
                print("🔁 Page may be stuck. Refreshing...")
                self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'page_load',
                        'data_point': 'page_refresh',
                        'type': 'page_not_load',
                        'page': self.driver.current_url,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'critical': False,
                        'timestamp': time.time(),
                        'max_attempts': attempt + 1,
                    })
                try:
                    self.driver.refresh()
                    time.sleep(3)
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'page_load',
                        'data_point': 'page_refresh',
                        'type': 'page_refresh_successfully',
                        'page': self.driver.current_url,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'critical': False,
                        'timestamp': time.time(),
                        'max_attempts': attempt + 1,
                    })
                except Exception as e:
                    self.reporter.report_performance(**{
                        'service': 'instagram',
                        'end_point': 'page_load',
                        'data_point': 'page_refresh',
                        'type': 'exception_page_refresh',
                        'page': self.driver.current_url,
                        'task': kwargs.get('uuid'),
                        'run_id': kwargs.get('run_id'),
                        'critical': True,
                        'timestamp': time.time(),
                        'max_attempts': attempt + 1,
                        'string': {
                            'name': type(e).__name__,
                            'args': str(e)
                        },
                        'traceback': traceback.format_exc()
                    })
                    print(f"[!] Refresh failed: {e}")
            else:
                end_time = time.time()
                latency = round(end_time - start_time, 2)
                print("❌ All retries exhausted. Giving up.")

                self.reporter.report_performance(**{
                    'service': 'instagram',
                    'end_point': 'page_load',
                    'data_point': 'end',
                    'type': 'page_failed_to_load_after_retries',
                    'page': self.driver.current_url,
                    'task': kwargs.get('uuid'),
                    'run_id': kwargs.get('run_id'),
                    'critical': True,
                    'timestamp': end_time,
                    'max_attempts': attempt + 1,
                    'latency': latency  # ✅ Log how long it waited before failing
                })

        raise RuntimeError("Page did not load required interactive elements after retries.")
    
    def visit(self, url,**kwargs):
        """Visit URL and wait until page is fully loaded"""
        print(f"\n🌐 Visiting: {url}")
        if 'http' in url or 'https' in url:
            pass
        else:
            url='https://'+url
        self.driver.get(url)
        wait_timeout = kwargs.pop("wait_timeout", 50)
        max_retries = kwargs.pop("max_retries", 5)
        self.wait_until_page_loaded(wait_timeout=wait_timeout, max_retries=max_retries, **kwargs)
        

       

