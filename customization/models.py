from django.db import models
from products.models import Product

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    small_image = models.ImageField(upload_to="customize/recipe/",null=True,blank=True,help_text="Use a square Image")
    video = models.FileField(upload_to="customize/recipe/",null=True,blank=True,help_text="Use a Image with aspect ratio 3/2")

    def __str__(self):
        return self.title

class Herobanner(models.Model):
    main_heading = models.CharField(max_length=500)
    side_heading = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="customize/herobanner")
    order = models.PositiveIntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return self.main_heading

    class Meta:
        ordering = ['order','main_heading']
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"

class Handpicked(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="products")
    image = models.ImageField(upload_to="customize/handpicked",null=True,help_text="Upload image with same dimensions as other images on the site")

    def __str__(self):
        if self.product.flavour:
            return self.product.title + " " + self.product.flavour
        return self.product.title

    class Meta:
        verbose_name = "Handpicked Product"
        verbose_name_plural = "Handpicked Products"

class HomePageBanner(models.Model):
    image = models.ImageField(upload_to="customize/homepagebanner/",null=True,blank=True,help_text="Do not save without placing image")
    text  = models.CharField(max_length=300)
    link  = models.CharField(max_length=300)
    closemark_color = models.CharField(max_length=20,default="#000000",help_text="Use Hexadecimal form for color like #000000 for black and #ffffff for white")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Homepage Offer Banner"
        verbose_name_plural = "Homepage Offer Banners"

class Miscellaneous(models.Model):
    name = models.CharField(max_length=100,help_text="Do not edit this")
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Miscellaneous Item"
        verbose_name_plural = "Miscellaneous Items"

class HomePageIngredientIndex(models.Model):
    letter      = models.CharField(max_length=1)
    image       = models.ImageField(upload_to="customize/ingredientindex/")
    name        = models.CharField(max_length=120)
    description = models.TextField()
    browse_link = models.CharField(max_length=200,null=True,blank=True)
    slide_order = models.PositiveIntegerField(help_text="The order in which you want in the website")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['slide_order','name']
        verbose_name = "Homepage Ingredient Index"
        verbose_name_plural = "Homepage Ingredient Indexes"

class Option(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    description = models.TextField()
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Font(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    font_size = models.DecimalField(max_digits=10,decimal_places=5)
    color = models.CharField(max_length=15,default="#080808")
    bold = models.BooleanField(default=False)
    underline = models.BooleanField(default=False)
    italic = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class HowDoWeDoIt(models.Model):
    description = models.TextField()
    video = models.FileField(upload_to="customize/howdowedoit/",null=True,blank=True)

    def __str__(self):
        return "How do we do it"

    class Meta:
        verbose_name = "How do we do it"
        verbose_name_plural = "How Do We Do It"


class ShiprocketCredentials(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ("-created_at",)