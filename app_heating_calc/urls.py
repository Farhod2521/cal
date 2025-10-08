# urls.py
from django.urls import path
from .views import RegionDistrictAPIView

urlpatterns = [
    path('api/regions-districts/', RegionDistrictAPIView.as_view(), name='regions-districts'),

]