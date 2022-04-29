from django.contrib.auth.forms import UserCreationForm, User
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Account, Post


class CreateArticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'photo': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        }
        labels = {
            'title': '標題',
            'content': '內文',
            'photo': '照片',
            'location': '地址'
        }


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_('電子信箱'),
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        error_messages={
            'invalid': '請輸入有效電子信箱',
            'required': '尚未輸入電子信箱',
        }
    )
    password1 = forms.CharField(
        label=_('密碼'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={'required': '尚未輸入密碼'},
    )
    password2 = forms.CharField(
        label=_('確認密碼'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={'required': '尚未輸入確認密碼'},
    )
    error_messages = {
        'password_mismatch': _('兩次密碼輸入不同'),
    }

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')


def clean_email(self):
    email = self.cleaned_data['email']
    try:
        account = Account.objects.get(email=email)
    except Exception as e:
        return email
    raise forms.ValidationError(f'{email} 已被註冊')
