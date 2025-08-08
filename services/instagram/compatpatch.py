# -*- coding: utf-8 -*-
import re
import json

class ClientCompatPatch(object):
    """Utility to make entities from the private api similar to the ones
    from the public one by adding the necessary properties, and if required,
    remove any incompatible properties (to save storage space for example).
    """

    IG_IMAGE_URL_EXPR = r'/((?P<crop>[a-z])[0-9]{3}x[0-9]{3}/)'

    @classmethod
    def _generate_image_url(cls, url, size, crop):
        """
        Try to generate an IG cropped  image url.

        :param url: target url
        :param size: width/height of the image
        :param crop: 'p' or 's'
        :return:
        """
        mobj = re.search(cls.IG_IMAGE_URL_EXPR, url)
        if not mobj:
            replacement_expr = r'\g<eparam>{crop!s}{size!s}x{size!s}/'.format(
                **{'crop': crop, 'size': size})
            return re.sub(r'(?P<eparam>/e[0-9]+/)', replacement_expr, url)
        replacement_expr = '/{crop!s}{size!s}x{size!s}/'.format(
            **{'crop': mobj.group('crop') or crop, 'size': size})
        return re.sub(cls.IG_IMAGE_URL_EXPR, replacement_expr, url)

    @staticmethod
    def _drop_keys(obj, keys):
        """
        Remove the specified keys from the object.

        :param obj: target object
        :param keys: list of keys
        :return:
        """
        if not obj:
            return obj
        for k in keys:
            obj.pop(k, None)
    @staticmethod
    def _keep_keys(obj, keys):
        """
        Remove the specified keys from the object.

        :param obj: target object
        :param keys: list of keys
        :return:
        """
        if not obj:
            return obj
        for k in list(obj.keys()):
            if not k in keys:
                obj.pop(k, None)
    @classmethod
    def media(cls, media, drop_incompat_keys=True):
        """Patch a media object"""
        if 'data' in media.keys():
            media=media.get('data',{}).get('shortcode_media',{})
        media_shortcode = media.get('code') or media.get('shortcode')   # for media_info2
        media['link'] = 'https://www.instagram.com/p/{0!s}/'.format(media_shortcode)
        try:
            caption ={'text': media.get('caption') or
                       media.get('edge_media_to_caption', {}).get('edges', [{}])[0].get(
                           'node', {}).get('text')}
        except IndexError:
            # no caption - edge_media_to_caption: { edges: [] }
            caption = None
        media['rest_id']=media['id']
        
        media['caption']=caption
        media['tags'] = []
        media['filter'] = ''
        media['attribution'] = None
        media['user_has_liked'] = False
        media_user = {
            'id': media['owner']['id'],
        }
        if 'username' in media['owner']:
            media_user['username'] = media['owner']['username']
        if 'full_name' in media['owner']:
            media_user['full_name'] = media['owner']['full_name']
        if 'profile_pic_url' in media['owner']:
            media_user['profile_picture'] = media['owner']['profile_pic_url']
        media['user'] = media_user
        media['type'] = 'video' if media['is_video'] else 'image'
        display_src = media.get('display_src') or media.get('display_url')  # for media_info2
        images=[]
        images.append({
            'standard_resolution': {
                'url': display_src,
                'width': media['dimensions']['width'],
                'height': media['dimensions']['height']},
            'low_resolution': {'url': cls._generate_image_url(display_src, '320', 'p')},
            'thumbnail': {'url': cls._generate_image_url(display_src, '150', 's')},
        })
        media['images'] = images
        videos=[]
        if media['is_video'] and media.get('video_url'):
            videos.append({
                'standard_resolution': {
                    'url': media['video_url'],
                    'width': media['dimensions']['width'],
                    'height': media['dimensions']['height']},
                'low_resolution': {'url': media['video_url']},
                'low_bandwidth': {'url': media['video_url']},
            })
            media['videos'] = videos
        media['likes'] = media.get('likes', {}) or media.get('edge_liked_by', {}).get('count',0) or media.get('edge_media_preview_like', {}).get('count', 0)
            
     
        media['comments'] =media.get('comments', {}) or media.get('edge_media_to_comment', {}).get('count', 0)
            
        # Try to preserve location even if there's no lat/lng
        if 'location' not in media or not media['location']:
            media['location'] = None
        elif media.get('location', {}).get('lat') and media.get('location', {}).get('lng'):
            media['location']['lat'] = media['location']['lat']
            media['location']['lng'] = media['location']['lng']
            media['location']['name']=media['location']['name']
        media['location']=media['location']
        media['id'] = media['id']
        media['created_time'] = str(
            media.get('date', '') or media.get('taken_at_timestamp', ''))

        usertags = (
            media.get('usertags', {}).get('nodes', []) or
            [ut['node'] for ut in media.get('edge_media_to_tagged_user', {}).get('edges', [])])
        if not usertags:
            media['users_in_photo'] = []
        else:
            users_in_photo = [{
                'position': {'y': ut['y'], 'x': ut['x']},
                'user': ut['user']
            } for ut in usertags]
            media['users_in_photo'] = []

        # Try to make carousel_media for app api compat
        media['coauthor_producers']=media['coauthor_producers']
        media['clips_music_attribution_info']=media.get('clips_music_attribution_info',{})
        media['dash_info']=media.get('dash_info',{})
        media['has_audio']=media.get('has_audio',False)
        media['product_type']=media.get('product_type','')
        if media.get('edge_sidecar_to_children', {}).get('edges', []):
            carousel_media = []
            edges = media.get('edge_sidecar_to_children', {}).get('edges', [])
            for edge in edges:
                node = edge.get('node', {})
                images = {
                    'standard_resolution': {
                        'url': node['display_url'],
                        'width': node['dimensions']['width'],
                        'height': node['dimensions']['height']},
                   
                    'thumbnail': {
                        'url': cls._generate_image_url(node['display_url'], '150', 's')},
                }
                node['images'] = images
                node['type'] = 'image'
                if node.get('is_video'):
                    videos = {
                        'standard_resolution': {
                            'url': node['video_url'],
                            'width': node['dimensions']['width'],
                            'height': node['dimensions']['height']},
                        
                    }
                    node['videos'] =videos
                node['pk'] = node['id']
                node['id'] = '{0!s}_{1!s}'.format(node['id'], media['owner']['id'])
                node['original_width'] = node['dimensions']['width']
                node['original_height'] = node['dimensions']['height']
                carousel_media.append(node)
            
         
            

        if drop_incompat_keys:
            cls._keep_keys(
                                media,[
                    "id",
                    "shortcode",
                    "has_audio",
                    "video_view_count",
                    "taken_at_timestamp",
                    "location",
                    "nft_asset_info",
                    "like_and_view_counts_disabled",
                    "product_type",
                    "clips_music_attribution_info",
                    "downloaded_medias",
                    "is_video"


                    "link",
                    "rest_id",
                    "caption",
                    "filter",
                    "attribution",
                    "user_has_liked",
                    "user",
                    "type",
                    "likes",
                    "comments",
                    "created_time",
                    "users_in_photo",

                ])
                            
        return media

    @classmethod
    def comment(cls, comment, drop_incompat_keys=False):
        """Patch a comment object"""
        comment['created_time'] = str(int(comment['created_at']))
        comment_user = comment.get('user') or comment.get('owner')
        from_user = {
            'id': comment_user['id'],
            'profile_picture': comment_user.get('profile_pic_url'),
            'username': comment_user['username'],
            'full_name': comment_user.get('full_name') or ''
        }
        comment['from'] = from_user
        if drop_incompat_keys:
            cls._drop_keys(comment, ['created_at', 'user'])
        return comment
    @classmethod
    def location_section_media(cls,data,drop_incompat_keys=False):

        post={
            'caption':data.get('caption',{}),
            'thumbnails':data.get('image_versions2',{}),
            'code':data.get('code'),
            'organic_cta_info':data.get('organic_cta_info',{}),
            'preview_comments':data.get('preview_comments'),
            'top_likers':data.get('top_likers',[]),
            'timestamp':data.get('taken-at',''),
            'organic_tracking_token':data.get('organic_tracking_token'),
            'pk':data.get('pk'),
            'original_height':data.get('original_height'),
            'original_width':data.get('original_width'),
            'like_and_view_counts_disabled':data.get('like_and_view_counts_disabled',False),
            'like_count':data.get('like_count',False),
            'is_paid_partnership':data.get('is_paid_partnership',False),
            'media_type':data.get('media_type',''),
            'comment_count':data.get('comment_count',''),
            'media_cropping_info':data.get('media_cropping_info'),
            'play_count':data.get('play_count',''),
            'video_versions':data.get('video_versions'),
            'social_context':data.get('social_context'),
            'commerciality_status':data.get('commerciality_status'),
            'comment_likes_enabled':data.get('comment_likes_enabled'),
            'comment_threading_enabled':data.get('comment_threading_enabled')
        }
        user=data.get('user',{})
        location=data.get('location')
        return {'post':post,'user':user}
    @classmethod
    def location_posts(cls,data):
        posts=[]
        next_page_info={}
        data=data['data']
        page_info=data['xdt_location_get_web_info_tab']['page_info']
        if data.get('xdt_location_get_web_info_tab',{}).get('edges',[]):
            for row in data.get('xdt_location_get_web_info_tab').get('edges'):
                post=row['node']
                posts.append(post)
        return {'location_posts':posts,'next_page_info':page_info}
    @classmethod
    def search_keyword(cls,data):
        posts=[]
      
        
        page_info={"has_next_page":data['media_grid'].get("has_more"),"next_max_id":data['media_grid'].get('next_max_id')}
        if data.get('media_grid',{}).get('sections',[]):
            for row in data.get('media_grid',{}).get('sections',[]):
                for media in row.get('layout_content',{}).get('medias',[]):
                    posts.append(media['media'])
        return {'search_keyword_posts':posts,'next_page_info':page_info}
    @classmethod
    def location_sections(cls,data,tab='recent',drop_incompat_keys=False):
        zemfury=[]
        ranked_posts_next_page_info={}
        recent_posts_next_page_info={}
        sections=[]
        if data.get('native_location_data'):
            recent_section=data.get('native_location_data',{}).get('recent',None)
            ranked_section=data.get('native_location_data',{}).get('ranked',None)
            sections.append({'recent':recent_section})
            sections.append({'ranked':ranked_section})
        else:
            sections=[data]
            
        for section in sections:
            if section.get('recent'):
                _tab='recent'
                _data=section.get('recent')
            elif section.get('ranked'):
                _tab='ranked'
                _data=section.get('ranked')
            else:
                _tab=tab
                _data=data
            if _tab=='recent':

                recent_posts_next_page_info={'next_max_id':_data.get('next_max_id'),'next_page':_data.get('next_page'),'next_media_ids':_data.get('next_media_ids',[])}
                recent_posts_section=_data.get('sections')
            else:
                ranked_posts_next_page_info={'next_max_id':_data.get('next_max_id'),'next_page':_data.get('next_page'),'next_media_ids':data.get('next_media_ids',[])}
                ranked_posts_section=_data.get('sections')
           

            #**********************************************************
     
       


        medias=[]
        recents=[]
        ranked=[]
        for section in recent_posts_section:
            fill_items=  section.get('layout_content',{}).get('fill_items',[])
            one_by_two_items=section.get('layout_content',{}).get('one_by_two_item',{}).get('clips',{}).get('items',[])
            other_items=section.get('layout_content',{}).get('medias',[])
            
            for item in fill_items:
                
                medias.append(item)
            for item in one_by_two_items:
                medias.append(item)
            for item in other_items:
                print(item)
                medias.append(item)
        for media in medias:
            _=cls.location_section_media(media.get('media',{}))
            recents.append(_)
        #************************************************************
        medias=[]
        ranked_posts_section=[]
        for section in ranked_posts_section:
            fill_items=  section.get('layout_content',{}).get('fill_items',[])
            one_by_two_items=section.get('layout_content',{}).get('one_by_two_item',{}).get('clips',{}).get('items',[])
            other_items=section.get('layout_content',{}).get('medias',[])
            
            for item in fill_items:
                
                medias.append(item)
            for item in one_by_two_items:
                medias.append(item)
            for item in other_items:
                print(item)
                medias.append(item)
        for media in medias:
            _=cls.location_section_media(media.get('media',{}))
            ranked.append(_)
        location_info=data.get('native_location_data',{}).get('location_info',{})
        return {'recent_posts':recents,'recent_posts_next_page_info':recent_posts_next_page_info,
                'ranked_posts':ranked,'ranked_posts_next_page_info':ranked_posts_next_page_info,
                'location_info':location_info
                
                
                }
    @classmethod
    def user_graphql(cls, data, drop_incompat_keys=False):
        """Patch a user object"""
        
        user={
                'username':data.get('username',None),
                'name':data.get('full_name'),
                'followers_count':data.get('follower_count'),
                'followings_count':data.get('following_count'),
                'bio':data.get('biography',None),
                'post_count':data.get('media_count'),
                'external_links':data.get('bio_links'),
                'media_count':data.get('media_count',None),
                
                 'is_business_account':data.get('is_business',None),
                 'is_professional_account':data.get('is_professional_account',None),
                 'is_supervision_enabled':data.get('is_supervision_enabled',None),
                 'is_joined_recently':data.get('is_joined_recently',None),
                 'guardian_id':data.get('guardian_id',None),
                 'business_address_json':data.get('business_address_json',None),
                 'business_contact_method':data.get('business_contact_method',None),
                 "business_email":data.get("business_email",None),
                 "business_phone_number":data.get("business_phone_number",None),
                 "business_category_name": data.get("business_category_name",None),
                 "overall_category_name": data.get("overall_category_name",None),
                 "category_name":data.get("category_name",None),
                'profile_picture':data.get('profile_pic_url',None),
                
                'is_verified':data.get('is_verified',None),
                'is_official_profile':data.get('is_official',None),
                'is_private':data.get('is_private'),
                'fb_profile_bio_link_web':data.get('fb_profile_bio_link_web'),
                'external_links':data.get('external_url',[]),
                'pronouns':','.join(data.get('pronouns',[])),
                'rest_id':data.get('id'),

                'pinned_tweet_ids':','.join(data.get('pinned_tweet_ids',[])),
        }
        
        return user
    @classmethod
    def user(cls, data, drop_incompat_keys=False):
        """Patch a user object"""
        
        user={
                'username':data.get('username',None),
                'name':data.get('full_name'),
                'followers_count':data.get('edge_followed_by',{}).get('count',None),
                'followings_count':data.get('edge_follow',{}).get('count',None),
                'bio':data.get('biography',None),
                'post_count':data.get('edge_owner_to_timeline_media',{}).get('count',None),
                'media_count':data.get('media_count',None),
                'likes_count':data.get('likes_count',None),
                 'is_business_account':data.get('is_business',None),
                 'is_professional_account':data.get('is_professional_account',None),
                 'is_supervision_enabled':data.get('is_supervision_enabled',None),
                 'is_joined_recently':data.get('is_joined_recently',None),
                 'guardian_id':data.get('guardian_id',None),
                 'business_address_json':data.get('business_address_json',None),
                 'business_contact_method':data.get('business_contact_method',None),
                 "business_email":data.get("business_email",None),
                 "business_phone_number":data.get("business_phone_number",None),
                 "business_category_name": data.get("business_category_name",None),
                 "overall_category_name": data.get("overall_category_name",None),
                 "category_name":data.get("category_name",None),
                'profile_pic_url':data.get('profile_pic_url',None),
                'header_picture':data.get('header_pic',None),
                'location':data.get('location',None),
                'is_verified_profile':data.get('is_verified',None),
                'is_official_profile':data.get('is_official',None),
                'is_private':data.get('is_private'),
                'fb_profile_bio_link_web':data.get('fb_profile_bio_link_web'),
                'external_links':data.get('external_url',[]),
                'pronouns':','.join(data.get('pronouns',[])),
                'rest_id':data.get('id'),

                'pinned_tweet_ids':','.join(data.get('pinned_tweet_ids',[])),
        }
        
        return user

    @classmethod
    def list_user(cls, user, drop_incompat_keys=False):
        """Patch a user list object"""
        user['profile_picture'] = user['profile_pic_url']
        if drop_incompat_keys:
            cls._drop_keys(
                user,
                [
                    'followed_by_viewer',
                    'is_verified',
                    'profile_pic_url',
                    'requested_by_viewer',
                ]
            )
        return user
