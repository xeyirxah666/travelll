from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad (AZ)")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Ad (EN)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Ad (RU)")
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, default='fa-globe-europe')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"

class Destination(models.Model):
    name = models.CharField(max_length=150, verbose_name="Məkan adı (AZ)")
    name_en = models.CharField(max_length=150, blank=True, verbose_name="Məkan adı (EN)")
    name_ru = models.CharField(max_length=150, blank=True, verbose_name="Məkan adı (RU)")
    country_code = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=500, blank=True)
    tours_count = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Məkan"
        verbose_name_plural = "Məkanlar"

class Guide(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Turun Baş Bələdçisi', verbose_name="Vəzifə (AZ)")
    role_en = models.CharField(max_length=100, blank=True, verbose_name="Vəzifə (EN)")
    role_ru = models.CharField(max_length=100, blank=True, verbose_name="Vəzifə (RU)")
    avatar = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bələdçi"
        verbose_name_plural = "Bələdçilər"

class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlıq (AZ)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Başlıq (EN)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Başlıq (RU)")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=7)
    duration_nights = models.PositiveIntegerField(default=6)
    
    group_size = models.CharField(max_length=50, default='Maks. 16 nəfər', verbose_name="Qrup ölçüsü (AZ)")
    group_size_en = models.CharField(max_length=50, blank=True, verbose_name="Qrup ölçüsü (EN)")
    group_size_ru = models.CharField(max_length=50, blank=True, verbose_name="Qrup ölçüsü (RU)")

    guide_language = models.CharField(max_length=100, default='Azərbaycan & Rus', verbose_name="Bələdçi dili (AZ)")
    guide_language_en = models.CharField(max_length=100, blank=True, verbose_name="Bələdçi dili (EN)")
    guide_language_ru = models.CharField(max_length=100, blank=True, verbose_name="Bələdçi dili (RU)")

    visa_support = models.CharField(max_length=100, default='Şengen (Tam Dəstək)', verbose_name="Viza dəstəyi (AZ)")
    visa_support_en = models.CharField(max_length=100, blank=True, verbose_name="Viza dəstəyi (EN)")
    visa_support_ru = models.CharField(max_length=100, blank=True, verbose_name="Viza dəstəyi (RU)")

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=45)
    
    short_description = models.TextField(blank=True, verbose_name="Qısa məlumat (AZ)")
    short_description_en = models.TextField(blank=True, verbose_name="Qısa məlumat (EN)")
    short_description_ru = models.TextField(blank=True, verbose_name="Qısa məlumat (RU)")

    description = models.TextField(blank=True, verbose_name="Ətraflı məlumat (AZ)")
    description_en = models.TextField(blank=True, verbose_name="Ətraflı məlumat (EN)")
    description_ru = models.TextField(blank=True, verbose_name="Ətraflı məlumat (RU)")

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

    class Meta:
        verbose_name = "Tur"
        verbose_name_plural = "Turlar"

class TourInclusion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='inclusions')
    title = models.CharField(max_length=255, verbose_name="Daxildir (AZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Daxildir (EN)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Daxildir (RU)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Daxil olan xidmət"
        verbose_name_plural = "Daxil olanlar"

class TourExclusion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='exclusions')
    title = models.CharField(max_length=255, verbose_name="Daxil deyil (AZ)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Daxil deyil (EN)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Daxil deyil (RU)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Daxil olmayan xidmət"
        verbose_name_plural = "Daxil olmayanlar"

class TourItinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, verbose_name="Gün Başlığı (AZ)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Gün Başlığı (EN)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Gün Başlığı (RU)")
    description = models.TextField(verbose_name="Açıqlama (AZ)")
    description_en = models.TextField(blank=True, verbose_name="Açıqlama (EN)")
    description_ru = models.TextField(blank=True, verbose_name="Açıqlama (RU)")

    class Meta:
        ordering = ['day_number']
        verbose_name = "Günlük Proqram"
        verbose_name_plural = "Günlük Proqramlar"

class BlogPost(models.Model):
    title = models.CharField(max_length=250, verbose_name="Başlıq (AZ)")
    title_en = models.CharField(max_length=250, blank=True, verbose_name="Başlıq (EN)")
    title_ru = models.CharField(max_length=250, blank=True, verbose_name="Başlıq (RU)")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    author = models.CharField(max_length=100, default='Fərid Mahmudov')
    short_summary = models.TextField(blank=True, verbose_name="Qısa xülasə (AZ)")
    short_summary_en = models.TextField(blank=True, verbose_name="Qısa xülasə (EN)")
    short_summary_ru = models.TextField(blank=True, verbose_name="Qısa xülasə (RU)")
    content = models.TextField(verbose_name="Məzmun (AZ)")
    content_en = models.TextField(blank=True, verbose_name="Məzmun (EN)")
    content_ru = models.TextField(blank=True, verbose_name="Məzmun (RU)")
    image = models.CharField(max_length=500, blank=True)
    reading_time = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bloq Yazısı"
        verbose_name_plural = "Bloq Yazıları"

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Şərh"
        verbose_name_plural = "Şərhlər"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Təsdiqlənmiş Səyahətçi', verbose_name="Vəzifə/Status (AZ)")
    role_en = models.CharField(max_length=100, blank=True, verbose_name="Vəzifə/Status (EN)")
    role_ru = models.CharField(max_length=100, blank=True, verbose_name="Vəzifə/Status (RU)")
    text = models.TextField(verbose_name="Rəy mətni (AZ)")
    text_en = models.TextField(blank=True, verbose_name="Rəy mətni (EN)")
    text_ru = models.TextField(blank=True, verbose_name="Rəy mətni (RU)")
    avatar = models.CharField(max_length=500, blank=True)
    rating = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = "Müştəri Rəyi"
        verbose_name_plural = "Müştəri Rəyləri"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    service = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Əlaqə Mesajı"
        verbose_name_plural = "Əlaqə Mesajları"
