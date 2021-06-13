"""invoicesystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Invoice system urls
    path('api/v1/', include('payparc_invoicing.urls', namespace='invoice-routing')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Django url's
    path('admin/', admin.site.urls),
    # DRF url's
    path('', include_docs_urls(title='Invoice System')),
    path('schema', get_schema_view(
        title="Invoice System",
        description="Invoice System API",
        version="1.0.0"
    ), name='openapi-schema'),

]
