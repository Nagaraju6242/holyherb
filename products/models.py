from django.db import models
from django.db.models.signals import pre_save,post_save
from holyherb.utils import unique_slug_generator
from django.urls import reverse
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from analytics.models import OrderedQuantity
User = get_user_model()

PRODUCT_QTY_PRICE_CHOICES = (
    ('gm','GM'),
    ('ml','ML'),
    ('pcs','Pieces'),
)

PRODUCT_CATEGORY_CHOICES = (
    ('haircare','Hair Care'),
    ('facecare','Face Care'),
    ('bodycare','Body Care'),
    ('gifting','Gifting')
)

REVIEW_CHOICES = (
    ('1','Terrible'),
    ('2','Poor'),
    ('3','Average'),
    ('4','Very Good'),
    ('5','Excellent'),
)

# Create your models here.

class ProductManager(models.Manager):
    def order_lth(self,products=None):
        if products == None : return []
        try:
            return sorted(products,key=lambda n : n.quantity_price.last().price)
        except:
            return products

    def order_htl(self,products=None):
        if products == None : return []
        try:
            return sorted(products,key=lambda n : n.quantity_price.last().price,reverse=True)
        except:
            return products

    def order_atz(self,products=None,category=None):
        if products == None : return []
        try:
            if category:
                return sorted(products,key=lambda n : n.title)
            return sorted(products,key=lambda n : n.title + n.flavour)
        except:
            return products


    def order_zta(self,products=None,category=None):
        if products == None : return []
        try:    
            if category:
                return sorted(products,key=lambda n : n.title,reverse=True)
            return sorted(products,key=lambda n : n.title + n.flavour,reverse=True)
        except:
            return products

    def order_otn(self,products=None):
        if products == None : return []
        try:
            return products
        except:
            return products

    def order_nto(self,products=None):
        if products == None : return []
        try:
            new_products = reversed(products)
            return list(new_products)
        except:
            return products

    def order_bytrending(self,products):
        products = list(products)
        all_qs = reversed(OrderedQuantity.objects.all())
        for i in all_qs:
            if i.product in products:
                products.insert(0, products.pop(products.index(i.product)))
        return products


class Quantity_Price(models.Model):
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity_type = models.CharField(max_length=100,default="gm",choices=PRODUCT_QTY_PRICE_CHOICES)

    def __str__(self):
        return str(self.quantity) + self.quantity_type + " -- " + str(self.price)

    class Meta:
        ordering = ("-price",)


class Product(models.Model):
    title           = models.CharField(max_length=120)
    category        = models.CharField(max_length=100,choices=PRODUCT_CATEGORY_CHOICES,default="haircare",blank=True,null=True)
    slug            = models.SlugField(unique=True,blank=True)
    flavour         = models.CharField(max_length=120,null=True,blank=True)
    description     = models.TextField()
    quantity_price  = models.ManyToManyField(Quantity_Price,blank=True)
    avg_rating      = models.IntegerField(default=0,null=True,blank=True)
    handpicked      = models.BooleanField(default=False)
    has_multiple_quantity_images = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return self.title + " -- " +  self.flavour if self.flavour else self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug" : self.slug})

    def get_main_image_url(self):
        if self.images.filter(main_image=True).exists():
            return self.images.filter(main_image=True).first().image.url
        if self.images.exists():
            return self.images.first().image.url
        return None
    def get_artistic_image_url(self):
        if self.images.filter(artistic=True).exists():
            return self.images.filter(artistic=True).first().image.url
        return None
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "products/" ,null=True,blank=True)
    artistic = models.BooleanField(default=False)
    main_image = models.BooleanField(default=False)
    quantity = models.ForeignKey(Quantity_Price,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        if self.product.flavour:
            return self.product.title + " -- " + self.product.flavour
        return self.product.title

    class Meta:
        ordering = ['artistic','main_image','quantity']


class ProductSku(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.ForeignKey(Quantity_Price,on_delete=models.SET_NULL,null=True)
    sku = models.CharField(max_length=50)

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name = "Product Sku"
        verbose_name_plural = "Products Sku"


class Review(models.Model):
    product = models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
    rating = models.CharField(max_length=100,choices=REVIEW_CHOICES,blank=True,null=True)
    description = models.TextField()
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    number = models.CharField(max_length=20,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    inappropriate = models.BooleanField(default=False)

    def __str__(self):
        return self.rating


def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.slug: 
        instance.slug = unique_slug_generator(instance) 

def post_save_revire_receiver(sender, instance, *args, **kwargs):
    product = instance.product
    all_reviews = product.reviews.all()
    ratings = [int(r.rating) for r in all_reviews]
    avg_rating = int(sum(ratings) / len(ratings))
    product.avg_rating = avg_rating
    product.save()

pre_save.connect(pre_save_receiver, sender = Product) 
post_save.connect(post_save_revire_receiver, sender = Review)