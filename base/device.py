import uiautomator2 as u2
from uiautomator2 import Direction
from base.storage_sense import Saver
import json
import random
import time
class Device():
    def __init__(self):
       self.serial_number=''
       self.proxy=''
       self.service=''
       self.app_package=''
       self.ip_address=''
    def connect_device(self):
        try:
        
            device=u2.connect(self.serial_number,)
            self.device=device
            self.device_info=device.device_info
            self.device_info.update({'serial_number':self.device_info['serial']})
            """ self.device_info['display']=json.dumps(self.device_info.get('display',{}))
            self.device_info['memory']=json.dumps(self.device_info['memory'])
            self.device_info['battery']=json.dumps(self.device_info['battery'])
            self.device_info['cpu']=json.dumps(self.device_info['cpu']) """
            self.device_info.pop('serial',None)
        except Exception as e:
            print(e)
            if 'offline' in str(e):
                print('Device is Offline')
                raise Exception('DeviceOffline')
        return self
    def get_device_info(self):
        if self.device:
            self.device_info={'brand':self.device_info.get('brand'),'android_version':self.device_info.get('version'),'serial':self.device_info.get('serial'),
                         'model':self.device_info.get('model'),'sdk':self.device_info.get('sdk'),'health':self.device_info.get('health'),
                         'ram':self.device_info.get('memory',{}).get('around',''),'cpu':self.device_info.get('cpu',{}).get('cores'),
                          'battery_health':self.device_info.get('battery',{}).get('health',''),'battery_level':self.device_info.get('battery',{}).get('level','')                
                         }
        else:
            raise Exception("NoDeviceFoundException")
    def is_battery_optimum(self):
        if self.device_info.get('battery_level')>15:
           return True
        else:
            return  False
    def unlock_screen(self):
        self.device.unlock()
        return self
    def start_app(self):   
        self.device.app_start(self.app_package,use_monkey=True)
        return self
    def stop_app(self):
        self.device.app_stop(self.app_package)
        return self
    def list_all_apps(self,keyword=None):
        print(self.device.app_list('instagram'))
        return self
    def get_device(self,serial):
        s=Saver()
        s.block={
            'address':'devices',
            'file_name':'register',
           
        }
        s.load_resources()
        df=s.data_frame
        if df.empty:
            return False
        else:
            row=df.loc[df['serial']==serial]
            if row>0:
                print('Device Already Added')
            else:
                return False
    def save_device(self,device_name):
        s=Saver()

        
        if self.get_device(self.device_info['serial']):
            print('Device Already Added')
        else:
            data={'name':device_name}
            data.update(self.device_info)
            s.block={
            'address':'devices',
            'file_name':'register',
            'data':data
                    }
            s.load_resources()
            s.add_values_to_file()
    def create_dump(self):
        
        s=Saver()
        s.file_extension='.html'
        s.block={'address':'','file_name':'tmp','data':self.device.dump_hierarchy()}
        s.load_resources()
        
        s.open_file()
        print('dump saved to '+str(s.file_path))
        s.write_data_block_to_file()
    def swipe(self):
        y1=random.randint(50,300)
        y2=random.randint(250,300)
        wait=random.uniform(0,0.1)
        print(y1,y2,wait)
        d.device.swipe(300,300,300,y2,wait)


""" d=Device()
d.serial_number='NMNA0A0351'
d.connect_device()
for i in range(0,100):
    #d.device.drag(300,600,300,800,0)
    #d.device.drag(300,100,100,20000,0)
    y1=random.randint(250,800)
    y2=random.randint(0,50)
    wait=random.uniform(0,0.2)
    print(y1,y2,wait)
    d.device.swipe(300,y1,300,y2,wait)

    
    time.sleep(random.randint(1,3))
d.device.screen_on()
d.device.screen_on()   """