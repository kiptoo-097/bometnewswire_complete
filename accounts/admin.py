from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, NewsArticle, Epaper, AdditionalImage
from .forms import CustomUserCreationForm

# ---------- Custom User Admin ----------
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# ---------- Publisher Admin ----------
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'facebook', 'twitter', 'linkedin')
    search_fields = ('name', 'email')

admin.site.register(Publisher, PublisherAdmin)

# ---------- Additional Image Inline ----------
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

# ---------- News Article Admin ----------
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_published', 'trending', 'published_by', 'breaking')
    list_filter = ('category', 'trending', 'breaking', 'date_published')
    search_fields = ('title', 'content')
    ordering = ('-date_published',)
    list_editable = ('trending', 'breaking')
    date_hierarchy = 'date_published'
    inlines = [AdditionalImageInline]
    readonly_fields = ('date_published',)

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'category',
                'content',
                'image',
                'og_image',
                'caption',
                'published_by',
                'trending',
                'breaking',
            )
        }),
    )

admin.site.register(NewsArticle, NewsArticleAdmin)

# ---------- Epaper Admin ----------
class EpaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'pdf', 'date_uploaded')
    search_fields = ('title',)
    ordering = ('-date_uploaded',)

admin.site.register(Epaper, EpaperAdmin)

# ---------- Admin Panel Branding ----------
admin.site.site_header = 'Bomet Newswire Admin Panel'
admin.site.site_title = 'Bomet Newswire Admin'
admin.site.index_title = 'Welcome to Bomet Newswire Administration'
