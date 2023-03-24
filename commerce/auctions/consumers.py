import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import User,Auction,Bid,Comment
import re

CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

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

        # remove html dangerous content
        data["value"]=cleanhtml(data["value"])

        if data["type"] == "end":
            return

        user=User.objects.get(id=int(data["user_id"]))
        auction = Auction.objects.get(id=int(data["auction_id"]))

        if auction.close==True:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': "send_error",
                    "value": "The auction is closed",
                }
            )
            return

        if data["type"]=="bid":
            price = float(data["value"])
            if price< auction.price:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': "send_error",
                        "value": "The price must be greater than previous bid",
                    }
                )
                return
            else:
                newOffer=Bid(price=price,author=user,auction=auction)
                newOffer.save()
                auction.price=price
                auction.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "send_group",
                        "form_type": data["type"],
                        "value": data["value"],
                        "user": user.username,
                        "img": user.img.url
                    }
                )
                return

        com=Comment(text=data["value"],author=user,auction=auction)
        com.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"send_group",
                "form_type": data["type"],
                "value": data["value"],
                "user": user.username,
                "img": user.img.url
            }
        )

    def send_group(self,event):

        self.send(text_data=json.dumps({
            'type': event["form_type"],
            "value":event["value"],
            "user":event["user"],
            "img":event["img"]
        }))

    def send_error(self,event):

        self.send(text_data=json.dumps({
            'type': "error",
            "value":event["value"]
        }))
