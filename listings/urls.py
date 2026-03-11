from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('',                    views.home,           name='home'),
    path('properties/',         views.listing_list,   name='list'),
    path('properties/<slug:slug>/', views.listing_detail, name='detail'),
    path('enlist/',             views.enlist,         name='enlist'),
    path('enlist/success/',     views.enlist_success, name='enlist_success'),
    path('agents/',             views.agent_list,     name='agents'),
    path('agents/<int:pk>/',    views.agent_detail,   name='agent_detail'),
]
