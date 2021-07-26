import re
import channels
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import time
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
# Create your views here.

def index(request):

    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context))


async def home(request):
    channel_layer = get_channel_layer() 
    for i in range(1, 10): 
        data = "hello from Home"
        await(channel_layer.group_send)(
            'async_test_consumer_group', {
                'type': 'send_notification', 
                'value': json.dumps(data)
            }
        )
        time.sleep(1)
    return render(request, 'home.html')