from django.urls import path
from django.conf.urls import include, url
from . import views
from musicapp.views import *

# Add URLConf
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index1, name='Index'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('mymusic/', views.mymusic, name='mymusic'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('recent/', views.recent, name='recent'),
    path('Soul_songs/', Soul_songs, name='Soul_songs'),
    path('Rock_songs/', Rock_songs, name='Rock_songs'),
    path('Emo_songs/', Emo_songs, name='Emo_songs'),
    path('Jazz_songs/', Jazz_songs, name='Jazz_songs'),
    path('Autotunes_songs/', Autotunes_songs, name='Autotunes_songs'),
    path('BoomBap_songs/', BoomBap_songs, name='BoomBap_songs'),
    path('Trap_songs/', Trap_songs, name='Trap_songs'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),
    url(r'^songs/', include([
        url(r'^upload', SongUploadView, name='upload'),
    ])),
    path('profile/', profile, name='profile'),

]
