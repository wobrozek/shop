import json
from channels.generic.websocket import WebsocketConsumer

class HistoryConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_esabilished',
            'message':'udalo sie'
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