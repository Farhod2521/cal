from django.contrib import admin
from .models import Type_of_premises, Room_Type, Room_Type_Category
from mptt.admin import MPTTModelAdmin


admin.site.register(Room_Type_Category, MPTTModelAdmin)

@admin.register(Room_Type)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'light_type']
    list_filter = ['category']

admin.site.register(Type_of_premises)