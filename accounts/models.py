from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser , BaseUserManager
)
# from products.models import Product

class WishlistManager(models.Manager):

    def get_or_none(self,request):
        qs = self.get_queryset().filter(user=request.user)
        if qs.count() == 1:
            existed = True
            wishlist_obj = qs.first()
            if request.user.is_authenticated and wishlist_obj.user is None:
                wishlist_obj.user = request.user
                wishlist_obj.save()
        else:
            existed = False
            wishlist_obj = None
        return wishlist_obj,existed

class UserManager(BaseUserManager):
    def create_user(self,email,name,number,password=None,is_staff=False,is_admin=False,is_active=True):
        if not email:
            raise ValueError("Users must have an email")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.name = name
        user_obj.number = number
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,name,number,password=None):
        user = self.create_user(
            email,
            name,
            number,
            password,
            is_staff=True
        )
        return user

    def create_superuser(self,email,name,number,password=None):
        user = self.create_user(
            email,
            name,
            number,
            password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255,unique=True)
    name        = models.CharField(max_length=255,blank=True,null=True)
    active      = models.BooleanField(default=True)  # Can Login
    staff       = models.BooleanField(default=False) # Is Staff not super user
    admin       = models.BooleanField(default=False) # Is super User
    number      = models.CharField(max_length=20,null=True,blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name' , 'number']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.name:
            return self.name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    

class Wishlist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product')

    objects = WishlistManager()

    def __str__(self):
        return self.user.email

class JoinOurCircle(models.Model):
    email = models.EmailField(null=True,blank=True)
    
    def __str__(self):
        return self.email