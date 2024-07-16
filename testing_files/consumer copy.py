# from channels.generic.websocket import WebsocketConsumer
# import json
# from celery.result import AsyncResult
# from .tasks import Gold_Price, fetch_quote, add,Crypto_Price

# class TaskStatusConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass


#     def receive(self, text_data):     
#             global status   
#             data = json.loads(text_data)
#             action = data.get('action')


#             if action == 'start_task':
#                 status = 'start_task'
#                 result = add.delay(4, 4)
#                 print('resultid', result.id)

#                 response = {
                   
#                     'task_id': result.id,
#                     'status': 'PENDING',
#                     'result': None
#                 }
#                 self.send(text_data=json.dumps(response))

#             elif action == 'fetch_quote':
#                 status = 'fetch_quote'
#                 category = data.get('category')
#                 result = fetch_quote.delay(category)
#                 response = {
                 
#                     'task_id': result.id,
#                     'status': 'PENDING',
#                     'result': None
#                 }
#                 self.send(text_data=json.dumps(response))

#             else:               
#                 task_id = data.get('task_id')
#                 if task_id:
#                     result = AsyncResult(task_id)
#                     response = {                    
#                         'type' : status,
#                         'task_id': task_id,
#                         'status': result.status,
#                         'result': result.result
#                     }
#                     self.send(text_data=json.dumps(response))

