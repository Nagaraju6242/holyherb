from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Wishlist,JoinOurCircle
from carts.models import Cart
from products.models import Product
from orders.models import Order
from django.http import HttpResponse


from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import perform_login
from django.dispatch import receiver

User = get_user_model()
from orders.models import Order


# @receiver(pre_social_login)
# def link_to_local_user(sender, request, sociallogin, **kwargs):
#     ''' Login and redirect
#     This is done in order to tackle the situation where user's email retrieved
#     from one provider is different from already existing email in the database
#     (e.g facebook and google both use same email-id). Specifically, this is done to
#     tackle following issues:

#     '''
#     email_address = sociallogin.account.extra_data['email']
#     User = get_user_model()
#     users = User.objects.filter(email=email_address)
#     print("email_address",email_address)
#     if users:
#         # allauth.account.app_settings.EmailVerificationMethod
#         perform_login(request, users[0], email_verification='none')
#         raise ImmediateHttpResponse(redirect("/"))

def register(request):
    if(request.user.is_authenticated):
        return redirect('home')

    elif request.is_ajax():
        if(request.POST.get('password',None) == request.POST.get('password2',None)):
            username = request.POST.get('username',None)
            password = request.POST.get("password",None)
            try:
                user = User.objects.get(email = username)
                return JsonResponse({"success" : False , "errors" : "Email Already Exists"})
            except User.DoesNotExist:
                name = request.POST.get("name",None)
                number = request.POST.get("number",None)
                if(len(number) != 10):
                    return JsonResponse({"success" : False , "errors" : "Phone number must be 10 digit long"})
                try:
                    x = int(number)
                except:
                    return JsonResponse({"success" : False , "errors" : "Phonenumber cannot contain characters"})
                try:
                    validate_password(password)
                except ValidationError as error:
                    return JsonResponse({"success" : False , "errors" : ", ".join(error.messages) })
                user = User.objects.create_user(email=username,name=name,number=number,password=password)
                django_login(request, user)
                return JsonResponse({"success" : True})
                
        else:
            return JsonResponse({"success" : False , "errors" : "Passwords must match"})

    elif request.method == "POST":
        if(request.POST.get('password',None) == request.POST.get('password2',None)):
            username = request.POST.get('username',None)
            password = request.POST.get("password",None)
            try:
                user = User.objects.get(email = username)
                return render(request,'accounts/register.html' , {"errors" : "Email Already Exists"})
            except User.DoesNotExist:
                name = request.POST.get("name",None)
                number = request.POST.get("number",None)
                if(len(number) != 10):
                    return render(request,'accounts/register.html' , {"errors" : "Phone number must be 10 digit long"})
                try:
                    x = int(number)
                except:
                    return render(request,'accounts/register.html' , {"errors" : "Phonenumber cannot contain characters"})
                try:
                    validate_password(password)
                except ValidationError as error:
                    return render(request,'accounts/register.html' , {"errors" : ", ".join(error.messages)})
                user = User.objects.create_user(email=username,name=name,number=number,password=password)
                django_login(request, user)
                return redirect("home")
        else:
            return render(request,'accounts/register.html' , {"errors" : "Passwords must match"})
    return render(request,'accounts/register.html')


def login(request):
    if(request.user.is_authenticated):
        return redirect('home')
    elif request.is_ajax():
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            django_login(request, user)
            data = {"logged_in" : True }
            return JsonResponse(data)
        else:
            data = {"logged_in" : False ,"errors" : "Invalid Email or Password"}
            return JsonResponse(data)
    

    elif(request.method == "POST"):
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect("home")
        else:
            return render(request,'accounts/login.html' , {"errors" : "Invalid Login Details"})
    return render(request,'accounts/login.html')


def logout(request):
    if request.method == "POST":
        django_logout(request)
    return redirect('home')


def profile(request):
    if(request.user.is_authenticated):
        orders = Order.objects.filter(user=request.user,status = "paid")
        context = {"user" : request.user ,
                    "orders" : orders
                    }
        return render(request,"accounts/profile.html",context)
        return redirect("home")
    else:
        return redirect("login")

def orders_home(request):
    if(request.user.is_authenticated):
        orders = Order.objects.filter(user=request.user).exclude(status="created")
        orders = reversed(list(orders))
        context = {
            "logged_in" : True,
            "orders" : orders,
        }
        return render(request,"accounts/orders.html",context)
    context = {
        "logged_in" : False,
    }
    return render(request,"accounts/orders.html",context)
    
