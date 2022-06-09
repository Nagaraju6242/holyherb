from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField()
    phone_number = models.BigIntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=300)
    address_line_2 = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    postal_code = models.PositiveIntegerField()


    def __str__(self):
        return str(self.email)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}\n{country}, \n{postal_code}".format(
            line1 = self.address_line_1,
            line2 = self.address_line_2 or "",
            city = self.city,
            state = self.state,
            postal_code = self.postal_code,
            country = self.country
        )