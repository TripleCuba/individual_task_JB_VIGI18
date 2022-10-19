from django.contrib import admin
from .models import User, Account, Bank, Record

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Record)
