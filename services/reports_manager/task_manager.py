w={
    'total_workflows_created':200,
    'total_tasks_ran':200,
    'failure_count':200,
    'failed_tasks':{'task1':['flow']},
    'failure_by_service':{

        '24h':{'instagram':{'count':100,'endpoints':[{'user':'10','common_reasons':['xpath_errors','unknown_errors','connection_errors','resource_allocation']}]},
                'tiktok':{'instagram':{'count':100,'endpoints':[{'user':'10','common_reasons':['xpath_errors','unknown_errors','connection_errors','resource_allocation']}]}
                          
                          }},
        '48h':{'instagram':{'count':100,'endpoints':[{'user':'10','common_reasons':['xpath_errors','unknown_errors','connection_errors','resource_allocation']}]},
                'tiktok':{'instagram':{'count':100,'endpoints':[{'user':'10','common_reasons':['xpath_errors','unknown_errors','connection_errors','resource_allocation']}]}
                          
                          }},
                
            
       
    }
}

###Lets say after 5 minutes, the report creator runs. Checks the dump for each end-point, data-point.
###Whenever a file is added or remove to the database, a dump is created, which contains the path to
##the block/file. The dumps are grouped into various categories, for example dumps related to reports
##are placed in for_report_manager, these dumps only contains the block/files that Report manager needs i.e. reports
## After adding the dumps, it runs the analyzer all together and generates a report and sends to central.



