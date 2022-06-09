from django.contrib import admin
from .models import Address
# Register your models here.

class addressAdmin(admin.ModelAdmin):
    readonly_fields = ["user","email","phone_number","first_name","last_name","address_line_1","address_line_2","city","state","country","postal_code"]

admin.site.register(Address,addressAdmin)