import uuid
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .serializers import DeviceSerializer, ChildBotSerializer, ProxySerializer, InteractionSerializer, TaskSerializer
#from crawl.external_party_communication_facilitator import create_workflow_from_payload, queue_vivid_mind_payload, get_logs, handle_automation_task_creation
import ast
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crawl.models import ChildBot, Device, Interaction, Proxy, Task
from rest_framework.pagination import CursorPagination
from django.views.decorators.http import require_http_methods
import psutil
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.db import transaction
from datetime import datetime
import uuid
from django.db import models
import json


@require_http_methods(["GET", "POST", "PUT"])
def getLogs(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        # Fetch logs from the external party communication facilitator
        logs = get_logs()
        print(logs)

        # Paginate the logs, 50 per page
        paginator = Paginator(logs, 50)
        page_number = request.GET.get('page')

        try:
            logs = paginator.page(page_number)
        except PageNotAnInteger:
            logs = paginator.page(1)  # If the page is not an integer, deliver the first page.
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)  # If the page is out of range, deliver the last page.

        # Render the logs on the 'log.html' page
        return render(request, "log.html", {"logs": logs})

def getReports(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        resp = get_logs()
        context = {"logs": resp}        
        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def resources(request):
    print('yes')
    if request.method == 'GET':
        bots = ChildBot.objects.all().values()
        return JsonResponse(list(bots), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)

        if data.get('resources',[]):
            
            resources=data.get('resources')
           
            bots=resources.get('bots')
            devices=resources.get('devices')
            for device in devices:
                data=device['data']
                if device['method']=='create' or device['method']=='update':
                            
                    data.pop('id') 
                    print(data)
                    device=Device.objects.filter(serial_number=data['serial_number'])
                    if len(device)>0:
                        device.update(name=data['name'])
                    else:
                        d=Device(**data)
                        d.save()
            for bot in bots:
                resource=bot
                if resource['type']=='bot':
                    if resource['method']=='create' or resource['method']=='update':
                        print(bot)
                        bot=bot.get('data')
                        if bot.get('device'):
                            device=Device.objects.all().filter(serial_number=bot['device'])
                            if device:
                                device=device[0]

                                bot['device_id']=device.id
                                bot.pop('device')
                            else:
                                bot.pop('device')
                            
                        else:
                            bot.pop('device')
                        bot.pop('logged_in',False)
                        bot.pop('challenged',False)
                        bot.pop('failed_api_requests',False)
                        
                        c=ChildBot.objects.all().filter(username=bot['username']).filter(service=bot['service'])
                        if c:
                            c.update(**bot)
                        else:

                        
                            ChildBot.objects.update_or_create(**bot)
               
            return JsonResponse({'status':'success'}, safe=False)

        
        
    return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def deleteWorkerDevice(request, serial_number: str) -> JsonResponse:
    print('Device Delete Request received')
    if request.method == 'DELETE':
        try:
            device = Device.objects.get(serial_number=serial_number)
            device.delete()
            return JsonResponse({'status': 'success', 'message': 'Device deleted from worker.'})
        except Device.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Device not found in worker.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def deleteWorkerProxy(request, proxy_url: str) -> JsonResponse:
    print('Proxy Delete Request received')
    if request.method == 'DELETE':
        try:
            proxy = Proxy.objects.get(proxy_url=proxy_url)
            proxy.delete()
            return JsonResponse({'status': 'success', 'message': 'Proxy deleted from worker.'})
        except Proxy.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Proxy not found in worker.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def task(request):
    
    if request.method == 'GET':
        tasks = Task.objects.all().values()
        return JsonResponse(list(tasks), safe=False)

    elif request.method == 'POST':
        
           
            body = json.loads(request.body)
            
         
            if not isinstance(body, list):  
                return JsonResponse({'error': 'Payload must be a list of tasks'}, status=400)
            try:
                for task_data in body:
                    print(task_data)
                    if task_data.get('method')=='delete':
                        Task.objects.all().filter(uuid=task_data['uuid']).delete()
                        continue
                    task_data.pop('id',False)
                    # Validate required fields
                    required_fields = ['service', 'os', 'data_point', 'end_point', 'add_data', 'ref_id']
                    missing_fields = [field for field in required_fields if field not in task_data]
                    outputs=[]
                    if missing_fields:
                        outputs.append({'verb':'failed','noun':'task','object':None,'identifier':task_data['uuid'],'adjective':'missing_field','add_info':{'missing_fields: '+','.join(missing_fields)}})
                        
                   
                    exstn_tasks=Task.objects.all().filter(uuid=task_data['uuid'])
                    
                    
                    if len(exstn_tasks)>0:
                       
                            
                        task=exstn_tasks[0]
                        task.add_data=task_data['add_data']
                        task.targets=task_data.get('targets', '')
                        task.alloted_bots=task_data.get('alloted_bots')        
                        if not task.status=='running':
                            if task_data.get('status'):
                                task.status=task_data.get('status')   
                        task.save()
                        print('updated')
                        outputs.append({'verb':'updated','noun':'task','object':model_to_dict(task),'identifier':task.uuid})
                    else:
                        task = Task(
                            uuid=task_data.get('uuid'),
                            service=task_data.get('service'),
                            os=task_data.get('os'),
                            data_point=task_data.get('data_point'),
                            end_point=task_data.get('end_point'),
                            input=task_data.get('input', ''),
                            targets=task_data.get('targets', ''),
                            condition=task_data.get('condition', ''), 
                            profile=task_data.get('profile', ''), 
                            device=task_data.get('device', ''), 
                            add_data=task_data.get('add_data'),
                            repeat=task_data.get('repeat', False),
                            repeat_duration=task_data.get('repeat_duration', ''),
                            status=task_data.get('status', 'pending'),  
                            last_state_changed_at=None,
                            report=task_data.get('report', False),
                            retries_count=task_data.get('retries_count', 0),
                            paused=task_data.get('paused', False),
                            ref_id=task_data.get('ref_id',''),
                            alloted_bots=task_data.get('alloted_bots'),
                           

                            
                            
                        )

                        task.save()
                        outputs.append({'verb':'created','noun':'task','object':model_to_dict(task),'identifier':task.uuid})
                    if task_data.get('dependent_on'):
                        _task=Task.objects.all().filter(uuid=task_data.get('dependent_on'))
                        if _task:
                            _task=_task[0]
                            task.dependent_on=_task
                            task.save()
                return JsonResponse({'message': 'success'}, status=200)

           
            except Exception as e:
                import traceback
 
                outputs.append({'verb':'failed','noun':'task','object':model_to_dict(task),'identifier':task.uuid,'add_data':{'traceback':traceback.format_exc()}})
                print(outputs)
                return JsonResponse({'message': 'error'}, status=500)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            task_id = body.get('task_id')
            task = get_object_or_404(Task, id=task_id)

            task.service = body.get('service', task.service)
            task.os = body.get('os', task.os)
            task.add_data = body.get('add_data', task.add_data)
            task.save()
            return JsonResponse({'message': 'Task updated', 'task_id': task.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            task_id = body.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return JsonResponse({'message': 'Task deleted successfully'}, status=204)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def interactions(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            # Initialize a queryset to fetch interactions
            queryset = Interaction.objects.all()

            # Apply filters based on provided keys in the request body
            if 'username' in body:
                queryset = queryset.filter(bot__username=body['username'])  # Adjust according to your relationships

            if 'ref_id' in body:
                queryset = queryset.filter(ref_id=body['ref_id'])

            if 'task_id' in body:
                queryset = queryset.filter(task_id=body['task_id'])

            if 'service' in body:
                queryset = queryset.filter(service=body['service'])

            # Convert the filtered queryset to a list of dictionaries
            interactions = list(queryset.values())

            return JsonResponse(interactions, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    else:
        return HttpResponse('Method not allowed', status=405)
    
def worker_info(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload from the request body
            payload = json.loads(request.body)

            # Dummy task manager info
            task_manager_info = {
                'dummy_key': 'dummy_value', 
                'status': 'active',           
            }

            # Retrieve server info using psutil
            ram_info = psutil.virtual_memory()
            cpu_info = psutil.cpu_times()
            network_info = psutil.net_if_stats()

            server_info = {
                'ram': {
                    'total': ram_info.total,
                    'used': ram_info.used,
                    'free': ram_info.available,
                    'percent': ram_info.percent,
                },
                'cpu': {
                    'physical_cores': psutil.cpu_count(logical=False),
                    'logical_cores': psutil.cpu_count(logical=True),
                    'percent': psutil.cpu_percent(interval=1),
                },
                'network': {
                    'interfaces': {
                        iface: {
                            'is_up': stats.isup,
                            'mtu': stats.mtu,
                            'speed': stats.speed  
                        }
                        for iface, stats in network_info.items()
                    },
                },
            }

            response_data = {
                'task_manager_info': task_manager_info,
                'server_info': server_info,
            }

            return JsonResponse(response_data, safe=False)

        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON payload', status=400)

    else:
        return HttpResponse('Method not allowed', status=405)

@api_view(['POST'])
def sync(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        all_successful_sync_ids = {}
        errors = []  # List to store errors for failed rows
      
        for row in data.get('data'):
            payload = row
            object_id = payload.get("uuid")
            operation = payload.get("operation")
            object_body = payload.get("object_body")
            object_type = payload.get("object_type")
            sync_id = payload.get("sync_id")

            if not all([object_id, operation, object_type, sync_id]):
                error_message = "Each payload must contain uuid, operation, object_type, and sync_id"
                errors.append({"sync_id": sync_id, "error": error_message}) # Add error with sync_id
                continue  # Continue to the next row

            try:
                model_class = apps.get_model('crawl', object_type)
            except LookupError:
                error_message = f"Model {object_type} not found"
                errors.append({"sync_id": sync_id, "error": error_message})
                continue
            valid_fields = {field.name for field in model_class._meta.fields}
            with transaction.atomic():
                try:
                    if operation == "CREATE":
                        if object_body:
                            for key, value in object_body.items():
                                if not key in valid_fields:
                                    continue
                                field = model_class._meta.get_field(key)
                                if isinstance(field, models.DateTimeField) and value:
                                    object_body[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                                elif isinstance(field, models.UUIDField) and value:
                                    object_body[key] = uuid.UUID(value)
                                elif isinstance(field, models.BooleanField) and isinstance(value, str):
                                    object_body[key] = value.lower() == 'true'
                                elif isinstance(field, models.Model) and value:
                                    try:
                                        fk_model = field.related_model
                                        object_body[key] = fk_model.objects.get(uuid=value)
                                    except fk_model.DoesNotExist:
                                        error_message = f"{field.name} with UUID {value} not found"
                                        errors.append({"sync_id": sync_id, "error": error_message})
                                        continue # skip to next row since FK is invalid
                            model_instance = model_class(**object_body)
                            model_instance.save()
                            all_successful_sync_ids.setdefault(object_type, []).append(sync_id)

                        else:
                            error_message = "Object body is required for CREATE"
                            errors.append({"sync_id": sync_id, "error": error_message})
                            continue

                    elif operation == "UPDATE":
                 
                        if object_body:
                            try:
                                model_instance = model_class.objects.get(uuid=object_id)
                                
                            except model_class.DoesNotExist:
                                
                                model_instance = model_class()
                              
                                for key, value in object_body.items():
                                    if not key in valid_fields:
                                        continue
                                    field = model_class._meta.get_field(key)
                                    if isinstance(field, models.DateTimeField) and value:
                                        setattr(model_instance, key, datetime.fromisoformat(value.replace('Z', '+00:00')))
                                    elif isinstance(field, models.UUIDField) and value:
                                        setattr(model_instance, key, uuid.UUID(value))
                                    elif isinstance(field, models.BooleanField) and isinstance(value, str):
                                        setattr(model_instance, key, value.lower() == 'true')
                                    elif isinstance(field, models.Model) and value:
                                        try:
                                            fk_model = field.related_model
                                            setattr(model_instance, key, fk_model.objects.get(uuid=value))
                                        except fk_model.DoesNotExist:
                                            error_message = f"{field.name} with UUID {value} not found"
                                            errors.append({"sync_id": sync_id, "error": error_message})
                                            continue # skip to next row since FK is invalid
                                    else:
                                        setattr(model_instance, key, value)
                                model_instance.save()
                                all_successful_sync_ids.setdefault(object_type, []).append(sync_id)
                                continue # Object created, move to the next row

                            for key, value in object_body.items():
                                if not key in valid_fields:
                                    continue
                                if key =='id':
                                    continue
                                field = model_class._meta.get_field(key)
                                if isinstance(field, models.DateTimeField) and value:
                                    setattr(model_instance, key, datetime.fromisoformat(value.replace('Z', '+00:00')))
                                elif isinstance(field, models.UUIDField) and value:
                                    setattr(model_instance, key, uuid.UUID(value))
                                elif isinstance(field, models.BooleanField) and isinstance(value, str):
                                    setattr(model_instance, key, value.lower() == 'true')
                                elif isinstance(field, models.Model) and value:
                                    try:
                                        fk_model = field.related_model
                                        setattr(model_instance, key, fk_model.objects.get(uuid=value))
                                    except fk_model.DoesNotExist:
                                        error_message = f"{field.name} with UUID {value} not found"
                                        errors.append({"sync_id": sync_id, "error": error_message})
                                        continue # skip to next row since FK is invalid
                                else:
                                    setattr(model_instance, key, value)
                           
                            model_instance.save()
                            
                            all_successful_sync_ids.setdefault(object_type, []).append(sync_id)

                        else:
                            error_message = "Object body is required for UPDATE"
                            errors.append({"sync_id": sync_id, "error": error_message})
                            continue

                    elif operation == "DELETE":
                        try:
                            model_instance = model_class.objects.get(uuid=object_id)
                            model_instance.delete()
                            print('deleted')
                            all_successful_sync_ids.setdefault(object_type, []).append(sync_id)
                        except model_class.DoesNotExist:
                            pass

                    else:
                        error_message = f"Invalid operation: {operation}"
                        errors.append({"sync_id": sync_id, "error": error_message})
                        continue

                except Exception as e:
                    error_message = f"Error in data house sync: {e}"
                    errors.append({"sync_id": sync_id, "error": str(e)})
                    continue  # Continue to the next row

        response_data = {"message": "Sync request processed", "successful_sync_ids": all_successful_sync_ids}
        print(response_data)
        if errors:
            print(errors)
            response_data["errors"] = errors # Add errors to the response
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS) # 207 for partial success
        else:
            return Response(response_data, status=status.HTTP_200_OK)  
# Placeholder function for further data handling once the above views are completed.

@csrf_exempt
def retrieve(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    
        service=data['service']
        end_point=data['end_point']
        data_point=data.get('data_point',False)
        identifier=data.get('identifier',False)
        block_name=data.get('block_name',False)
        sub_block=data.get('sub_block',False)
        read=data.get('read',True)
        from base.storage_sense import Saver
        import os
        s=Saver()
        s.service=service
        
        print(data)
        if service=='deep_stuff':

            address=end_point+'.'+identifier
            if data_point:
                address+='.'+data_point
            if block_name:
                address+='.'+block_name
            if sub_block:
                address+='.'+sub_block
            s.block={'address':address}
            s.load_deep_stuff()

        else:
            address=end_point
            if identifier:
                address+='.'+identifier
            if data_point:
                address+='.'+data_point
            if block_name:
                address+='.'+block_name
            s.block={'address':address}
            s.load_block()
        print(s.block_address)
        if not os.path.exists(s.block_address):
            return {"error": "Folder not found"}
        def folder_to_dict(root_folder):
            result = {}
            data=[]
            for item in os.listdir(root_folder):
                item_path = os.path.join(root_folder, item)
                if os.path.isdir(item_path):
                    result[item] = folder_to_dict(item_path)
                else:
                    if item.lower().endswith(".json"):
                        try:
                            if read:
                                with open(item_path, "r") as f:
                                # result[item] = json.load(f) 
                                    data.append(json.load(f)[0]) # Parse JSON data
                            else:
                                data.append(item)
                        except Exception as e:
                            result[item] = f"Error: Could not read JSON file - {e}"
                    else:
                        try:
                            result[item] = os.path.getsize(item_path)
                        except OSError:
                            result[item] = "Error: Could not get file size"
        
            return data
        data=folder_to_dict(s.block_address)
        return JsonResponse(data={'status':'success','data':data},status=200)
@csrf_exempt
def save_task_output(request):
    
    if request.method == 'POST':

        data = json.loads(request.body)
        print(data)
        task_uuid=data.get('task_uuid',False)  
        block_name=data.get('block_name',False)
        output_data=data.get('data',[])
        file_name=data.get('file_name',False)
        from base.storage_sense import Saver
        s=Saver()
        address='tasks'+'.'+task_uuid+'.outputs'
        s.block={'address':address}
        s.load_deep_stuff()
        for output in output_data:
            print(output)
            try:
                import threading
                threading.Thread(s.create_task_outputs,args=(task_uuid,output_data,block_name,True,file_name)).start()
            except Exception as e:
                pass 
        return JsonResponse(data={'status':'success','data':data},status=200)
@csrf_exempt
def save_task_input(request):
    
    if request.method == 'POST':

        data = json.loads(request.body)
        print(data)
        task_uuid=data.get('task_uuid',False)  
        block_name=data.get('block_name',False)
        input_data=data.get('data',[])
        file_name=data.get('file_name',False)
        from base.storage_sense import Saver
        s=Saver()
        address='tasks'+'.'+task_uuid+'.inputs'
        s.block={'address':address}
        s.load_deep_stuff()
        s.create_task_inputs(id=task_uuid,block_name=block_name,data=input_data,file_name=file_name) 
        return JsonResponse(data={'status':'success','data':data},status=200)
def data(request):
    if request.method == 'GET':
        # Implement logic for handling data-related operations here.
        pass

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class ChildBotViewSet(viewsets.ModelViewSet):
    queryset = ChildBot.objects.all()
    serializer_class = ChildBotSerializer

class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer