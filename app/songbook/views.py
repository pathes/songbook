from django.contrib.auth import login, logout
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import *
from models import *
from serializers import *
from authenticators import *
from tasks import *


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
            request.session['django_language'] = request.DATA['locale']
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=False)  # the only change between ModelViewSet and this
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )


class SonglistPDFView(View):
    def get(self, request, songlist_id=None):
        tex_content = """
\documentclass[12pt]{article}
\\begin{document}
\LaTeX\ test

This is songlist """ + str(songlist_id) + """
\end{document}
"""
        pdf_content = tex_to_pdf(tex_content)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=songbook' + str(songlist_id) + '.pdf'
        return response
