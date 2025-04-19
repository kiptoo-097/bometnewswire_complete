from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from PIL import Image
import os
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# Publisher Model
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Publishers'

# News Article Model
class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Politics', 'Politics'),
        ('National', 'National'),
        ('Business', 'Business'),
        ('Sports', 'Sports'),
        ('Lifestyle', 'Lifestyle'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=False, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 🔥 This auto updates on every save
    trending = models.BooleanField(default=False)
    published_by = models.ForeignKey(Publisher, null=True, on_delete=models.CASCADE)
    breaking = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    og_image = models.ImageField(upload_to='og_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Resize og_image if it exists
        if self.og_image:
            img_path = os.path.join(settings.MEDIA_ROOT, self.og_image.name)
            with Image.open(img_path) as img:
                img = img.convert("RGB")
                img = img.resize((1200, 630), Image.ANTIALIAS)
                img.save(img_path, "JPEG", quality=85)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'News Articles'

# Additional Images Model
class AdditionalImage(models.Model):
    article = models.ForeignKey(NewsArticle, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)
    placeholder = models.CharField(max_length=100, default='placeholder_1')  # Default value added

    def __str__(self):
        return f"Image for {self.article.title} at {self.placeholder}"

# E-paper Model
class Epaper(models.Model):
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='epapers/', default='epapers/News_Wire.pdf')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Epapers'

# Comment Model with support for replies
class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    class Meta:
        verbose_name_plural = 'Comments'
