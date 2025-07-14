from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, Post, Category 
from django.contrib.auth import logout

class CustomAdminSite(admin.AdminSite):
    site_header = 'Администрирование сайта'
    
    def logout(self, request, extra_context=None):
        from django.contrib.auth import logout
        logout(request)
        # Явно указываем редирект на страницу входа в админку
        return HttpResponseRedirect(reverse('admin:login'))

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'category')
    list_filter = ('category', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'post_count')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

    def logout(self, request, extra_context=None):
        logout(request)
        return HttpResponseRedirect(reverse('admin:login'))
    
admin_site = CustomAdminSite(name='myadmin')
admin.site = admin_site
    

admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)