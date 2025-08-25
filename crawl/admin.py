from django.contrib import admin
from crawl.models import Interaction,Task,ChildBot,Device,Proxy,DeviceReport,RequestRecord,TaskAnalysisReport
admin.site.register(TaskAnalysisReport)
import json
import uuid
from django_admin_relation_links import AdminChangeLinksMixin

class RequestRecordAdmin(admin.ModelAdmin):
    list_filter=['service','end_point','data_point','bot_username']
admin.site.register(RequestRecord,RequestRecordAdmin)
#from sessionbot.resource_utils import convert_bulk_campaign_to_workflow_for_vivide_mind_worker
class SessionBotAdmin(admin.ModelAdmin):
    list_select_related = True
    search_fields = ('username',)
    list_display = ('id', 'username', 'service', 'followers', 'following','auth_code')
    list_filter = ('device', 'service')
    actions = ['login', 'open_browser_profiles']

    def followers(self, obj):
        return obj.followers_count

    def following(self, obj):
        return obj.following_count

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if request.method == 'POST':
            body_unicode = request.POST.get('googlesheet_link', None)
            print(body_unicode)
            print('The task was executed asynchronously')
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description='Login Selected bots')
    def login(self, request, queryset):
        for bot in queryset:
            profile = bot.username
            t = Task.objects.filter(data_point='login', profile=profile)
            if t.exists():
                t[0].status = 'pending'
                t[0].save()
            else:
                t = Task(
                    service=bot.service,
                    end_point='interact',
                    data_point='login',
                    profile=profile,
                    os='browser',
                    uuid=str(uuid.uuid1())
                )
                t.save()

    @admin.action(description='Open Browser Profiles for Selected bots')
    def open_browser_profiles(self, request, queryset):
        for bot in queryset:
            profile = bot.username
            t = Task.objects.filter(data_point='open_browser_profile', profile=profile)
            if t.exists():
                t[0].status = 'pending'
                t[0].save()
            else:
                t = Task(
                    service=bot.service,
                    end_point='interact',
                    data_point='open_browser_profile',
                    profile=profile,
                    os='browser',
                    uuid=str(uuid.uuid1())
                )
                t.save()

admin.site.register(ChildBot, SessionBotAdmin)
    
admin.site.register(Device)
    
# Register your models here.
admin.site.register(Proxy)
class DeviceReportsAdmin(admin.ModelAdmin):
    list_display=['serial_number','service','current_state','disconnected_since','last_report_time']
admin.site.register(DeviceReport,DeviceReportsAdmin)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['ref_id','status','profile','os','end_point','data_point','device']
    
    # Add created_at and updated_at here
    list_display = [
        'uuid','name','service','end_point','data_point','input','os',
        'success_count','failed_count','repeat','profile','device',
        'status','retries_count','dependent_on','created_at','updated_at'
    ]
    
    actions = ['start_tasks','stop_tasks','resume_tasks','pause_tasks','clone_tasks']
    
    search_fields = ('profile',)

    @admin.action(description='Pause Selected Tasks')
    def pause_tasks(self, request, queryset):
        queryset.update(paused=True)

    @admin.action(description='Start Selected Tasks')
    def start_tasks(self, request, queryset):
        queryset.update(status='pending')

    @admin.action(description='Stop Selected Tasks')
    def stop_tasks(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Resume Selected Tasks')
    def resume_tasks(self, request, queryset):
        queryset.update(status='pending', paused=False)

    @admin.action(description='Clone Selected Tasks')
    def clone_tasks(self, request, queryset):
        for task in queryset:
            task.clone()

admin.site.register(Task, TaskAdmin)

class InteractionAdmin(admin.ModelAdmin):

    list_display=['bot_username','target_profile','target_post','activity','interaction_time','view_screenshot']

    list_filter=['target_profile','target_post','bot_username']
    

admin.site.register(Interaction,InteractionAdmin)
