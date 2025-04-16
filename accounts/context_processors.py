# accounts/context_processors.py
from .models import NewsArticle

def breaking_news_processor(request):
    breaking_news = NewsArticle.objects.filter(breaking=True).order_by('-date_published')
    return {'breaking_news': breaking_news}
