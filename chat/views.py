from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
import channels.layers
from asgiref.sync import async_to_sync
from django.http import HttpResponse

channel_layer = channels.layers.get_channel_layer()
# Create your views here.
# chat/views.py
# from django.shortcuts import render


def index(request):
    t = async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
    print(async_to_sync(channel_layer.receive)('test_channel'))
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def alarm(request):
    # layer=channels.layers.get_channel_layer()

    async_to_sync(layer.group_send)('events', {
        'type': 'events.alarm',
        'content': 'triggered'
    })

    return HttpResponse('<p>Done</p>')
