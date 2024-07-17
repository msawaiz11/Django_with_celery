from channels.generic.websocket import WebsocketConsumer
import json
from celery.result import AsyncResult
from image_formats_conversion.tasks import jpgtopng
import time
from time import sleep
import base64
from django.core.files.storage import default_storage

from django.conf import settings
from image_formats_conversion.tasks import jpgtopng
import os
from django.core.files.base import ContentFile
base_path = settings.BASE_DIR
Img_Directory = os.path.join(base_path, 'image_formats_conversion', 'static', 'uploads')

os.makedirs(Img_Directory, exist_ok=True)

class TaskImageConversion(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'jpgtopng':
            print('in jpgtopng')
            file_name = data.get('fileName')
            file_content = data.get('content')
            # print('FILECONNET', file_content)
            decoded_data = base64.b64decode(file_content.split(',')[1]) 
            static_file_path = os.path.join(Img_Directory, file_name)
            
            # Write the decoded data to the file
            with open(static_file_path, 'wb') as f:
                f.write(decoded_data)  # Write the decoded data directly

            print('Image saved successfully at', static_file_path)
            
            output_file_name = os.path.splitext(file_name)[0] + '.png'
            output_file_path = os.path.join(Img_Directory, output_file_name)

        # Call the Celery task to convert JPG to PNG
            result = jpgtopng.delay(static_file_path, output_file_path)
            task_id = result.id
            self.check_task_status(task_id, output_file_path)

    def check_task_status(self, task_id, output_path):
        print('oouputtt', output_path )
        result = AsyncResult(task_id)

        while not result.ready():
            status = result.status
            response = {
                'task_id': task_id,
                'status': status,
            }
            self.send(text_data=json.dumps(response))
            result = AsyncResult(task_id)
            sleep(3)  # Adjust the sleep time as needed for polling interval


        final_response = {
            'task_id': task_id,
            'status': result.status,
           
        }
        if result.status == 'SUCCESS':
            print('insdie a pdf')
            # exit()
            if os.path.exists(output_path):
                with open(output_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                    final_response['jpg_to_png'] = f"data:application/pdf;base64,{pdf_base64}"

        self.send(text_data=json.dumps(final_response))
