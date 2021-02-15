from django import forms

from .models import CustomUser


class UserLoginForm(forms.ModelForm):
    """Форма для получения номера телефона"""

    class Meta:
        model = CustomUser
        fields = ('phone',)
        labels = {
            'phone': 'Введите свой номер телефона'
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['phone'] = self.data.get('phone')[2:]
        return cleaned_data


class FakeSmsAuthForm(forms.Form):
    """Форма для фековых смс-кодов"""

    sms_code = forms.IntegerField(label='Введите смс код, который вам пришел', required=False)


class InviteCodeForm(forms.ModelForm):
    """Форма для добавления инвайт-кода"""

    referrer_code = forms.CharField(label='Введите инвайт-код вашего реферрала', max_length=7, required=True)

    class Meta:
        model = CustomUser
        fields = ('referrer_code',)

    def is_valid(self):
        invite_code = self.data.get('referrer_code')
        existing = CustomUser.objects.filter(invite_code=invite_code).exists()
        return existing
