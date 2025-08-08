from services.instagram.compatpatch import  ClientCompatPatch
class Parser(object):
    def __init__(self):
        self.json_data={}
        self.end_point=''
        self.user_followers=[]


    def parse_request_maker_response(self,data):
        if data['status']!='success':
            return False
        return True
    def forward_to_handler(self,end_point,data):
        if self.parse_request_maker_response()=='error':
            pass
        elif self.parse_request_maker_response()=='banned':
            pass
        elif self.parse_request_maker_response()=='terminate':
            pass
        elif self.parse_request_maker_response()=='end_point_banned':
            pass
        else:
            self.parse_end_point_response()

    def parse_end_point(self,data={},bypass=True,**kwargs):  ##explain kwargs
        P={}
        if not self.parse_request_maker_response(data):
            self.forward_to_handler(self.end_point,data)
            return False,data
        users=[]
        posts=[]
        locations=[]
        data=data['data']    
        cursors={}
        if self.end_point=='user_followers':
            users=[]
            if data.get('data',{}).get('user',{}).get('edge_followed_by',{}).get('edges',[]):              
                for edge in data['data']['user']['edge_followed_by']['edges']:
                       users.append(ClientCompatPatch.user(edge['node']))
            next_cursor=data['data']['user']['edge_followed_by']['page_info']['end_cursor']
            cursors={'next_cursor':next_cursor}
            P['username']=kwargs.get('username')
        elif self.end_point=='user_info':    
            if data.get('data',{}).get('user',{}):
                user=ClientCompatPatch.user(data.get('data',{}).get('user',{}))
                posts=[]
                if data.get('data',{}).get('user',{}).get('edge_owner_to_timeline_media',{}):
                    for node in data.get('data',{}).get('user',{}).get('edge_owner_to_timeline_media',{}).get('edges',[]):
                        media = ClientCompatPatch.media(node['node'])
                        posts.append(media) 
                P['username']=kwargs.get('username')
                users=[user]
        elif self.end_point=='location':
            if self.data_point=='search_locations':
                for venue in data.get('venues',[]):
                    location={'name':venue.get('name'),'address':venue.get('address'),
                              'latitude':venue.get('latitude'),'longitude':venue.get('lng'),
                              'external_id':venue.get('external_id'),'external_id_source':venue.get('external_id_source')
                              }
                    locations.append(location)
        P.update({'users':users,'cursors':cursors,'posts':posts,'locations':locations})     
        return P       
