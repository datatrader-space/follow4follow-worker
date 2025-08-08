


class EndPoints:
    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''
  
    def get_value_of_attribute(self,end_point,data_point):
        from xpaths import Xpaths
        x=Xpaths()
        endpoint=getattr(x, end_point)
        datapoint=getattr(endpoint,data_point)
        return (datapoint(endpoint))
    def create_json_rep_of_xpaths(self):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        j_rep={'pages':[]}
        pages=j_rep['pages']
        xpaths=[]
        import inspect
        from xpaths import Xpaths
        x=Xpaths()
        
        members = [attr for attr in dir(x) if callable(getattr(x, attr)) and not attr.startswith("__")]
        for member in members:
            xx=getattr(x,member)
            print(xx)
            

            members__ = [attr for attr in dir(xx) if callable(getattr(xx, attr)) and not attr.startswith("__")]
            pages.append({'name':member,'xpaths':members__})
            for member__ in members__:
                cld_m__=''.join(ch for ch in member__ if ch.isalnum())
                xpaths.append(member__+'.'+member)
           
        print(xpaths)
        return {'xpaths':xpaths,'pages':j_rep}
    def find_nearest_neighbor(self):
        data=self.create_json_rep_of_xpaths()
        sub='profile_button'
        #sub=''.join(ch for ch in sub if ch.isalnum())
        x=list(s for s in data['xpaths'] if sub in s)
        return x[0]
    def internal_get_required_data_point(self,**kwargs):
        getattr()
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)

    class location:
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
        

        
    class hashtag():
        def __init__(self):
            super().__init__()
        

    class user():
        
        def __init__(self):
            super().__init__()
            self.storage_sense=Saver()  
            self.register_assistant=RegisterAssistant()
        
e=EndPoints()
e.get_value_of_attribute('Navigation','get_profile_button')