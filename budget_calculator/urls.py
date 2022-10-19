from django.urls import path
from .views import index, sign_up,add_account, show_accounts, show_account, add_record, show_records_history

urlpatterns = [
    path('', index, name='index'),
    path('sign_up', sign_up, name='sign_up'),
    path('add_account', add_account, name='add_account'),
    path('add_record/<id>', add_record, name='add_record'),
    path('accounts', show_accounts, name='show_accounts'),
    path('account/<id>', show_account, name='show_account'),
    path('records_history/<id>', show_records_history, name='show_records_history')
]
