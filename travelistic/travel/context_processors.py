# -*- coding: utf-8 -*-
from django.conf import settings
from .translations import get_translations
from .models import SiteSetting

LANG_INFO = {
    'az': {'code': 'az', 'name': 'Azərbaycan', 'flag': '🇦🇿', 'short': 'AZ'},
    'en': {'code': 'en', 'name': 'English', 'flag': '🇬🇧', 'short': 'EN'},
    'ru': {'code': 'ru', 'name': 'Русский', 'flag': '🇷🇺', 'short': 'RU'},
}

def language_context(request):
    """
    Context processor that provides active language information,
    list of available languages, and the translation dictionary (t)
    to all templates.
    """
    # 1. Determine active language
    lang = None
    if hasattr(request, 'session') and request.session.get('django_language'):
        lang = request.session.get('django_language')
    elif request.COOKIES.get('django_language'):
        lang = request.COOKIES.get('django_language')
    elif hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
        code = request.LANGUAGE_CODE.split('-')[0].lower()
        if code in LANG_INFO:
            lang = code

    if not lang or lang not in LANG_INFO:
        lang = getattr(settings, 'LANGUAGE_CODE', 'az')
        if lang not in LANG_INFO:
            lang = 'az'

    current_info = LANG_INFO[lang]
    available_languages = list(LANG_INFO.values())

    site_settings = None
    try:
        site_settings = SiteSetting.objects.first()
        if site_settings:
            if lang == 'en':
                site_settings.display_tagline = site_settings.site_tagline_en or site_settings.site_tagline
                site_settings.display_address = site_settings.address_en or site_settings.address
                site_settings.display_working_hours = site_settings.working_hours_en or site_settings.working_hours
                site_settings.display_hero_badge = site_settings.hero_badge_en or site_settings.hero_badge
                site_settings.display_hero_title_p1 = site_settings.hero_title_p1_en or site_settings.hero_title_p1
                site_settings.display_hero_title_p2 = site_settings.hero_title_p2_en or site_settings.hero_title_p2
                site_settings.display_hero_desc = site_settings.hero_desc_en or site_settings.hero_desc
                site_settings.display_about_story_p1 = site_settings.about_story_p1_en or site_settings.about_story_p1
                site_settings.display_about_story_p2 = site_settings.about_story_p2_en or site_settings.about_story_p2
                site_settings.display_about_mission_desc = site_settings.about_mission_desc_en or site_settings.about_mission_desc
                site_settings.display_about_vision_desc = site_settings.about_vision_desc_en or site_settings.about_vision_desc
            elif lang == 'ru':
                site_settings.display_tagline = site_settings.site_tagline_ru or site_settings.site_tagline
                site_settings.display_address = site_settings.address_ru or site_settings.address
                site_settings.display_working_hours = site_settings.working_hours_ru or site_settings.working_hours
                site_settings.display_hero_badge = site_settings.hero_badge_ru or site_settings.hero_badge
                site_settings.display_hero_title_p1 = site_settings.hero_title_p1_ru or site_settings.hero_title_p1
                site_settings.display_hero_title_p2 = site_settings.hero_title_p2_ru or site_settings.hero_title_p2
                site_settings.display_hero_desc = site_settings.hero_desc_ru or site_settings.hero_desc
                site_settings.display_about_story_p1 = site_settings.about_story_p1_ru or site_settings.about_story_p1
                site_settings.display_about_story_p2 = site_settings.about_story_p2_ru or site_settings.about_story_p2
                site_settings.display_about_mission_desc = site_settings.about_mission_desc_ru or site_settings.about_mission_desc
                site_settings.display_about_vision_desc = site_settings.about_vision_desc_ru or site_settings.about_vision_desc
            else:
                site_settings.display_tagline = site_settings.site_tagline
                site_settings.display_address = site_settings.address
                site_settings.display_working_hours = site_settings.working_hours
                site_settings.display_hero_badge = site_settings.hero_badge
                site_settings.display_hero_title_p1 = site_settings.hero_title_p1
                site_settings.display_hero_title_p2 = site_settings.hero_title_p2
                site_settings.display_hero_desc = site_settings.hero_desc
                site_settings.display_about_story_p1 = site_settings.about_story_p1
                site_settings.display_about_story_p2 = site_settings.about_story_p2
                site_settings.display_about_mission_desc = site_settings.about_mission_desc
                site_settings.display_about_vision_desc = site_settings.about_vision_desc
    except Exception:
        site_settings = None

    return {
        'CURRENT_LANG': lang,
        'CURRENT_LANG_NAME': current_info['name'],
        'CURRENT_LANG_FLAG': current_info['flag'],
        'CURRENT_LANG_SHORT': current_info['short'],
        'AVAILABLE_LANGUAGES': available_languages,
        't': get_translations(lang),
        'site_settings': site_settings,
        'current_path': request.get_full_path(),
    }
