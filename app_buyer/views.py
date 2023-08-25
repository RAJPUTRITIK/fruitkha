from django.shortcuts import render,redirect
from .models import *
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from seller_app.models import *
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        try:
            user_data=User.objects.get(email=request.POST["email"])
            return render(request,'register.html',{'msg':'user already exists'})
        except:
            if request.POST['password'] == request.POST['confirm_password']:
                global fotp
                fotp=random.randint(100000,999999)
                subject = 'Otp verification Process'
                message = f'Thanks for choosing us your otp is {fotp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                
                global temp
                temp={
                    'name':request.POST['name'],
                    'email':request.POST['email'],
                    'password':request.POST['password']
                }
                return render(request,'otp.html')
            else:
                return render(request,'register.html',{'msg':'password and confirm password not match'})
    else:
        return render(request,'register.html')


def otp(request):
    if request.method=='POST':
        if request.POST['otp']:
            # otp= request.POST['otp']
            # if otp=='': 
                # return render(request,'otp.html',{'msg':'please enter otp first'})
            # else: 
            if fotp==int(request.POST['otp']):
                    User.objects.create(
                    firstname=temp['name'],
                    email=temp['email'],
                    password=make_password(temp['password'])
                )
                    return render(request,'register.html',{'msg':'registration successfully'})
            else:
                    
                return render(request,'otp.html',{'msg':'otp not matched'}) 
        else:
            return render(request,'otp.html',{'msg':'otp daal kute'})   
    else:
        return render(request,'otp.html')






def login(request):
    if request.method=='POST':
        try:
            user_data=User.objects.get(email=request.POST['email'])
            # if user_data.password==request.POST['password']:
            if check_password(request.POST['password'],user_data.password):
                request.session['email']=request.POST['email']
                session_data=User.objects.get(email=request.session['email'])
                return render(request,'shop.html',{'session_data':session_data})
            else:
                return render(request,'login.html',{'msg':'password not matched'})
        except:
            return render(request,'login.html',{'msg':'user not exist'})
    else:
        return render(request,'login.html')


def logout(request):
    try:
        del request.session['email']
        return render(login)
    except:
        return render(request,'login.html',{'msg':'logout succeccfully'})

def profile(request):
    if request.method=='POST':
        session_data=User.objects.get(email=request.session['email'])
        try:
            image_data=request.FILES['pic']
        except:
            image_data=session_data.propic
        if request.POST['oldpassword'] and request.POST['newpassword'] and request.POST['confirm_password']:
            if check_password(request.POST['oldpassword'],session_data.password):
                if request.POST['newpassword'] == request.POST['confirm_password']:
                    session_data.firstname=request.POST['name']
                    session_data.propic=image_data
                    session_data.password=make_password(request.POST['newpassword'])
                    session_data.save()
                    return render(request,'profile.html',{'msg':'updated successfully'})
                else:
                    return render(request,'profile.html',{'session_data':session_data,'msg':'new password and new confirm password not match'})
            else:
                return render(request,'profile.html',{'session_data':session_data,'msg':'your old password not match'})
        else:
            session_data.firstname=request.POST['name']
            session_data.propic=image_data
            session_data.save()
            return render(request,'profile.html',{'session_data':session_data,'msg':'Profile updated successfully'})
    else:
        # request.session['email']=request.POST['email']
        session_data=User.objects.get(email=request.session['email'])
        return render(request,'profile.html',{'session_data':session_data})



def contact(request):
    return render(request,'contact.html')

def single_product(request,pk):
    session_data=User.objects.get(email=request.session['email'])
    one_data=Product.objects.get(id=pk)
    return render(request,'single-product.html',{'one_data':one_data,'session_data':session_data})



def shop(request):
    session_data=User.objects.get(email=request.session['email'])
    all_product=Product.objects.all()
    return render(request,'shop.html',{'all_product':all_product,'session_data':session_data})


def add_to_cart(request,pk):
    session_data=User.objects.get(email=request.session['email'])
    myproduct=Product.objects.get(id=pk)
    try:
        mycart=Cart.objects.get(Q(product=myproduct) & Q(buyer=session_data))
        mycart.quantity+=1
        mycart.total=mycart.quantity*mycart.product.price
        mycart.save()
    except:
        Cart.objects.create(
            product=myproduct,
            buyer=session_data,
            quantity=1,
            total=myproduct.price*1
        )
    return shop(request)



def showcart(request):
    session_data=User.objects.get(email=request.session['email'])
    all_cart=Cart.objects.filter(buyer=session_data)
    final_total=0
    for i in all_cart:
        final_total+=i.total
    return render(request,'cart.html',{'all_cart':all_cart,'final_total':final_total,'session_data':session_data})


def update_cart(request):
    if request.method=='POST':
        session_data=User.objects.get(email=request.session['email'])
        all_cart=Cart.objects.filter(buyer=session_data)
        all_quantity=request.POST.getlist("quantity")
        print(all_quantity)
        for i,j in zip(all_cart,all_quantity):
            i.quantity=int(j)
            i.total=i.quantity*i.product.price
            i.save()
        return showcart(request)


def delete_cart(request,pk):
    session_data=User.objects.get(email=request.session['email'])
    one_cart=Cart.objects.get(id=pk)
    one_cart.delete()
    return redirect(showcart)


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    

def search(request):
    # session_data=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        data=request.POST['ser']
        all_product=Product.objects.filter(Q(pname__icontains=data) | Q(desc__icontains=data))
        return render(request,'shop.html',{'all_product':all_product})
    else:
        return redirect('shop')