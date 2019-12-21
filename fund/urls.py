"""funds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.index,name='index'),
    path('donate/', views.dform,name='donate'),
    path('citizen/',views.cform,name='citizen'),
    path('required/',views.rform,name='required'),
    path('food/',views.fform,name='food'),
    path('medicine/',views.mform,name='medicine'),
    path('stay/',views.sfrom,name='stay'),
    path('chart/',views.chart,name='chart'),
    path('admin/',views.update,name='update'),
    path('foodlist/',views.foodlist,name='list'),
    path('requiredlist/',views.requiredlist,name='list'),
    path('staylist/',views.staylist,name='list'),
    path('medlist/',views.medlist,name='list'),
    path('spentlist/',views.spentlist,name='list'),
    path('signup/',views.signup,name='list'),
    path('admin/login/',auth_views.login,{'template_name': 'admin/login.html'}),
    path('admin/logout/', views.logout_view),
    path('search/', views.search,name='search'),
    path('chart1/',views.chart2,name='chart1'),
    path('admin/chart/',views.adchart,name='chart1'),
    path('admin/chart1/',views.adchart2,name='chart1'),
    path("admin/submit/",views.submit,name='submit'),
    
    
    
     
    
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
