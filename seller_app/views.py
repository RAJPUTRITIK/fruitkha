from django.shortcuts import render
from .models import *
# Create your views here.
def seller_index(request):
    return render(request,'seller_index.html')

def seller_register(request):
    if request.method=='POST':
        try:
            Seller_User.objects.get(email=request.POST['email'])
            return render(request,'seller_register.html',{'msg':'User already exists'})
        except:
            Seller_User.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            return render(request,'seller_register.html',{'msg':'seller account register successfully'})
    else:
        return render(request,'seller_register.html')


def seller_login(request):
    if request.method=='POST':
        try:
            one_d=Seller_User.objects.get(email=request.POST['email'])
            request.session['email']=request.POST['email']
            session_data=Seller_User.objects.get(email=request.session['email'])
            return render(request,'seller_shop.html',{'session_data':session_data})
        except:
            return render(request,'seller_login.html',{'msg':'USER NOT EXISTS'})
    else:
        return render(request,'seller_login.html')
    
def add_product(request):
    if request.method=='POST':
        session_data=Seller_User.objects.get(email=request.session['email'])
        Product.objects.create(
            pname=request.POST['pname'],
            price=request.POST['price'],
            p_quantity=request.POST['quantity'],
            desc=request.POST['desc'],
            pimage=request.FILES['pro_pic'],
            seller=session_data
        )
        return render(request,'add_product.html',{'msg':'Your product added successfully','session_data':session_data})
    else:
        session_data=Seller_User.objects.get(email=request.session['email'])
        return render(request,'add_product.html')


def seller_logout(request):
    del request.session['email']
    return render(request,'seller_login.html',{'msg':'successfully logout'})