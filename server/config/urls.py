from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from apps.api.routers import router
from .yasg import urlpatterns as docs_urls
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/token', views.obtain_auth_token, name='tokens'),
]

urlpatterns += docs_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [
          path('__debug__/', include(debug_toolbar.urls)),
    ]

