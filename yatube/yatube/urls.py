from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('', include('posts.urls', namespace='posts')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('api-token-auth/', views.obtain_auth_token),
]

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
handler403 = "core.views.permission_denied"

'''if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )'''

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
