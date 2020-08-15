from django.urls import path
from . import views

app_names = "poll"

urlpatterns = [
    path('', views.index, name="home"),
    path('detail/<int:id>/', views.details, name="detail"),
    path('result/<int:id>/', views.result, name="result"),
]
