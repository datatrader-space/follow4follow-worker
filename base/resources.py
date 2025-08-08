import os
from storage_sense import Saver
from device import Device
from profiles import Profile

class SocialMediaProfile:
    def __init__(self):
        self.service = "instagram"

    def add_profile(self):
        username = input("Enter Username")

        print(username)
        print("Now opening browser, when you are done type exit")
        p = Profile()
        profile=p.get_profile(service=self.service,username=username)
        if profile:
            print('Profile already exists')
            _del=input('Do you want to delete Profile. Press Y and enter to yes, and enter to move ahead')
            if _del == 'yes':
                import shutil
                shutil.rmtree(profile['user_data_dir'])
            else:
                user_data_dir=profile['user_data_dir']
        from browser import Browser

        b = Browser()
        service = "1"
        if service == "1":
            service = "instagram"

        use_proxies = None
        print(
            "Do you want to specify proxies.If no value is provided the browser will use Local Proxy"
        )
        proxy = input("Please add Proxies. Press Enter to leave blank")
        if len(proxy) > 3:
            use_proxies = proxy
        if not user_data_dir:
            user_data_dir = os.path.join(
                os.getcwd(), "resources", "profiles", service, username, "browser"
            )
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

        b.initialize_chrome_browser(
            user_data_dir=user_data_dir, use_proxies=use_proxies, selenium_wire=True
        )
        try:
            b.get("https://ipinfo.io/")
        except Exception as e:
            print(e)
        else:
            if use_proxies:
                ip = use_proxies.split(":")[2]
                xpath = '//*[contains(text(),"' + ip + '")]'
                try:
                    b.find_element(xpath=xpath, wait_time=20)
                except Exception as e:
                    print("Proxy not loaded successfully")
                else:
                    print("Proxy Loaded succesffulyy")

        done = input(
            "When you are done Saving the Profile, press enter. To stop saving the profile type exit and press enter"
        )
        if done == "exit":
            return
        else:
            data = {
                "service": service,
                "proxy": use_proxies,
                "username": username,
                "status": "active",
                "user_data_dir": user_data_dir,
                "available": True,
            }

            data = {"data": data}
            

            
            p.create_newbie(**data)
            p.update_profiles_register()


class AndroidDevice:
    def __init__(self):
        self.serial_number = None

    def add(self):
        print("Welcome to Android Device Connector")
        print("Make sure your device has developer option configured")
        print("Make Sure that the Wireless Debugging is on")
        d = Device()
        d.serial_number = self.serial_number
        d.connect_device()
        info = d.get_device_info()
        print(d.device_info)
        d.save_device()
        usernames = []
        username = ""
        while not username == "exit":
           
                username = input(
                    " Do you want to add social media profiles as well.Press Enter to exit or type username and press enter"
                )
                if len(username)==0 or not username:
                    return
                proxy=input('Do you want to add proxy to this profile as well. Leave blank to use local device proxy.Press enter to leave blankl')
                if len(proxy) and len(proxy)>5:
                    p=Profile()
                    data=d.device_info
                    data.update({'proxy':proxy})
                else:
                    data=d.device_info
                    
                data={'service':'instagram',
                        'username':username,
                        'device':data
                        
                        }
                p.create_newbie(**{'data':data})
                p.update_profiles_register()
                print('Resource successfully added')

                    
          


class CheckProfile:
    def __init__(self):
        self.service = "instagram"

    def check_profile(self, read_from_profiles_register=False):
        username = "craftycanvasart"
        service = "instagram"
        s = Saver()
        if not read_from_profiles_register:
            s.block = {
                "address": "profiles." + service + "." + username + "",
                "file_name": "register",
            }
            s.load_resources()
            s.open_file()
            profile = s.data_frame.to_dict(orient="records")[0]
            user_data_dir = profile["user_data_dir"]
        else:
            df = s.read_profiles_register()
            row = []
            if not df.empty:
                row = df.loc[df["username"] == "craftycanvasart"]
            if len(row) > 0:
                row = row.to_dict(orient="records")[0]
                user_data_dir = row["user_data_dir"]
                user_data_dir = os.path.normpath(user_data_dir)
            else:
                user_data_dir = os.path.join(
                    os.getcwd(), "resources", "profiles", service, username, "browser"
                )
                if os.path.exists(user_data_dir):
                    print(
                        "User Data Directory Already Exists. Deleting and creating new one"
                    )
                    import shutil

                    shutil.rmtree(user_data_dir)
                    os.makedirs(user_data_dir)
        from browser import Browser

        b = Browser()
        b.initialize_chrome_browser(
            user_data_dir=user_data_dir,
            selenium_wire=True,
            use_proxies="jcamar:hurley92:154.13.200.125:29842",
        )

        data = {
            "service": service,
            "proxy": "jcamar:hurley92:154.13.200.125:298442",
            "username": username,
            "status": "active",
            "user_data_dir": user_data_dir,
            "available": True,
        }

        data = {"data": data}
        from profiles import Profile

        p = Profile()
        p.create_newbie(**data)
        p.update_profiles_register()
        stats = p.get_profiles_stats()
        print(stats.to_dict(orient="records"))
        i = input("press enter to exit")


#c = CheckProfile()
#c.check_profile()
s=SocialMediaProfile()
#s.add_profile()
a=AndroidDevice()
a.serial_number='8b41c342'
a.add()
# ['8b41c342','N7GV460108','ZY22F82FWS']
