from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, default='fa-globe-europe')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=150)
    country_code = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=500, blank=True)
    tours_count = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Guide(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Turun Baş Bələdçisi')
    avatar = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=7)
    duration_nights = models.PositiveIntegerField(default=6)
    group_size = models.CharField(max_length=50, default='Maks. 16 nəfər')
    guide_language = models.CharField(max_length=100, default='Azərbaycan & Rus')
    visa_support = models.CharField(max_length=100, default='Şengen (Tam Dəstək)')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=45)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    main_image = models.CharField(max_length=500, blank=True)
    banner_image = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class TourInclusion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='inclusions')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class TourExclusion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='exclusions')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class TourItinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['day_number']

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    author = models.CharField(max_length=100, default='Fərid Mahmudov')
    short_summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.CharField(max_length=500, blank=True)
    reading_time = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Təsdiqlənmiş Səyahətçi')
    text = models.TextField()
    avatar = models.CharField(max_length=500, blank=True)
    rating = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.author_name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    service = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
