from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Property, PropertyImage, Agent, Inquiry, PropertyEnlistRequest, City


admin.site.site_header  = "HouseSquare Admin"
admin.site.site_title   = "HouseSquare"
admin.site.index_title  = "Property Management Dashboard"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ('name', 'state')
    search_fields = ('name', 'state')


class PropertyImageInline(admin.TabularInline):
    model   = PropertyImage
    extra   = 3
    fields  = ('image', 'caption', 'is_primary', 'order')


class InquiryInline(admin.TabularInline):
    model      = Inquiry
    extra      = 0
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    can_delete = False


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display   = ('thumb', 'title', 'property_type', 'purpose', 'formatted_price_display',
                      'city', 'status', 'is_featured', 'is_verified', 'views_count', 'created_at')
    list_filter    = ('property_type', 'purpose', 'status', 'is_featured', 'is_verified', 'city')
    search_fields  = ('title', 'locality', 'address', 'owner_name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable  = ('status', 'is_featured', 'is_verified')
    date_hierarchy = 'created_at'
    inlines        = [PropertyImageInline, InquiryInline]
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'description', 'property_type', 'purpose', 'status', 'is_featured', 'is_verified')
        }),
        ('Location', {
            'fields': ('address', 'locality', 'city', 'pincode', 'latitude', 'longitude')
        }),
        ('Pricing', {
            'fields': ('price', 'price_negotiable', 'maintenance_charges')
        }),
        ('Specifications', {
            'fields': ('bedrooms', 'bathrooms', 'balconies', 'parking_spots',
                       'floor_number', 'total_floors', 'built_up_area', 'carpet_area', 'plot_area',
                       'furnishing', 'facing', 'age_of_property')
        }),
        ('Amenities', {
            'fields': ('has_gym', 'has_pool', 'has_security', 'has_lift',
                       'has_garden', 'has_clubhouse', 'has_power_backup', 'pet_friendly'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Contact', {
            'fields': ('agent', 'owner_name', 'owner_phone', 'owner_email')
        }),
        ('Stats', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumb(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:4px;">', obj.cover_image.url)
        return "—"
    thumb.short_description = ''

    def formatted_price_display(self, obj):
        return obj.formatted_price
    formatted_price_display.short_description = 'Price'


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display  = ('photo_thumb', 'name', 'phone', 'email', 'verified', 'listings_count')
    list_editable = ('verified',)
    search_fields = ('name', 'email', 'phone')

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">', obj.photo.url)
        return "👤"
    photo_thumb.short_description = ''


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'property_link', 'status', 'created_at')
    list_filter   = ('status',)
    list_editable = ('status',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

    def property_link(self, obj):
        return format_html('<a href="/admin/listings/property/{}/change/">{}</a>', obj.property.pk, obj.property.title[:50])
    property_link.short_description = 'Property'


@admin.register(PropertyEnlistRequest)
class PropertyEnlistRequestAdmin(admin.ModelAdmin):
    list_display  = ('owner_name', 'owner_phone', 'property_type', 'purpose',
                     'city', 'locality', 'formatted_price', 'status', 'submitted_at')
    list_filter   = ('status', 'property_type', 'purpose')
    list_editable = ('status',)
    search_fields = ('owner_name', 'owner_phone', 'owner_email', 'city')
    readonly_fields = ('submitted_at',)

    fieldsets = (
        ('Owner', {'fields': ('owner_name', 'owner_phone', 'owner_email')}),
        ('Property', {'fields': ('property_type', 'purpose', 'city', 'locality', 'price', 'built_up_area', 'bedrooms', 'description')}),
        ('Review', {'fields': ('status', 'admin_notes', 'submitted_at')}),
    )

    def formatted_price(self, obj):
        price = float(obj.price)
        if price >= 10_000_000:
            return f"₹{price/10_000_000:.2f} Cr"
        elif price >= 100_000:
            return f"₹{price/100_000:.2f} L"
        return f"₹{price:,.0f}"
    formatted_price.short_description = 'Price'

    actions = ['mark_approved', 'mark_rejected']

    def mark_approved(self, request, queryset):
        queryset.update(status='approved', reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} requests approved.")
    mark_approved.short_description = "✅ Approve selected requests"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected', reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} requests rejected.")
    mark_rejected.short_description = "❌ Reject selected requests"
