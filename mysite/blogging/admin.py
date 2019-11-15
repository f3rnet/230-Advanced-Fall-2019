from django.contrib import admin
from blogging.models import Post, Category
# Register your models here.
# and a new admin registration


class CategoryInline(admin.TabularInline):
    model = Category.posts.through
# @admin.register(Post)


class PostAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
# @admin.register(Category)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('posts',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
