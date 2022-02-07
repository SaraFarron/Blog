"""blog URL Configuration

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

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from BlogApp.views import Index, About


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Documentation for all api endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="syulinnikita@gmail.com"),
        license=openapi.License(name="Unlicense"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta', include('rosetta.urls')),
    path('', include('BlogApp.urls')),
    path('api/', include('api.urls')),
    path('user/', include('user.urls')),
    path('about/', About.as_view()),

    path('docs/', include_docs_urls(title='Blog Api')),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

)
urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
    path('', Index.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'BlogApp.views.handler404'
handler400 = 'BlogApp.views.handler400'
handler403 = 'BlogApp.views.handler403'
handler500 = 'BlogApp.views.handler500'
