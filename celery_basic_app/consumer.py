from channels.generic.websocket import WebsocketConsumer
import json
from celery.result import AsyncResult
from .tasks import  docx_to_pdf, pdf_to_docx  # Assuming `add` is your Celery task
import time
from time import sleep
import base64
from django.conf import settings
import os
from django.core.files.base import ContentFile
base_path = settings.BASE_DIR
# PDF_DIRECTORY = os.path.join(base_path, 'static','uploads')
PDF_DIRECTORY = os.path.join(base_path, 'celery_basic_app', 'static', 'uploads')

PDF_to_docx_DIRECTORY = os.path.join(base_path, 'celery_basic_app', 'static', 'uploads','pdf_to_docx')

os.makedirs(PDF_DIRECTORY, exist_ok=True)
os.makedirs(PDF_to_docx_DIRECTORY, exist_ok=True)
class TaskStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')


        if action == 'pdf_file':
            file_name = data.get('fileName')
            file_content = data.get('content')
            file_data = base64.b64decode(file_content.split(',')[1])
            file = ContentFile(file_data, name=file_name)
            static_file_path = os.path.join(PDF_DIRECTORY, file_name)
            with open(static_file_path, 'wb') as f:
                    f.write(file.read())
            
            output_pdf_name = f"{os.path.splitext(file_name)[0]}.pdf"
            output_path = os.path.join(PDF_DIRECTORY, output_pdf_name)
            
            
            task = docx_to_pdf.delay(static_file_path, output_path)
            task_id = task.id
            self.check_task_status(task_id, output_path)

        elif action == 'pdf_docx_file':
            file_name = data.get('fileName')
            file_content = data.get('content')
            print('filename', file_name)
            file_data = base64.b64decode(file_content.split(',')[1])
            file = ContentFile(file_data, name=file_name)
            static_file_path = os.path.join(PDF_to_docx_DIRECTORY, file_name)
            with open(static_file_path, 'wb') as f:
                    f.write(file.read())
            output_pdf_to_docx_name = f"{os.path.splitext(file_name)[0]}.docx"
            output_pdf_to_docx_path = os.path.join(PDF_to_docx_DIRECTORY, output_pdf_to_docx_name)
            
            task = pdf_to_docx.delay(static_file_path, output_pdf_to_docx_path)
            task_id = task.id
            self.check_task_status(task_id, output_pdf_to_docx_path)
            print('outputtt', output_pdf_to_docx_name)

            # exit()
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
        print('dsfsdf',output_path)
        if result.status == 'SUCCESS' and output_path.endswith('.pdf'):
            print('insdie a pdf')
            if os.path.exists(output_path):
                with open(output_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                    final_response['pdf_file'] = f"data:application/pdf;base64,{pdf_base64}"

        elif result.status == 'SUCCESS' and output_path.endswith('.docx'):
            print('insdie a docx')
            if os.path.exists(output_path):
                with open(output_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                    final_response['pdf_docx_file'] = f"data:application/pdf;base64,{pdf_base64}"
                    
        self.send(text_data=json.dumps(final_response))
