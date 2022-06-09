from django.urls import path,include
from .views import get_product,get_handpicked

urlpatterns = [
    path('handpicked/',get_handpicked,name='handpicked'),
    path('<str:slug>/',get_product,name="detail"),
]