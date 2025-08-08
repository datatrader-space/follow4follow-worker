from base.storage_sense import Saver
import pandas as pd
import datetime as dt
import os
import uuid
class Profile(Saver):
    
    def __init__(self):
        super().__init__()
    
    def create_profile_request_dump(self,data):
        file_name=str(uuid.uuid1())
        self.block={'address':'profiles.dump','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False)
        self.block={'address':'profiles.records','file_name':file_name,'data':data}
        self.load_resources()
        self.add_values_to_file(load_block=False) 
    def update_profiles_request_register(self):
        self.block={'address':'profiles.dump'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        time_start=dt.datetime.now()
        for i,record in enumerate(records):
            self.block={'address':'profiles.dump','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            row=self.data_frame.to_dict(orient='records')[0]
            records_.append(row)
            os.remove(self.file_path)
        if records:
            self.block={'address':'profiles','file_name':'requests_register','data':records_}
            self.load_resources()
            self.add_values_to_file(load_block=False)
    def read_browser_profiles_request_register(self):        
        self.block={'address':'profiles','file_name':'requests_register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame
        if df.empty:
            return {},{}
        service_groups=df.groupby(['service'])
        df.loc[:, 'time_elapsed_in_hours']=df['timestamp'].apply(self.calculate_time_elapsed)   
        output={}
        min_output={}
        time_record=[]
        service_groups=df.groupby(['service'])
        for service in service_groups.groups:
            service_grouped_df=service_groups.get_group(service)
            bot_groups=service_grouped_df.groupby(['bot_username'])
            min_output.update({service:[]})
            for bot in bot_groups.groups:
                bot_grouped_df=bot_groups.get_group(bot)
                time_record_groups=bot_grouped_df.groupby(['time_elapsed_in_hours'])
                for i in range(0,48):
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
                min_output[service].append({bot:{'time_record':time_record,'time_record_stats':time_record_stats,'total':len(service_grouped_df)}})
    
        time_record=[]
        for service in service_groups.groups:
            output.update({service:[]})
        
            service_grouped_df=service_groups.get_group(service)
            bot_groups=service_grouped_df.groupby(['bot_username'])
        
            for bot_index,bot in enumerate(bot_groups.groups):
                bot_grouped_df=bot_groups.get_group(bot)
                end_point_groups=bot_grouped_df.groupby(['end_point'])
                output[service].append({bot:[]})
            
                for end_point_index,end_point in enumerate(end_point_groups.groups):
                    output[service][bot_index][bot].append({end_point:{}})
                    end_point_grouped_df=end_point_groups.get_group(end_point)
                    data_point_groups=end_point_grouped_df.groupby(['data_point'])
                    for data_point in data_point_groups.groups:
                        output[service][bot_index][bot][end_point_index][end_point].update({data_point:{}})
                        data_point_grouped_df=data_point_groups.get_group(data_point)
                        status_code_groups=data_point_grouped_df.groupby(['status_code'])
                        for status_code in status_code_groups.groups:
                            status_code_grouped_df=status_code_groups.get_group(status_code)
                            output[service][bot_index][bot][end_point_index][end_point][data_point].update({status_code:{'total':len(status_code_grouped_df)}})

                            time_elapsed_groups=status_code_grouped_df.groupby(['time_elapsed_in_hours'])
                            time_record=[]
                            for i in range(0,49):
                                if i in time_elapsed_groups.groups:
                                        time_elapsed_grouped_df=time_elapsed_groups.get_group(i)
                                        time_record.append({i:len(time_elapsed_grouped_df)})
                                else:
                                    time_record.append({i:0})                          
                                output[service][bot_index][bot][end_point_index][end_point][data_point][status_code].update({'time_record':time_record})
                            
                            
                            time_record_stats={}

                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,24)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,30)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,36)})
                            time_record_stats.update({'24h':self.get_workrecord_in_last_n_hours(time_record,42)})
                            time_record_stats.update({'12h':self.get_workrecord_in_last_n_hours(time_record,12)})
                            time_record_stats.update({'1h':self.get_workrecord_in_last_n_hours(time_record,1)})
                            time_record_stats.update({'6h':self.get_workrecord_in_last_n_hours(time_record,6)})
                            output[service][bot_index][bot][end_point_index][end_point][data_point][status_code].update({'time_record_stats':time_record_stats})
        return min_output,output
    def add_newbies_to_register(self):
        self.block={'address':'profiles.newbies'}
        self.load_resources()
        records=os.listdir(self.block_address)
        records_=[]
        for i,record in enumerate(records):
            self.block={'address':'profiles.newbies','file_name':record.split('.')[0]}
            self.load_resources()       
            self.open_file()
            file_path=self.file_path
            if self.data_frame.empty:
                continue
            row=self.data_frame.to_dict(orient='records')[0]
            profile=self.get_profile(row['service'],row['username'])
            if profile:
                profile.update(row)
                self.delete_profile(service=row['service'],username=row['username'])
            else:
                profile=row
            records_.append(profile)
            try:
                os.remove(file_path)
            except Exception as e:
                print(e)
                print('Failed to remove file. Add report here')

        if records_:
            self.block={'address':'profiles','file_name':'register','data':records_}
            self.load_resources()
            self.add_values_to_file(load_block=False)
    def get_profile(self,service,username):
        df=self.read_profiles_register()
        if df.empty:
            return False
        row=df.loc[df['service']==service]

        if len(row)>0:
            row=df.loc[df['username']==username]
            if len(row)>0:
                return row.to_dict(orient='records')[0]
        return False
    def delete_profile(self,service,username):
        df=self.read_profiles_register()
        row=df.loc[df['service']==service]

        if len(row)>0:
            row=df.loc[df['username']==username]
            if len(row)>0:
                df.drop(row.index,inplace=True)
                self.block={'address':'profiles','file_name':'register','data':df.to_dict(orient='records')}
                self.load_resources()
                self.overwrite=True
                self.add_values_to_file(load_block=False)
                return True
        return False
    def create_newbie(self,**kwargs):

        data=kwargs.get('data')      
        file_name=data.get('username')
        file_name=file_name.replace('.',',')
        print(file_name)
        self.block = {
            "address": "profiles.newbies",
            "file_name":file_name,
            "data": data,
        }
        self.overwrite=True
        self.load_resources()
        
        self.add_values_to_file(load_block=False)
        self.overwrite=False
        
    def read_profiles_register(self):
        block={'address':'profiles','file_name':'register'}
        self.block=block
        self.load_resources()
        self.open_file()
 
        return self.data_frame
    def update_profiles_register(self):    
        self.add_newbies_to_register()
        self.block={'address':'profiles','file_name':'register'}
        self.load_resources()
        self.open_file()
        df=self.data_frame     
        self.block={'address':'profiles.allocated'}
        self.load_resources()
        a_s=[]
        """ for r in os.listdir(self.block_address):
            self.block={'address':'profiles.allocated','file_name':r.split('.')[0]}
            self.load_resources()       
            self.open_file()
            _row=self.data_frame.to_dict(orient='records')[0]
            row=df.loc[df['username']==_row['username']]
            row.update(_row)
        self.block={'address':'profiles.deallocated'}
        self.load_resources()
        a_s=[]
        for r in os.listdir(self.block_address):
            self.block={'address':'profiles.deallocated','file_name':r.split('.')[0]}
            self.load_resources()       
            self.open_file()
            _row=self.data_frame.to_dict(orient='records')[0]
            row=df.loc[df['username']==row['username']]
            row.update(_row) """
        """ self.block={'address':'profiles','file_name':'register','data':df.to_dict(orient='records')}
        self.load_resources()
        self.overwrite=True
        self.add_values_to_file(load_block=False) """
    def get_profiles_stats(self,service='instagram',username=None):
        block={'address':'profiles','file_name':'settings'}
        self.block=block
        self.load_resources()
        pth=os.path.join(self.block_address,'settings.json')
        import json
        _settings=open(pth,'r')
        
        settings=json.loads(_settings.read())
        _settings.close()
        min_output,output=self.read_browser_profiles_request_register()

        profiles_df=self.read_profiles_register()
        if username:
            profiles_df= profiles_df.loc[profiles_df["username"] == username]
            if profiles_df.empty:
                return False

        good_bots=[]
        exclude_usernames=[]
        if min_output and output:           
            exclude_usernames=[]
            for _bot in min_output[service]:
                for key,value in _bot.items():
                    username=key
                    bot=_bot[username]
                    right_record=0
                    t_tests=0
                    time_record_stats=bot['time_record_stats']
                    for key, value in time_record_stats.items():
                        if key in settings[service]:
                            t_tests+=1
                            if value > settings[service][key]:
                                pass
                                #print('max requests exceeded for '+str(key))
                            else:
                                right_record+=1
                                #print('good bot for'+str(key))
            
                    #print('Goodness level is '+str(right_record))
                    #print('ideal level is' +str(t_tests))
                    row=profiles_df.loc[(profiles_df['username']==username) & (profiles_df['available']==True)]
                
                    if not row.empty:
                        good_bots.append(row.to_dict(orient='records')[0] )
                    else:
                        exclude_usernames.append(username)
        df=pd.DataFrame(good_bots)
        if df.empty:
            v=[]
        
            v=list(set(profiles_df['username'])-set(exclude_usernames))
            #print(v)
        else:
            v=list(set(profiles_df['username'])-set(df['username']))
        idle_bots=[]
        for bot in v:
        
            buka=profiles_df.loc[(profiles_df['username']==bot) & profiles_df['available']==True]
            if len(buka)>0:
                buka=buka.to_dict(orient='records')[0]
                good_bots.insert(0,buka)
        df=pd.DataFrame(good_bots)
        return df
    def get_profiles_stats_by_device(self,service):
        devices=[]
        usage_counter=[]
        df=self.read_profiles_register()
        
        service_groups=df.groupby(['service'])
        for service in service_groups.groups:
            service_grouped_df=service_groups.get_group(service)
          
            device_groups=service_grouped_df.groupby(['device_serial_number'])
            for device in device_groups.groups:
                    device_df=device_groups.get_group(device)
                    devices.append(device)
                    usage_counter.append(len(device_df))
        _df=pd.DataFrame()
        _df.insert(0,'device_serial_number',devices)
        _df.insert(1,'usage_count_by_service',usage_counter)
        return _df
                

            

