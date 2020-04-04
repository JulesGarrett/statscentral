from django import forms
from django.contrib.auth.models import User
from .models import Account

class UserForm(forms.ModelForm):
  class Meta:
      model = Account
      fields = (
        'current_city',
          )
