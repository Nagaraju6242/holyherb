from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

class Pixel(models.Model):
    name = models.CharField(max_length=120)
    pixel_id = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class OrderedQuantity(models.Model):
    product = models.OneToOneField("products.Product",unique=True,on_delete=models.SET_NULL,null=True,blank=True)
    ordered_quantity = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.product.title

    class Meta:
        ordering = ["-ordered_quantity"]
        verbose_name_plural = "Ordered Quantities"


def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    try:
        ip_address = get_client_ip(request)
    except:
        pass
    new_view_instance = ObjectViewed.objects.create(
                user= request.user if request.user.is_authenticated else None , 
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )

object_viewed_signal.connect(object_viewed_receiver)