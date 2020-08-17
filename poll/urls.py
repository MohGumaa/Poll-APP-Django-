from django.urls import path
from . import views

app_name = "poll"

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('result/<int:pk>/', views.ResultView.as_view(), name="result"),
    path('vote/<int:pk>/', views.vote, name="vote"),
]
