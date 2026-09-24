# -*- coding: utf-8 -*-
from django import template
from travel.translations import (
    TRANSLATIONS,
    TOUR_TRANSLATIONS,
    CATEGORY_TRANSLATIONS,
    localize_tour_object,
    localize_category_name,
)

register = template.Library()

@register.simple_tag(takes_context=True)
def t(context, key, default=None):
    """
    Template tag to translate a key based on active language in context.
    Usage: {% t "nav_home" %} or {% t "some_key" "Default Text" %}
    """
    t_dict = context.get('t')
    if t_dict and hasattr(t_dict, 'get'):
        return t_dict.get(key, default or key)
    
    current_lang = context.get('CURRENT_LANG', 'az')
    lang_dict = TRANSLATIONS.get(current_lang, TRANSLATIONS.get('az', {}))
    return lang_dict.get(key, default or key)


@register.simple_tag(takes_context=True)
def tour_title(context, tour):
    """
    Returns localized title for a tour.
    """
    if not tour:
        return ""
    current_lang = context.get('CURRENT_LANG', 'az')
    if current_lang == 'az':
        return getattr(tour, 'title', '')
    
    tour_trans = TOUR_TRANSLATIONS.get(tour.title, {}).get(current_lang, {})
    return tour_trans.get('title', tour.title)


@register.simple_tag(takes_context=True)
def tour_desc(context, tour):
    """
    Returns localized short description for a tour.
    """
    if not tour:
        return ""
    current_lang = context.get('CURRENT_LANG', 'az')
    if current_lang == 'az':
        return getattr(tour, 'short_description', '')
    
    tour_trans = TOUR_TRANSLATIONS.get(tour.title, {}).get(current_lang, {})
    return tour_trans.get('short_description', tour.short_description)


@register.simple_tag(takes_context=True)
def cat_title(context, category):
    """
    Returns localized category name.
    """
    if not category:
        return ""
    name = getattr(category, 'name', str(category))
    current_lang = context.get('CURRENT_LANG', 'az')
    return localize_category_name(name, current_lang)
