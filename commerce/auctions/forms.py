from django import forms
from django.forms import ModelForm, NumberInput, ValidationError
from .models import Bid, Auction, Comment, User
from datetime import datetime

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'img', 'price', 'category', 'endDate')
        labels = {
            'endDate':'End date of auction'
        }
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'img':forms.FileInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'endDate':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'})
        }
    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price<0:
            raise ValidationError("The price must be greater than zero")
        
        return price

    def clean_endDate(self):
        endDate = self.cleaned_data.get("endDate")

        if endDate < datetime.now(endDate.tzinfo):
            raise ValidationError("The end of auction date must be in the future")
       
        return endDate


class BidForm(ModelForm):
    class Meta():
        model=Bid
        fields=('price',)

        labels={
            'price':'Your offert',
        }
        widgets={
            'price':forms.NumberInput(attrs={'class':'form-control'}),
        }

    
    def clean_price(self):
        return AuctionForm.clean_price(self)

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields=('text',)

        labels={
        'text':"Add comment"
        }

        widgets={
            'text':forms.TextInput(attrs={'class':'form-control'})
        }

class EditProfileForm(ModelForm):
    class Meta():
        model= User
        fields=('username','email','img')

        widgets={
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "img": forms.FileInput(attrs={'class': 'form-control'})
        }





