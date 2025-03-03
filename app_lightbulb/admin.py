from django.contrib import admin
from .models import Type_of_premises, Room_Type, Room_Type_Category
from mptt.admin import MPTTModelAdmin
from import_export.admin import ImportExportModelAdmin
@admin.register(Room_Type_Category)
class Room_Type_CategoryAdmin(MPTTModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']  # Name bo‘yicha qidirish
    list_filter = ['name']  # Name bo‘yicha filtr qo‘shish


@admin.register(Room_Type)
class RoomTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','category', 'ugr']
    list_filter = ['category']

admin.site.register(Type_of_premises)