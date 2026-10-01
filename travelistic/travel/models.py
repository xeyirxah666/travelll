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


class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default='Travelistic', verbose_name="Sayt Adı")
    site_tagline = models.CharField(max_length=200, default='Səyahət və Turizm Agentliyi', verbose_name="Sayt Şüarı (AZ)")
    site_tagline_en = models.CharField(max_length=200, blank=True, verbose_name="Sayt Şüarı (EN)")
    site_tagline_ru = models.CharField(max_length=200, blank=True, verbose_name="Sayt Şüarı (RU)")
    
    phone = models.CharField(max_length=50, default='+994 (12) 555-77-88', verbose_name="Telefon")
    email = models.EmailField(default='info@travelistic.az', verbose_name="E-poçt")
    address = models.CharField(max_length=255, default='Nizami küçəsi 45, Bakı, Azərbaycan', verbose_name="Ünvan (AZ)")
    address_en = models.CharField(max_length=255, blank=True, verbose_name="Ünvan (EN)")
    address_ru = models.CharField(max_length=255, blank=True, verbose_name="Ünvan (RU)")
    working_hours = models.CharField(max_length=150, default='Bazar ertəsi - Şənbə: 09:00 - 20:00', verbose_name="İş Saatları (AZ)")
    working_hours_en = models.CharField(max_length=150, blank=True, verbose_name="İş Saatları (EN)")
    working_hours_ru = models.CharField(max_length=150, blank=True, verbose_name="İş Saatları (RU)")
    whatsapp_number = models.CharField(max_length=50, default='+994505557788', verbose_name="WhatsApp Nömrəsi")

    # Social links
    facebook_url = models.URLField(blank=True, default='https://facebook.com', verbose_name="Facebook Link")
    instagram_url = models.URLField(blank=True, default='https://instagram.com', verbose_name="Instagram Link")
    telegram_url = models.URLField(blank=True, default='https://telegram.org', verbose_name="Telegram Link")
    youtube_url = models.URLField(blank=True, default='https://youtube.com', verbose_name="YouTube Link")
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com', verbose_name="LinkedIn Link")

    # Hero Section
    hero_badge = models.CharField(max_length=150, default='2026-cı İlin Ən Etibarlı Səyahət Agentliyi', verbose_name="Hero Nişan (AZ)")
    hero_badge_en = models.CharField(max_length=150, blank=True, verbose_name="Hero Nişan (EN)")
    hero_badge_ru = models.CharField(max_length=150, blank=True, verbose_name="Hero Nişan (RU)")
    hero_title_p1 = models.CharField(max_length=200, default='Dünyanın Ən Gözəl Guşələrini', verbose_name="Hero Başlıq 1-ci hissə (AZ)")
    hero_title_p1_en = models.CharField(max_length=200, blank=True, verbose_name="Hero Başlıq 1-ci hissə (EN)")
    hero_title_p1_ru = models.CharField(max_length=200, blank=True, verbose_name="Hero Başlıq 1-ci hissə (RU)")
    hero_title_p2 = models.CharField(max_length=200, default='Bizimlə Kəşf Edin', verbose_name="Hero Başlıq 2-ci hissə (AZ)")
    hero_title_p2_en = models.CharField(max_length=200, blank=True, verbose_name="Hero Başlıq 2-ci hissə (EN)")
    hero_title_p2_ru = models.CharField(max_length=200, blank=True, verbose_name="Hero Başlıq 2-ci hissə (RU)")
    hero_desc = models.TextField(default='Xəyal etdiyiniz tətil artıq əlçatandır. Peşəkar bələdçilər, premium otellər, zəmanətli viza dəstəyi və fərdiləşdirilmiş marşrutlarla unudulmaz xatirələr toplayın.', verbose_name="Hero Təsviri (AZ)")
    hero_desc_en = models.TextField(blank=True, verbose_name="Hero Təsviri (EN)")
    hero_desc_ru = models.TextField(blank=True, verbose_name="Hero Təsviri (RU)")
    hero_image = models.CharField(max_length=500, default='https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1920&q=80', verbose_name="Hero Arxa Fon Şəkli")

    # About Section
    about_story_p1 = models.TextField(blank=True, verbose_name="Hekayəmiz 1-ci abzas (AZ)")
    about_story_p1_en = models.TextField(blank=True, verbose_name="Hekayəmiz 1-ci abzas (EN)")
    about_story_p1_ru = models.TextField(blank=True, verbose_name="Hekayəmiz 1-ci abzas (RU)")
    about_story_p2 = models.TextField(blank=True, verbose_name="Hekayəmiz 2-ci abzas (AZ)")
    about_story_p2_en = models.TextField(blank=True, verbose_name="Hekayəmiz 2-ci abzas (EN)")
    about_story_p2_ru = models.TextField(blank=True, verbose_name="Hekayəmiz 2-ci abzas (RU)")
    about_mission_desc = models.TextField(blank=True, verbose_name="Missiyamız (AZ)")
    about_mission_desc_en = models.TextField(blank=True, verbose_name="Missiyamız (EN)")
    about_mission_desc_ru = models.TextField(blank=True, verbose_name="Missiyamız (RU)")
    about_vision_desc = models.TextField(blank=True, verbose_name="Vizyonumuz (AZ)")
    about_vision_desc_en = models.TextField(blank=True, verbose_name="Vizyonumuz (EN)")
    about_vision_desc_ru = models.TextField(blank=True, verbose_name="Vizyonumuz (RU)")
    about_experience_years = models.CharField(max_length=50, default='12+', verbose_name="Təcrübə İli")

    def __str__(self):
        return "Sayt Sazlamaları və Əlaqə Məlumatları"

    class Meta:
        verbose_name = "Sayt Sazlaması"
        verbose_name_plural = "Sayt Sazlamaları"


