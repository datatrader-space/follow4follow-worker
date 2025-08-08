
"""
def switch_account         if self.locator.page=='profile_page':  
            imagebin=self.device.screenshot(format='raw')
            s=Saver()
            pth=s.save_screenshot(imagebin)
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'located_profile_page','screenshot':pth,'task':self.task['uuid']
                                                })
            time.sleep(3)
            elem,_info=self.locator.locate(**{'touch_point':'get_username','notrack':True})
            if elem:
     
                if elem.text.lower().strip(' ')== kwargs.get('username').lower():
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'target_profile_is_active', 'query':kwargs.get('username'),'screenshot':pth,'task':self.task['uuid']
                                                })
                    print('matched')
                    return True
            else:
                print('username element missing')
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'switching_profile', 'query':kwargs.get('username'),'task':self.task['uuid']
                                                })
            elem,_info=self.locator.locate(**{'touch_point':'click_profile_tab','notrack':True})
            self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'find_profile_tab', 'query':kwargs.get('username'),'task':self.task['uuid']
                                                })
            if elem:
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'found_profile_tab', 'query':kwargs.get('username'),'task':self.task['uuid']
                                                })
                elem.click()
                imagebin=self.device.screenshot(format='raw')
                s=Saver()
                pth=s.save_screenshot(imagebin)
                self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'clicked_profile_tab', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                                'screenshot':pth
                                                })

                
                elem,_info=self.locator.locate(**{'touch_point':'click_account_switcher','notrack':True})
                if elem:
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'found_account_switcher', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                                'screenshot':pth
                                                })
                    elem.click()
                    imagebin=self.device.screenshot(format='raw')
                    s=Saver()
                    pth=s.save_screenshot(imagebin)
                    self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'clicked_account_switcher', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                                'screenshot':pth
                                                })
                    time.sleep(2)
                    self.locator.page='add_switch_account_page'
                    self.locator.sub_page='add_account'
                
                    if self.device(text=kwargs.get('username').lower()).exists:
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'user_already_logged_in', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                                'screenshot':pth
                                                })
                        print('profile already logged in')
                        self.device(text=kwargs.get('username').lower()).click()
                        imagebin=self.device.screenshot(format='raw')
                        s=Saver()
                        pth=s.save_screenshot(imagebin)
                        self.reporter.report_performance(**{'service':'instagram','end_point':'run_bot','data_point':'switch_account',
                                                'type':'clicked_choose_account', 'query':kwargs.get('username'),'task':self.task['uuid'],
                                                'screenshot':pth
                                                })
                        time.sleep(1)
                        self.device.press("back")
                        return True #self.switch_account(**kwargs)
                    else:
                        
                        self.stop_app()
                        
                        self.start_app()
                        return False 
                    elem,_info=self.locator.locate(**{'touch_point':'get_logged_in_accounts','notrack':True,'elements':True})
                    if elem:
                        for username in elem:
                           if username.info.get('text')==kwargs.get('username').lower():
                                self.logged_in=True
                                
                                print('profile already logged in')
                                username.click()
                                self.device.press("back")
                                time.sleep(1)
                                return self.switch_account(**kwargs)
                                
                             
                        return False """