from base.local_csv_saver import Saver
import datetime as dt
import json
import pandas as pd

from base.storage_sense import Saver
class StorageSense(Saver):
    def __init__(self):
        super().__init__()
        self.block={}
        self.saver=Saver()
        self.page_data={}
        self.find_by={}
        self.end_point=''
        self.page_number=''
        self.spreadsheet_title='test-of-scraper-2'
        self.worksheet_title='test'
        self.folder_name='test-seo-automation'
        self.identifier=''
        self.share_with_email_addresses=[]
        self.filters= [
    {"field_name": "country", "filter_type": "equal", "value": "us"},
    {"field_name": "city", "filter_type": "like", "value": "lah"},
    {"field_name": "timestamp", "filter_type": "range", "value": ["2023-03-01", "2023-03-07"]}
]  

    def retrieve_filtered_data_from_register(self):
        self.build_query()
        return self
    def sort_data_by_specific_columns(self,columns,ascending=True):
            if type(columns)==str:
                columns=[columns]
            data=self.data_frame.sort_values(by=columns,ascending=ascending)
            data=self.data_frame.to_dict(orient='records')
            return data          
    def build_query(self):
        """Builds a dynamic query from a list of filters.

        Args:
            data: A Pandas DataFrame.
            filters: A list of filters.

        Returns:
            A Pandas DataFrame.
        """

        df = self.data_frame.copy()
        if not df.empty:
            for filter in self.filters:
                field_name = filter["field_name"]
                filter_type = filter["filter_type"]
                value = filter["value"]

                if filter_type == "equal":
                    df = df[df[field_name] == value]
                elif filter_type == "like":
                    df = df[df[field_name].str.contains(value)]
                elif filter_type == "range":
                    start_date = pd.to_datetime(value[0])
                    end_date = pd.to_datetime(value[1])
                    df = df[df[field_name].between(start_date, end_date)]

        self.df=df
        return self
    def save_data_to_google_sheet(self):
        _g=GoogleSheet()
        _g.spreadsheet_title=self.spreadsheet_title
        _g.worksheet_title=self.worksheet_title
        _g.folder_name=self.folder_name

        _g.data=self.page_data
        _g.share_with_email_addresses=self.share_with_email_addresses
        _g.initialize_connection()
        _g.initialize_google_drive_api().check_if_folder_exists().check_if_file_exists_in_active_folder().open_google_sheet().find_worksheet().update_worksheet().check_if_folder_has_been_shared_with_user()
        
#s=StorageSense()
#s.block={'service':'google','end_point':'search_results','identifier':'curd','username':'seo'}
#s.open_register().add_values_to_register()