from django.contrib import admin
from target_habr.models import Category, Creator, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'label')


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name')


class PostAdmin(admin.ModelAdmin):
    @staticmethod
    def creator_name(instance):
        return instance.creator.name

    @staticmethod
    def get_categories(obj):
        return ", ".join([p.label for p in obj.category.all()])

    list_display = ('pub_date', 'creator_name', 'title', 'get_categories')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Post, PostAdmin)
