import pandas as pd
from services.instagram.storage_sense import StorageSense
class RegisterAssistant():
    
    def __init__(self):
        self.register=pd.DataFrame()
        self.storage_sense=StorageSense()
        
    
    def sort_df_and_return_the_latest_row(self,df):
        df = df.where(pd.notnull(df), None)
        
        
        sorted_df=df.sort_values(['last_scraped_at'],ascending=False)
    
        row=sorted_df.iloc[0]
    
   
        return {'next_cursor':row.get('next_cursor') if type(row.get('next_cursor',''))==str else None,'has_next_page':row.get('has_next_page'),
                'total_pages_crawled':len(sorted_df),
                
                'id':row.get('id'),
                'name':row.get('name'),
                'slug':row.get('slug'),
                'next_max_id':row.get('next_max_id',None),
                'next_media_ids':row.get('next_media_ids',None),
                'next_page':row.get('next_page',None)
                }

    def cities_register(self,method,operation):
        from services.instagram.end_points import EndPoints
        EndPoints().location.city_directory
        if method =='get' and operation=='crawl':
            self.register = self.register.where(pd.notnull(self.register), None)
        
            sorted_df=self.register.sort_values(['last_scraped_at'])
            row=sorted_df.iloc[0]
            next_cursor=row['next_cursor']

            return {'next_cursor':row['next_cursor'] if type(row['next_cursor'])==str else None,'has_next_page':row['has_next_page'],
                    'total_pages_crawled':len(sorted_df),
                  
                    'id':row['id'],
                    'name':row['name'],
                    'slug':row['slug']
                    }

    def locations_register(self,method,operation,**kwargs):
        from services.instagram.end_points import EndPoints
        EndPoints().location.location_directory
        country_info=kwargs.get('country_info')
        country_slug=country_info.get('slug')
        city_info=kwargs.get('city_info')
        city_slug=city_info.get('slug')
        location=kwargs.get('location')
        self.storage_sense.block={'address':'location.countries.'+country_slug+'.cities.'+city_slug+'.'+location+'','file_name':'register'}
        self.storage_sense.load_block()
        self.storage_sense.open_file()
        self.register=self.storage_sense.data_frame
        if method =='get' and operation=='crawl':
            self.register = self.register.where(pd.notnull(self.register), None)   
            if self.register.empty:
                return {}    
            sorted_df=self.register.sort_values(['last_scraped_at'])
            row=sorted_df.iloc[0]
            next_cursor=row['next_cursor']

            return {'next_cursor':row['next_cursor'] if type(row['next_cursor'])==str else None,'has_next_page':row['has_next_page'],
                    'total_pages_crawled':len(sorted_df),               
                    'id':row['id'],
                    'name':row['name'],
                    'slug':row['slug']
                    }
        
    



        