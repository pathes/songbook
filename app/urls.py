from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from .songbook import urls as app_songbook_urls

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^', include(app_songbook_urls)),
]
