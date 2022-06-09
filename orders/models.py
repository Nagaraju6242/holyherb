from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save,post_save
from holyherb.utils import unique_order_id_generator
from django.contrib.auth import get_user_model
from addresses.models import Address
from analytics.models import OrderedQuantity
from products.models import ProductSku
from utm_tracker.models import LeadSource
import math,string,random
import datetime
from customization.utils import send_shiprocket_req
import json
# Create your models here.

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)

class OrderManager(models.Manager):
    def send_neworder(self,order_obj):
        data = {
            "order_id" : order_obj.order_id,
            "order_date" : order_obj.timestamp.strftime("%Y-%m-%d"),
            "pickup_location" : "HOLYHERB",
            "billing_customer_name" : order_obj.shipping_address.first_name,
            "billing_last_name" : order_obj.shipping_address.last_name,
            "billing_address" : order_obj.shipping_address.address_line_1,
            "billing_city" : order_obj.shipping_address.city,
            "billing_pincode" : int(order_obj.shipping_address.postal_code),
            "billing_state" : order_obj.shipping_address.state,
            "billing_country" : order_obj.shipping_address.country,
            "billing_email" : order_obj.shipping_address.email,
            "billing_phone" : int(order_obj.shipping_address.phone_number),
            "shipping_is_billing" : 1,
            "order_items": [],
            "payment_method" : "COD" if order_obj.shipping_method.name == "cod" else "Prepaid" ,
            "sub_total" : int(order_obj.total),
            "length" : float(order_obj.length),
            "breadth" : float(order_obj.breadth),
            "height" : float(order_obj.height),
            "weight" : float(order_obj.weight),
        }
        for item in order_obj.cart.items.all():
            try:
                sku = ProductSku.objects.filter(product=item.product,quantity=item.quantity_price.first()).first().sku
            except:
                sku = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
            data["order_items"].append(
                {
                    "name": item.product.title + " " + item.product.flavour if item.product.flavour else "",
                    "sku": sku,
                    "units": int(item.quantity),
                    "selling_price": int(item.price),
                }
            )
        data = json.dumps(data)
        res = send_shiprocket_req("https://apiv2.shiprocket.in/v1/external/orders/create/adhoc",data,"post")
        return res


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=30,help_text="This is the code the user needs to use to get discount")
    title = models.CharField(max_length=120)
    expiry = models.DateTimeField()
    percent_discount = models.DecimalField(max_digits=10,decimal_places=2)
    max_discount = models.DecimalField(max_digits=10,decimal_places=2,help_text="Set this to a large value if you don't want a max discount")
    min_order_amount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(blank=True,null=True,help_text="This will appear as remarks in the website")

    def __str__(self):
        return self.coupon_code

class ShippingMethod(models.Model):
    name = models.CharField(max_length=120,help_text="This is for the functionality don't change it")
    title = models.CharField(max_length=200)
    min_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    percent = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    has_fixed_price = models.BooleanField(default=False,help_text="Either use fixed price or percent discount with min price")
    fixed_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user     = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    is_user  = models.BooleanField(null=True,blank=True,default=False)
    order_id = models.CharField(max_length=120,blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=120,blank=True,null=True)
    cart     = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status   = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    coupon_code = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    coupon_discount = models.DecimalField(default=0,max_digits=10,decimal_places=2,null=True,blank=True)
    shipping_total = models.DecimalField(max_digits=100,decimal_places=2,default=0,null=True,blank=True)
    shipping_method = models.ForeignKey(ShippingMethod,on_delete=models.SET_NULL,null=True,blank=True)
    total = models.DecimalField(max_digits=100,decimal_places=2,default=0)
    shipping_address    = models.ForeignKey(Address, related_name="shipping_address",null=True, blank=True,on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(null=True,blank=True)
    length = models.CharField(blank=True,null=True,max_length=200,help_text="The length of the item in cms. Must be more than 0.5.")
    breadth = models.CharField(blank=True,null=True,max_length=200,help_text="The breadth of the item in cms. Must be more than 0.5.")
    height = models.CharField(blank=True,null=True,max_length=200,help_text="The height of the item in cms. Must be more than 0.5.")
    weight = models.CharField(blank=True,null=True,max_length=200,help_text="The weight of the item in kgs. Must be more than 0.")
    shipment_id = models.CharField(max_length=120,null=True,blank=True)
    utm = models.ForeignKey(LeadSource,on_delete=models.CASCADE,blank=True,null=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total , shipping_total])
        if self.coupon_code:
            coupon = self.coupon_code
            expiry_date = coupon.expiry.replace(tzinfo=None)
            if coupon.min_order_amount <= cart_total and datetime.datetime.now() < expiry_date:
                discount = (cart_total * coupon.percent_discount) / 100
                discount = min(discount,coupon.max_discount)
            else:
                self.coupon_code = None
                discount = 0
            self.coupon_discount = discount
            new_total = new_total - float(discount) + float(self.shipping_total)
        else:
            self.coupon_discount = 0
        formatted_total = format(new_total,'.2f')
        self.total = formatted_total
        self.save()
        return formatted_total

    def check_done(self):
        shipping_address = self.shipping_address
        total = self.total
        if shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        items = self.cart.items.all()
        for item in items:
            oq,created = OrderedQuantity.objects.get_or_create(product=item.product)    
            oq.ordered_quantity += item.quantity
            oq.save()
        return self.status


def pre_save_create_order_id(sender,instance,*args,**kwargs):

    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    if instance.shipping_method:
        method = instance.shipping_method
        if(instance.cart.total >= 1500):
            instance.shipping_total = 0
        elif(method.has_fixed_price):
            instance.shipping_total = int(method.fixed_price)
        else:
            instance.shipping_total = int(max(method.min_price,(method.percent * instance.cart.total) / 100))
    else:
        instance.shipping_total = 0
    instance.total = instance.cart.total - instance.coupon_discount + instance.shipping_total



pre_save.connect(pre_save_create_order_id,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)