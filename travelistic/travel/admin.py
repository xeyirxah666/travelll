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
    ContactMessage,
    SiteSetting,
    Feature,
    CompanyStatistic,
    TeamMember,
    FAQ,
    Partner,
    TourBooking,
    NewsletterSubscriber
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


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Əsas Məlumatlar və Əlaqə', {
            'fields': (
                'site_title', 'phone', 'email', 'whatsapp_number',
                'address', 'address_en', 'address_ru',
                'working_hours', 'working_hours_en', 'working_hours_ru'
            )
        }),
        ('Sosial Şəbəkələr', {
            'fields': ('facebook_url', 'instagram_url', 'telegram_url', 'youtube_url', 'linkedin_url')
        }),
        ('Hero Bölməsi', {
            'fields': (
                'hero_badge', 'hero_badge_en', 'hero_badge_ru',
                'hero_title_p1', 'hero_title_p1_en', 'hero_title_p1_ru',
                'hero_title_p2', 'hero_title_p2_en', 'hero_title_p2_ru',
                'hero_desc', 'hero_desc_en', 'hero_desc_ru',
                'hero_image'
            )
        }),
        ('Haqqımızda Bölməsi', {
            'fields': (
                'about_experience_years',
                'about_story_p1', 'about_story_p1_en', 'about_story_p1_ru',
                'about_story_p2', 'about_story_p2_en', 'about_story_p2_ru',
                'about_mission_desc', 'about_mission_desc_en', 'about_mission_desc_ru',
                'about_vision_desc', 'about_vision_desc_en', 'about_vision_desc_ru',
            )
        }),
    )

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'title_en', 'title_ru')

    fieldsets = (
        ('Azərbaycan dili', {
            'fields': ('title', 'description', 'icon_class', 'order', 'is_active')
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en')
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru')
        }),
    )


@admin.register(CompanyStatistic)
class CompanyStatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'suffix', 'icon_class', 'order')
    list_editable = ('number', 'suffix', 'order')
    search_fields = ('title', 'title_en', 'title_ru')

    fieldsets = (
        ('Azərbaycan dili', {
            'fields': ('title', 'number', 'suffix', 'icon_class', 'order')
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': ('title_en', 'suffix_en')
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'suffix_ru')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'role_en', 'role_ru')

    fieldsets = (
        ('Əsas Məlumatlar (AZ)', {
            'fields': ('name', 'role', 'photo', 'linkedin_url', 'instagram_url', 'order', 'is_active')
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': ('role_en',)
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': ('role_ru',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'question_en', 'question_ru', 'answer')

    fieldsets = (
        ('Azərbaycan dili', {
            'fields': ('question', 'answer', 'icon_class', 'order', 'is_active')
        }),
        ('İngilis dili tərcüməsi (EN)', {
            'classes': ('collapse',),
            'fields': ('question_en', 'answer_en')
        }),
        ('Rus dili tərcüməsi (RU)', {
            'classes': ('collapse',),
            'fields': ('question_ru', 'answer_ru')
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'website_url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'tour_display', 'travel_date', 'guests_count', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('full_name', 'phone', 'email', 'tour_name', 'notes')
    readonly_fields = ('created_at',)

    def tour_display(self, obj):
        if obj.tour:
            return obj.tour.title
        return obj.tour_name or "Ümumi Paket"
    tour_display.short_description = "Tur"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)


