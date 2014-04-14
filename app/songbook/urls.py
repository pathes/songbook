from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'song', views.SongViewSet)
router.register(r'songlist', views.SonglistViewSet)
router.register(r'article', views.ArticleViewSet)


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^(?P<subpage>.*)$', views.main_view),
)
