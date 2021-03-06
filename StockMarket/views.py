from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Stock, Query
from django.http import JsonResponse
from django.contrib import messages


def home(request):
    messages.warning(request, f'Login to Stock Market for checking Stocks')
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
    return render(request, 'register.html', {'form': form, 'title': 'Register'})


@login_required
def StockMarket(request):
    if request.method == "POST" and request.POST['action']=='search':
        search = request.POST['search']
        stock_obj = Stock.objects.filter(title=search)[0:2]
        total_obj = Stock.objects.filter(title=search).count()
    else:
        stock_obj = Stock.objects.all()[0:5]
        total_obj = Stock.objects.count()
    return render(request, 'StockMarket.html', context={'Stocks': stock_obj, 'total_obj': total_obj})


def load_more(request):
    loaded_item = request.GET.get('loaded_item')
    loaded_item_int = int(loaded_item)
    limit = 5
    stock_obj = list(Stock.objects.values()[loaded_item_int:loaded_item_int + limit])
    data = {'Stocks': stock_obj}
    return JsonResponse(data=data)


def details(request, id_num):
    if request.method == "POST":
        if request.POST['action'] == 'back':
            return redirect('StockMarket')
        elif request.POST['action'] == 'query':
            stock_id = request.POST['stock_id']
            return redirect('query',stock_id)

    stock = Stock.objects.filter(id=id_num).values()
    desc = stock[0]['desc'].split(',')
    return render(request, 'details.html', context={'stock': stock[0],'desc': desc, 'title': 'Details'})


def query(request, id_num):
    if request.method == "POST":
        if request.POST['action'] == 'back':
            pass
        elif request.POST['action'] == 'submit':
            stockname = request.POST['stockname']
            username = request.POST['username']
            query = request.POST['query']
            query_obj = Query(stockname=stockname, username=username, query=query)
            query_obj.save()
        return redirect('StockMarket')

    stock = Stock.objects.filter(id=id_num).values()
    return render(request, 'query.html', context={'stock': stock[0], 'title': 'Query'})
