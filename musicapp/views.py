from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from .forms import *
    
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/signup.html', {'form': form})
    
    
    
@login_required()
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def SongUploadView(request):
    if request.method == 'POST':
        sform = SongUploadForm(request.POST)
        if sform.is_valid():
            sform.save()
            messages.success(request, f'Your song is uploaded!')
            return redirect('index')
    else:
        sform = SongUploadForm()
    return render(request, 'musicapp/upload.html', {'sform': sform})


def index1(request):
    return render(request, 'musicapp/new_index.html')

# Create your views here.
def index(request):

    #Display recent songs
    if not request.user.is_anonymous :
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent = None
        recent_songs = None

    first_time = False
    #Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(id=7)

    else:
        first_time = True
        last_played_song = Song.objects.get(id=7)

    #Display all songs
    songs = Song.objects.all()

    #Display few songs on home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:5]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Soul Songs
    Type_Soul = list(Song.objects.filter(SongType='R&B/Soul').values('id'))
    sliced_ids = [each['id'] for each in Type_Soul][:5]
    indexpage_Soul_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Rock Songs
    Type_Rock = list(Song.objects.filter(SongType='Rock').values('id'))
    sliced_ids = [each['id'] for each in Type_Rock][:5]
    indexpage_Rock_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display Emo Songs
    Type_Emo = list(Song.objects.filter(SongType='Emo').values('id'))
    sliced_ids = [each['id'] for each in Type_Emo][:5]
    indexpage_Emo_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display Jazz Songs
    Type_Jazz = list(Song.objects.filter(SongType='Jazz').values('id'))
    sliced_ids = [each['id'] for each in Type_Jazz][:5]
    indexpage_Jazz_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display BoomBap Songs
    Type_BoomBap = list(Song.objects.filter(SongType='BoomBap').values('id'))
    sliced_ids = [each['id'] for each in Type_BoomBap][:5]
    indexpage_BoomBap_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display Trap Songs
    Type_Trap = list(Song.objects.filter(SongType='Trap').values('id'))
    sliced_ids = [each['id'] for each in Type_Trap][:5]
    indexpage_Trap_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display Auto-Tunes Songs
    Type_Autotunes = list(Song.objects.filter(SongType='Autotunes').values('id'))
    sliced_ids = [each['id'] for each in Type_Autotunes][:5]
    indexpage_Autotunes_songs = Song.objects.filter(id__in=sliced_ids)

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query)).distinct()
        context = {'all_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/index.html', context)

    context = {
        'all_songs':indexpage_songs,
        'recent_songs': recent_songs,
        'Soul_songs':indexpage_Soul_songs,
        'Rock_songs':indexpage_Rock_songs,
        'Emo_songs':indexpage_Emo_songs,
        'last_played':last_played_song,
        'first_time': first_time,
        'query_search':False,
    }
    return render(request, 'musicapp/index.html', context=context)


def Soul_songs(request):

    Soul_songs = Song.objects.filter(SongType='R&B/Soul')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Soul_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Soul_songs': Soul_songs}
        return render(request, 'musicapp/Soul_songs.html', context)

    context = {'Soul_songs':Soul_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Soul_songs.html',context=context)

def Emo_songs(request):

    Emo_songs = Song.objects.filter(SongType='Emo')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Soul_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Emo_songs': Emo_songs}
        return render(request, 'musicapp/Emo_songs.html', context)

    context = {'Emo_songs':Emo_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Emo_songs.html',context=context)

def Jazz_songs(request):

    Jazz_songs = Song.objects.filter(SongType='Jazz')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Jazz_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Jazz_songs': Jazz_songs}
        return render(request, 'musicapp/Jazz_songs.html', context)

    context = {'Jazz_songs':Jazz_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Jazz_songs.html',context=context)
    
def Trap_songs(request):

    Trap_songs = Song.objects.filter(SongType='Trap')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Trap_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Trap_songs': Trap_songs}
        return render(request, 'musicapp/Trap_songs.html', context)

    context = {'Trap_songs':Trap_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Trap_songs.html',context=context)
    
def BoomBap_songs(request):

    BoomBap_songs = Song.objects.filter(SongType='BoomBap')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Jazz_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'BoomBap_songs': Jazz_songs}
        return render(request, 'musicapp/BoomBap_songs.html', context)

    context = {'BoomBap_songs':BoomBap_songs,'last_played':last_played_song}
    return render(request, 'musicapp/BoomBap_songs.html',context=context)

def Rock_songs(request):

    Rock_songs = Song.objects.filter(SongType='Rock')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Rock_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Rock_songs': Rock_songs}
        return render(request, 'musicapp/Rock_songs.html', context)

    context = {'Rock_songs':Rock_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Rock_songs.html',context=context)
    
def Autotunes_songs(request):

    Autotunes_songs = Song.objects.filter(SongType='Autotunes')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        Autotunes_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'Autotunes_songs': Autotunes_songs}
        return render(request, 'musicapp/Autotunes_songs.html', context)

    context = {'Autotunes_songs':Autotunes_songs,'last_played':last_played_song}
    return render(request, 'musicapp/Autotunes_songs.html',context=context)

@login_required(login_url='login')
def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('index')

@login_required(login_url='login')
def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('recent')


def all_songs(request):
    songs = Song.objects.all()

    first_time = False
    #Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
    else:
        first_time = True
        last_played_song = Song.objects.get(id=7)

    
    # apply search filters
    qs_singers = Song.objects.values_list('singer').all()
    s_list = [s.split(',') for singer in qs_singers for s in singer]
    all_singers = sorted(list(set([s.strip() for singer in s_list for s in singer])))
    qs_SongType = Song.objects.values_list('SongType').all()
    all_SongType = sorted(list(set([l.strip() for lang in qs_SongType for l in lang])))
    
    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        search_singer = request.GET.get('singers') or ''
        search_SongType = request.GET.get('SongType') or ''
        filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(Q(SongType__icontains=search_SongType)).filter(Q(singer__icontains=search_singer)).distinct()
        context = {
        'songs': filtered_songs,
        'last_played':last_played_song,
        'all_singers': all_singers,
        'all_SongType': all_SongType,
        'query_search': True,
        }
        return render(request, 'musicapp/all_songs.html', context)

    context = {
        'songs': songs,
        'last_played':last_played_song,
        'first_time':first_time,
        'all_singers': all_singers,
        'all_SongType': all_SongType,
        'query_search' : False,
        }
    return render(request, 'musicapp/all_songs.html', context=context)


def recent(request):
    
    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    #Display recent songs
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if recent and not request.user.is_anonymous :
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs = None

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {'recent_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/recent.html', context)

    context = {'recent_songs':recent_songs,'last_played':last_played_song,'query_search':False}
    return render(request, 'musicapp/recent.html', context=context)


@login_required(login_url='login')
def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()

    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)


    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)

    context = {'songs': songs, 'playlists': playlists, 'is_favourite': is_favourite,'last_played':last_played_song}
    return render(request, 'musicapp/detail.html', context=context)


def mymusic(request):
    return render(request, 'musicapp/mymusic.html')


def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')
    
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs}
    return render(request, 'musicapp/favourite.html', context=context)
    
    
