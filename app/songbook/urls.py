from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'song', views.SongViewSet)
router.register(r'songlist', views.SonglistViewSet)
router.register(r'article', views.ArticleViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/$', views.AuthView.as_view(), name='authenticate'),
    url(r'^api/locale/$', views.LocaleView.as_view(), name='locale'),
    url(r'^api/pdf/(?P<songlist_id>.*)/$', views.SonglistPDFView.as_view(), name='locale'),
    url(r'^(?P<subpage>.*)$', views.main_view),
]
