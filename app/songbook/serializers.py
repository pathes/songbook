from django.contrib.auth.models import User

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


class SonglistSerializer(serializers.ModelSerializer):
    pk = serializers.Field()

    class Meta:
        model = Songlist
        fields = ('pk', 'author', 'title', 'is_public', 'songs')


class ArticleSerializer(serializers.ModelSerializer):
    pk = serializers.Field()

    class Meta:
        model = Article
        fields = ('pk', 'author', 'title', 'content')
