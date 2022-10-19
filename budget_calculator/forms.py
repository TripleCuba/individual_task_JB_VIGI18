from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import User, Account, Record


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['iban', 'bank', 'user']
        widgets = {
            'bank': forms.Select(attrs={'class': 'form-select form-select-lg'})
        }


class AddRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['amount', 'account', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateBalanceForm(ModelForm):
    class Meta:
        model = Account
        fields = ['balance']


class UserTotalBalanceForm(ModelForm):
    class Meta:
        model = User
        fields = ['total_balance']
