from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    total_balance = models.IntegerField(default=0)


class Bank(models.Model):
    title = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    def __str__(self):
        return f'{self.title}'


class Account(models.Model):
    iban = models.CharField(max_length=25, unique=True)
    balance = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, default='1')


class Record(models.Model):
    amount = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.amount} {self.description}'
