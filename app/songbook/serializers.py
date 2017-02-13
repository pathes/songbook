from itertools import count

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from .models import *

# restore_object -> update / create
#   http://www.django-rest-framework.org/topics/3.0-announcement/#the-create-and-update-methods

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'email')
        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def update(self, instance, attrs):
        super().update(instance, attrs)
        instance.set_password(attrs['password'])
        return instance

class SongSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()

    class Meta:
        model = Song
        fields = ('pk', 'author', 'title', 'performer', 'composer', 'genre', 'year', 'confirmed', 'content')
        read_only_fields = ('confirmed',)

    def update(self, instance, attrs):
        attrs['confirmed'] = False
        return super().update(instance, attrs)

class SonglistSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    songs = serializers.PrimaryKeyRelatedField(many=True, queryset=Song.objects.all())
    author_name = serializers.Field(source='author.__unicode__', required=False)

    class Meta:
        model = Songlist
        fields = ('pk', 'author', 'author_name', 'title', 'is_public', 'songs')

    @transaction.atomic
    def __create_items(self, songlist, songs):
        # Now the funny part, deleting every existing SonglistItem...
        #raise ValueError(songlist.id)
        if songlist.id is not None:
            SonglistItem.objects.filter(songlist=songlist).delete()
        songlist.save()
        # ...and creating new.
        for (order, song) in zip(count(), songs):
            SonglistItem.objects.create(song=song, songlist=songlist, order=order)
        # Note that it won't remove items on some exception because transaction is atomic.

    def update(self, instance, attrs):
        songs = attrs.get('songs', ())
        attrs.pop('songs', None)

        songlist = super().update(instance, attrs)

        self.__create_items(songlist, songs)
        return songlist

class ArticleSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ('pk', 'author', 'title', 'content')
