from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record

from django import forms
from .models import Lead

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

#  Register/Create a user
class CreateUserForm(UserCreationForm):
   class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']


    

# Login a user
class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=TextInput())
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Create a record
class CreateRecordForm(forms.ModelForm):
    class Meta:
       model = Record
       fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'country']



# Update a record
class UpdateRecordForm(forms.ModelForm):
    class Meta:
       model = Record
       fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'country']


# Lead form

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'status',
            'assigned_to'
        ]




# Update a lead

class UpdateLeadForm(forms.ModelForm):
     class Meta:
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'status',
            'assigned_to'
        ]

