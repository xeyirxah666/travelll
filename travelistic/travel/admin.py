from django.contrib import admin
from .models import (
    Category,
    Destination,
    Guide,
    Tour,
    TourInclusion,
    TourExclusion,
    TourItinerary,
    BlogPost,
    BlogComment,
    Testimonial,
    ContactMessage
)

class TourInclusionInline(admin.TabularInline):
    model = TourInclusion
    extra = 1

class TourExclusionInline(admin.TabularInline):
    model = TourExclusion
    extra = 1

class TourItineraryInline(admin.StackedInline):
    model = TourItinerary
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'duration_days', 'is_featured')
    list_filter = ('is_featured', 'category', 'destination')
    search_fields = ('title', 'title_en', 'title_ru')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TourInclusionInline, TourExclusionInline, TourItineraryInline]

    fieldsets = (
        ('Əsas Məlumatlar (AZ)', {
            'fields': (
                'title', 'slug', 'category', 'destination', 'guide', 'price',
                'duration_days', 'duration_nights', 'short_description', 'description',
                'group_size', 'guide_language', 'visa_support'
            )
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': (
                'title_en', 'short_description_en', 'description_en',
                'group_size_en', 'guide_language_en', 'visa_support_en'
            )
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': (
                'title_ru', 'short_description_ru', 'description_ru',
                'group_size_ru', 'guide_language_ru', 'visa_support_ru'
            )
        }),
        ('Şəkillər və Parametrlər', {
            'fields': ('main_image', 'banner_image', 'rating', 'reviews_count', 'is_featured')
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'title_en', 'title_ru')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Məzmun (AZ)', {
            'fields': ('title', 'slug', 'category', 'author', 'short_summary', 'content', 'image', 'reading_time')
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': ('title_en', 'short_summary_en', 'content_en')
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'short_summary_ru', 'content_ru')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_ru', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_ru', 'country_code', 'tours_count')

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'role_en', 'role_ru', 'phone')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'role', 'rating')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'service', 'message', 'created_at')

