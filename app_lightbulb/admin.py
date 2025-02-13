from django.contrib import admin
from .models import Type_of_premises, Room_Type, Room_Type_Category
class RoomTypeInline(admin.TabularInline):  # Inline form qo'shish
    model = Room_Type
    extra = 1  # Qo'shimcha bo'sh forma

@admin.register(Room_Type_Category)
class RoomTypeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [RoomTypeInline]

@admin.register(Room_Type)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'light_type']
    list_filter = ['category']

admin.site.register(Type_of_premises)