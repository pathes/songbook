from rest_framework import serializers
from models import *


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
