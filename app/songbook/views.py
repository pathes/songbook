from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import *
from .models import *
from .serializers import *
from .authenticators import *
from .tasks import *


def main_view(request, **kwargs):
    return render(
        request,
        'songbook/main.html',
        kwargs
    )


class LocaleView(APIView):
    def get(self, request, format=None):
        return Response({'locale': request.session['django_language']})

    def post(self, request, format=None):
        if request.method == 'POST':
            request.session['django_language'] = request.data['locale']
        return Response({'locale': request.session['django_language']})


class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication, )

    def post(self, request, format=None):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, format=None):
        logout(request)
        return Response()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )


class SonglistViewSet(viewsets.ModelViewSet):
    queryset = Songlist.objects.all()
    serializer_class = SonglistSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        q = Q(is_public=True)
        if user.is_authenticated():
            q = q | Q(author=user)
        return Songlist.objects.filter(q)

    # def perform_create(self, serializer):
    #     #  self.object = serializer.save(force_insert=False)  # the only change between ModelViewSet and this
    #     serializer.save(force_insert=False)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         self.pre_save(serializer.object)
    #         self.object = serializer.save(force_insert=False)  # the only change between ModelViewSet and this
    #         self.post_save(self.object, created=True)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                         headers=headers)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )


class SonglistPDFView(View):
    def get(self, request, songlist_id=None):
        songlist = get_object_or_404(Songlist, pk=songlist_id)
        tex_content = render_to_string('songbook/songbook.tex', {'songs': songlist.songs.all()})
        pdf_content = tex_to_pdf(tex_content)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + songlist.title + '.pdf'
        return response


class SonglistTEXView(View):
    def get(self, request, songlist_id=None):
        songlist = get_object_or_404(Songlist, pk=songlist_id)
        tex_content = render_to_string('songbook/songbook.tex', {'songs': songlist.songs.all()})
        response = HttpResponse(tex_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=' + songlist.title + '.tex'
        return response
 