class Feature(models.Model):
    title = models.CharField(max_length=150, verbose_name="Başlıq (AZ)")
    title_en = models.CharField(max_length=150, blank=True, verbose_name="Başlıq (EN)")
    title_ru = models.CharField(max_length=150, blank=True, verbose_name="Başlıq (RU)")
    description = models.TextField(verbose_name="Təsvir (AZ)")
    description_en = models.TextField(blank=True, verbose_name="Təsvir (EN)")
    description_ru = models.TextField(blank=True, verbose_name="Təsvir (RU)")
    icon_class = models.CharField(max_length=100, default='fa-shield-alt', verbose_name="İkon klassı (FontAwesome)")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Üstünlük / Xüsusiyyət"
        verbose_name_plural = "Üstünlüklərimiz"


class CompanyStatistic(models.Model):
    title = models.CharField(max_length=150, verbose_name="Göstərici Adı (AZ)")
    title_en = models.CharField(max_length=150, blank=True, verbose_name="Göstərici Adı (EN)")
    title_ru = models.CharField(max_length=150, blank=True, verbose_name="Göstərici Adı (RU)")
    number = models.CharField(max_length=50, default='8500', verbose_name="Rəqəm")
    suffix = models.CharField(max_length=50, default='+', verbose_name="Şəkilçi / Simvol (AZ)")
    suffix_en = models.CharField(max_length=50, blank=True, verbose_name="Şəkilçi / Simvol (EN)")
    suffix_ru = models.CharField(max_length=50, blank=True, verbose_name="Şəkilçi / Simvol (RU)")
    icon_class = models.CharField(max_length=100, default='fa-users', verbose_name="İkon klassı")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    def __str__(self):
        return f"{self.title}: {self.number}{self.suffix}"

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Statistika Göstəricisi"
        verbose_name_plural = "Statistika Göstəriciləri"


class TeamMember(models.Model):
    name = models.CharField(max_length=120, verbose_name="Ad və Soyad")
    role = models.CharField(max_length=120, verbose_name="Vəzifə (AZ)")
    role_en = models.CharField(max_length=120, blank=True, verbose_name="Vəzifə (EN)")
    role_ru = models.CharField(max_length=120, blank=True, verbose_name="Vəzifə (RU)")
    photo = models.CharField(max_length=500, blank=True, verbose_name="Şəkil URL / Yol")
    linkedin_url = models.URLField(blank=True, default='#', verbose_name="LinkedIn")
    instagram_url = models.URLField(blank=True, default='#', verbose_name="Instagram")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Komanda Üzvü"
        verbose_name_plural = "Komanda Heyəti"


class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Sual (AZ)")
    question_en = models.CharField(max_length=300, blank=True, verbose_name="Sual (EN)")
    question_ru = models.CharField(max_length=300, blank=True, verbose_name="Sual (RU)")
    answer = models.TextField(verbose_name="Cavab (AZ)")
    answer_en = models.TextField(blank=True, verbose_name="Cavab (EN)")
    answer_ru = models.TextField(blank=True, verbose_name="Cavab (RU)")
    icon_class = models.CharField(max_length=100, default='fa-question-circle', verbose_name="İkon")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Tez-tez Verilən Sual"
        verbose_name_plural = "Tez-tez Verilən Suallar (FAQ)"


class Partner(models.Model):
    name = models.CharField(max_length=120, verbose_name="Tərəfdaş / Aviaşirkət Adı")
    icon_class = models.CharField(max_length=100, default='fa-plane', verbose_name="İkon klassı")
    logo_image = models.CharField(max_length=500, blank=True, verbose_name="Loqo Şəkli (URL)")
    website_url = models.URLField(blank=True, verbose_name="Veb Sayt")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Tərəfdaş / Aviaşirkət"
        verbose_name_plural = "Tərəfdaşlar və Aviaşirkətlər"


class TourBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Gözləmədə'),
        ('confirmed', 'Təsdiqləndi'),
        ('cancelled', 'Ləğv edildi'),
    )
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings', verbose_name="Tur")
    tour_name = models.CharField(max_length=200, blank=True, verbose_name="Tur Adı")
    full_name = models.CharField(max_length=150, verbose_name="Ad və Soyad")
    phone = models.CharField(max_length=50, verbose_name="Telefon Nömrəsi")
    email = models.EmailField(verbose_name="E-poçt Ünvanı")
    travel_date = models.CharField(max_length=100, blank=True, verbose_name="Səyahət Tarixi")
    guests_count = models.CharField(max_length=50, blank=True, verbose_name="Qonaq Sayı")
    notes = models.TextField(blank=True, verbose_name="Əlavə Qeydlər")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sifariş Tarixi")

    def __str__(self):
        return f"{self.full_name} - {self.tour_name or (self.tour.title if self.tour else 'Ümumi Səyahət')}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tur Rezervasiyası"
        verbose_name_plural = "Tur Rezervasiyaları"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="E-poçt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Abunəlik Tarixi")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bülleten Abunəçisi"
        verbose_name_plural = "Bülleten Abunəçiləri"
