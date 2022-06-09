from django.shortcuts import render,redirect
from carts.models import Cart
from .models import Order,ShippingMethod,Coupon
from django.http import JsonResponse
from datetime import datetime

# Create your views here.


def shipping_method_reuse(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
    shipping_method_id = request.POST.get("shipping-method",None)
    if(shipping_method_id and len(shipping_method_id) > 0):
        shipping_method = ShippingMethod.objects.filter(id=shipping_method_id[0])
        if(shipping_method.exists()):
            shipping_method = shipping_method.first()
            order_obj.shipping_method = shipping_method
            order_obj.save()
    return redirect("checkout")

def remove_shipping(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
    if(order_obj):
        order_obj.shipping_address = None
        order_obj.save()
    return redirect("checkout")

def remove_payment(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
    if(order_obj):
        order_obj.shipping_method = None
        order_obj.save()
    return redirect("checkout")

def add_coupon_api(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
    coupon = request.POST.get("coupon_code")
    added = False
    error = ""
    if(order_obj):
        if(coupon):
            coupons = Coupon.objects.filter(coupon_code__iexact=coupon)
            if(coupons.exists()):
                coupon = coupons.first()
                expiry_date = coupon.expiry.replace(tzinfo=None)
                if(datetime.now() > expiry_date):
                    error = "Coupon Expired"
                    return JsonResponse({"added" : added,"error":error})
                if(cart_obj.total < coupon.min_order_amount):
                    error = "Minimum order of Rs %s is required" % (str(coupon.min_order_amount))
                    return JsonResponse({"added" : added,"error":error})
                added = True
                order_obj.coupon_code = coupon
                order_obj.update_total()
            else:
                error = "Invalid Coupon Code"
                JsonResponse({"added" : added,"error":error})
    return JsonResponse({"added" : added,"error":error})

def remove_coupon_api(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,status="created")
    if(order_obj):
        if(order_obj.coupon_code):
            order_obj.coupon_code = None
            order_obj.save()
            order_obj.update_total()
            return JsonResponse({"removed" : True,"error":""})
        return JsonResponse({"removed":False,"error":"Coupon not found"})
    return JsonResponse({"removed":False,"error":"Order not found"})
    
