from django import forms

class UserLoginForm(forms.Form):
    user_qq = forms.CharField(label="QQ：", max_length=20)
    password = forms.CharField(label="密码(不是QQ密码)：", max_length=20, widget=forms.PasswordInput)