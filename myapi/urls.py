"""myapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from myapi.core import views
from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HelloView.as_view(), name='hello'),
    #this path is for getting tokens with username and password
    #NOTE: this currently does not expire on server side
    path('login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('create_callout/', views.CreateRoadsideCalloutView.as_view(), name='create_roadside_callout'),
    path('update_callout/', views.UpdateRoadsideCalloutView.as_view(), name='update_roadside_callout'),
    path('all_callouts/', views.AllRoadsideCalloutsView.as_view(), name='view_all_callouts'),    
    path('add_subscription/', views.AddSubscriptionView.as_view(), name='add_subscription'),
    path('update_subscription/', views.UpdateSubscriptionView.as_view(), name='update_subscription'),
    path('my_subscriptions/', views.MySubscriptionsView.as_view(), name='view_my_subscriptions'),
    path('create_location/', views.CreateLocationView.as_view(), name='create_location'),
    path('update_location/', views.UpdateLocationView.as_view(), name='update_location'),    
    path('get_location/', views.GetLocationView.as_view(), name='get_location'),
    path('update_user_details/', views.UpdateUserDetailsView.as_view(), name='update_user_details'),    
    path('get_user_details/', views.GetUserDetailsView.as_view(), name='get_user_details'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
