from django.db import models
from django.contrib.auth.models import User, Permission
from PIL import Image



class Genre(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="genres", default="default.jpeg")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Create your models here.
class Song(models.Model):

    SongType_Choice = (
            ('R&B/Soul','R&B/Soul'),
            ('Rock','Rock'),
            ('Jazz/Blues','Jazz/Blues'),
            ('Emo','Emo'),
            ('Bomb bap','Bomb bap'),
            ('Trap','Trap'),
            ('Auto-tunes','Auto-tunes')
          )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    SongType = models.CharField(max_length=20,choices=SongType_Choice,default='')
    song_img = models.FileField()
    year = models.IntegerField()
    singer = models.CharField(max_length=200)
    song_file = models.FileField()
    description = models.TextField(default='', null=True)

    def __str__(self):
        return self.name
    @property
    def song_img_url(self):
        if self.song_img and hasattr(self.song_img, 'url'):
            return self.song_img_url


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)