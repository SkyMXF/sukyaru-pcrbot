from django import forms

class UserLoginForm(forms.Form):
    userqq = forms.CharField(label="QQ：", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "QQ",'autofocus': ''}))
    password = forms.CharField(label="密码(不是QQ密码)：", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "密码(不是QQ密码)"}))