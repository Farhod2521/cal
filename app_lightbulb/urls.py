from django.urls import path
from .views import Type_of_premises_ListApiview, LampCalculationAPIView, RoomTypeCategoryListView, RoomTypeListView, RoomTypeCategoryByParentView, RoomTypeCategoryAPIView, RoomCalculationAPIView



urlpatterns = [
    path("list/", Type_of_premises_ListApiview.as_view(), name="Type_of_premises"),
    path('calculate-ja/', LampCalculationAPIView.as_view(), name='calculate_lamps'), 
    path('room_categories/', RoomTypeCategoryListView.as_view(), name='room_type_category_list'),
    path('rooms/<int:category_id>/', RoomTypeListView.as_view(), name='room_type_list'),
    path('room_categories/parent/<int:tree_id>/', RoomTypeCategoryByParentView.as_view(), name='category-by-parent'),


    path('api/room-categories/', RoomTypeCategoryAPIView.as_view()),  # Root kategoriyalarni olish
    path('api/room-categories/<int:category_id>/', RoomTypeCategoryAPIView.as_view()),  # Subkategoriya olish



    ##############################  ABBDULQOSIM AKA ##################################
    path('calculate-aa/', RoomCalculationAPIView.as_view(), name='room_type_category_list'),

]