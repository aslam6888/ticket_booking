from django import forms
from .models import seat_booking,trains,train_charts

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class registration_form(UserCreationForm):
    class Meta:
        model=User
        fields =['username','email']
class passenger_form(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'form-control col'}))
    age= forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control col'}))
    gender = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'form-control col'}))
    address=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'form-control col'}))
    phone=forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control col'}))

class train_form(forms.ModelForm):
    class Meta:
        model= trains
        fields="__all__"

class chart_form(forms.ModelForm):
    class Meta:
        model= train_charts
        exclude=["seats"]