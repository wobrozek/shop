import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class HistoryConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route']['kwargs']['listing_id'])
        self.room_group_name =str(self.scope['url_route']['kwargs']['listing_id'])

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_esabilished',
            'message':'udalo sie'
        }))

    def receive(self, text_data):
        data=json.loads(text_data)

        if 'bid' in data:
            print(data['bid'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                'type': "send_group",
                'message': "sieam"
                }
            )

        if 'comment' in data:
            print(data['comment'])
            self.send(text_data=json.dumps({
                'type': "send_group",
                "message":'hej'
            }))

    def send_group(self,event):
        bid=event['message']

        self.send(text_data=json.dumps({
            'type':'bid',
            'price':bid
        }))

#
# class commentConsumer(WebsocketConsumer,id):
#     def connect(self):
#         self.accept()
#
#         self.send(text_data=json.dumps({
#             'type':'connection_esabilished',
#             "message":"udalo sie"
#         }))