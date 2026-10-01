from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('services/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('about/', views.about_view, name='about'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('set-language/<str:lang_code>/', views.set_language_view, name='set_language'),
    path('api/book-tour/', views.book_tour_ajax, name='book_tour_ajax'),
    path('api/subscribe-newsletter/', views.subscribe_newsletter_ajax, name='subscribe_newsletter_ajax'),
]
