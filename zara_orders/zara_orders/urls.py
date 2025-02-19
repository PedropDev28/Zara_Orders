"""
URL configuration for zara_orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from CRUD_orders.views import ReadAttributesView, UpdateDocumentView, CreateDocumentView, DeleteDocumentView, ReadDocumentView, ReadAvailabilityView, ReadBrandsView, ReadColorsView, ReadConditionsView, ReadDocumentsView, ReadDocumentsByFilterView, TestDatabaseConnectionView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Zara Orders API",
        default_version='v1',
        description="API para gestionar órdenes de Zara en MongoDB"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read_attributes/', ReadAttributesView.as_view()),
    path('read_availability/', ReadAvailabilityView.as_view()),
    path('read_brands/', ReadBrandsView.as_view()),
    path('read_colors/', ReadColorsView.as_view()),
    path('read_conditions/', ReadConditionsView.as_view()),
    path('read_documents/', ReadDocumentsView.as_view()),
    path('filter/', ReadDocumentsByFilterView.as_view()),
    path('test_database_connection/', TestDatabaseConnectionView.as_view()),
    path('read_document/<int:document_id>/', ReadDocumentView.as_view()),
    path('update_document/<int:document_id>/', UpdateDocumentView.as_view()),
    path('create_document/', CreateDocumentView.as_view()),
    path('delete_document/<int:document_id>/', DeleteDocumentView.as_view()),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)