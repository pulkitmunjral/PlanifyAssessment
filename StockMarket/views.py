from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from .models import Stock, Query
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def StockMarket(request):
    if request.method == "POST" and request.POST['action']=='search':
        search = request.POST['search']
        stock_obj = Stock.objects.filter(title=search)[0:2]
        total_obj = Stock.objects.filter(title=search).count()
    else:
        stock_obj = Stock.objects.all()[0:2]
        total_obj = Stock.objects.count()
    return render(request, 'StockMarket.html', context={'Stocks': stock_obj, 'total_obj': total_obj})


def load_more(request):
    loaded_item = request.GET.get('loaded_item')
    loaded_item_int = int(loaded_item)
    limit = 2
    stock_obj = list(Stock.objects.values()[loaded_item_int:loaded_item_int + limit])
    data = {'Stocks': stock_obj}
    return JsonResponse(data=data)


def details(request, id_num):
    if request.method == "POST" and request.POST['action'] == 'back':
        return redirect('StockMarket')

    stock = Stock.objects.filter(id=id_num).values()
    return render(request, 'details.html', context={'Stocks': stock})


def query(request, id_num):
    if request.method == "POST":
        if request.POST['action'] == 'back':
            pass
        elif request.POST['action'] == 'submit':
            stockname = request.POST['StockName']
            username = request.POST['UserName']
            query = request.POST['query']
            query_obj = Query(stockname=stockname, username=username, query=query)
            query_obj.save()
        return redirect('StockMarket')
    stock = Stock.objects.filter(id=id_num).values()
    return render(request, 'details.html', context={'Stocks': stock})
