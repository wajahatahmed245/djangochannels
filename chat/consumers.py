from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class EventConsumer(JsonWebsocketConsumer):
  def connect(self):
    print('inside EventConsumer connect()')
    async_to_sync(self.channel_layer.group_add)('events', self.channel_name)

    self.accept()

  def disconnect(self, close_code):
    print('inside EventConsumer disconnect()')
    print("Closed websocket with code: ", close_code)
    async_to_sync(self.channel_layer.group_discard)(
        'events',
        self.channel_name
    )
    self.close()

  def receive_json(self, content, **kwargs):
    print('inside EventConsumer receive_json()')
    print("Received event: {}".format
    (content))
    self.send_json(content)

  def events_alarm(self, event):
    print('inside EventConsumer events_alarm()')
    self.send_json(
        {
            'type': 'events.alarm',
            'content': event['content']
        }
    )
