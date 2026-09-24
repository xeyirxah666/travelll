# -*- coding: utf-8 -*-
from django.conf import settings
from .translations import get_translations

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
        # e.g., 'az', 'en', 'ru' (or 'en-us' -> 'en')
        code = request.LANGUAGE_CODE.split('-')[0].lower()
        if code in LANG_INFO:
            lang = code

    if not lang or lang not in LANG_INFO:
        lang = getattr(settings, 'LANGUAGE_CODE', 'az')
        if lang not in LANG_INFO:
            lang = 'az'

    current_info = LANG_INFO[lang]
    available_languages = list(LANG_INFO.values())

    return {
        'CURRENT_LANG': lang,
        'CURRENT_LANG_NAME': current_info['name'],
        'CURRENT_LANG_FLAG': current_info['flag'],
        'CURRENT_LANG_SHORT': current_info['short'],
        'AVAILABLE_LANGUAGES': available_languages,
        't': get_translations(lang),
        'current_path': request.get_full_path(),
    }
