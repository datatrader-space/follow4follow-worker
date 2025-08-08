import uuid
import os
from base.storage_sense import Saver
import pandas as pd
class Device:
    def __init__(self):
        pass
    def get_device_by(self,**kwargs):
        df=self.read_devices_register()
        if df.empty:
            return []
        df=df.loc[df['serial_number']==kwargs.get('serial_number')]
        if len(df)>0:
            return df
    def read_devices_register(self):
        from base.storage_sense import Saver
        s=Saver()
        s.block={'address':'devices','file_name':'register'}
        s.load_resources()
        s.open_file()
        return s.data_frame
    def update_devices_register(self,**kwargs):
        s=Saver()
        s.block={'address':'devices.dump','file_name':'register'}
        s.load_resources()
        updates=[]
        
        for update in os.listdir(s.block_address):       
            s.block={'address':s.block_address,'file_name':update.split('.')[0]}
            s.open_file()
            data=s.data_frame.to_dict(orient='records')[0]
            print(os.path.getmtime(s.file_path))
            data.update({'last_status_update_time':os.path.getmtime(s.file_path)})
            updates.append(data)
            os.remove(s.file_path)
        df=self.read_devices_register()
        register_dict=df.to_dict(orient='records')
        updates=pd.DataFrame(updates)
        if updates.empty:
            return
        updates_grouped_by_derial=updates.groupby('serial_number')##Group all the rows in update data by device serial number       
        for serial_number in updates_grouped_by_derial.groups:#Go through all the 
            row={}
            
            device_updates=updates_grouped_by_derial.get_group(serial_number)
            if not df.empty:

                row=df.loc[df['serial_number']==serial_number]
                if len(row)>0:
                    for index,row in row.iterrows():
                    
                        row=row.to_dict()
                        for ind,_ in enumerate(register_dict):
                            if _['serial_number']==serial_number:
                                register_dict.pop(ind)
                        
                else:
                    row={}
           
            device_updates.sort_values(by=['last_status_update_time'],inplace=True)
            for i,device_update in device_updates.iterrows():
                    device_update.dropna(inplace=True)
                 
                    row.update(device_update.to_dict())
            register_dict.append(row)

        
            
        s.block={'address':'devices','file_name':'register','data':register_dict}
        s.overwrite=True
        s.load_resources()
        s.add_values_to_file(load_block=False)

    def add_profile_to_device(self,**kwargs):
        device=self.get_device_by(**kwargs)
        service=kwargs.get('profile',{})['service']
        if device.empty:
            print('Add report here')
        else:
            device=device.to_dict(orient='records')[0]
        profiles=device.get(service,False)
        if profiles:
            profiles=profiles.split(',')
        else:
            profiles=[]
        if kwargs.get('profile',{}).get('username') in profiles:
            return
        profiles.append(kwargs.get('profile',{}).get('username'))
        device[service]=','.join(profiles)
        kwargs.update({'device':device})
        self.create_newbie_device(**kwargs)
        self.update_devices_register()
    def remove_profile_from_device(self,**kwargs):
        device=self.get_device_by(**kwargs)
        service=kwargs.get('profile',{})['service']
        if device.empty:
            print('Add report here')
        else:
            device=device.to_dict(orient='records')[0]
        profiles=device.get(service,False)
        if profiles:
            profiles=profiles.split(',')
        else:
            profiles=[]
        if kwargs.get('profile',{}).get('username') in profiles:
            profiles.remove(kwargs.get('profile',{}).get('username'))
      
        device[service]=','.join(profiles)
        kwargs.update({'device':device})
        self.create_newbie_device(**kwargs)
        self.update_devices_register()

    def create_newbie_device(self,**kwargs):
        file_name=str(uuid.uuid1()) 
        s=Saver()
        s.block={'address':'devices.dump','file_name':file_name,'data':kwargs.get('device')}
        s.load_resources()
        s.add_values_to_file(load_block=False)
    def update_device_info(self,**kwargs):
        from base.device import Device
        dv=Device()
        dv.serial_number=kwargs.get('serial_number')
        try:
            dv.connect_device()
        except Exception as e:
            kwargs.update({'device':{'serial_number':kwargs.get('serial_number'),'status':'offline'},})
            self.create_newbie_device(**kwargs)
            print('Device Offline. Failed to Connect. Not registering')
            return

        if dv.device_info:
            print(dv.device_info)
        device=dv.device_info
        device.update({'status':'online'})
        kwargs.update({'device':dv.device_info})
        self.create_newbie_device(**kwargs)

        self.ensure_device_integrity()   
    def ensure_device_integrity(self,**kwargs):
        service='instagram'
        from services.resource_manager.profiles import Profile
        p=Profile()
        stats=self.get_profiles_attached_stats(service)
        for stat in stats:
            if stat['profiles']:
                for profile in stat['profiles']:
                    from services.resource_manager.profiles import Profile
                    p=Profile()
                    if not p.get_profile(service,username=profile):
                        self.remove_profile_from_device(**{'serial_number':stat['serial_number'],'profile':{'username':profile,'service':service}})

    def get_profiles_attached_stats(self,service):
        stats=[]
        df=self.read_devices_register()
        has_service_profiles=[]
        if not df.empty:    
            df=df.loc[df['status']=='online']
            for index,row in df.iterrows():
                if service in df.columns.values:
                    has_service_profiles=row.get(service,False)
                    if has_service_profiles:
                        has_service_profiles=has_service_profiles.split(',')
                        count_of_service_profiles_attached=len(has_service_profiles)
                    else:
                        count_of_service_profiles_attached=0

                else:
                    count_of_service_profiles_attached=0
                stats.append({'serial_number':row['serial_number'],'service_profiles_attached':count_of_service_profiles_attached,'profiles':has_service_profiles})
        return stats
        