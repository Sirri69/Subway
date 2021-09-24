from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('swipe_in', views.swipe_in),
    path('swipe_out', views.swipe_out),
    path('get-avg-time', views.get_avg_time)
]