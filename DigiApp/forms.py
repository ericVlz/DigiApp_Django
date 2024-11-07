from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Documento, Tag



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']




class DocumentoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'})
    )

    class Meta:
        model = Documento
        fields = ['nombre', 'archivo', 'propietario', 'tags']


        