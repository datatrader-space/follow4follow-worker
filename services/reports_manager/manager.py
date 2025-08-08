

from services.reports_manager.endpoints import EndPoints
import datetime as dt
class Manager:
    def __init__(self):
        self.task=False
        self.task_id=False
        
        self.run_id=False
        self.service=False
    def report_log(self,**kwargs):
        
            e=EndPoints()
            kwargs.update({'_end_point':'log','_data_point':kwargs.get('type')})
            e.create_output(**kwargs)
            #e.get_required_data_point(**kwargs)
    def report_performance(self,**kwargs):
        
            e=EndPoints()
            #e.create_output(**kwargs)
            from django.utils import timezone
            kwargs.update({'datetime':timezone.now()})
            kwargs.update({'object_type':'log'})
            if self.service and self.task_id and self.run_id:
                kwargs.update({'service':self.service,'task':self.task_id,'run_id':str(self.run_id)})
        
               
            if kwargs.get('task'):  
                try:
                    EndPoints.Create().create_task_output(**kwargs)
                except Exception as e:
                     EndPoints.Create().create_task_output(**{'type':'failed_to_save_report_output','output':str(kwargs)})
                from crawl.models import Task
                if not self.task:
                    task=Task.objects.all().filter(uuid=self.task_id)
                    if task:
                         self.task=task[0]
                    
            if self.task:
                self.task.refresh_from_db()
                if self.task.status=='running':
                        pass
                else:
                 
                        e.create_output(**{'service':'instagram',
                                                'task':self.task.uuid,'type':'TaskStoppedbyUser',})
                        raise Exception('TaskStopped')
    def report_unhandled_scenario(self,**kwargs):
        e=EndPoints()
        kwargs.update({'_end_point':'unhandled','_data_point':kwargs.get('type')})
        kwargs.update({'datetime':str(self.datetime)})
        e.create_output(**kwargs)
    def create(self,**kwargs):
        e=EndPoints()
        
        #e.create_output(**kwargs)
        return e.get_required_data_point(**kwargs)
        

#im""" port json
task={'end_point':'Create','data_point':'create_devices_report'}
m=Manager()
#data=m.create(**task)
"""
import pandas as pd
import matplotlib.pyplot as plt

# Sample list of dictionaries (replace with your actual data)


# Create a pandas DataFrame
df = pd.DataFrame(data)
print(list(df.columns))
# Ensure the 'timestamp' column is converted to datetime format (if necessary)
hourly_counts = df.resample('H', on='datetime')['type'].count()

# Create the graph (assuming there can be missing hours with no task runs)
plt.figure(figsize=(100, 60))  # Adjust figure size as needed
plt.bar(hourly_counts.index.hour, hourly_counts.values)  # Use bar plot for distinct counts per hour
plt.xlabel('Hour of the Day')

# Specify y-axis label for clarity
plt.ylabel('Number of Task Runs Started')

plt.title('Task Runs Started Today (2024-03-11)')
plt.xticks(range(24))  # Set x-axis ticks for all hours (0-23)
plt.grid(True)
plt.show() """