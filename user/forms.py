from django import forms

class UserLoginForm(forms.Form):
    userqq = forms.CharField(label="QQ", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "QQ"}))
    password = forms.CharField(label="密码(不是QQ密码)", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "密码(不是QQ密码)"}))

class SetPasswordForm(forms.Form):
    password = forms.CharField(label="新的登录密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "新的登录密码"}))
    retype_password = forms.CharField(label="再输入一遍", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "再输入一遍"}))
