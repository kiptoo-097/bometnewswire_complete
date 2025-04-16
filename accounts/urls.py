from django.urls import path
# from . views import register_view, login_view, logout_view
from . views import home_view,all_news_view, epaper_list_view, epaper_detail_view
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', home_view, name='home'),
    path('search/', views.search_view, name='search'),

    path('news/<int:pk>/<slug:slug>/', views.news_detail, name='news_detail'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('all-news/', views.all_news_view, name='all_news'),  # New URL for all news
    path('epapers/', epaper_list_view, name='epaper_list'),
    path('epaper/<int:pk>/', epaper_detail_view, name='epaper_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete-account/', views.delete_account, name='delete_account'),

        # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

