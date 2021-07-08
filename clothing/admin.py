from django.contrib import admin
from .models import ClothCategory, ClothingItem, WornEvent


@admin.register(ClothCategory)
class ClothCategoryAdminConfig(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(ClothingItem)
class ClothingItemAdminConfig(admin.ModelAdmin):
    ordering = ('owner', 'category', 'tag_id',)
    list_display = ('owner', 'name', 'category', 'tag_id')


@admin.register(WornEvent)
class WornEventAdminConfig(admin.ModelAdmin):
    ordering = ('item','-time_stamp',)
    list_display = ('item', 'time_stamp', 'temperture')