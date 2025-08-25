
import datetime as dt
import time
import uuid
from datetime import datetime, timedelta
from typing import Tuple

#from cloud.models import EC2Instance


from django.core.cache import cache
#from tools.model import ConcurrentModificationError, LockedModel
from django.db import IntegrityError, models, transaction
from django.db.models import (Count, ExpressionWrapper, F, Max,
                              ObjectDoesNotExist, OuterRef, Q, Subquery)
from django.db.models.fields import Field
from django.db.models.signals import post_save,pre_save,post_delete
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
#from django_celery_beat.models import CrontabSchedule, IntervalSchedule

from django import forms

from typing import Tuple, Dict


SERVICES: Tuple[Tuple[str]] = (
    ('instagram', 'Instagram'),
    ('twitter','twitter'),
    ('threads','threads'),
    ('tiktok','tiktok'),
    ('facebook','facebook'),
    ('cleaner','cleaner'),
    ('reports_manager','reports_manager'),
    ('data_enricher','Data Enricher'),
    ('openai','OpenAI'),
    ('audience','Audience'),
    ('datahouse','DataHouse'),
    ('daraz','Daraz.pk')
)

class Device(models.Model):
    uuid=models.UUIDField(blank=False,null=True,unique=True)
    name=models.CharField(max_length=500,blank=False,null=False)
    serial_number=models.CharField(max_length=500,blank=False,null=False)
    info=models.JSONField(null=True,blank=True)
    is_connected=models.BooleanField(default=False)
    is_running=models.BooleanField(default=False)
    rest_period_between_same_service_tasks=models.FloatField(default=0.5,help_text='Enter Rest Period between Intra Service tasks in hours')


    def __str__(self):
        return self.serial_number

class ChildBot(models.Model):
    uuid=models.UUIDField(blank=False,null=True,unique=True)
    """Represents a bot for managing child accounts on various services."""

    display_name = models.CharField(max_length=100, null=True, blank=True)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, null=True, blank=True,related_name='profiles')

    editable_attributes = [
        'dob', 'sex', 'first_name', 'last_name', 'bio',
        'email_address', 'email_password', 'imap_email_host',
        'imap_email_username', 'imap_email_password', 'imap_email_port'
    ]

    service = models.CharField(choices=SERVICES, default='instagram', max_length=50, db_index=True)
    
    username = models.CharField(max_length=50, blank=False, null=False, db_index=True)
    password = models.CharField(max_length=50, blank=False, null=False)
    
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    proxy_url=models.CharField(blank=True,null=True,max_length=500)
    email_address = models.EmailField(max_length=254, blank=True, null=True, db_index=True)
    email_password = models.CharField(max_length=100, blank=True, null=True)
    auth_code = models.CharField(max_length=500, blank=True, null=True)
    
    recovery_email = models.EmailField(max_length=254, blank=True, null=True)
    
    imap_email_host = models.CharField(max_length=100, blank=True, null=True)
    imap_email_username = models.CharField(max_length=100, blank=True, null=True)
    imap_email_password = models.CharField(max_length=100, blank=True, null=True)
    imap_email_port = models.CharField(max_length=6, blank=True, null=True)
    
    is_challenged = models.BooleanField(default=False)

    @property
    def followers_count(self):
        return 0  # Placeholder

    @property
    def following_count(self):
        return 0  # Placeholder

    def __str__(self):
        return self.display_name or self.username
        
