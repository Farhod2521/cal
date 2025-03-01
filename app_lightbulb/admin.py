from django.contrib import admin
from .models import Type_of_premises, Room_Type, Room_Type_Category
from mptt.admin import MPTTModelAdmin


@admin.register(Room_Type_Category, MPTTModelAdmin)
class Room_Type_CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Room_Type)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['id','category', 'ugr']
    list_filter = ['category']

admin.site.register(Type_of_premises)