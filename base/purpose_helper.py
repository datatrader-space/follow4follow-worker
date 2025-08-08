class PurposeHelper(object):
    def __init__(self):
        self.end_point='user_posts'
        self.service='instagram'
        self.data_block={}
        self.purpose='download'
        self.download_type='media' #image, video, gif, file
        self.results=[]
        self.data_point={'images':[{'standard_resolution':{'url':'pass'}}]}
    
    def help(self,search=True):
    
                #obj=get_service_object('instagram')
                #obj.get_self.data_points('end_point')
                
                parent_key=list(self.data_point.keys())[0]
                parent_key_value=self.data_point[parent_key]
                is_list=type(self.data_point[parent_key])==list
            
                if is_list:
                    if type(self.data_block[parent_key])==list:
                         for i, row in enumerate(self.data_block[parent_key]):
                            keys=row.keys()
                            for key in keys:
                                if key in list(self.data_point[parent_key][0].keys()):
                                            #print(self.data_point[parent_key][0][key])
                                            if type(self.data_point[parent_key][0][key])==str:
                                                  if search:
                                                        if self.data_point[parent_key][0][key]==row[key]:
                                                             self.results.append(self.data_block[parent_key][i])
                                                  else:
                                                    self.results.append(self.data_block[parent_key][i][key])
                                            elif type(self.data_point[parent_key][0][key])==list:
                                                 if type(self.data_block[parent_key][i][key])==list:
                                                      pass
                                                 else:
                                                      continue
                                         
                                            elif type(self.data_point[parent_key][0][key])==dict:
                                                 if type(self.data_block[parent_key][i][key])==dict:
                                                        row=self.data_block[parent_key][i][key]
                                                        for _key in list(row.keys()):
                                                            #print(list(self.data_point[parent_key][0][key].keys())[0])
                                                            if _key in list(self.data_point[parent_key][0][key].keys()):
                                                                    if search:
                                                                         if row[_key]==self.data_point[parent_key][0][key][_key]:
                                                                            self.results.append(row)
                                                                    else:
                                                                       self.results.append(row[_key])
                                                 else:
                                                      continue
                                            
                elif type(self.data_point[parent_key])==dict:
                    if type(self.data_block[parent_key])==dict:
                    
                        for key in self.data_point[parent_key].keys():

                            if key in self.data_block[parent_key].keys():
                                if type(self.data_point[parent_key][key])==dict:
                                     for key in self.data_block[parent_key][key].keys():
                                        if key in list(self.data_point[parent_key][key].keys()):
                                            return self.data_block[parent_key][key]
                                else:
                                     if search:
                                          if self.data_block[parent_key][key]==self.data_point[parent_key][key]:
                                            self.results.append(self.data_block[parent_key])#Returns the final dict in which the key was present
                                     else:
                                        self.results.append( self.data_block[parent_key][key])#Returns the final str value for the key
                                


def find_key_in_nested_json(json_data, target_key):
    """
    Recursively searches for a key in a nested JSON structure (dictionary or list).

    Args:
        json_data: The JSON data to search (dictionary or list).
        target_key: The key to find.

    Returns:
        The value associated with the key if found, otherwise None.
    """
    if isinstance(json_data, dict):
        if target_key in json_data:
            return json_data[target_key]
        for value in json_data.values():
            result = find_key_in_nested_json(value, target_key)
            if result is not None:                
                return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_key_in_nested_json(item, target_key)
            if result is not None:
                return result
    return None
def find_all_keys_with_value(json_data, target_key, target_value):
    """
    Recursively searches for all occurrences of a key with a specific value
    in a nested JSON structure (dictionary or list).

    Args:
        json_data: The JSON data to search (dictionary or list).
        target_key: The key to find.
        target_value: The value to match.

    Returns:
        A list of all occurrences of the key with the matching value.
        Returns an empty list if no matches are found.
    """
    results = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key and value == target_value:
                results.append({key:value})
            results.extend(find_all_keys_with_value(value, target_key, target_value))
    elif isinstance(json_data, list):
        for item in json_data:
            results.extend(find_all_keys_with_value(item, target_key, target_value))
    return results

data = {
    'images': [
        {
            'standard_resolution': {
                'url': 'image_url_1'
            }
        },
        {
            'standard_resolution': {
                'url': 'image_url_2'
            }
        }
    ]
}