class Proxy(models.Model):
    uuid=models.UUIDField(blank=False,null=True,unique=True)
    LOCK_DURATION = int(0.5*3600)


    max_threads=models.IntegerField(default=1)
    proxy_url = models.CharField(max_length=500, null=True, blank=True)

    ua_string = models.CharField(max_length=5000, null=True)

    is_available = models.BooleanField(default=True)

    

    proxy_blacklisted = models.BooleanField(default=False)

   

    provider = models.CharField(max_length=1000, null=True, blank=True)

    
    tagged_bad_on = models.DateTimeField(null=True, blank=True)

    verified = models.BooleanField(default=False)

    proxy_type = models.CharField(
        max_length=20,
        choices=(
            ('static_proxy', 'Static Proxy'),
            ('rotating_proxy', "Rotating Proxy")
        ),
        default="static_proxy"
    )

    proxy_protocol = models.CharField(
        max_length=20,
        choices=(
            ("http", 'Http'),
            ("socks", 'Socks'),
            ("http_socks", 'Both')
        ),
        default='http'
    )

    class Meta:
        
        verbose_name_plural = "proxies"

    @classmethod
    def calculate_lock_duration(cls, proxy):
        import random
        if proxy.proxy_type == "rotating_proxy":
            return (random.randint(3, 5) * 60)
        return cls.LOCK_DURATION

    @classmethod
    def get_proxy_by_location(cls, location: str, **kwargs):
        """[summary]

        Args:
            location (str): [description]

        Returns:
            [type]: [description]
        """
        kwargs.update(
            {
                'proxy_blacklisted': False,
                'proxy_country': location
            }
        )
        return cls.objects.filter(
            **kwargs
        ).annotate(
            proxy_pk=F('pk')
        ).values('proxy_url', 'pk', 'proxy_pk', 'proxy_country', 'proxy_city')

    @classmethod
    def get_proxy_by_config(cls,  config: Dict[str, str]):
        """[summary]

        Args:
            customer (Customer): [description]
            config (Dict[str, str]): [description]

        Returns:
            [type]: [description]
        """
        proxy_type = config.get('type', None)
        if not proxy_type:
            return []

        query = {
            "proxy_blacklisted": False,
            "proxy_type": proxy_type,
           
        }

        location = config.get('location', None)
        if location is not None:
            query['proxy_country'] = location

        provider = config.get("provider", None)
        if provider is not None:
            query['provider'] = provider

        proxy_protocol = config.get("proxy_protocol", None)
        if proxy_protocol is not None:
            query['proxy_protocol'] = proxy_protocol

        return cls.objects.filter(
            **query
        ).annotate(
            proxy_pk=F('pk')
        ).values('proxy_url',
                 'pk',
                 'proxy_pk',
                 'proxy_country',
                 'proxy_city'
                 )

    
    def use_count(self,service):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.login_profiles.filter(service=service).count()

    @property
    def available(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        if self.is_locked():
            return False
        if not self.last_used_at:  # hasn't ran
            return True
        return (timezone.now() - self.last_used_at).total_seconds() > self.LOCK_DURATION

    def __str__(self):
        return f'{self.proxy_url}'  

    name=models.CharField(unique=True,max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else self.proxy_url if self.proxy_url else "Unnamed Proxy"

class Interaction(models.Model):
   
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        pass

    bot_username = models.CharField(max_length=500,
                            verbose_name="bot_username",
                            blank=False,
                            null=True,

                            )

    ref_id = models.CharField(
     
        verbose_name="Automation Task Id",
        blank=True,
        null=True,
        max_length=500
        
    )

    ACTIVITY_CHOICES = [
        ('dm', 'DM'),
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('watch_story','WatchStory')
    ]

    activity = models.CharField(
        blank=False,
        null=False,
        choices=ACTIVITY_CHOICES,
        max_length=500
    )

    DM_CHOICES = [
        ('reachout', 'Reach Out'),
        ('welcome', 'Welcome'),
    ]

    dm_type=models.CharField(
        blank=True,
        null=True,
        choices=DM_CHOICES,
        max_length=100
    )
    interaction_time = models.DateTimeField(
        blank=False,
        null=True,
        default=dt.datetime.now()
    )

    target_profile = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )

    target_post = models.CharField(
        blank=True,
        null=True,
        max_length=500
    )

    # Holds an Arbitrary data relating to the activity performed
    # example if the activity was a `comment` data here will represent
    # the comment that was sent to the target_post
    
    data = models.JSONField(
        blank=True,
        null=True,
        max_length=1000
    )
    screenshot=models.CharField(blank=True,null=True,unique=True,max_length=500)
    entry_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    
    def __str__(self):
        return f'{self.entry_id}'
    
    def view_screenshot(self):
        
        if self.screenshot:
            from django.utils.safestring import mark_safe
            return mark_safe(f'<a href="http://localhost/media/screenshots/'+self.screenshot+'" target="_blank" rel="noopener noreferrer">View Screenshot </a>')
           
        else:
            return ''        

class Task(models.Model):
    name=models.CharField(default='',max_length=500,blank=True,null=True)
    uuid=models.CharField(default=str(uuid.uuid1()),unique=True,max_length=50000)
    ref_id=models.CharField(max_length=5000,default=uuid,blank=True,null=True)
    service = models.CharField(choices=SERVICES,
                               default='instagram',
                               max_length=50,
                               db_index=True
                               )
    dependent_on=models.ForeignKey('self',blank=True,related_name='dependents',on_delete=models.CASCADE,null=True)
    interact=models.BooleanField(default=False)
    os=models.CharField(max_length=500,blank=True,null=True,choices=(('android','android'),('browser','browser')))
    data_point = models.CharField(blank=True,
                                null=True,
                                max_length=500
                               )
    end_point = models.CharField(blank=True,
                                null=True,
                                max_length=500
                               )
    input=models.CharField(blank=True,
                                null=True,
                                max_length=500
                               )
    targets=models.JSONField(blank=True,null=True)
    condition=models.CharField(blank=True,null=True,max_length=500) 
    profile=models.TextField(blank=True,
                          null=True)
    alloted_bots=models.TextField(blank=True,
                        null=True)
    device=models.TextField(blank=True,
                          null=True)
    targets=models.TextField(blank=True,null=True)
    add_data=models.JSONField(blank=True,null=True,default={"max_threads": 10, "datahouse_url": "", 
                                                            "datahouse_blocks": [],
                                                              "reporting_house_url": "", 
                                                              "max_requests_per_bot": "100", "max_requests_per_day": 200,
                                                                "max_requests_per_run": 5, "save_to_storage_house": True})
   
    repeat=models.BooleanField(default=False)
    repeat_duration=models.CharField(max_length=20,blank=True,null=True)
    status=models.CharField(max_length=100,default='pending',choices=(('pending','pending'),('running','running'),('failed','failed'),('completed','completed')))
    last_state_changed_at=models.FloatField(blank=True,null=True)
    report=models.BooleanField(default=False)
    retries_count=models.IntegerField(default=0)
    paused=models.BooleanField(default=False)
    success_count=models.IntegerField(default=0)
    failed_count=models.IntegerField(default=0)
    blacklisted_usernames=models.TextField(null=True,blank=True)
    consumed_usernames=models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # set once when created
    updated_at = models.DateTimeField(auto_now=True)      # updated automatically on save


    def __str__(self):
        return str(str(self.name)) 
    def clone(self):
        """
        Clones the current Task object, creating a new Task with the same 
        attributes but a different name.

        Returns:
            The newly created Task object.
        """
        exclude_keys = ['_state']
        data = {key: value for key, value in self.__dict__.items() if key not in exclude_keys}
        data['uuid']=uuid.uuid1()
        new_task = self.__class__(**data) 
        new_task.pk = None  # Remove primary key to create a new object
        new_task.name = f"{self.name} (Clone)"
        new_task.save()
        return new_task              
    def get_job_tasks(self):
        """
        Returns a QuerySet of all active tasks with the same ref_id.
        """
        return Task.objects.filter(ref_id=self.ref_id,data_point=self.data_point,end_point=self.end_point, paused=False)
    def calculate_fair_share(self):
        """
        Calculates the fair share of requests for this task within the job.

        Args:
            bot_username: The username of the bot making the request.

        Returns:
            A tuple containing:
                - The number of requests allowed for this task today.
                - The total number of requests allowed for the job today.
        """

        today_start = datetime.datetime.combine(timezone.now(), datetime.time.min)
        today_end = datetime.datetime.combine(timezone.now(), datetime.time.max)

        job_tasks = self.get_job_tasks()
        num_job_tasks = job_tasks.count()

        if num_job_tasks == 0:
            return 0, 0  # No active tasks in the job

        # Calculate the fair share of requests per task per day
        fair_share_per_task_per_day = self.add_data.get('max_requests_per_day',30) // num_job_tasks
        
        # Calculate the number of requests already made by the bot for this task today
        task_requests_today = self.requestrecord_set.filter(
            bot_username=self.profile,
            datetime__gte=today_start,
            datetime__lte=today_end
        ).count()

        # Calculate the number of requests allowed for this task today, considering fair share
        requests_allowed_for_task_today = max(fair_share_per_task_per_day - task_requests_today, 0)
        if requests_allowed_for_task_today>self.add_data.get('max_requests_per_run',15):
            requests_allowed_for_task_today=requests_allowed_for_task_today-(requests_allowed_for_task_today-self.add_data.get('max_requests_per_run',10))
        
        return requests_allowed_for_task_today

    def check_job_request_limits(self):
        """
        Checks if the job-level request limits have been exceeded.
        Pauses the task if limits are exceeded.

        Args:
            bot_username: The username of the bot making the request.

        Returns:
            True if the limits are not exceeded, False otherwise.
        """
        now_aware = timezone.now()

        today_start = now_aware.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now_aware.replace(hour=23, minute=59, second=59, microsecond=999999)

        #today_start = datetime.datetime.combine(timezone.now(), datetime.time.min)
        #today_end = datetime.datetime.combine(timezone.now(), datetime.time.max)

        # Count requests for all tasks within the job today
        job_requests_today = 0
        for task in self.get_job_tasks():
            job_requests_today += task.requestrecord_set.filter(
                bot_username=self.profile,
                datetime__gte=today_start,
                datetime__lte=today_end
            ).count()
        if self.add_data:
            if job_requests_today >= self.add_data.get('max_requests_per_day',120):
                # Pause the task if job limit is exceeded
                self.is_paused = True
                self.last_paused_at = timezone.now()  # Record the time of pausing
                self.resume_at = timezone.now() + datetime.timedelta(hours=1)  # Resume after 1 hour (adjust as needed)
                self.save()
                return False

        return True

    def check_bot_request_limits(self):
        """
        Checks if the task-level request limits have been exceeded.

        Args:
            bot_username: The username of the bot making the request.

        Returns:
            True if the limits are not exceeded, False otherwise.
        """
        now_aware = timezone.now()

        today_start = now_aware.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now_aware.replace(hour=23, minute=59, second=59, microsecond=999999)
        """ today_start = datetime.datetime.combine(timezone.now(), datetime.time.min)
        today_end = datetime.datetime.combine(timezone.now(), datetime.time.max) """
        task_requests_today_by_bot=0
        # Count requests for this task today
        for task in self.get_job_tasks():
            if task.profile==self.profile:
                task_requests_today_by_bot += task.requestrecord_set.filter(
                    bot_username=self.profile,
                    datetime__gte=today_start,
                    datetime__lte=today_end
                ).count()
       

        # Count total requests for this task by the user

        if task_requests_today_by_bot >= int(self.add_data.get('max_requests_per_bot',20)):
            return False

        

        return True
    def check_task_request_limits(self):
        if not self.add_data:
            return True
        now_aware = timezone.now()

        today_start = now_aware.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now_aware.replace(hour=23, minute=59, second=59, microsecond=999999)
        """ today_start = datetime.datetime.combine(timezone.now(), datetime.time.min)
        today_end = datetime.datetime.combine(timezone.now(), datetime.time.max) """
        job_tasks = self.get_job_tasks()
        num_job_tasks = job_tasks.count()
        fair_share_per_task_per_day = self.add_data.get('max_requests_per_day',30) // num_job_tasks
        task_requests_today=self.requestrecord_set.filter(
                    
                    datetime__gte=today_start,
                    datetime__lte=today_end,
                    data_point=self.data_point
                ).count()
        if task_requests_today>=fair_share_per_task_per_day:
            return False
        return True
    def check_request_limits(self):
        """
        Checks if the request limits for this task and all tasks within the same job have been exceeded.

        Args:
            bot_username: The username of the bot making the request.

        Returns:
            True if the limits are not exceeded, False otherwise.
        """

        return self.check_job_request_limits() and self.check_task_request_limits()


class Output(models.Model):      
        type=models.CharField(blank=True,null=True,max_length=1000)
        data=models.TextField(blank=True,null=True)
        reported_at=models.DateTimeField(blank=True,null=True)

        def __str__(self):
            return self.type
# myapp/models.py
from django.db import models
from django.contrib.postgres.fields import JSONField # If using PostgreSQL

class TaskAnalysisReport(models.Model):
    overall_task_status = models.CharField(max_length=50)
    report_start_datetime = models.DateTimeField(null=True, blank=True)
    report_end_datetime = models.DateTimeField(null=True, blank=True)
    total_task_runtime_text = models.CharField(max_length=100)
    total_task_runtime_seconds = models.FloatField()
    runs_initiated = models.IntegerField()
    runs_completed = models.IntegerField()
    runs_failed_exception = models.IntegerField()
    runs_incomplete = models.IntegerField()
    found_next_page_info_count = models.IntegerField()
    next_page_info_not_found_count = models.IntegerField()
    saved_file_count = models.IntegerField()
    downloaded_file_count = models.IntegerField()
    failed_download_count = models.IntegerField()
    overall_bot_login_status = models.CharField(max_length=50)
    last_status_of_task = models.CharField(max_length=255)
    billing_issue_resolution_status = models.CharField(max_length=255)

    # You might use JSONField for scraped data, errors, exceptions if using PostgreSQL
    # For other databases, you might store these as JSON strings in a TextField
    scraped_data_summary = models.JSONField(default=dict)
    data_enrichment_summary = models.JSONField(default=dict) # If using PostgreSQL
    # For other databases: scraped_data_summary_json = models.TextField(default='{}')

    non_fatal_errors_summary = models.TextField()
    exceptions_summary = models.TextField()
    specific_exception_reasons = models.TextField()
    failed_downloads_summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.report_start_datetime} - {self.overall_task_status}"