def get_cart_wishlist_api(request):
    wishlength = 0
    cartlength = 0
    if request.user.is_authenticated:
        wishlist,existed = Wishlist.objects.get_or_none(request)
        if existed:
            wishlength = len(wishlist.products.all())
    cart_obj,exsisted = Cart.objects.get_or_none(request)
    if exsisted:
        cartlength = len(cart_obj.items.all())
    return JsonResponse({
        "wishlist" : wishlength,
        "cart" : cartlength
    })


def get_wishlist_api(request):
    if request.user.is_authenticated:    
        user = request.user
        wishlist,created = Wishlist.objects.get_or_create(user=user)
        if request.is_ajax():
            d = {
                "logged_in" : True,
                "products" : []
            }
            if(created == False): 
                for product in wishlist.products.all():
                    x = {
                        "id" : product.id,
                        "title" : product.title,
                        "image" : product.images.first().image.url,
                        "price" : product.quantity_price.first().price
                    }
                    
                    if(product.images.filter(main_image=True).exists()):
                        x["image"] = product.images.filter(main_image=True).first().image.url
                    elif product.images.filter(artistic=True).exists():
                        x["image"] = product.images.filter(artistic=True).first().image.url
                    elif product.images.all().exists():
                        x["image"] = product.images.last().image.urls
                    else:
                        x["image"] = None
                    d["products"].append(x)
            return JsonResponse(d)
    else:
        if request.is_ajax():
            return JsonResponse({ "logged_in" : False })
    return redirect("/")

def toggle_to_wishlist_api(request):
    if(request.user.is_authenticated):
        product_id = request.POST.get("id",None)
        if(product_id):
            wishlist,created = Wishlist.objects.get_or_create(user=request.user)
            product = Product.objects.filter(id=product_id)
            if(product.exists()):
                product = product.first()
                if product in wishlist.products.all():
                    wishlist.products.remove(product)
                    return JsonResponse({
                        "success" : True,
                        "added" : False
                    })
                else:
                    wishlist.products.add(product)
                    return JsonResponse({
                        "success" : True,
                        "added" : True
                    })
        return JsonResponse({
                        "success" : False,
                        "added" : True
                    })
    return redirect("/")

def remove_item_from_wishlist_api(request): 
    if request.user.is_authenticated:
        removed = False
        product_id = request.POST.get("id",None)
        wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        product = Product.objects.filter(id=product_id)
        if product.exists():
            product = product.first()
        if(product in wishlist.products.all()):
            wishlist.products.remove(product)
            removed = True
        return JsonResponse({ "removed" : removed })
    return redirect("/")

def move_to_cart_api(request):
    if request.is_ajax() and request.user.is_authenticated:
        removed = False
        product_id = request.POST.get("id",None)
        wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        product = Product.objects.filter(id=product_id)
        if product.exists():
            product = product.first()
        if(product in wishlist.products.all()):
            wishlist.products.remove(product)
            removed = True
            li =  [ x.product for x in cart_obj.items.all() ]
            if product not in li:
                q_p = product.quantity_price.first()
                x = cart_obj.items.create(product=product,quantity=1,price=q_p.price)
                x.quantity_price.add(q_p)
        return JsonResponse({ "removed" : removed })
    return redirect("/")

def join_our_circle(request):
    try:
        email = request.POST.get("email",None)
        if(email):
            qs = JoinOurCircle.objects.filter(email=email)
            if(qs.exists()):
                return JsonResponse({"success" : False , "msg" : "You are Already Subscribed"})
            else:
                JoinOurCircle.objects.create(email=email)
                return JsonResponse({"success" : True})
    except:
        return JsonResponse({"success" : False , "msg" : "An error Occured"})

def download_file(request):
    filename = "joc-list.csv"
    data  = ""
    for i in JoinOurCircle.objects.all():
        data += i.email + "\n"
    fl = bytes(data,"UTF-8")
    mime_type = "text/csv"
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def update_profile_api(request):
    if request.method == "POST" and request.user.is_authenticated:
        new_name = request.POST.get("name",None)
        new_number = request.POST.get("number",None)
        old_password = request.POST.get("password",None)
        new_password = request.POST.get("password2",None)
        user = request.user
        if(new_name and new_name != ""):
            user.name = new_name
        if(new_number and new_number != ""):
            try:
                x = int(new_number)
                user.number = new_number
            except:
                return JsonResponse({"success" : False , "errors" : "Number must contain only digits" })
        if(old_password and new_password and old_password != "" and new_password != ""):
            result = user.check_password(old_password)
            if(result):
                user.set_password(new_password)
            else:
                return JsonResponse({"success" : False , "errors" : "Old password is Incorrect" })

        user.save()
        return JsonResponse({"success" : True})
    return redirect("/")