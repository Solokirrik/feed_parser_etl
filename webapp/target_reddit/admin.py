from django.contrib import admin
from target_reddit.models import Author, Category, Post


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'uri')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'term')
    list_filter = ('term',)


class PostAdmin(admin.ModelAdmin):
    @staticmethod
    def category_term(instance):
        return instance.category.term

    @staticmethod
    def author_name(instance):
        return instance.author.name

    list_display = ('updated_at', 'author_name', 'category_term', 'title')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
