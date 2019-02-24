from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    select2 = select2_modelform(Category, attrs={'width': '250px'})
    form = select2


class PostAdmin(admin.ModelAdmin):
    fields = ('title',('author','slug'),('date','featured_image'),('category', 'tags'),'content','featured','album')
    list_display = ('title', 'author', 'category')
    list_filter = ('author','category','tags')
    search_fields = ['title', 'author', 'category', 'tags']
    select2 = select2_modelform(Post, attrs={'width': '250px'})
    form = select2

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_view_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return True

admin.site.register(Tag)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ExternalPost)