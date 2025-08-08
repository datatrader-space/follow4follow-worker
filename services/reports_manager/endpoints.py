import os
import json
import time
from base.storage_sense import Saver
import uuid

class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
        self.resource_types=['profiles','proxies','servers','devices']

        
    def get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def create_output(self,**kwargs):
        address='performance'+'.'+kwargs.get('type')
       
        task=kwargs.get('task')
        datetime=kwargs.get('datetime')
        if datetime:
            datetime=str(datetime)
            kwargs.update({'datetime':datetime})
        if task:
            kwargs.update({'task_id':task})#'workflow':task['workflow']
        s=Saver()
        file_name=str(uuid.uuid1())
        s.block={'address':address,'file_name':file_name,'data':kwargs}
        s.load_reports()
        s.add_values_to_file(load_block=False)
    

    class error:
        def __init__(self):
            super().__init__()         
        def makedirs_error(self,**kwargs):
            print(str(kwargs))
        def run_bot_error(self,**kwargs):
            print(str(kwargs))
        def openfile_error(self,**kwargs):
            print(str(kwargs))
        def unknown_service(self,**kwargs):
            self.create_output(**kwargs)


    class log:
     
        def makedirs_success(self,**kwargs):
            print(str(kwargs))
    class developer:
        def log(self,**kwargs):
            print(str(kwargs))

    class performance:
        def resource_stock_update(self,**kwargs):
            print(str(kwargs))
        def resource_allocation_failure(self,**kwargs):
            print(str(kwargs))
        def allocated_resource(self,**kwargs):
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def task_preparation_failed(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def task_manager_register_updated(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def task_state_changed(self,**kwargs):
           if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def changed_state_of_running_task(self,**kwargs):
           if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def pushed_task_manager_register_to_google_sheets(self,**kwargs):
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def checked_recurring_task_state(self,**kwargs):
            pass
        def changed_state_of_recurring_task(self,**kwargs):
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)   
        def changed_state_of_pending_task(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)   
        def new_task_entry(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def task_run_completed(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)        
                ##Now we have saved a dump in the counter folder for data_type. The celery task will then read the dump folder and increment it.
        def task_run_started(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)      
        def task_run_failed(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)      
        def task_achieved_result(self,**kwargs):
            pass
        def task_stop_condition_satisfied(self,**kwargs):
            pass
        def task_failed_due_to_missing_resources(self,**kwargs):
            pass
        def task_failed_due_to_network_errors(self,**kwargs):
            pass
        def task_failed_due_to_webdriver_errors(self,**kwargs):
            pass
        def opened_search_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def located_profile_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def target_profile_is_active(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def switching_profile(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def find_profile_tab(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_profile_tab(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def not_found_profile_tab(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_profile_tab(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_account_switcher(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_account_switcher(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def user_already_logged_in(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_choose_account(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def account_switched(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def no_targets_found(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def searching_and_interacting_with_user(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def pressed_enter(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def sent_keys(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def cleared_text(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs) 
        def opened_search_results_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)      
        def find_search_text_field(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_enter_search_text_field(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_search_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def get_search_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def not_found_search_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def find_enter_search_text_field(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_enter_search_text_field(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def not_found_enter_search_text_field(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def search_text_field_already_filled(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_search_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def opened_explore_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def find_get_accounts_section(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_get_accounts_section(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_get_accounts_section(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def find_target_username(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_target_username(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_target_username(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_target_username(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def located_profile_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def located_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def sniffer_turned_on(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def check_profile_login_status(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def get_initialize_values_for_end_point(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def not_found_initialize_values_for_end_point(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def opened_link(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def located_home_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def located_login_page(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def sniffing_requests(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def target_request_sniffed(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def create_request_headers_from_sniffed_request(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def copied_request_headers_from_sniffed_request(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def acquired_data(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def bot_started_successfully(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def find_follow_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def found_follow_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def following_user(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def clicked_follow_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def not_found_follow_button(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def run_bot_launch_success(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def run_bot_launch_failure(self,**kwargs):
            if kwargs.get('task'):  
                kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
                kwargs.update({'end_point':'Create','data_point':'create_task_output'})
                self.internal_get_required_data_point(**kwargs) 
                kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
                self.internal_get_required_data_point(**kwargs)
        def created_dependent_task(self,**kwargs):
            pass
        def updated_active_workflows(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def not_unqiue_workflow_name(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def unqiue_workflow_name(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def find_dependent_nodes(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def task_created_for_job(self,**kwargs):      
            kwargs.update({'_end_point':kwargs.get('end_point'),'_data_point':kwargs.get('data_point')})
            kwargs.update({'end_point':'Create','data_point':'create_task_manager_output'})
            self.internal_get_required_data_point(**kwargs) 
            kwargs.update({'end_point':'Create','data_point':'create_counter_entry'})
            self.internal_get_required_data_point(**kwargs)
        def created_workflow(self,**kwargs):
            pass
        def created_job(self,**kwargs):
            pass
        def created_task(self,**kwargs):
            pass
        def failed_to_assign_device_to_profile(self,**kwargs):
            pass
        def removed_profile_from_device(self,**kwargs):
            pass
        def failed_to_create_workflow(self,**kwargs):
            pass
        def updated_device_in_use(self,**kwargs):
            pass
        def updated_profile_in_use(self,**kwargs):
            pass
        def updated_active_workflows(self,**kwargs):
            pass
        def find_dependent_nodes(self,**kwargs):
            pass
        def job_created_successfully(self,**kwargs):
            pass
        def job_creation_failed(self,**kwargs):
            pass
        def task_created_for_job(self,**kwargs):
            pass
        def task_creation_failed_for_job(self,**kwargs):
            pass
        def assigned_input_to_task(self,**kwargs):
            print('Assigned input to the task. This function will check if the input was assigned correctly or not')
            print('it will cross match the final task image with pre provided task images.')
            print('if it finds a mismatch, it will be trained to take actions')
            print('the actions list will be pre loaded into the system, the software will try to correct and bring the')
            print('faulty image near the right or user provided images')
            
    class unhandled:
        def unhandled_end_point(self,**kwargs):
            pass
        def unhandled_data_point(self,**kwargs):
            pass

    class Instagaram:
        
        def create_run_log_report(self, **kwargs):
            """
            Creates a structured report dictionary from summarized run log.
            This version works with the nested summary structure.
            """
            import uuid
            from base.storage_sense import Saver
            from analysis import summarize_run_log_folder # Assuming summarize_run_log_folder is in 'analysis.py'

            task = kwargs
            s = Saver()

            # Summarize logs
            summary = summarize_run_log_folder(task, report_creation_task_uuid=kwargs.get('uuid'))

            report_data_dict = {
                "report_start_datetime" : summary.get('start_datetime'),
                "report_end_datetime": summary.get('end_datetime'),
                "run_id" : summary.get('run_id'),
                "task_id": summary.get('task_id'),
                "service": summary.get('service'),
                "end_point": summary.get('end_point'),
                "data_point": summary.get('data_point'),
                "total_logs": summary.get("total_logs"),
                "critical_events_count": len(summary.get("critical_events", [])),
                "critical_events_summary": summary.get("critical_events"),
                "attempt_failed_errors" : summary.get('attempt_failed_errors'),
                "total_run_time_of_this_instance": summary.get('total_run_time_of_this_instance'),
                "total_run_time_seconds": summary.get('total_run_time_seconds'),
                "exception": summary.get('exception'),
                "specific_exception_reason": summary.get('specific_exception_reason'),
                "has_billing_exception": summary.get('has_billing_exception'),
                "bot_username": summary.get('bot_username'),
                "last_log_details": summary.get('last_log_details'),
                "task_completion_status": summary.get('task_completion_status'),
                "bot_login_status_for_run": summary.get('bot_login_status_for_run'),
                "scraped_data_summary": summary.get('scraped_data_summary'),
                "found_next_page_info_count": summary.get('found_next_page_info_count'),
                "next_page_info_not_found_count": summary.get('next_page_info_not_found_count'),
                "saved_file_count": summary.get('saved_file_count'),
                "downloaded_file_count": summary.get('downloaded_file_count'),
                "failed_to_download_file_count": summary.get('failed_to_download_file_count'),
                "storage_house_upload_failures":summary.get('storage_house_failure'),
                 "storage_house_uploads":summary.get('storage_house_uploads'),

                "failed_downloads_details": summary.get('failed_downloads_details'),
                "error_details": summary.get('error_details')
            }
           
            # Handle login summary
            login_summary = summary.get("login_summary", {})
            report_data_dict.update({
                "total_login_attempts": login_summary.get("total_login_attempts"),
                "successful_logins": login_summary.get("successful_logins"),
                "total_login_time": login_summary.get("total_login_time"),
                "failed_logins": login_summary.get("total_failed_logins"),
                "2fa_attempts": login_summary.get("2fa_attempts"),
                "2fa_successes": login_summary.get("2fa_successes"),
                "2fa_failures": login_summary.get("2fa_failures"),
                "2fa_total_time": login_summary.get("2fa_total_time"),
                "login_exceptions_summary": login_summary.get("login_exceptions"),
                "login_exceptions_count": len(login_summary.get("login_exceptions", [])),
                "total_attempt_failed": login_summary.get('total_failed_attempts', 0)
            })

            # Initialize page_load_details with existing page load data
            page_load_details = summary.get("page_load_summary", {})

            # Nest page_detection_details and locate_element_xpaths under their respective pages
            for page_url, page_data in summary.get("page_detection_details", {}).items():
                page_load_details.setdefault(page_url, {})["page_detection_details"] = page_data.get("xpaths", {})
                # Also add page-specific exceptions for detection if desired
                if page_data.get("exceptions"):
                    page_load_details[page_url].setdefault("page_detection_exceptions", []).extend(page_data["exceptions"])


            for page_url, page_data in summary.get("locate_element_xpaths", {}).items():
                page_load_details.setdefault(page_url, {})["locate_element_xpaths"] = page_data.get("xpaths", {})
                # Also add page-specific exceptions for locate if desired
                if page_data.get("exceptions"):
                    page_load_details[page_url].setdefault("locate_element_exceptions", []).extend(page_data["exceptions"])


            report_data_dict["page_load_details"] = page_load_details
            
            # Global exceptions for page detection and locate element
            report_data_dict["page_detection_exceptions_summary"] = summary.get("page_detection_exceptions", [])
            report_data_dict["page_detection_exceptions_count"] = len(summary.get("page_detection_exceptions", []))

            report_data_dict["locate_element_exceptions_summary"] = summary.get("locate_element_exceptions", [])
            report_data_dict["locate_element_exceptions_count"] = len(summary.get("locate_element_exceptions", []))

            # Save the report
            s.file_extension='.json'
            s.create_task_outputs(
                id=kwargs.get('uuid'),
                block_name='reports',
                file_name='task_analysis_report__' + str(uuid.uuid4()),
                data=report_data_dict
            )


        

       

        
        def create_run_report(self,**kwargs):
            task=kwargs
         
                
            from base.storage_sense import Saver
            import pandas as pd
            s=Saver()
            from analysis import analyze_task
            flattened_report=analyze_task(task,report_creation_task_uuid=kwargs.get('uuid'))  
            import json

            from crawl.models import TaskAnalysisReport
            import datetime

            # Example of how you'd create and save an instance
            # You'd get 'flattened_report' from my output.
            # For datetimes, ensure they are correctly parsed from string to datetime objects

            report_start_dt = None
            if flattened_report["Report Start Datetime"] != "N/A":
                report_start_dt = datetime.datetime.fromisoformat(flattened_report["Report Start Datetime"]).timestamp()
                report_start_dt = datetime.datetime.fromtimestamp(report_start_dt , tz=datetime.timezone.utc).isoformat()

            report_end_dt = None
            if flattened_report["Report End Datetime"] != "N/A":
                report_end_dt = datetime.datetime.fromisoformat(flattened_report["Report End Datetime"]).timestamp()
                report_end_dt = datetime.datetime.fromtimestamp(report_end_dt , tz=datetime.timezone.utc).isoformat()

                report_data_dict = {
                "overall_task_status": flattened_report["Overall Task Status"],
                "report_start_datetime": report_start_dt,
                "report_end_datetime": report_end_dt,
                "total_task_runtime_text": flattened_report["Total Task Runtime (Text)"],
                "total_task_runtime_seconds": flattened_report["Total Task Runtime (Seconds)"],
                "runs_initiated": flattened_report["Runs Initiated"],
                "runs_completed": flattened_report["Runs Completed"],
                "runs_failed_exception": flattened_report["Runs Failed (Exception)"],
                "runs_incomplete": flattened_report["Runs Incomplete"],
                "found_next_page_info_count": flattened_report["Found Next Page Info Count"],
                "next_page_info_not_found_count": flattened_report["Next Page Info Not Found Count"],
                "saved_file_count": flattened_report["Saved File Count"],
                "downloaded_file_count": flattened_report["Downloaded File Count"],
                "failed_download_count": flattened_report["Failed Download Count"],
                "overall_bot_login_status": flattened_report["Overall Bot Login Status"],
                "last_status_of_task": flattened_report["Last Status of Task"],
                "billing_issue_resolution_status": flattened_report["Billing Issue Resolution Status"],
                "non_fatal_errors_summary": flattened_report["Non-Fatal Errors Summary"],
                "exceptions_summary": flattened_report["Exceptions Summary"],
                "specific_exception_reasons": flattened_report["Specific Exception Reasons"],
                "failed_downloads_summary": flattened_report["Failed Downloads Summary"],
                "data_enrichment_summary":flattened_report["Data Enrichment Summary"],
                "scraped_data_summary":flattened_report["Scraped Data Summary"]
            }
                
                s.create_task_outputs(id=kwargs.get('uuid'),block_name='reports',file_name='task_analysis_report__'+str(uuid.uuid4()),data=report_data_dict)
                
                    #scraped_data = {k: v for k, v in flattened_report.items() if k.startswith(('Total ', 'Pages ', 'Comments '))}
                    #new_report.scraped_data_summary = scraped_data

                    # For TextField storing JSON string:
                    # scraped_data_json = {k: v for k, v in flattened_report.items() if k.startswith(('Total ', 'Pages ', 'Comments '))}
                    # new_report.scraped_data_summary_json = json.dumps(scraped_data_json)


                  # This would save the record to your database       


    class Create:
        def create_task_output(self,**kwargs):
            s=Saver()
            file_name=str(uuid.uuid1())
            task=kwargs.get('task')
            if kwargs.get('run_id',False):
                address='tasks.'+str(task)+'.outputs.logs.'+str(kwargs.get('run_id'))
            else:
                address='tasks.'+str(task)+'.outputs.logs'
            s.block={'address':address,'file_name':kwargs.get('type')+'__'+file_name,'data':kwargs}
            s.load_deep_stuff()
            s.add_values_to_file(load_block=False)
        def create_task_manager_output(self,**kwargs):
            s=Saver()
            file_name=str(uuid.uuid1())
            task=kwargs.get('task')
            s.block={'address':'output.managers.task','file_name':kwargs.get('_data_point')+'__'+file_name,'data':[{}]}
            s.load_reports()
            s.add_values_to_file(load_block=False)
        def create_counter_entry(self,**kwargs):
            s=Saver()
            s.block={'address':'counters.'+kwargs.get('_data_point')+'','file_name':str(uuid.uuid1())}
            s.load_reports()
            s.add_values_to_file(load_block=False)
        def create_performance_report(self,**kwargs):
            data=[]
            for ep in [kwargs.get('eps')]:
                from base.storage_sense import Saver
                s=Saver()
                s.block={'address':'performance.'+ep+''}
                s.load_reports()
                
                for i,report in enumerate(os.listdir(s.block_address)):
                   print(i)
                   if i>5000:
                       break
                   s.block={'address':'performance.'+ep+'','file_name':report.split('.json')[0]}
                   s.load_reports()
                   s.open_file()

                   data.append(s.data_frame.to_dict(orient='records')[0])
                   
                return data
            
        def create_task_report(self,**kwargs):
            from base.storage_sense import Saver
            s=Saver()
            if kwargs.get('add_data',{}).get('task','18cb815d-a6a0-11ef-89b3-047c1611323a'):
                task=kwargs.get('add_data',{}).get('task','')
            else:
                task=None

            logs=s.get_logs_for_task(task=task)
            print(logs)
            if kwargs.get('add_data'):
                add_data=kwargs.get('add_data')
                if add_data.get('save_to_googlesheet'):
                    for key,value in logs.items():
                        s.push_data_frame_to_google_sheet(**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1HFuOOcZFngcgCkaljPablTMwE3uvmk8Z1man3C-g7Cs/edit?gid=0#gid=0',
                                                                    'worksheet_name':key,
                                                                    'data':value,
                                                                    'update':False
                                                                    
                                                                    })
        def create_devices_report(self,**kwargs):
            import glob
            import datetime as dt
            import pandas as pd
            log_dir = os.path.join(os.getcwd(), 'reports','performance')
            device_log_files = glob.glob(os.path.join(log_dir, '*device*'))

            data = []
            counter=0
            for root, dirs, files in os.walk(log_dir):
                for dir in dirs:
                    if 'device' in dir:
                        device_dir = os.path.join(root, dir)
                        for file in glob.glob(os.path.join(device_dir, '*.json')):
                            with open(file, 'r') as f:
                                log_data = json.load(f)
                                 
                                for log_entry in log_data:
                                    if dir == 'device_connected_successfully':
                                        if counter<9:
                                            log_entry['type']='device_conected_successfully'
                                        
                                    #log_entry['file_path'] = file
                                    log_entry['file_creation_time'] = os.path.getctime(file)
                                    log_entry['timestamp'] = dt.datetime.fromtimestamp(log_entry['file_creation_time']).strftime('%Y-%m-%d %H:%M:%S')
                                    if 'reason' in log_entry:
                                        log_entry['add_info'] = log_entry['reason']['args'][0]
                                        del log_entry['reason']
                                    data.append(log_entry)


            df = pd.DataFrame(data)
            from base.storage_sense import Saver
            s=Saver()
            s.block={'address':'devices','file_name':'test','data':data}
            s.load_reports()
            s.overwrite=False
            s.add_values_to_file(load_block=False)
            import pandas as pd
            from datetime import datetime

            # Assuming the data is in a list of dictionaries
            

            # Group by device and sort by timestamp
            from crawl.models import DeviceReport
            df_grouped = df.groupby(['device'],)
            data={'devices':[{'device':''}]}
            group_by_device=df_grouped #First Create Device Groups. i.e Group together by serial number.
            
            for device in group_by_device.groups: #Iterate through the device. Serial Number
                
                device_group_df=group_by_device.get_group(device) # #
                 #Now Group the current device or group w.r.t to type
                
                
                device_logs_grouped_by_service=device_group_df.groupby('service')
                for service in device_logs_grouped_by_service.groups:
                    d=DeviceReport.objects.all().filter(serial_number=device).filter(service='')
                    if len(d)>0:
                        d=d[0]
                    else:
                        d=DeviceReport()
                        d.service=service
                    d.serial_number=device
                    service_df=device_logs_grouped_by_service.get_group(service)
                    task_groups=service_df.groupby('task')
                    tasks=[]
                    for task in task_groups.groups:
                        _={}
                        task_df=task_groups.get_group(task)
                        task_df.sort_values(by=['timestamp'],ascending=True)
                        for index,row in task_df.iterrows():
                            if index==0:
                                if 'success' in row['type']:
                                    _['status']='success'
                                    _['timestamp']=row['timestamp']
                                elif 'fail' in row['type']:
                                    _['status']='failed'
                                    _['timestamp']=row['timestamp']
                                elif 'release' in row['type']:
                                    _status='success'
                                    _['timestamp']=row['timestamp']
                                _['task']=row['task']
                                tasks.append(_)
                            dt_object = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")

# Format the datetime object
                            formatted_timestamp = dt_object.strftime("%A, %B %d, %Y, %H:%M:%S")
                            
                            print(row['task'],row['type'],formatted_timestamp)
                            dicto={'device_serial_number':{'connection_metrics':{'successful_connections_in_last_24hours':30,'failed_tasks_in_last_24hours':40,'failure_reasons':{'device_offline':30}},
                                    'current_data':{'status':'off','disconnected_since':'thursday'},
                                    'usage_by_service':{'instagram':{'total_active_hours':30,'average_task_duration':'5m','total_task_runs':30,
                                                                        'last_usage_date_time':'thursday','last_reported_date_time':'thursday',
                                                                        'successfull_tasks_in_last_1h':'20','failed_tasks_in_last_1h':20
                                                                        }},
                                    'history':{'connected_on':'March 2025'}                                                 
                                    },                     
                           }
                    tasks_df=pd.DataFrame(tasks)
                    tasks_df.sort_values(by=['timestamp'])
                    last_task_connection_status=tasks_df.iloc[0].to_dict()                   
                    if last_task_connection_status['status']=='success':
                        d.service=service
                        d.current_state='Online'
                        d.last_usage_datetime=last_task_connection_status['timestamp']
                        if d.disconnected_since:
                            d.disconnected_since=None
                        d.last_used_by_task=last_task_connection_status['task']
                            
                    else:
                        d.current_state='Offline'
                        if d.disconnected_since:
                            pass
                        else:
                            failure_rows = task_df[task_df['status'] == 'failed']
                            failure_rows.sort_values(by='timestamp',ascending=True)
                            disconnected_since=failure_rows.to_dict()['timestamp']
                            task_df.sort_values(ascending=True,by='timestamp')
                            d.disconnected_since=disconnected_since
                        d.last_report_time=last_task_connection_status['timestamp']
                        d.save()
                    d.save()
            failure_count=devices_group_grouped_by_log_type.groupby('device_connection_failure')
            s.push_data_frame_to_google_sheet(df,**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1UASGdm1W-lAPER9ppFq1E7Fg-PVKzUX-Y7uncPbaRL8/edit?gid=1629488551#gid=1629488551','worksheet_name':'test'})
            # Determine the latest state by 'type' for each device
            df_latest_state = df_grouped.groupby('device').first()[['type']]

            # Merge the latest state with the original DataFrame
            df_with_latest_state = df.merge(df_latest_state, on='device')

            # Analyze the data and create a final DataFrame
            final_df = df_with_latest_state.groupby('device').agg({
                'type': 'first',  # Latest state
                'timestamp': 'first',  # Last task start or device connected time
                'timestamp': 'last',  # Last task stop time
                'add_info': 'value_counts',  # Frequent errors
                'service': 'value_counts',  # Service usage count
                'task': 'count',  # Total tasks
                'device': 'count'  # Count of devices
            })

            # Flatten the multi-index
            final_df = final_df.reset_index()

            # Rename columns for clarity
            final_df.columns = ['Device', 'Latest State', 'Last Task Start', 'Last Task Stop', 'Frequent Errors', 'Service Usage', 'Total Tasks', 'Device Count']

            print(final_df)
            s.push_data_frame_to_google_sheet(df,**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1UASGdm1W-lAPER9ppFq1E7Fg-PVKzUX-Y7uncPbaRL8/edit?gid=1629488551#gid=1629488551','worksheet_name':'test'})
            report={}
            from base.storage_sense import Saver
            s=Saver()
            from crawl.models import Device
            d=Device.objects.all()
            for device in Device.objects.all():
                report.update({device.serial_number:{'logs':[]}})
                active_dict=report[device.serial_number]
                profiles=device.profiles.all() 
                interactions=0
                logs=[]
                for profile in profiles:
                    from crawl.models import Task
                    tasks= Task.objects.all().filter(os='android').filter(profile=profile.username)
                    from base.storage_sense import Saver
                    for task in tasks:
                        s=Saver()
                        _logs=s.get_logs_for_task(task=task.uuid)
                        if _logs.get(task.uuid):

                            logs.extend(_logs.get(task.uuid))
                            print(logs)
                            active_dict['logs'].extend(_logs.get(task.uuid))

            if kwargs.get('add_data'):
                add_data=kwargs.get('add_data')
                if add_data.get('save_to_googlesheet'):
                    for key,value in report.items():
                        s.push_data_frame_to_google_sheet(**{'spreadsheet_url':add_data.get('spreadsheet_url'),
                                                                    'worksheet_name':key,
                                                                    'data':value['logs'],
                                                                    'update':False
                                                                    
                                                                    })
        def create_hourly_report(self,**kwargs):
            import pandas as pd
            from base.storage_sense import Saver
            s=Saver()
            from pathlib import Path
            import datetime as dt
            s.block={'address':'performance.reports'}
            s.load_reports()
            paths = sorted(Path(s.block_address).iterdir(), key=os.path.getctime,reverse=True)   
            modification_times = [dt.datetime.fromtimestamp(os.path.getmtime(path)) for path in paths]     
            if len(modification_times)==0:
                pass
            elif (dt.datetime.now()-modification_times[0]).total_seconds()<600:
                print('Last Report time not greate than 60s')
                return False
            
            

            reports_dict={'task_manager':['task_run_started','task_run_failed','task_run_completed','bot_started_successfully','run_bot_launch_success','run_bot_launch_failure'],
                    'login':['failed_login','user_already_logged_in','switching_profile','target_profile_is_active','account_switched'],
                    'sniffing':['target_request_sniffed','create_request_headers_from_sniffed_request','acquired_data','crawl_count_incremented','saving_user_info',
                                'saving_location_posts'],
                    'activity':['not_found_follow_button','clicked_follow_button','located_home_page','located_login_page']
                    
                    
                    
                    }
            
            for report_type,logs_type in reports_dict.items(): 
                reports=[{}]
                for l_type in logs_type:

                    count=0
                    s.block={'address':'performance.'+l_type}     
                    s.load_reports()
                    paths = sorted(Path(s.block_address).iterdir(), key=os.path.getctime,reverse=True)
                
                    modification_times = [dt.datetime.fromtimestamp(os.path.getmtime(path)) for path in paths]
                
                    count = sum(1 for _ in modification_times if (dt.datetime.now() - _).total_seconds() <= 3600 * 48)
                    reports[0].update({l_type:count})
                
        
                    import pandas as pd
                    df=pd.DataFrame(data=reports)

                    from base.googlesheets import GoogleSheet
                    from base.google_api import GoogleAPI
                    g=GoogleSheet()
                    g.initialize_google_drive_api()
                    g.initialize_connection()
                    g.folder_name='gary_automates'
                    g.spreadsheet_title='hourly_report'
                    worksheet=report_type
                    g.check_if_folder_exists()
                    g.check_if_file_exists_in_active_folder()
                    g.open_google_sheet()
                    g.data=df
                    df.fillna(0,inplace=True)
                    g.find_worksheet(worksheet).update_worksheet(drop_duplicates=False)
                    file_id=g.active_file['id']
                    print(g.spreadsheet.url)
            _g=GoogleAPI()

            _g.service_account_from_dict()
            _g.share_with_user(**{'email_address':'hamza@northrays.com','type':'user','role':'writer','msg':'Your Hourly Report for Gary Autoamtes','id':file_id})
            return True