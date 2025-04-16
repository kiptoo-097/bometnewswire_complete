from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import NewsArticle

class Command(BaseCommand):
    help = 'Populate slugs for existing NewsArticle records'

    def handle(self, *args, **kwargs):
        for article in NewsArticle.objects.all():
            if not article.slug:
                base_slug = slugify(article.title)
                slug = base_slug
                counter = 1
                while NewsArticle.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                article.slug = slug
                article.save()
                self.stdout.write(self.style.SUCCESS(f'Updated slug for "{article.title}" to "{slug}"'))