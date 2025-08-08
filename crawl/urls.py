from django.urls import path, include
from django.contrib import admin
from .views import save_task_input,save_task_output,retrieve,sync,resources,deleteWorkerDevice, deleteWorkerProxy, getLogs, getReports, DeviceViewSet, ChildBotViewSet, ProxyViewSet, InteractionViewSet, TaskViewSet, task
from rest_framework import routers

# Customize admin site
admin.site.site_header = 'GaryAutomates'
admin.site.index_title = 'GaryAutomates Admin Dashboard'
admin.site.site_url = 'https://3e53-2400-adc5-491-1500-4827-80bc-96fc-26e8.ngrok-free.app/crawl/api/logs/'

# Set up router
router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'childbots', ChildBotViewSet)
router.register(r'proxies', ProxyViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'tasks', TaskViewSet)

# URL patterns
urlpatterns = [
    path("api/logs/", getLogs, name="get_logs"),
    path("api/reports/", getReports, name="get_reports"),
    path("api/tasks/", task, name="tasks"),  
    path("api/sync/", sync, name="sync"),
    path("api/retrieve/", retrieve, name="retrieve"),
    path("api/save_task_output/", save_task_output, name="save_task_output"),
     path("api/save_task_input/", save_task_input, name="save_task_input"),
    path("api/resources/", resources, name="resources"),  
    
    path('devices/<str:serial_number>/', deleteWorkerDevice, name='delete_worker_device'),
    path('proxy/<str:proxy_url>/', deleteWorkerProxy, name='delete_worker_proxy'),
    path('', include(router.urls)),  
]
