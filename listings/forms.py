from django import forms
from .models import Inquiry, PropertyEnlistRequest, Property


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-input'}),
            'email':   forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-input'}),
            'phone':   forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'I am interested in this property…', 'rows': 4, 'class': 'form-input'}),
        }


class EnlistForm(forms.ModelForm):
    class Meta:
        model  = PropertyEnlistRequest
        fields = [
            'owner_name', 'owner_phone', 'owner_email',
            'property_type', 'purpose', 'city', 'locality',
            'price', 'built_up_area', 'bedrooms', 'description',
        ]
        widgets = {
            'owner_name':    forms.TextInput(attrs={'placeholder': 'Rahul Sharma'}),
            'owner_phone':   forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'owner_email':   forms.EmailInput(attrs={'placeholder': 'owner@email.com'}),
            'city':          forms.TextInput(attrs={'placeholder': 'Bengaluru'}),
            'locality':      forms.TextInput(attrs={'placeholder': 'Indiranagar'}),
            'price':         forms.NumberInput(attrs={'placeholder': '8500000'}),
            'built_up_area': forms.NumberInput(attrs={'placeholder': '1200'}),
            'bedrooms':      forms.NumberInput(attrs={'placeholder': '3', 'min': 1, 'max': 20}),
            'description':   forms.Textarea(attrs={'placeholder': 'Describe key highlights, amenities, special features…', 'rows': 4}),
        }
        labels = {
            'owner_name':    'Your Name',
            'owner_phone':   'Phone Number',
            'owner_email':   'Email Address',
            'property_type': 'Property Type',
            'purpose':       'Listing Purpose',
            'price':         'Expected Price (₹)',
            'built_up_area': 'Built-up Area (sqft)',
            'bedrooms':      'Bedrooms (BHK)',
            'description':   'Property Description',
        }


class PropertySearchForm(forms.Form):
    SORT_CHOICES = [
        ('-created_at', 'Newest First'),
        ('price',       'Price: Low to High'),
        ('-price',      'Price: High to Low'),
        ('-views_count','Most Viewed'),
    ]

    q             = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'City, locality, or keyword…'}))
    property_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + Property.PROPERTY_TYPES)
    purpose       = forms.ChoiceField(required=False, choices=[('', 'Buy / Rent')] + Property.LISTING_PURPOSE)
    bedrooms      = forms.ChoiceField(required=False, choices=[('', 'Any BHK'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5+')])
    min_price     = forms.DecimalField(required=False, label='Min Price')
    max_price     = forms.DecimalField(required=False, label='Max Price')
    sort          = forms.ChoiceField(required=False, choices=SORT_CHOICES)
