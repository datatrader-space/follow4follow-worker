            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'find_enter_search_text_field','screenshot':pth })
        
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'found_enter_search_text_field','screenshot':pth })
          
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'clicked_enter_search_text_field','screenshot':pth })
imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'cleared_text','screenshot':pth })
            self.device.send_keys(query)   
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'search','data_point':'make_search',
                                            'type':'sent_keys','keys':query,'screenshot':pth }) 