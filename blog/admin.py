from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = [('name', 'slug', 'parent')]
    search_fields = ['name']
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    select2 = select2_modelform(Category, attrs={'width': '250px'})
    form = select2


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = [('name', 'slug')]
    search_fields = ['name']
    list_display = ('name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = [
        ('title', 'slug'),
        ('author', 'date', 'featured_image'),
        ('category', 'tags'),
        'content',
        'featured',
        'album'
    ]
    list_display = ('title', 'author', 'category')
    list_filter = ('author', 'category', 'tags')
    search_fields = ['title', 'author', 'category', 'tags']
    select2 = select2_modelform(Post, attrs={'width': '250px'})
    form = select2

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('featured')
        return fields

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return True


@admin.register(ExternalPost)
class ExternalPostAdmin(admin.ModelAdmin):
    fields = [
        ('title', 'slug'),
        ('author', 'date', 'featured_image'),
        ('category', 'tags'),
        'url',
        'featured'
    ]
    list_display = ('title', 'author', 'category')
    list_filter = ('author', 'category', 'tags')
    search_fields = ['title', 'author', 'category', 'tags']
    select2 = select2_modelform(ExternalPost, attrs={'width': '250px'})
    form = select2

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('featured')
        return fields

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return True
