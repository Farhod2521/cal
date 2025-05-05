from django.contrib import admin
from .models import Type_of_premises, Room_Type, Room_Type_Category, LEDPanel
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
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



@admin.register(LEDPanel)
class LEDPanelAdmin(admin.ModelAdmin):
    list_display = ('name', 'power', 'voltage', 'color_temperature', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_tag.short_description = 'Rasm'