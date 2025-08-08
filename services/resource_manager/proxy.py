import uuid
from base.storage_sense import Saver
import os
import pandas as pd
class Proxy(Saver):
    def __init__(self):
        super().__init__()
    def create_proxy_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'proxies.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        self.block={'address':'proxies.records','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
    def create_profile_request_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'profiles.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        self.block={'address':'profiles.records','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)  
    def read_proxies_register(self):
        block={'address':'proxies','file_name':'register'}
        self.block=block
        self.load_resources()
        self.open_file()
        return self.data_frame
    def get_proxy(self,url):
        block={'address':'proxies','file_name':'register'}
        self.block=block
        self.load_resources()
        self.open_file()
        return self.data_frame[self.data_frame['url']==url]

    def update_proxies_register(self):
        block={'address':'resources.proxies.dump'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        for i,record in enumerate(records):
            self.block={'address':'resources.proxies.dump','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            row=self.data_frame.to_dict(orient='records')[0]
            records_.append(row)
            os.remove(self.file_path)
        self.block={'address':'resources.proxies','file_name':'register','data':records_}
        self.load_resources()
        self.add_values_to_file(load_block=False)
    def read_proxies_requests_register(self):
  
        self.block={'address':'proxies','file_name':'requests_register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame
        df.loc[:, 'time_elapsed_in_hours']=df['timestamp'].apply(self.calculate_time_elapsed)
        proxy_groups=df.groupby(['proxy'])
        output={}
        min_output={}
        time_record=[]
        for proxy in proxy_groups.groups:
            proxy_grouped_df=proxy_groups.get_group(proxy)
            service_groups=proxy_grouped_df.groupby(['service'])
            output.update({proxy:{}})
            for service in service_groups.groups:
                service_grouped_df=service_groups.get_group(service)
                time_record_groups=service_grouped_df.groupby(['time_elapsed_in_hours'])
                for i in range(0,24):
                    if i in time_record_groups.groups:

                            time_elapsed_grouped_df=time_record_groups.get_group(i)
                            time_record.append({i:len(time_elapsed_grouped_df)})
                    else:
                        time_record.append({i:0}) 
                time_record_stats={}
                time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,24)})
                time_record_stats.update({'30h':self.get_workrecord_in_last_n_hours(time_record,30)})
                time_record_stats.update({'36h':self.get_workrecord_in_last_n_hours(time_record,36)})
                time_record_stats.update({'42h':self.get_workrecord_in_last_n_hours(time_record,42)})
                time_record_stats.update({'12h':self.get_workrecord_in_last_n_hours(time_record,12)})
                time_record_stats.update({'1h':self.get_workrecord_in_last_n_hours(time_record,1)})
                time_record_stats.update({'6h':self.get_workrecord_in_last_n_hours(time_record,6)})
                min_output.update({proxy:{service:{'time_record':time_record,'time_record_stats':time_record_stats,'total':len(service_grouped_df)}}})
        #print(min_output)
        for proxy in proxy_groups.groups:
            proxy_grouped_df=proxy_groups.get_group(proxy)
            service_groups=proxy_grouped_df.groupby(['service'])
            output.update({proxy:{}})
            for service in service_groups.groups:        
                service_grouped_df=service_groups.get_group(service)
                output[proxy].update({service:[],'total':len(service_grouped_df)})
                end_point_groups=service_grouped_df.groupby(['end_point'])
                for end_point_index,end_point in enumerate(end_point_groups.groups):
                    output[proxy][service].append({end_point:{}})
                    end_point_grouped_df=end_point_groups.get_group(end_point)
                    data_point_groups=end_point_grouped_df.groupby(['data_point'])
                    for data_point in data_point_groups.groups:
                        output[proxy][service][end_point_index][end_point].update({data_point:{}})
                        data_point_grouped_df=data_point_groups.get_group(data_point)
                        status_code_groups=data_point_grouped_df.groupby(['status_code'])
                        for status_code in status_code_groups.groups:
                            status_code_grouped_df=status_code_groups.get_group(status_code)
                            output[proxy][service][end_point_index][end_point][data_point].update({status_code:{'total':len(status_code_grouped_df)}})
                            time_elapsed_groups=status_code_grouped_df.groupby(['time_elapsed_in_hours'])
                            time_record=[]
                            for i in range(0,24):
                                if i in time_elapsed_groups.groups:

                                        time_elapsed_grouped_df=time_elapsed_groups.get_group(i)
                                        time_record.append({i:len(time_elapsed_grouped_df)})
                                else:
                                    time_record.append({i:0})                          
                                output[proxy][service][end_point_index][end_point][data_point][status_code].update({'time_record':time_record})
        return min_output,output
    def get_proxies_stats(self,service='instagram',task={}):
        block={'address':'proxies','file_name':'settings'}
        self.block=block
        self.load_resources()
        pth=os.path.join(self.block_address,'settings.json')
        import json
        _settings=open(pth,'r')
        
        settings=json.loads(_settings.read())
        _settings.close()
        
       
        min_output,output=self.read_proxies_requests_register()
        proxies_df=self.read_proxies_register()
        output_stats={}
        exclude_proxies=[]
        for key, value in settings.items():
            output_stats.update({key:[]})
        for key, value in min_output.items():
            proxy_url=key
            proxy_record=min_output[proxy_url]

            for service,_settings in settings.items():
                right_record=0
                t_tests=0
                service_proxy_record=proxy_record.get(service,{})
                time_record_stats=service_proxy_record.get('time_record_stats',{})
                for key, value in time_record_stats.items():
                    if key in _settings:
                        t_tests+=1
                        if value > _settings[key]:
                            pass
                            #print('max requests exceeded for '+str(key))
                        else:
                            right_record+=1
                if t_tests==0:
                    ratio=0
                else:
                
                    ratio=right_record/t_tests

                
                if ratio==0 or ratio ==1 or ratio>0.5:
                    row=proxies_df.loc[proxies_df['url']==proxy_url]  
                    if row.empty:
                        pass
                    else:
                        
                        output_stats[service].append(row.to_dict(orient='records')[0])
                        exclude_proxies.append(proxy_url)
        intersect=list(set(proxies_df['url'])-set(exclude_proxies))
      
        self.block={'address':'workflows','file_name':'register'}
        self.load_deep_stuff()
        self.open_file()
        df=self.data_frame
    
     
        for proxy_url in intersect:
            row=proxies_df.loc[proxies_df['url']==proxy_url]
            if not row.empty:
                for key,value in output_stats.items():
                    
                    if not type(row)==dict:
                        row=row.to_dict(orient='records')[0]
                    usage_counter=self.get_proxy_usage_stats(df,row['url'],service) 
                    row.update({'usage_counter':usage_counter})
                    output_stats[key].append(row)
                   
                    

        return output_stats
    def get_proxy_usage_stats_by_task_state_type(self,df,proxy_url,service):
        usage_counter=0 
        if df.empty:
            return usage_counter
        df=df.loc[(df['status']=='running') | (df['status']=='pending') ]
        for index,row in df.iterrows():
            task=row['task']
            if task['service']==service:
                if task.get('resources'):
                    resources=task.get('resources')
                    if resources.get('proxy',False):
                        proxy=resources.get('proxy')
                        if proxy.get('url')==proxy_url:
                            print('Found One active Usage for proxy')
                            usage_counter+=1
        return usage_counter
    def get_proxy_usage_stats_by(self,**kwargs):
        proxies=self.read_proxies_register()      
        if proxies.empty:
            return {}
        from services.resource_manager.profiles import Profile       
        __=[]
        p=Profile()
        df=p.read_profiles_register()
        for i,proxy in proxies.iterrows():
            if kwargs.get('service')=='instagram':
                proxy_url=kwargs.get('proxy_url')
                service=kwargs.get('service')             
               
                if not df.empty:
                    _=df.loc[(df['proxy']==proxy['url']) & (df['service']==service)]
                    __.append(len(_))   
                else:
                    __.append(0)            
        proxies.insert(0,'usage_count_by_service',__)
        proxies.sort_values(by=['usage_count_by_service'],ascending=False,inplace=True)
        return proxies
        

