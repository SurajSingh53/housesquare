from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Property, Agent, Inquiry, PropertyEnlistRequest, City
from .forms import InquiryForm, EnlistForm, PropertySearchForm


# ─── HOME ───────────────────────────────────────────────────────────────────
def home(request):
    featured    = Property.objects.filter(is_featured=True, status='available')[:6]
    latest      = Property.objects.filter(status='available').order_by('-created_at')[:3]
    agents      = Agent.objects.filter(verified=True)[:4]
    total_count = Property.objects.filter(status='available').count()
    cities      = City.objects.all()[:8]

    context = {
        'featured':    featured,
        'latest':      latest,
        'agents':      agents,
        'total_count': total_count,
        'cities':      cities,
        'search_form': PropertySearchForm(),
    }
    return render(request, 'listings/home.html', context)


# ─── LISTING LIST ─────────────────────────────────────────────────────────
def listing_list(request):
    form        = PropertySearchForm(request.GET or None)
    properties  = Property.objects.filter(status='available')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            properties = properties.filter(
                Q(title__icontains=q) |
                Q(locality__icontains=q) |
                Q(city__name__icontains=q) |
                Q(description__icontains=q)
            )

        ptype = form.cleaned_data.get('property_type')
        if ptype:
            properties = properties.filter(property_type=ptype)

        purpose = form.cleaned_data.get('purpose')
        if purpose:
            properties = properties.filter(purpose=purpose)

        bedrooms = form.cleaned_data.get('bedrooms')
        if bedrooms:
            if bedrooms == '5':
                properties = properties.filter(bedrooms__gte=5)
            else:
                properties = properties.filter(bedrooms=int(bedrooms))

        min_price = form.cleaned_data.get('min_price')
        if min_price:
            properties = properties.filter(price__gte=min_price)

        max_price = form.cleaned_data.get('max_price')
        if max_price:
            properties = properties.filter(price__lte=max_price)

        sort = form.cleaned_data.get('sort') or '-created_at'
        properties = properties.order_by(sort)
    else:
        properties = properties.order_by('-created_at')

    paginator = Paginator(properties, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'listings/listing_list.html', {
        'form':     form,
        'page_obj': page_obj,
        'total':    properties.count(),
    })


# ─── LISTING DETAIL ───────────────────────────────────────────────────────
def listing_detail(request, slug):
    prop = get_object_or_404(Property, slug=slug)

    # Increment views
    prop.views_count += 1
    prop.save(update_fields=['views_count'])

    inquiry_form = InquiryForm()

    if request.method == 'POST':
        inquiry_form = InquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry          = inquiry_form.save(commit=False)
            inquiry.property = prop
            inquiry.save()
            messages.success(request, "✅ Your inquiry has been sent! The owner will contact you shortly.")
            return redirect('listings:detail', slug=slug)

    # Similar listings
    similar = Property.objects.filter(
        property_type=prop.property_type,
        status='available'
    ).exclude(pk=prop.pk)[:3]

    return render(request, 'listings/listing_detail.html', {
        'prop':         prop,
        'images':       prop.images.all(),
        'inquiry_form': inquiry_form,
        'similar':      similar,
    })


# ─── ENLIST ───────────────────────────────────────────────────────────────
def enlist(request):
    form = EnlistForm()

    if request.method == 'POST':
        form = EnlistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🏡 Your property has been submitted! Our team will review and reach out within 24 hours.")
            return redirect('listings:enlist_success')

    return render(request, 'listings/enlist.html', {'form': form})


def enlist_success(request):
    return render(request, 'listings/enlist_success.html')


# ─── AGENTS ───────────────────────────────────────────────────────────────
def agent_list(request):
    agents = Agent.objects.filter(verified=True)
    return render(request, 'listings/agents.html', {'agents': agents})


def agent_detail(request, pk):
    agent      = get_object_or_404(Agent, pk=pk)
    properties = Property.objects.filter(agent=agent, status='available')
    return render(request, 'listings/agent_detail.html', {
        'agent':      agent,
        'properties': properties,
    })
