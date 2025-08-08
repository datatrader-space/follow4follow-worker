from services.instagram.compatpatch import  ClientCompatPatch
import json
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
        resp=self.parse_request_maker_response(data)
        if resp=='error':
            pass
        elif resp=='banned':
            pass
        elif resp=='terminate':
            pass
        elif resp=='end_point_banned':
            pass
        else:
            self.parse_end_point_response()

    def parse_end_point(self,data={},bypass=True,**kwargs):  ##explain kwargs
        P={}
        if not self.parse_request_maker_response(data):
            #self.forward_to_handler(self.end_point,data)
            return False
        users=[]
        posts=[]
        locations=[]
        countries=[]
        city_directory={}
        location_directory={}
        location_info={}
        data=data['data']   
        recent_posts=[]
        recent_posts_next_page_info={}
        ranked_posts=[]
        ranked_posts_next_page_info={} 
        next_page_info={}
        nextos=[]
        location_posts=[]
        search_keyword_posts=[]
        
        if self.end_point=='user':
            if self.data_point=='user_info_graphql':
                user=ClientCompatPatch.user_graphql(data.get('data').get('user'))
                users=[user]
            if self.data_point=='user_info':    
                if data.get('data',{}).get('user',{}):
                    user=ClientCompatPatch.user(data.get('data').get('user'))
                    posts=[]
                    if data.get('data',{}).get('user',{}).get('edge_owner_to_timeline_media',{}):
                        for node in data.get('data',{}).get('user',{}).get('edge_owner_to_timeline_media',{}).get('edges',[]):
                            media =node['node']
                            
                            posts.append(media) 
                        page_info=data.get('data',{}).get('user',{}).get('edge_owner_to_timeline_media',{}).get('page_info',{})
                        next_cursor=page_info.get('end_cursor')
                        has_next_page=page_info.get('has_next_page')
                        next_page_info={'has_next_page':has_next_page,'next_cursor':next_cursor}
                    P['username']=kwargs.get('username')
                    users=[user]
            elif self.data_point=='user_posts':
                for node in data.get('data',{}).get('xdt_api__v1__feed__user_timeline_graphql_connection',{}).get('edges',{}):
                        media =node['node']
                        media.update({'shortcode':media.get('code')})
                        
                        posts.append(media) 
                page_info=data.get('data',{}).get('xdt_api__v1__feed__user_timeline_graphql_connection',{}).get('page_info',{})
                next_cursor=page_info.get('end_cursor')
                has_next_page=page_info.get('has_next_page')
                next_page_info={'has_next_page':has_next_page,'next_cursor':next_cursor}
            elif self.data_point=='user_followers1':
                users=[]
                if data.get('data',{}).get('user',{}).get('edge_followed_by',{}).get('edges',[]):              
                    for edge in data['data']['user']['edge_followed_by']['edges']:
                        users.append(ClientCompatPatch.user(edge['node']))
                next_cursor=data['data']['user']['edge_followed_by']['page_info']['end_cursor']
                has_next_page=data['data']['user']['edge_followed_by']['page_info']['has_next_page']
                next_page_info={'next_cursor':next_cursor}
                P['username']=kwargs.get('username')
            elif self.data_point=='user_followers':
                users=[]
                if data.get('users'):              
                    for edge in data.get('users'):
                        users.append(ClientCompatPatch.user(edge))
                next_max_id=data.get('next_max_id')
               
                next_page_info={'next_max_id':next_max_id}
                P['username']=kwargs.get('username')
                nextos=kwargs.get('nexto')
        elif self.end_point=='location':
            if self.data_point=='search_location':
                for venue in data.get('venues',[]):
                    location={'name':venue.get('name'),'address':venue.get('address'),
                              'latitude':venue.get('lat'),'longitude':venue.get('lng'),
                              'external_id':venue.get('external_id'),'external_id_source':venue.get('external_id_source')
                              }
                    locations.append(location)
            elif self.data_point=='country_directory':
                
                for country in data.get('country_list',[]):
                    countries.append(country)
                if data.get('next_page',''):
                    next_page_info={'next_cursor':data.get('next_page')}
                
            elif self.data_point=='city_directory':
                cities=[]
                for city in data.get('city_list',[]):
                    cities.append(city)
                if data.get('next_page',''):
                    next_page_info={'next_cursor':data.get('next_page')}
                country_info=data.get('country_info',{})
                city_directory={'cities':cities,'country_info':country_info}
            elif self.data_point=='location_directory':
                locations=[]
                for location in data.get('location_list',[]):
                    locations.append(location)
                if data.get('next_page',''):
                    next_page_info={'next_cursor':data.get('next_page')}
                country_info=data.get('country_info',{})
                city_info=data.get('city_info')
                location_directory={'locations':locations,'city_info':city_info,'country_info':country_info}
            elif self.data_point=='location_info':
                
                loc=data.get('native_location_data',{}).get('location_info',{})
                location_info={'category':loc.get('category'),'facebook_places_id':loc.get('facebook_places_id'),
                 'latitude':loc.get('lat'),'longitude':loc.get('lng'),'address':loc.get('location_address'),
                 'rest_id':loc.get('location_id'),'zip_code':loc.get('location_zip'),'name':loc.get('name'),
                 'phone_number':loc.get('phone'),'website':loc.get('website'),'location_city':loc.get('city'),
                 'schedule':json.dumps(loc.get('hours',{}).get('schedule',{})),'ig_business':loc.get('ig_business').get('profile',{}),
                   
                 }
                _=ClientCompatPatch.location_sections(data=data)
                recent_posts=_.get('recent_posts'),
                recent_posts_next_page_info=_.get('recent_posts_next_page_info')
                ranked_posts=_.get('ranked_posts'),
                ranked_posts_next_page_info=_.get('ranked_posts_next_page_info')
            

            elif self.data_point=='location_posts':
                tab=kwargs.get('tab')
                print(data)
                if not data.get('data'):
                    return False
                _=ClientCompatPatch.location_posts(data=data)
                location_posts=_.get('location_posts')
                next_page_info=_.get('next_page_info')
                ranked_posts=_.get('ranked_posts'),
                ranked_posts_next_page_info=_.get('ranked_posts_next_page_info')
                location_info=_.get('location_info')
                
                nextos=kwargs.get('nexto')
            
        elif self.end_point=='search':
            if self.data_point=='search_keyword':
                tab=kwargs.get('tab')
                _=ClientCompatPatch.search_keyword(data=data)
                search_keyword_posts=_.get('search_keyword_posts')
                next_page_info=_.get('next_page_info')
                
                
                nextos=kwargs.get('nexto')


        P.update({'users':users,'posts':posts,'locations':locations,'countries':countries,
                  'city_directory':city_directory,'location_directory':location_directory,
                  'location_info':location_info,
                  'recent_posts':recent_posts,
                  'recent_posts_next_page_info':recent_posts_next_page_info,'ranked_posts':ranked_posts,
                  'ranked_posts_next_page_info':ranked_posts_next_page_info,
                  'next_page_info': next_page_info if next_page_info else None,
                  'nextos':nextos,
                  'location_posts':location_posts,'search_keyword_posts':search_keyword_posts
                  
                  })     
        return P       
