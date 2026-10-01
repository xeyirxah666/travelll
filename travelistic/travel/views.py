from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.utils import translation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
import json

from .models import (
    Tour,
    Category,
    Destination,
    BlogPost,
    BlogComment,
    Testimonial,
    ContactMessage,
    Feature,
    CompanyStatistic,
    TeamMember,
    FAQ,
    Partner,
    TourBooking,
    NewsletterSubscriber,
)
from .translations import (
    get_translations,
    localize_tour_object,
    localize_category_name,
    localize_destination_name,
    localize_blog_post,
)

def localize_feature(feat, lang='az'):
    if not feat:
        return feat
    if lang == 'en':
        feat.display_title = feat.title_en or feat.title
        feat.display_description = feat.description_en or feat.description
    elif lang == 'ru':
        feat.display_title = feat.title_ru or feat.title
        feat.display_description = feat.description_ru or feat.description
    else:
        feat.display_title = feat.title
        feat.display_description = feat.description
    return feat

def localize_statistic(stat, lang='az'):
    if not stat:
        return stat
    if lang == 'en':
        stat.display_title = stat.title_en or stat.title
        stat.display_suffix = stat.suffix_en or stat.suffix
    elif lang == 'ru':
        stat.display_title = stat.title_ru or stat.title
        stat.display_suffix = stat.suffix_ru or stat.suffix
    else:
        stat.display_title = stat.title
        stat.display_suffix = stat.suffix
    return stat

def localize_team_member(member, lang='az'):
    if not member:
        return member
    if lang == 'en':
        member.display_role = member.role_en or member.role
    elif lang == 'ru':
        member.display_role = member.role_ru or member.role
    else:
        member.display_role = member.role
    return member

def localize_faq(faq, lang='az'):
    if not faq:
        return faq
    if lang == 'en':
        faq.display_question = faq.question_en or faq.question
        faq.display_answer = faq.answer_en or faq.answer
    elif lang == 'ru':
        faq.display_question = faq.question_ru or faq.question
        faq.display_answer = faq.answer_ru or faq.answer
    else:
        faq.display_question = faq.question
        faq.display_answer = faq.answer
    return faq

def set_language_view(request, lang_code):
    """
    Switch active language and redirect back to previous page.
    Stores language preference in both session and cookie.
    """
    valid_languages = ['az', 'en', 'ru']
    if lang_code not in valid_languages:
        lang_code = 'az'

    # Determine redirect target
    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    
    # Security check: only allow local relative redirects or same domain
    parsed = urlparse(next_url)
    if parsed.netloc and parsed.netloc != request.get_host():
        next_url = '/'

    response = redirect(next_url)

    # Set session
    if hasattr(request, 'session'):
        request.session['django_language'] = lang_code

    # Set translation in thread
    translation.activate(lang_code)
    request.LANGUAGE_CODE = lang_code

    # Set cookie
    cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
    cookie_age = getattr(settings, 'LANGUAGE_COOKIE_AGE', 365 * 24 * 60 * 60)
    response.set_cookie(
        cookie_name,
        lang_code,
        max_age=cookie_age,
        path='/',
        samesite='Lax'
    )
    return response

def _get_current_lang(request):
    if hasattr(request, 'session') and request.session.get('django_language'):
        return request.session.get('django_language')
    if request.COOKIES.get('django_language'):
        return request.COOKIES.get('django_language')
    return getattr(request, 'LANGUAGE_CODE', 'az')

def home_view(request):
    lang = _get_current_lang(request)
    featured_tours = list(Tour.objects.filter(is_featured=True)[:6])
    for tour in featured_tours:
        localize_tour_object(tour, lang)

    categories = list(Category.objects.all()[:4])
    for cat in categories:
        cat.display_name = localize_category_name(cat.name, lang)

    destinations = list(Destination.objects.all()[:3])
    for dest in destinations:
        dest.display_name = localize_destination_name(dest.name, lang)

    testimonials = list(Testimonial.objects.all()[:3])
    latest_blogs = list(BlogPost.objects.order_by('-created_at')[:3])
    for post in latest_blogs:
        localize_blog_post(post, lang)

    features = list(Feature.objects.filter(is_active=True).order_by('order'))
    for feat in features:
        localize_feature(feat, lang)

    stats = list(CompanyStatistic.objects.all().order_by('order'))
    for stat in stats:
        localize_statistic(stat, lang)

    context = {
        'featured_tours': featured_tours,
        'categories': categories,
        'destinations': destinations,
        'testimonials': testimonials,
        'latest_blogs': latest_blogs,
        'features': features,
        'stats': stats,
    }
    return render(request, 'index.html', context)

