from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state}"


class Agent(models.Model):
    name        = models.CharField(max_length=120)
    phone       = models.CharField(max_length=20)
    email       = models.EmailField()
    photo       = models.ImageField(upload_to='agents/', blank=True, null=True)
    bio         = models.TextField(blank=True)
    verified    = models.BooleanField(default=False)
    listings_count = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('villa',     'Villa'),
        ('plot',      'Plot / Land'),
        ('penthouse', 'Penthouse'),
        ('commercial','Commercial'),
        ('office',    'Office Space'),
        ('shop',      'Shop / Showroom'),
        ('warehouse', 'Warehouse'),
    ]

    LISTING_PURPOSE = [
        ('sale',  'For Sale'),
        ('rent',  'For Rent'),
        ('lease', 'For Lease'),
    ]

    STATUS_CHOICES = [
        ('available',  'Available'),
        ('under_offer','Under Offer'),
        ('sold',       'Sold'),
        ('rented',     'Rented'),
    ]

    FURNISHING = [
        ('unfurnished',       'Unfurnished'),
        ('semi_furnished',    'Semi-Furnished'),
        ('fully_furnished',   'Fully Furnished'),
    ]

    FACING = [
        ('north', 'North'),
        ('south', 'South'),
        ('east',  'East'),
        ('west',  'West'),
        ('ne',    'North-East'),
        ('nw',    'North-West'),
        ('se',    'South-East'),
        ('sw',    'South-West'),
    ]

    # Core fields
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title          = models.CharField(max_length=200)
    slug           = models.SlugField(max_length=220, unique=True, blank=True)
    description    = models.TextField()
    property_type  = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    purpose        = models.CharField(max_length=10, choices=LISTING_PURPOSE, default='sale')
    status         = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    # Location
    address        = models.CharField(max_length=300)
    locality       = models.CharField(max_length=150)
    city           = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    pincode        = models.CharField(max_length=10, blank=True)
    latitude       = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude      = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Pricing
    price          = models.DecimalField(max_digits=14, decimal_places=2)
    price_negotiable = models.BooleanField(default=False)
    maintenance_charges = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Specs
    bedrooms       = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms      = models.PositiveSmallIntegerField(null=True, blank=True)
    balconies      = models.PositiveSmallIntegerField(null=True, blank=True)
    parking_spots  = models.PositiveSmallIntegerField(default=0)
    floor_number   = models.PositiveSmallIntegerField(null=True, blank=True)
    total_floors   = models.PositiveSmallIntegerField(null=True, blank=True)
    built_up_area  = models.DecimalField(max_digits=10, decimal_places=2, help_text='sqft')
    carpet_area    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='sqft')
    plot_area      = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='sqft')

    # Features
    furnishing     = models.CharField(max_length=20, choices=FURNISHING, default='unfurnished')
    facing         = models.CharField(max_length=5, choices=FACING, blank=True)
    age_of_property= models.PositiveSmallIntegerField(null=True, blank=True, help_text='years')

    # Amenities (booleans)
    has_gym        = models.BooleanField(default=False)
    has_pool       = models.BooleanField(default=False)
    has_security   = models.BooleanField(default=False)
    has_lift       = models.BooleanField(default=False)
    has_garden     = models.BooleanField(default=False)
    has_clubhouse  = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)
    pet_friendly   = models.BooleanField(default=False)

    # Cover image
    cover_image    = models.ImageField(upload_to='properties/', blank=True, null=True)

    # Relations
    agent          = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')

    # Owner contact (direct listings without agent)
    owner_name     = models.CharField(max_length=120, blank=True)
    owner_phone    = models.CharField(max_length=20, blank=True)
    owner_email    = models.EmailField(blank=True)

    # Meta
    is_featured    = models.BooleanField(default=False)
    is_verified    = models.BooleanField(default=False)
    views_count    = models.PositiveIntegerField(default=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'slug': self.slug})

    @property
    def formatted_price(self):
        price = float(self.price)
        if price >= 10_000_000:
            return f"₹{price/10_000_000:.2f} Cr"
        elif price >= 100_000:
            return f"₹{price/100_000:.2f} L"
        else:
            return f"₹{price:,.0f}"

    @property
    def amenities_list(self):
        amenities = []
        if self.has_gym:       amenities.append(('🏋️', 'Gym'))
        if self.has_pool:      amenities.append(('🏊', 'Swimming Pool'))
        if self.has_security:  amenities.append(('🔒', '24/7 Security'))
        if self.has_lift:      amenities.append(('🛗', 'Elevator'))
        if self.has_garden:    amenities.append(('🌿', 'Garden'))
        if self.has_clubhouse: amenities.append(('🏡', 'Clubhouse'))
        if self.has_power_backup: amenities.append(('⚡', 'Power Backup'))
        if self.pet_friendly:  amenities.append(('🐾', 'Pet Friendly'))
        return amenities


class PropertyImage(models.Model):
    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='properties/gallery/')
    caption     = models.CharField(max_length=200, blank=True)
    is_primary  = models.BooleanField(default=False)
    order       = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.property.title}"


class Inquiry(models.Model):
    STATUS = [
        ('new',      'New'),
        ('contacted','Contacted'),
        ('closed',   'Closed'),
    ]

    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    name        = models.CharField(max_length=120)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20)
    message     = models.TextField()
    status      = models.CharField(max_length=12, choices=STATUS, default='new')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} — {self.property.title}"


class PropertyEnlistRequest(models.Model):
    """Submitted via the public 'Enlist Your Property' form — reviewed by admin."""
    PROPERTY_TYPES = Property.PROPERTY_TYPES
    LISTING_PURPOSE = Property.LISTING_PURPOSE

    STATUS = [
        ('pending',  'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Owner details
    owner_name  = models.CharField(max_length=120)
    owner_phone = models.CharField(max_length=20)
    owner_email = models.EmailField()

    # Property basics
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    purpose       = models.CharField(max_length=10, choices=LISTING_PURPOSE)
    city          = models.CharField(max_length=100)
    locality      = models.CharField(max_length=150)
    price         = models.DecimalField(max_digits=14, decimal_places=2)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms      = models.PositiveSmallIntegerField(null=True, blank=True)
    description   = models.TextField()

    # Review
    status        = models.CharField(max_length=12, choices=STATUS, default='pending')
    admin_notes   = models.TextField(blank=True)

    submitted_at  = models.DateTimeField(auto_now_add=True)
    reviewed_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.owner_name} — {self.get_property_type_display()} in {self.city}"
