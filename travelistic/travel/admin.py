from django.contrib import admin
from .models import Category, Destination, Guide, Tour, TourItinerary, BlogPost, Testimonial, ContactMessage

admin.site.register(Category)
admin.site.register(Destination)
admin.site.register(Guide)
admin.site.register(Tour)
admin.site.register(TourItinerary)
admin.site.register(BlogPost)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
