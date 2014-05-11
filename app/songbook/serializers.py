from itertools import count, izip

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'email')
        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


class SongSerializer(serializers.ModelSerializer):
    pk = serializers.Field()

    class Meta:
        model = Song
        fields = ('pk', 'author', 'title', 'performer', 'composer', 'genre', 'year', 'confirmed', 'content')
        read_only_fields = ('confirmed',)

    def restore_object(self, attrs, instance=None):
        attrs['confirmed'] = False
        return super(SongSerializer, self).restore_object(attrs, instance)


class SonglistSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    songs = serializers.PrimaryKeyRelatedField(many=True)
    author_name = serializers.Field(source='author.__unicode__')

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
        for (order, song) in izip(count(), songs):
            SonglistItem.objects.create(song=song, songlist=songlist, order=order)
        # Note that it won't remove items on some exception because transaction is atomic.

    def restore_object(self, attrs, instance=None):
        songs = attrs.get('songs', ())
        attrs.pop('songs', None)
        if instance is None:
            songlist = Songlist(**attrs)
        else:
            songlist = super(SonglistSerializer, self).restore_object(attrs, instance)
        self.__create_items(songlist, songs)
        return songlist


class ArticleSerializer(serializers.ModelSerializer):
    pk = serializers.Field()

    class Meta:
        model = Article
        fields = ('pk', 'author', 'title', 'content')
