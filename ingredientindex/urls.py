from django.urls import path
from .views import ingredientindexhome,get_ingredient


urlpatterns = [
    path("",ingredientindexhome,name="ii_home"),
    path("<str:ingredient>/",get_ingredient,name="get_ingredient")
]