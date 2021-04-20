# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Background_Task

class StatusConsumer(WebsocketConsumer):
    def connect(self):
        self.status_name = self.scope['url_route']['kwargs']['status_name']
        self.status_group_name = 'status_%s' % self.status_name

        # Join room group
        self.channel_layer.group_add(
            self.status_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.status_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request = text_data_json['request']

        msg_dict = {
            'type': request,
            'status' : 'idle',
        }

        if request == 'web_scrape_status':
            check = Background_Task.objects.filter(activity='web_scrape', status=1)

            if check:
                msg_dict = {
                    'type': request,
                    'status' : 'in progress',
                    'current' : check[0].current,
                    'total' : check[0].total
                }

        elif request == 'word_collection_status':
            check = Background_Task.objects.filter(activity='word_collection', status=1)

            if check:
                msg_dict = {
                    'type': request,
                    'status' : 'in progress',
                    'current' : check[0].current,
                    'total' : check[0].total
                }

        elif request == 'word_harvest_status':
            check = Background_Task.objects.filter(activity='word_harvest', status=1)

            if check:
                msg_dict = {
                    'type': request,
                    'status' : 'in progress',
                    'current' : check[0].current,
                    'total' : check[0].total
                }

        # Send message to WebSocket
        self.send(text_data=json.dumps(msg_dict))
