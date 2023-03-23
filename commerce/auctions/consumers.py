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


    def receive(self, text_data):
        data=json.loads(text_data)
        print(data)


        if data["type"]=="bid":
            if data["value"]<0:
                self.send(text_data=json.dumps({
                'type': "send_error",
                "value": "Your offer must be higher than previous offert",
                }))
                return

        
            self.send(text_data=json.dumps({
                'type': "send_group",
                "value":data["value"],
                "user":data["user"],
                "img":data["img"]
            }))

    def send_group(self,event):

        self.send(text_data=json.dumps({
            'type': event["type"],
            "value":event["value"],
            "user":event["user"],
            "img":event["img"]
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