def services_view(request):
    lang = _get_current_lang(request)
    category_slug = request.GET.get('category')
    tours = Tour.objects.all()
    if category_slug and category_slug != 'all':
        tours = tours.filter(category__slug=category_slug)
    
    tour_list = list(tours)
    for tour in tour_list:
        localize_tour_object(tour, lang)

    categories = list(Category.objects.all())
    for cat in categories:
        cat.display_name = localize_category_name(cat.name, lang)

    faqs = list(FAQ.objects.filter(is_active=True).order_by('order'))
    for f in faqs:
        localize_faq(f, lang)

    return render(request, 'services.html', {
        'tours': tour_list,
        'categories': categories,
        'faqs': faqs
    })

def service_detail_view(request, slug):
    lang = _get_current_lang(request)
    tour = get_object_or_404(Tour, slug=slug)
    localize_tour_object(tour, lang)

    related_tours = list(Tour.objects.exclude(id=tour.id)[:3])
    for rt in related_tours:
        localize_tour_object(rt, lang)

    return render(request, 'service-single.html', {'tour': tour, 'related_tours': related_tours})

def about_view(request):
    lang = _get_current_lang(request)
    t = get_translations(lang)

    stats = list(CompanyStatistic.objects.all().order_by('order'))
    for s in stats:
        localize_statistic(s, lang)

    team_members = list(TeamMember.objects.filter(is_active=True).order_by('order'))
    for tm in team_members:
        localize_team_member(tm, lang)

    partners = list(Partner.objects.filter(is_active=True).order_by('order'))

    return render(request, 'about.html', {
        'stats': stats,
        'team_members': team_members,
        'partners': partners,
    })

def blog_view(request):
    from django.core.paginator import Paginator

    lang = _get_current_lang(request)
    category_slug = request.GET.get('category')
    posts_qs = BlogPost.objects.all().order_by('-created_at')
    if category_slug:
        posts_qs = posts_qs.filter(category__slug=category_slug)
        
    posts_list = list(posts_qs)
    for post in posts_list:
        localize_blog_post(post, lang)

    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = list(Category.objects.all())
    for cat in categories:
        cat.display_name = localize_category_name(cat, lang)

    recent_posts = list(BlogPost.objects.order_by('-created_at')[:3])
    for rp in recent_posts:
        localize_blog_post(rp, lang)

    return render(request, 'blog.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
    })

def blog_detail_view(request, slug=''):
    lang = _get_current_lang(request)
    post = None
    if slug:
        post = BlogPost.objects.filter(slug=slug).first()
    if not post:
        post = BlogPost.objects.first()
    if post:
        localize_blog_post(post, lang)
        recent_posts = list(BlogPost.objects.exclude(id=post.id)[:3])
    else:
        recent_posts = list(BlogPost.objects.all()[:3])

    for rp in recent_posts:
        localize_blog_post(rp, lang)

    return render(request, 'blog-single.html', {'post': post, 'recent_posts': recent_posts})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message = request.POST.get('message', '').strip()
        if name and (email or phone):
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                service=service,
                message=message
            )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
            return JsonResponse({'success': True})
        return render(request, 'contact.html', {'submitted': True})

    return render(request, 'contact.html')

@csrf_exempt
def book_tour_ajax(request):
    """
    Receives booking modal submissions and stores them in TourBooking model.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Yalnız POST sorğusu qəbul olunur.'}, status=405)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
    else:
        data = request.POST

    full_name = (data.get('name') or data.get('full_name') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    tour_name = (data.get('tour') or data.get('tour_name') or '').strip()
    travel_date = (data.get('date') or data.get('travel_date') or '').strip()
    guests_count = (data.get('guests') or data.get('guests_count') or '').strip()
    notes = (data.get('notes') or '').strip()

    if not full_name or not (phone or email):
        return JsonResponse({'success': False, 'error': 'Zəhmət olmasa ad və əlaqə vasitəsini (telefon və ya email) daxil edin.'}, status=400)

    tour_obj = None
    if tour_name:
        tour_obj = Tour.objects.filter(title__iexact=tour_name).first()

    booking = TourBooking.objects.create(
        tour=tour_obj,
        tour_name=tour_name,
        full_name=full_name,
        phone=phone,
        email=email,
        travel_date=travel_date,
        guests_count=guests_count,
        notes=notes
    )

    return JsonResponse({
        'success': True,
        'booking_id': booking.id,
        'message': 'Rezervasiya uğurla qeydə alındı.'
    })

@csrf_exempt
def subscribe_newsletter_ajax(request):
    """
    Receives newsletter subscriptions and stores in NewsletterSubscriber.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Yalnız POST sorğusu qəbul olunur.'}, status=405)

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
    else:
        data = request.POST

    email = (data.get('email') or '').strip().lower()
    if not email or '@' not in email:
        return JsonResponse({'success': False, 'error': 'Düzgün e-poçt ünvanı daxil edin.'}, status=400)

    sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
    return JsonResponse({
        'success': True,
        'created': created,
        'message': 'Abunəlik uğurla tamamlandı.'
    })

