from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages

from .models import NewsArticle, Epaper, Comment
from .forms import CustomUserCreationForm


def home_view(request):
    latest_trending_news = NewsArticle.objects.filter(trending=True).order_by('-date_published').first()

    # Fetch multiple main news items (e.g., top 5 trending news)
    main_news_list = NewsArticle.objects.filter(trending=True).order_by('-date_published')[:5]

    latest_news = (
        NewsArticle.objects.exclude(pk=latest_trending_news.pk).order_by('-date_published')[:5]
        if latest_trending_news else NewsArticle.objects.order_by('-date_published')[:5]
    )

    trending_news = (
        NewsArticle.objects.filter(trending=True).order_by('-date_published')[1:5]
        if latest_trending_news else NewsArticle.objects.filter(trending=True).order_by('-date_published')[:4]
    )

    additional_news = (
        NewsArticle.objects.exclude(pk=latest_trending_news.pk).order_by('-date_published')[1:10]
        if latest_trending_news else NewsArticle.objects.order_by('-date_published')[1:10]
    )

    breaking_news = NewsArticle.objects.filter(breaking=True).order_by('-date_published')
    latest_epaper = Epaper.objects.latest('date_uploaded') if Epaper.objects.exists() else None
    latest_epapers = Epaper.objects.all().order_by('-date_uploaded')[:3] if Epaper.objects.exists() else []

    context = {
        'breaking_news': breaking_news,
        'main_news': latest_trending_news,
        'main_news_list': main_news_list,  # Pass the list of main news items
        'latest_news': latest_news,
        'trending_news': trending_news,
        'additional_news': additional_news,
        'latest_epaper': latest_epaper,
        'latest_epapers': latest_epapers,
    }
    return render(request, 'accounts/home.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import NewsArticle, Comment, AdditionalImage
from django.utils.html import format_html

# News Detail View with Placeholder Image Replacement and Comment/Reply System
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import NewsArticle, Comment
def news_detail(request, pk, slug):
    article = get_object_or_404(NewsArticle, pk=pk, slug=slug)

    # Track views per session
    session_key = f'article_{article.id}_viewed'
    if not request.session.get(session_key, False):
        article.views += 1
        article.save()
        request.session[session_key] = True

    # Prepare additional images rendering
    additional_images = {}
    for img in article.additional_images.all():
        key = img.slug if hasattr(img, 'slug') and img.slug else img.placeholder
        additional_images[key] = img

    rendered_content = article.content
    for placeholder, img in additional_images.items():
        img_html = f'''
            <div class="my-4 text-center">
                <img src="{img.image.url}" class="img-fluid rounded shadow-sm" alt="{img.caption}" style="max-height: 450px;">
                {'<p class="text-muted small mt-2">' + img.caption + '</p>' if img.caption else ''}
            </div>
        '''
        rendered_content = rendered_content.replace(f'{{{placeholder}}}', img_html)
        if hasattr(img, 'slug') and img.slug:
            rendered_content = rendered_content.replace(f'{{{img.slug}}}', img_html)

    # Fetch comments
    comments = Comment.objects.filter(article=article, parent=None).order_by('-timestamp')

    # Handle comment posting
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
        if content:
            Comment.objects.create(article=article, user=request.user, content=content, parent=parent_comment)
            return HttpResponseRedirect(request.path)

    # ✅ Fetch trending and latest news for sidebar
    trending_news = NewsArticle.objects.filter(trending=True).exclude(pk=article.pk).order_by('-date_published')[:5]
    latest_news = NewsArticle.objects.exclude(pk=article.pk).order_by('-date_published')[:5]

    context = {
        'article': article,
        'rendered_content': rendered_content,
        'comments': comments,
        'trending_news': trending_news,
        'latest_news': latest_news,
    }
    return render(request, 'accounts/news_detail.html', context)

def category_view(request, category):
    articles = NewsArticle.objects.filter(category=category).order_by('-date_published')
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/category.html', {
        'category': category,
        'page_obj': page_obj
    })


# Search View
def search_view(request):
    query = request.GET.get('q')
    results = NewsArticle.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)) if query else NewsArticle.objects.none()

    return render(request, 'accounts/search_results.html', {
        'results': results,
        'query': query
    })


# All News Paginated View
def all_news_view(request):
    all_articles = NewsArticle.objects.order_by('-date_published')
    paginator = Paginator(all_articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/all_news.html', {'page_obj': page_obj})


# Epaper List View
def epaper_list_view(request):
    epapers = Epaper.objects.all().order_by('-date_uploaded')
    paginator = Paginator(epapers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'epaper/epaper_list.html', {'page_obj': page_obj})


# Epaper Detail View
def epaper_detail_view(request, pk):
    epaper = get_object_or_404(Epaper, pk=pk)
    return render(request, 'epaper/epaper_detail.html', {'epaper': epaper})


# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Delete Account View
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return render(request, 'accounts/delete_account_confirm.html')
