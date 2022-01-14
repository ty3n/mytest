from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from . import views

urlpatterns= [
    # path("", views.index, name="index"),
    path('',TemplateView.as_view(template_name="index.html")),
    path("api/data/",views.Collect.as_view(),name="api-data"),
    path("api/dload/",views.GiteaDownload.as_view(),name="api-dload"),
    path("api/arp/",views.Arp.as_view(),name="api-arp"),
]

urlpatterns += staticfiles_urlpatterns()