import datetime

class RequestRecord(models.Model):
    datetime = models.DateTimeField(blank=False, default=timezone.now)
    request_record_type = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    data_point = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    r_type = models.CharField(max_length=255)
    bot_username = models.CharField(max_length=255)
    ip_address=models.CharField(blank=True,null=True,max_length=500)
    proxy=models.CharField(blank=True,null=True,max_length=500)
    task = models.ForeignKey(Task,blank=False,null=False,on_delete=models.CASCADE)
    logged_in = models.BooleanField(default=False)
    run_id=models.UUIDField(blank=True,null=True)
    # params is set to False in the dict, so we can make it a BooleanField
    params = models.JSONField(default={},blank=True)
  # data is set to False in the dict, so we can make it a BooleanField
    payload = models.JSONField(default={},blank=True)
    text=models.TextField(blank=True,null=True)
    status_code = models.IntegerField(default=200)
    data = models.JSONField(default={},blank=True)
    error=models.JSONField(default={},blank=True)
    request_made=models.IntegerField(blank=True,null=True)
    rate_limited=models.BooleanField(default=False)
    # payload is set to null in the dict, so we can make it a JSONField
    

    def __str__(self):
        return f'RequestRecord {{timestamp: {self.datetime}, request_record_type: {self.request_record_type}, service: {self.service}, end_point: {self.end_point}, data_point: {self.data_point}, url: {self.url}, r_type: {self.r_type}, bot_username: {self.bot_username},  logged_in: {self.logged_in},  status_code: {self.status_code}}}'
class DeviceReport(models.Model):
   
    serial_number = models.CharField(max_length=20, unique=True)
    current_state = models.CharField(max_length=20)
    disconnected_since = models.DateTimeField(null=True, blank=True)
    service = models.CharField(max_length=20,choices=SERVICES)
    total_active_hours = models.IntegerField()
    average_task_duration = models.IntegerField()
    total_tasks_run = models.IntegerField()
    last_usage_datetime = models.DateTimeField()
    last_report_time = models.DateTimeField()
    last_used_by_task = models.CharField(max_length=50)
    add_info = models.TextField()
    accounts = models.IntegerField()
    failed_tasks_in_last_6hrs = models.IntegerField()
    successful_tasks_in_last_30hrs = models.IntegerField()


    def __str__(self):
        return self.serial_number