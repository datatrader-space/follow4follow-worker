import logging
import os
from base.storage_sense import Saver
class Recursion(object):
    def __init__(self):
        self.crawler=None
        self.session_id='1231245'
        self.saver=Saver()
        self.scraped_so_far=0
        self.not_fine=0
        self.service=''
        self.next_cursors=[]
    def recursive_api_caller(self,move='forward',end_point=None,username=None,rest_id=None,parent_tweet_id=None,next_cursor=None,max_scrape_count=None,scraped_so_far=0,not_fine=0,query=None,query_url=None,query_type=None):
            if username:
                self.username=username
            self.end_point=end_point
            if end_point=='user_info':
                data=self.crawler.user_info(**{'username':username})
            if end_point=='user_followers':
                data=self.crawler.user_followers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            if end_point=='list_followers':
                data=self.crawler.list_followers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point=='followings':
                data=self.crawler.user_followings(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'user_feed':
                data=self.crawler.user_feed(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'trends':
                data=self.crawler.trends(**{'next_cursor':next_cursor,'query':query,'query_type':'Top','query_url':query_url,'query_type':query_type})
            elif end_point == 'media_info':
                data=self.crawler.media_info(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'media_likers':
                data=self.crawler.media_likers(**{'next_cursor':next_cursor,'rest_id':rest_id,'username':username})
            elif end_point == 'place':
                data=self.crawler.place(**{'query':query,'query_url':query_url})
            elif end_point=='lists':
                data=self.crawler.lists(**{'query':query,'query_url':query_url})
        
            next_cursor=self.next_recursion_status(end_point,data,username)
            if next_cursor:
                return self.recursive_api_caller(end_point=end_point,next_cursor=next_cursor,username=username,rest_id=rest_id,parent_tweet_id=parent_tweet_id,query=query,query_url=query_url,query_type=query_type, scraped_so_far=scraped_so_far,max_scrape_count=max_scrape_count,not_fine=not_fine) 
    def next_recursion_status(self,end_point,data,username):
            resp=self.handle_parsed_response(end_point,data,username)
            if resp.get('cursor',False):
                return resp.get('cursor')
            
            else:
                return False
    def handle_parsed_response(self,end_point,data,username):        
        users=data.get('users',[])
        tweets=data.get('tweets',[])
        posts=data.get('posts',[])
        comments=data.get('comments',[])
        parent_tweet=data.get('parent_tweet')
        lists=data.get('lists',[])
        comments_scraped=0
        users_scraped=0
        tweets_scraped=0  
        posts_scraped=0     
        if parent_tweet:
            self.parent_tweet=parent_tweet
            if not parent_tweet_id:
                parent_tweet_id=data.get('parent_tweet')[0]['rest_id']
        print('Ttotal Tweets Scraped in Currt Iter.'+str(len(tweets)))
        s=Saver()
        if end_point=='user_followers':
            s.overwrite=False
            s.sectioned_data={'data':users,'username':data.get('username'),'service':self.service,'end_point':end_point}
            s.save()
        for u in users:
            s.overwrite=True
            s.sectioned_data={'data':u,'end_point':'user_info','service':self.service,'username':u.get('username')}
            s.save()  
        for p in posts:
            s.overwrite=False
            s.sectioned_data={'data':p,'end_point':'user_posts','service':self.service,'username':data.get('username'),'identifier':p['rest_id']}
            s.save()  



        cursors=data.get('cursors',[])
        next_cursor=self.acquire_next_cursor(cursors)

        return {'data':data,'cursor':next_cursor}       
    def acquire_next_cursor(self,cursors):
        next_cursor=None
        if len(cursors)<1:
            self.not_fine+=1  
        
        if cursors.get('next_cursor',None):
            next_cursor=cursors.get('next_cursor')
            
        elif cursors.get('previous_cursor,None'):
            previous_cursor=cursors.get('previous_cursor')     
        print(self.scraped_so_far)
        if self.crawler.max_scrape_count:
            if self.scraped_so_far>self.crawler.max_scrape_count:                
                return False
        if next_cursor:             
            if next_cursor in self.next_cursors:               
                self.not_fine+=1
            else:
                print('new cursor')
                self.next_cursors.append(next_cursor)
                self.not_fine=0
        return next_cursor

    
        
"""   self.crawler.users.append(user)                
            if end_point=='followers':                
                _d={'follower_of':username,'followed_by':user['username']}
            if end_point=='followings':
                _d={'follower_of':user['username'],'followed_by':username}
            if end_point == 'media_info':
                _c={'comment_by':user['username']}
            if end_point =='user_feed':
                pass
            if _d:
                self.crawler.follow_relations.append(_d)
                  if end_point=='user_followers': 
            scraped_so_far+=users_scraped     
        if end_point=='media_likers': 
            scraped_so_far+=users_scraped            
        # _d={'follower_of':username,'followed_by':user['username']}
        if end_point=='user_followings':
            scraped_so_far+=users_scraped
            #_d={'follower_of':user['username'],'followed_by':username}
        if end_point == 'media_info':
            scraped_so_far+=comments_scraped
        
        if end_point =='user_feed':
            scraped_so_far+=tweets_scraped
            pass     
                  
                   
                    
                     
                   
  t_lists=[]
        for list in lists:                
                t_lists.append(list)
                #self.saver.t_lists.append(list)            
        _tweets=[]
        for tweet in tweets:
            _tweets.append(tweet)
            tweets_scraped+=1              
            #self.saver.feed_tweets.append(tweet)  
        _posts=[]
        for post in posts:
            _posts.append(post)
            posts_scraped+=1
            #self.saver.posts.append(post)      
        _comments=[]
        for comment in comments:
            _comments.append(comment)
            comments_scraped+=1
            #self.saver.comments.append(comment)           
        users=[i for n, i in enumerate(users) if i not in users[n + 1:]]
        _users=[]      
        for user in users:  
            users_scraped+=1
            _users.append(user)
        data={'users':_users,'tweets':_tweets,'posts':_posts,'locations':[],'lists':t_lists,'comments':_comments}  
        s=Saver()
        s.sectioned_data=_user    """