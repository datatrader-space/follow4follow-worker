import requests
from base.request_maker import Request
from base.storage_sense import Saver

def get_ip_info(ip=None,retry=0):


    # Replace 'YOUR_API_KEY' with your actual API key from https://ipinfo.io/signup
    api_key = '00d68c84675405'
    if retry>3:
        return {}
    if not ip:
        ip_address = get_current_ip()  # Replace with the IP address you want to look up
    if not ip_address:
        return {}
    url = f"https://ipinfo.io/{ip_address}/json?token={api_key}"
    print(url)
    try:
        response = requests.get(url)
    except Exception:
        print('Error in Ip Info')
        retry+=1
        return get_ip_info(retry)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return({'country':data['country'],'city':data['city']})
        print("IP Address:", data["ip"])
        print("Hostname:", data["hostname"])
        print("City:", data["city"])
        print("Region:", data["region"])
        print("Country:", data["country"])
        print("Location:", data["loc"])
        print("Organization:", data["org"])
    else:
        print("Failed to retrieve IP information.")
def get_current_ip(session):
    api_key = 'd305d1497728d6'
    try:
        response = session.get("http://ipinfo.io/json?token="+api_key+"")
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data.get("ip")
        else:
            return "Failed to retrieve IP"
    except Exception as e:
        print( f"Error: {e}")



class MyPrivateProxy():
    def __init__(self):
        self.proxy_type='static'
        self.proxy_protocol='http'
        self.max_intra_service_proxy_sharing=3
        self.max_concurrent_threads=10
        
    def update_proxies_list(self):
        r=Request()
        r.logged_in=False
        r.initialize_request_session()
        r.service='myprivateproxy'
        r.workflow=''
        url='https://api.myprivateproxy.net/v1/fetchProxies/json/full/showLocation/showPlanId/m6muru6nxz09hmpxq9k9m1u9j943fsre'
        resp=r.make_request('fetch','full_info',url)
        _proxies=resp['data']
        proxies=[]
        for _proxy in _proxies:
            proxy={}
            for key, value in _proxy.items():
                _=key.replace('proxy_','')
                proxy.update({_:value})
            proxy.update({'url':proxy['username']+':'+proxy['password']+':'+proxy['ip']+':'+proxy['port']})
            proxy.update({'type':self.proxy_type,'proxy_protocol':self.proxy_protocol,
                                'max_intra_service_proxy_sharing':self.max_intra_service_proxy_sharing,
                                'max_concurrent_threads':self.max_concurrent_threads})
            proxies.append(proxy)
        self.proxies=proxies
    def update_proxies_register(self):
        self.update_proxies_list()
        block={'address':'proxies','file_name':'register'}
        s=Saver()
        s.block=block
        s.load_resources()
        s.open_file()
        df=s.data_frame
        records=[]
        for proxy in self.proxies:
            if df.empty:
                records.append(proxy)
            else:
                row=df.loc[df['url']==proxy['url']]
                if row.empty:
                    records.append(proxy)
                
        if records:
            block={'address':'proxies','file_name':'register','data':records}
            s=Saver()
            s.block=block
            s.load_resources()
            s.add_values_to_file(load_block=False)
class StormProxy():
    def __init__(self):
        self.proxy_type='rotating'
        self.proxy_protocol='http'
        self.max_intra_service_proxy_sharing=1
        self.max_concurrent_threads=1
        self.text=''
        self.proxies=[]
    def update_proxies_list(self):
        text=self.text
        proxies=[]
        for row in text.splitlines():
            if len(row)<5:
                continue 
            else:
                ip=row.split(':')[0]
                port=row.split(':')[1]
                proxies.append({'ip':ip,'port':port,'url':ip+':'+port,'type':self.proxy_type,'proxy_protocol':self.proxy_protocol,
                                'max_intra_service_proxy_sharing':self.max_intra_service_proxy_sharing,
                                'max_concurrent_threads':self.max_concurrent_threads
                                })
             
        self.proxies=proxies
    def update_proxies_register(self):
        self.update_proxies_list()
        block={'address':'proxies','file_name':'register'}
        s=Saver()
        s.block=block
        s.load_resources()
        s.open_file()
        df=s.data_frame
        records=[]
        for proxy in self.proxies:
            if df.empty:
                records.append(proxy)
            else:
                row=df.loc[df['url']==proxy['url']]
                if row.empty:
                    records.append(proxy)
                
        if records:
            block={'address':'proxies','file_name':'register','data':records}
            s=Saver()
            s.block=block
            s.load_resources()
            s.add_values_to_file(load_block=False)
