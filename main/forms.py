from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.widgets import PasswordInput, TextInput, NumberInput
from .models import *

from django import forms
from django.forms import TextInput, PasswordInput

class AuthForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'grade', 'house', 'password']





class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['Position_name', 'House', 'Grades_voting']


class UploadFileForm(forms.Form):
    file = forms.FileField()




from django import forms
from .models import Candidate, Position

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['Candidate_name', 'position', 'Photo', 'House']
        widgets = {
            'Photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'House': forms.TextInput(attrs={'class': 'form-control'}),
        }
