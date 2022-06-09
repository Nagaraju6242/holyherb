from django.db import models
from django.db.models.signals import pre_save,post_save,m2m_changed
from django.conf import settings
from products.models import Product,Quantity_Price
import math

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get('cart_id',None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj,new_obj
    
    def get_or_none(self,request):
        cart_id = request.session.get('cart_id',None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            existed = True
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            existed = False
            cart_obj = None
        return cart_obj,existed


    def update_price(self,request,cart_obj=None):
        items = cart_obj.items.all()
        total = 0
        for item in items:
            total += item.price
        cart_obj.subtotal = total
        cart_obj.save()


    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class CartItem(models.Model):
    product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    quantity_price = models.ManyToManyField(Quantity_Price,blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)

    def __str__(self):
        try:
            x = ""
            x += self.product.title + " -- "
            if self.product.flavour:
                x += self.product.flavour + " -- "
            x += str(self.quantity) + " -- "
            if(self.quantity_price.exists()):
                y = self.quantity_price.first()
                x +=  str(y.quantity) + y.quantity_type + " -- " + str(self.price)
            return x
        except:
            return "NA"

class Cart(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem,blank=True)
    subtotal = models.DecimalField(default=0.00,max_digits=50,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=50,decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_save_cart_receiver(sender,instance,action,*args,**kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        items = instance.items.all()
        total = 0
        for item in items:
            total += item.price
        instance.subtotal = total
        instance.save()

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    if instance.subtotal > 0:
        instance.total = math.fsum([instance.subtotal , 0])
    else:
        instance.total = 0.00

def pre_save_cartitem_receiver(sender,instance,*args,**kwargs):
    if not instance.id:
        return 
    if(instance.quantity_price.exists()):
        instance.price = instance.quantity_price.first().price * int(instance.quantity)


pre_save.connect(pre_save_cartitem_receiver,sender=CartItem)
m2m_changed.connect(m2m_save_cart_receiver,sender=Cart.items.through)
pre_save.connect(pre_save_cart_receiver,sender=Cart)