from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.core import serializers
from .models import Notification

class TestConsumer(WebsocketConsumer):

    def connect(self):
        
        # print(self.scope['user'])
        # print(self.scope["headers"])
        # headers = dict(self.scope["headers"])
        # print(headers[b'bearer'])
        # if b'bearer' in self.scope["headers"]:
        #     print(b'bearer'.decode('UTF-8'))
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
       
        data = list(Notification.objects.all())
        notification = serializers.serialize('json', data)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': notification, }))
        # self.send(text_data=json.dumps({'status': 'connected from django channels'}))
        # return super().connect()
    
    def receive(self, text_data):
        print(text_data)
        return super().receive(text_data=text_data)
    
    def disconnect(self, code):
        print("Disconnected")
        return super().disconnect(code)
    
    def send_notification(self, event):
        data = event.get('value')
        self.send(text_data=json.dumps({'payload': data}))


class AsyncTestConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
      
       
        self.room_name = "async_test_consumer"
        self.room_group_name = "async_test_consumer_group"
        await (self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected from async django channels'}))
        # return super().connect()
    
    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps("we got you"))
        

    async def disconnect(self, code):
        await print("disconnected")
    
    async def send_notification(self, event):
        data = event.get('value')
        await self.send(text_data=json.dumps({'payload': data}))