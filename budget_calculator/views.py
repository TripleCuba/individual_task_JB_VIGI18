from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm, AddAccountForm, AddRecordForm, UpdateBalanceForm, UserTotalBalanceForm
from .models import Account, Record, Bank, User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import random


def update_total_balance(request):
    user = User.objects.filter(id=request.user.id).first()
    user_accounts = Account.objects.filter(user=request.user.id).all()
    total_balance = 0
    for account in user_accounts:
        total_balance += account.balance
    update_balance_form = UserTotalBalanceForm({'total_balance': total_balance}, instance=user)
    update_balance_form.save()


def update_balance(id):
    account_records = Record.objects.filter(account=id).all()
    total_balance = 0
    for record in account_records:
        total_balance += record.amount
    account = Account.objects.filter(id=id).first()
    account.balance = total_balance
    update_form = UpdateBalanceForm({'balance': account.balance}, instance=account)
    update_form.save()


def index(request):
    if request.user.is_authenticated:
        update_total_balance(request)
    return render(request, 'index.html')


def sign_up(request):
    form = SignUpForm
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'registration/sign_up.html', context=context)


@login_required(login_url='/registration/login')
def add_account(request):
    form = AddAccountForm()
    if request.method == 'POST':
        # Auto generating IBAN taking bank code part and adding unique ending to account iban
        bank_obj = Bank.objects.filter(id=request.POST['bank']).first()
        bank_code_part = str(bank_obj.code)[0:5]
        iban_start = f'LT11{bank_code_part}010'
        rng = random.randint(10000, 99999)
        iban = iban_start + str(rng)
        request_data = request.POST.copy()
        request_data['user'] = request.user.id
        request_data['iban'] = iban
        form = AddAccountForm(request_data)
        form.save()
        return redirect(reverse('index'))

    context = {
        'form': form
    }
    return render(request, 'add_account.html', context=context)


@login_required(login_url='/registration/login')
def show_accounts(request):
    data = Account.objects.filter(user=request.user.id)
    context = {
        'data': data
    }
    return render(request, 'show_accounts.html', context=context)


@login_required(login_url='/registration/login')
def show_account(request, id):
    account = Account.objects.filter(id=id).first()
    if not account or account.user.id != request.user.id:
        return redirect(reverse('show_accounts'))
    records = Record.objects.filter(account=account)
    income = 0
    outcome = 0
    for record in records:
        if record.amount >= 0:
            income += record.amount
        else:
            outcome += record.amount

    context = {
        'data': account,
        'income': income,
        'outcome': outcome
    }
    return render(request, 'show_account.html', context=context)


@login_required(login_url='/registration/login')
def add_record(request, id):
    account_validator = Account.objects.filter(id=id).first()
    if not account_validator or account_validator.user.id != request.user.id:
        return redirect(reverse('show_accounts'))
    form = AddRecordForm()
    if request.method == 'POST':
        # adding new record for specific account
        request_data = request.POST.copy()
        request_data['account'] = id
        form = AddRecordForm(request_data)
        form.save()
        # updating balance in that account and user
        update_balance(id)
        update_total_balance(request)
        return redirect('show_records_history', id=id)
    context = {
        'form': form,
        'page_id': id
    }
    return render(request, 'add_record.html', context=context)


@login_required(login_url='/registration/login')
def show_records_history(request, id):
    account_validator = Account.objects.filter(id=id).first()
    if not account_validator or account_validator.user.id != request.user.id:
        return redirect(reverse('show_accounts'))
    update_total_balance(request)
    data = Record.objects.filter(account=id).order_by('-date').all()
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'data': page_obj,
        'page_id': id
    }
    return render(request, 'show_records_history.html', context=context)
