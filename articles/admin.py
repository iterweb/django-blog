from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CustomUser, Category, Tag, Post, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms



class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_photo', 'username', 'email', 'is_superuser', 'is_staff', 'is_active',
                    'date_joined', 'last_login')
    list_display_links = ('id', 'username')
    search_fields = ('username',)

    def get_photo(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50">')
        else:
            return 'Нет фото'

    get_photo.short_description = 'pic'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'published', 'post', 'timestamp')
    list_display_links = ('name',)
    list_editable = ('published',)
    list_filter = ('published', 'name', 'post')


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'get_photo', 'title', 'author', 'category', 'created_at', 'updated_at',
                    'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('category', 'tags', 'author')
    search_fields = ('title',)
    autocomplete_fields = ('author',)
    form = PostAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'Нет фото'

    get_photo.short_description = 'pic'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

