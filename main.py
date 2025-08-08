import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerserver.settings')
django.setup()
#import deep_stuff.workflow_creator
#import services.extractor.run_bot
#import services.open_web.run_bot
#from services.reports_manager.endpoints import EndPoints
#e=EndPoints()
#e.Instagaram().create_run_report(**{'uuid':'cc523176-31ad-11f0-92b6-047c1611323a','data_point':'location_posts','end_point':'location'})
#import services.instagram.run_bot
#import services.instagram.device.run_bot
#import services.tiktok.run_bot
#import services.twitter.run_bot
#import services.threads.run_bot
#import base.proxy_utils
#import services.resource_manager.manager
#import services.openai.run_bot
#import services.data_enricher.run_bot
#import services.audience.run_bot
# import services.datahouse.run_bot
# import services.cleaner.run_bot
import services.task_manager.manager
#import services.resource_manager.proxy
#import base.device
#import services.proxy.device.run_bot
#import base.google_api
#import base.manager_testing
#import services.reports_manager.manager
#from services.bing.run_bot import Bing
#import services.twitter.run_bot 
#from base.downloader import Downloader
#from services.deepseek import run_bot

#e=EndPoints().GoogleForms().create_google_form_api()
#import services.instagram.testo 

#from services.instagram.usabe_funcs_for_business_no_bs import get_single_user_info_with_browser
#get_single_user_info_with_browser(username='smiirl',task={'add_data':{'use_proxies':'f2wSTy0:8CR2Iiyr2lbfM72:us4.4g.iproyal.com:7488'},'uuid':'59d6e5ab-29ad-11f0-a96c-b81ea4842696'})