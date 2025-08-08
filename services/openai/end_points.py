import os
import json
import time
from base.storage_sense import Saver
from base.browser import Browser
from services.reports_manager.manager import Manager as reports_manager
import random
from openai import OpenAI
import openai
class EndPoints:

    def __init__(self):
        self.end_point=''
        self.data_point=''
        self.make_request=''
        self.request_maker=''
        self.database=''

        self.storage_sense=Saver()
        self.browser=Browser()
        
        
    def get_required_data_point(self,**kwargs):
        #self.output.write('Fetching Data for the End-Point'+kwargs.get('end_point')+'data_point'+kwargs.get('data_point'))
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    
    def internal_get_required_data_point(self,**kwargs):
    
        end_point=getattr(self,kwargs.get('end_point'))
        data_point=getattr(end_point,kwargs.get('data_point'))
        return data_point(self,**kwargs)
    class Authenticate:
        def __init__(self):
            self.storage_sense = Saver()

        def API_token_authorization(self, **kwargs):
            client = OpenAI(api_key=kwargs.get('api_key'))
            return 'success', client
    class Models:
        def __init__(self):
            self.storage_sense = Saver()
        def models(self, **kwargs):
            openai.api_key = kwargs.get('api_key')
            models = openai.models.list()
            return 'success',models
    class Text_Generation:
        def __init__(self):
            self.storage_sense = Saver()
        def generate_content(self, **kwargs):
            from services.reports_manager.manager import Manager as reports_manager
            reports_manager=reports_manager()
            reports_manager.run_id=kwargs.get('run_id')
            reports_manager.task_id=kwargs.get('uuid')
            api_key=kwargs.get('add_data',{}).get('api_key','')
            try:
                bot = EndPoints.Authenticate().API_token_authorization(**{'api_key': api_key})
                bot = bot[1]
            except Exception as e:
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'generate_content',
                                        'type':'error_in_authentication','task':str(kwargs['uuid']),'error':e, 
                                        }) 
            else:

                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'generate_content',
                                        'type':'authentication_successful','task':str(kwargs['uuid']) 
                                        }) 
           
            completion = bot.chat.completions.create(
                model = 'gpt-4-turbo',
                messages = [
                    {
                        'role':'system','content':'You are a helpful assistant.',

                    },
                    {
                        'role':'user',
                        'content':kwargs.get('prompt')
                    }
                ]
            )
            try:
                content=completion.choices[0].message.content
                
                content=content.strip()
                res=content[content.find('{'):content.rfind('}')+1]
                res = json.loads(res)
            except Exception as e:
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'generate_content',
                                        'type':'error_in_parsing_response_as_json','response':res
                                        }) 
                return False
            else:
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'generate_content',
                                        'type':'succesfully_parsed_response_as_json','response':res
                                        }) 
                return res
    
        
        def reply_generation(self, **kwargs):
            add_data=kwargs.get('add_data',{})

            bot = EndPoints.Authenticate().API_token_authorization(**{'api_key':add_data.get('api_key')})
            bot = bot[1]
           
            
            #print(f""+add_data.get('prompt')+""+add_data.get('caption')+"",)
            resp = bot.chat.completions.create(
                model='gpt-4o',
                messages = [
                    {
                        'role':'system','content':'You are a helpful assistant.',

                    },
                    {
                        'role':'user',
                        'content':f""+add_data.get('prompt')+""+add_data.get('caption')+"",
                    }
                ],

                max_tokens=100,
                temperature=0.7,
                n = 1
            )
            #print(resp)
            comments = resp.choices[0].message.content.split('\n')
            comments = [comment.strip() for comment in comments if comment.strip()]
            print("Generated Comments: \n",comments)
            return 'success',comments
        
        def relative_reply(self, **kwargs):
            bot = EndPoints.Authenticate().API_token_authorization(**{'api_key':kwargs.get('api_key')})
            bot = bot[1]            
            
            resp = bot.chat.completions.create(
                model = 'gpt-4o',
                messages = [
                    {
                        'role':'system','content':'You are a helpful assistant',

                    },
                    {
                        'role':'user',
                        'content':f"""Post content :{kwargs.get('post_caption')}
                        Other Comments:
                        1. {kwargs.get('comments')[0]},
                        2. {kwargs.get('comments')[1]},
                        3. {kwargs.get('comments')[2]}
                        Wrtie a unique, realistic comment that adds to the conversation. Avoid sumarizing or repeating the comments. The comment should reflect individual perspective, respond to the post's content and engage with the mix of opinions from other users in a conversational tone. It should feel authentic, as if written by a person with their own viewpoint on the topic."""
                    }
                ],
                # prompt = f"The following is a social media post caption:{caption}. Write three relevant and contexual comments",
                max_tokens=80,
                temperature=0.7,
                n = 1
            )
            comment = resp.choices[0].message.content
            print(comment)
            return 'success', comment
        def names_and_generated_data(self, **kwargs):
            add_data=kwargs.get('add_data')

                
            bot = EndPoints.Authenticate().API_token_authorization(**{'api_key':add_data.get('api_key')})
            bot = bot[1]            
            
            resp = bot.chat.completions.create(
                model = 'gpt-4o',
                messages = [{"role":'user','content':add_data.get('prompt')}],
                max_tokens=30,
                temperature=0.7
            )

            response_text = resp.choices[0].message.content.strip()
            print(response_text)
            try:
                response_text=response_text.replace('```python','')
                response_dict = eval(response_text.replace('```python',''))
            except Exception as e:
                print(e)
            else:
                return response_dict
           

    class Image_Generation:
        def __init__(self):
            pass
        def generate_image(self, **kwargs):
            client = EndPoints.Authenticate().API_token_authorization(**{'api_key':kwargs.get('api_key')})
            client = client[1]

            res = client.images.generate(
                model='dall-e-3',
                prompt="Create a social media post which has a dark grey background with 'NorthRays Innovations' written in the top right corner of the image in a box. Now, write a line 'NorthRays, Developing Solutions' in the middle of the image in another rectangular shape. After this, write a line below as 'CEO:Hamza Zubair'. Please try to add all the details precisely. Make the image more presentable with good effects.",
                n=1,
                size="1024x1024"
            )
            print(res)
            image_url = res['data'][0]['url']
            print("Generated Image URL: ", image_url)

            image_data = requests.get(image_url).content
            with open("generated_image.png", "wb") as file:
                file.write(image_data)


            return image_url
    class ImageAnalysis:
        def upload_and_analyze_image(instructions,**kwargs):
            """
            Uploads an image to the OpenAI API and analyzes it based on the given instructions.

            Args:
                image_path (str): Path to the image file to be uploaded.
                instructions (str): Instructions for the analysis (e.g., "Describe the image", "Generate a caption for the image").

            Returns:
                str: The analysis result from the OpenAI API.
            """
            add_data=kwargs.get('add_data',{})
            image_path=add_data.get('image_path')
            instructions=add_data.get('instructions',{})
            bot = EndPoints.Authenticate().API_token_authorization(**{'api_key':add_data.get('api_key')})
            bot = bot[1]
            
            try:
                # Upload the image
                with open(image_path, "rb") as f:
                    file_response =bot.files.create(
                        file=f,
                        purpose="vision"  # Use "image" purpose for image files
                    )
                    file_id = file_response.id

                # Create an assistant with file retrieval tool
                f=open(image_path, "rb")
                assistant_response = bot.beta.assistants.create(
                    model="gpt-4-turbo",  # Use a model suitable for image analysis 
                    instructions=instructions, 
                    tools=[{"type": "file_search"}]
                )
                assistant_id = assistant_response.id

                # Create a thread
                thread_response = bot.beta.threads.create()
                thread_id = thread_response.id

                # Add a message to the thread
                print(file_response.to_dict())
                message_response = bot.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=[
                    {
                        "type": "text",
                        "text": "Analyse image"
                    },
                    {
                        "type": "image_file",
                        "image_file": {"file_id": file_id}
                    },
                    ]
                )

                # Run the assistant
                run_response = bot.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=assistant_id
                )
                run_id = run_response.id

                # Get the run results
                while True:
                    run_results = bot.beta.threads.runs.retrieve(
                        thread_id=thread_id,
                        run_id=run_id
                    )
                    status = run_results.status
                    if status == "completed":
                        break

                # Retrieve the assistant's response
                messages = bot.beta.threads.messages.list(thread_id=thread_id)
                assistant_message = next(
                    (
                        message
                        for message in messages.data
                        if message.role == "assistant"
                    ),
                    None
                )

                if assistant_message:
                    return assistant_message.content
                else:
                    return "No response from the assistant."

            except Exception as e:
                print(f"Error: {e}")
                return None
    class MultiModalAnalysis:
        def analyze_content(instructions, **kwargs):
            from services.reports_manager.manager import Manager as reports_manager
            reports_manager=reports_manager()
            reports_manager.run_id=kwargs.get('run_id')
            reports_manager.task_id=kwargs.get('uuid')
            """
            Analyzes text and/or images using the OpenAI API assistant.

            Args:
                instructions (str): Instructions for the analysis.
                **kwargs: Keyword arguments containing 'add_data' (dict).
                    add_data should contain:
                        text (str, optional): Text to analyze.
                        image_paths (list of str, optional): Paths to image files.
                        api_key (str): OpenAI API key.

            Returns:
                list: A list of analysis results from the OpenAI API, or None on error.
            """
            add_data = kwargs.get('add_data', {})
            text = add_data.get('text', None)
            instructions = add_data.get('text')
            image_paths = add_data.get('image_paths', [])
            api_key = add_data.get('api_key')

            if not api_key:
                print("Error: API key not provided.")
                return None
            from services.reports_manager.manager import Manager as reports_manager
            reports_manager=reports_manager()
            reports_manager.run_id=kwargs.get('run_id')
            reports_manager.task_id=kwargs.get('uuid')
            try:
                bot = EndPoints.Authenticate().API_token_authorization(**{'api_key': api_key})
                bot = bot[1]
            except Exception as e:
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'error_in_authentication','task':str(kwargs['uuid']),'error':e, 
                                        }) 
            else:

                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'authentication_successful','task':str(kwargs['uuid']) 
                                        }) 
            try:
                file_ids = []
                if image_paths and isinstance(image_paths, list):
                    for image_path in image_paths:
                     
                        # image_path = image_path[0]
                        if not os.path.exists(image_path):
                            print(f"Warning: Image file not found: {image_path}")
                            continue
                        try:
                            reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'uploading_media_to_openai','task':str(kwargs['uuid']) 
                                        }) 
                            with open(image_path, "rb") as f:
                                file_response = bot.files.create(
                                    file=f,
                                    purpose="vision"
                                )
                                file_ids.append(file_response.id)
                        except Exception as e:
                            reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'error_in_upload','task':str(kwargs['uuid']),'error':e 
                                        }) 

                message_content = []
                if text:
                    message_content.append({"type": "text", "text": text})

                for file_id in file_ids:
                    message_content.append({"type": "image_file", "image_file": {"file_id": file_id}})

                if not message_content:
                    reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'no_text_or_images_provided_exiting','task':str(kwargs['uuid']) 
                                        }) 
                    print("Error: No text or images provided.")
                    return None
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'creating_assistant_with_gpt-4_turbo','task':str(kwargs['uuid'])
                                        }) 
                assistant_response = bot.beta.assistants.create(
                    model="gpt-4-turbo",
                    instructions=instructions,
                    tools=[{"type": "file_search"}]
                )
                assistant_id = assistant_response.id

                thread_response = bot.beta.threads.create()

                thread_id = thread_response.id
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'created_thread','task':str(kwargs['uuid'])
                                        }) 
                message_response = bot.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=message_content
                )
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'got_message_response','task':str(kwargs['uuid'])
                                        }) 
                run_response = bot.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=assistant_id
                )
                run_id = run_response.id
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                        'type':'got_run_response','task':str(kwargs['uuid'])
                                        }) 
                while True:
                    run_results = bot.beta.threads.runs.retrieve(
                        thread_id=thread_id,
                        run_id=run_id
                    )
                    status = run_results.status
                    if status == "completed":
                        reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                            'type':'retrieve_from_threads_completed','task':str(kwargs['uuid'])
                                            }) 
                    
                        break
                    elif status=='failed' and run_results.last_error.code=='rate_limit_exceeded':
                        reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                            'type':'rate_limit_exceeded_for_api_key','task':str(kwargs['uuid'])
                                            }) 
                        return False

                messages = bot.beta.threads.messages.list(thread_id=thread_id)
                assistant_messages = [
                    message.content for message in messages.data if message.role == "assistant"
                ]
                # import traceback
                # print(traceback.format_exc())       
                if assistant_messages:
                    reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                            'type':'assistant_message_found_stopping_bot','task':str(kwargs['uuid'])
                                            }) 
                    return assistant_messages[0][0].text.value
                else:
                    reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                            'type':'got_no_response_from_assistant_failed','task':str(kwargs['uuid'])
                                            }) 
                    return ["No response from the assistant."]
                
            except Exception as e:
                reports_manager.report_performance(**{'service':'openai','end_point':'MultiModalAnalysis','data_point':'analyze_content',
                                            'type':'encountered_error','task':str(kwargs['uuid']),'error':e
                                            }) 
                print(f"Error: {e}")
                # import traceback
                # print(traceback.format_exc())
                return None
            
        # Example usage
        # Example usage

