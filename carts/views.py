from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
from datetime import datetime

RAZORPAY_API_KEY = getattr(settings,"RAZORPAY_API_KEY")
RAZORPAY_SECRET_KEY = getattr(settings,"RAZORPAY_SECRET_KEY")

import razorpay 
client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_SECRET_KEY))

from products.models import Product,Quantity_Price
from .models import Cart,CartItem
from orders.models import Order
from utm_tracker.models import LeadSource

from addresses.forms import AddressForm
from addresses.models import Address
from orders.models import ShippingMethod


def update_quantity(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if request.method == "POST":   
        item_id = request.POST.get('item_id',None)
        removed = False
        item = CartItem.objects.filter(id=item_id)
        if item.exists():
            item = item.first()
        else:
            return redirect("home")
        inc_or_dec = request.POST.get('inc_or_dec',None)
        if(inc_or_dec == "inc"):
            item.quantity += 1
            if(item.quantity > 10):
                item.quantity = 10
            item.save()
        elif(inc_or_dec == "dec"):
            if(item.quantity >= 2):
                item.quantity -= 1
                item.save()
            else:
                removed = True
                item.delete()   
        if request.is_ajax():
            Cart.objects.update_price(request,cart_obj=cart_obj)
            data = {
                "removed" : removed,
                "cart_subtotal" : cart_obj.subtotal,
                "cart_total" : cart_obj.total,
            }
            if not removed:
                data["quantity"] = item.quantity
                data["price"] = item.price
            return JsonResponse(data)
    Cart.objects.update_price(request,cart_obj=cart_obj)
    return redirect("home")
   
# def update_cart_price(request):
#     cart_obj,new_obj = Cart.objects.new_or_get(request)
#     items = cart_obj.items.all()
#     total = 0
#     for item in items:
#         total += item.price
#     cart_obj.subtotal = total
#     cart_obj.save()
#     return redirect("home")

def cart_update(request):
    product_id = request.POST.get('product_id',None)
    qp_id = request.POST.get('qp_id',None)
    req_quantity = request.POST.get('quantity',1)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            if request.is_ajax():
                return JsonResponse({},status=422)
            return redirect("home")
        if qp_id is None:
            qp_id = product_obj.quantity_price.last().id
        try: 
            qp_obj = Quantity_Price.objects.get(id=qp_id)
        except Quantity_Price.DoesNotExist:
            if request.is_ajax():
                return JsonResponse({},status=422)
            return redirect("home")
        if(qp_obj in product_obj.quantity_price.all()):
            cart_obj,new_obj = Cart.objects.new_or_get(request)
            li =  [ x.product for x in cart_obj.items.all() ]
            cart_item_qs = cart_obj.items.filter(product=product_obj)
            if(cart_item_qs.exists()):
                for cart_item in cart_item_qs:
                    if(qp_obj in cart_item.quantity_price.all()):
                        cart_item.quantity += int(req_quantity)
                        if(cart_item.quantity > 10):
                            cart_item.quantity = 10
                        cart_item.save()
                        Cart.objects.update_price(request,cart_obj=cart_obj)
                        if request.is_ajax():
                            return JsonResponse({
                                "added" : False,
                                "removed" : False,
                                "increased" : True
                                })
                        return redirect("home")
            if(int(req_quantity) > 10):
                req_quantity = 10
            new_cartitem = CartItem.objects.create(product=product_obj,quantity=req_quantity,price=qp_obj.price)
            new_cartitem.quantity_price.add(qp_obj)
            cart_obj.items.add(new_cartitem)
            new_cartitem.save()
            Cart.objects.update_price(request,cart_obj=cart_obj)
            if request.is_ajax():
                json_data = {
                    "added" : True,
                    "removed" : False
                }
                return JsonResponse(json_data)
    if request.is_ajax():
        return JsonResponse({},status=422)
    return redirect("home")


def cart_home(request):
    cart_obj,existed = Cart.objects.get_or_none(request)
    if request.method == "GET":
        return redirect("home")
    if not existed:
        return JsonResponse({
            "items" : [],
            "total" : 0,
        })
    cart_obj,new_obj = Cart.objects.new_or_get(request)

    if request.is_ajax():
        d = {
            "items" : [],
            "total" : cart_obj.total,
        }
        for item in cart_obj.items.all():
            x = {
                "id" : item.id,
                "name" : item.product.title,
                "quantity" : item.quantity,
                "price" : item.price
            }
            if(item.product.images.filter(main_image=True).exists()):
                x["image"] = item.product.images.filter(main_image=True).first().image.url
            elif item.product.images.filter(artistic=True).exists():
                x["image"] = item.product.images.filter(artistic=True).first().image.url
            elif item.product.images.all().exists():
                x["image"] = item.product.images.last().image.urls
            else:
                x["image"] = None
            d["items"].append(x)

        return JsonResponse(d)
    return redirect("home")

def checkout_home(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    address_form = AddressForm()
    order_obj = None
    address_qs = None
    shipping_address_id = request.session.get("shipping_address_id",None)
    if cart_created or cart_obj.items.count() == 0:
        return redirect("home")
    else:
        order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
        if "utm_id" in request.session.keys():
            try:
                lead_source = LeadSource.objects.filter(id=request.session.get("utm_id",None))
                if(lead_source.exists()):
                    order_obj.utm = lead_source.first()
                order_obj.save()
                del request.seesion["utm_id"]
            except:
                pass
        if(request.user.is_authenticated):
            order_obj.is_user = True
            order_obj.user = request.user
            order_obj.save()
        if(shipping_address_id is None):
            if(order_obj.shipping_address):
                shipping_address_id = order_obj.shipping_address.id
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(user=request.user)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            if(request.session.get("shipping_address_id",None)):
                del request.session["shipping_address_id"]
            order_obj.save()

            if(order_obj.shipping_method and order_obj.shipping_method.name == "online_payment"):
                order_amount = int(float(order_obj.total)) * 100
                order_currency = 'INR'
                receipt = order_obj.order_id
                razorpay_order = client.order.create(dict(amount=order_amount, currency=order_currency,receipt=receipt,payment_capture = '1'))
                request.session["order_id"] = razorpay_order["id"]
                order_obj.razorpay_order_id = razorpay_order["id"]
                order_obj.save()
                context = {
                    "object" : order_obj,
                    "address_form" : address_form,
                    "address_qs" : address_qs,
                    "razorpay_order" : razorpay_order,
                    "payment_type" : order_obj.shipping_method.name
                    }
                
                return render(request,"carts/checkout.html",context)
            elif(order_obj.shipping_method and order_obj.shipping_method.name == "cod"):
                context = {
                    "object" : order_obj,
                    "address_form" : address_form,
                    "address_qs" : address_qs,
                    "payment_type" : order_obj.shipping_method.name,
                }
                return render(request,"carts/checkout.html",context)
            context = {
                "object" : order_obj,
                "shippingmethods" : ShippingMethod.objects.all()
            }
            return render(request,"carts/checkout.html",context)


        context = {"object" : order_obj,
                "address_form" : address_form,
                "address_qs" : address_qs}
        
        return render(request,"carts/checkout.html",context)

    return redirect("login")

@csrf_exempt
def checkout_done_view(request):
    if request.method == "POST":   
        cart_obj,cart_created = Cart.objects.new_or_get(request)
        order_obj_cod,new_order_obj_cod = Order.objects.get_or_create(cart=cart_obj,status="created")
        payment_method = request.POST.get("method",None)
        if payment_method == "cod":
            context = {
                    "order_obj" : order_obj_cod,
                    "status" : True,
                }
            order_obj_cod.mark_paid()
            order_obj_cod.timestamp = datetime.now()
            order_obj_cod.save()
            if(request.session.get("cart_id",None)):
                del request.session["cart_id"]
            if(request.session.get("order_id",None)):
                del request.session["order_id"]
            return render(request,"carts/checkout-done.html",context)
        try:
            razorpay_order_id = request.POST["razorpay_order_id"]
            razorpay_payment_id = request.POST["razorpay_payment_id"]
            order_obj,new_order_obj = Order.objects.get_or_create(razorpay_order_id=razorpay_order_id,status="created")
            if new_order_obj:
                return  redirect("payment_error")
            api_secret_key = RAZORPAY_SECRET_KEY
            msg = razorpay_order_id + "|" + razorpay_payment_id

            secret_key = str.encode(api_secret_key)
            total_params = str.encode(msg)
            signature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
            if(request.POST["razorpay_signature"] == signature):    
                context = {
                    "order_obj" : order_obj,
                    "status" : True,
                }
                order_obj.mark_paid()
                order_obj.timestamp = datetime.now()
                order_obj.save()
                if(request.session.get("cart_id",None)):
                    del request.session["cart_id"]
                if(request.session.get("order_id",None)):
                    del request.session["order_id"]
                return render(request,"carts/checkout-done.html",context)
            else:
                return  redirect("payment_error")
        except:
            return  redirect("payment_error")
    return redirect("cart_home")

def payment_error(request):
    return render(request,"carts/error.html")

