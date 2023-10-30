from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from todolist.models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class CreateListForm(forms.ModelForm):
    class Meta:
        model = UserList
        fields = ['title']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-input'}),
        }

class CreateTaskForm(forms.ModelForm): # добавление нового задания
    is_finished = forms.BooleanField(required=False)
    class Meta:
        model = Task
        fields = ['content', 'is_finished']
        widgets = {
            'content':forms.TextInput(attrs={'class':'form-input'}),
        }