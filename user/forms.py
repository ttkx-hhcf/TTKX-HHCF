from django import forms
from .models import *


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="姓名", max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机", max_length=11,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="地址", max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 用户名验证
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 6:
            raise forms.ValidationError("用户名必须是6个字符以上！！")
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长啦！！")
        else:
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:  # 证明该用户存在
                raise forms.ValidationError("用户名已存在！！")
        return username

    # 密码验证
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("密码太短了！！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长了！！")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码输入不匹配！！")
        return password2

    # 验证名字
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("姓名必须是2个字符以上！！")
        elif len(name) > 50:
            raise forms.ValidationError("姓名太长啦！！")
        else:
            filter_result = User.objects.filter(name=name)
            if len(filter_result) > 0:  # 证明该姓名存在
                raise forms.ValidationError("姓名已存在！！")
        return name

    # 手机验证
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise forms.ValidationError("手机号长度错误！！")
        filter_result = User.objects.filter(phone=phone)
        if len(filter_result) > 0:
            raise forms.ValidationError("手机号已存在！！")
        return phone


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# 编辑信息
class EditForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['password', 'name', 'email', 'address', 'phone']
        labels = {
            'password': '密码',
            'name': '名字',
            'email': '邮箱',
            'address': '地址',
            'phone': '手机号'
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'})
        }




