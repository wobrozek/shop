from django.contrib import admin
from .models import Comment, Bid ,Auction ,User

admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Auction)
admin.site.register(User)