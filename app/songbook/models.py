from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    author = models.ForeignKey(User)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    performer = models.CharField(max_length=255, blank=True)
    composer = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=4, blank=True)
    confirmed = models.BooleanField(default=False)
    content = models.TextField()

    def __unicode__(self):
        return self.title


class Songlist(models.Model):
    author = models.ForeignKey(User)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, through='SonglistItem')
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class SonglistItem(models.Model):
    song = models.ForeignKey(Song)
    songlist = models.ForeignKey(Songlist)
    order = models.IntegerField()

    def __unicode__(self):
        return u'{}[{}] {}'.format(self.songlist.title, self.order, self.song.title)
