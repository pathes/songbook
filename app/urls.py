from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$','django.contrib.auth.views.logout_then_login'),
    url(r'^', include('app.songbook.urls')),
)
