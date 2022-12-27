from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import Code


class CodeForm(forms.ModelForm):
    number = forms.CharField(label=_('Код подтверждения'), help_text=_('Введите код отправленный на email'))

    class Meta:
        model = Code
        fields = ('number',)
