from django.urls import path
from .views import Type_of_premises_ListApiview, LampCalculationAPIView


urlpatterns = [
    path("list/", Type_of_premises_ListApiview.as_view(), name="Type_of_premises"),
    path('calculate-lamps/', LampCalculationAPIView.as_view(), name='calculate_lamps'),
]