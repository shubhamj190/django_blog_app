from django.contrib import admin
from dapp.models import Post, BlogComment
# Register your models here.

admin.site.register(BlogComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media():
        js=('tinyinject.js',)