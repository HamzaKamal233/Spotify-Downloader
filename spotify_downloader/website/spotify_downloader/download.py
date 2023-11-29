import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube

SPOTIPY_CLIENT_ID = '87699f4c2f8146aa929e2d0b80965c3f'
SPOTIPY_CLIENT_SECRET = 'bac8ce68890a447a916c37ef820719a8'

# Set up Spotify API authentication
sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
def get_youtube_links_from_spotify_link(spotify_link):
    if "track" in spotify_link:
        return [get_youtube_link_from_spotify_track(spotify_link)]
    elif "playlist" in spotify_link:
        return get_youtube_links_from_spotify_playlist(spotify_link)
    else:
        print("Invalid Spotify link. Please provide a valid track or playlist link.")
        return []

def get_youtube_link_from_spotify_track(spotify_track_link):
    track_id = spotify_track_link.split('/')[-1].split('?')[0]
    track_info = sp.track(track_id)
    search_query = f"{track_info['name']} {', '.join([artist['name'] for artist in track_info['artists']])} official video"
    videos_search = VideosSearch(search_query, limit=1)
    results = videos_search.result()
    if results['result']:
        return results['result'][0]['link']
    else:
        print(f"No YouTube video found for the given Spotify track: {spotify_track_link}")
        return None

def get_youtube_links_from_spotify_playlist(spotify_playlist_link):
    playlist_id = spotify_playlist_link.split('/')[-1].split('?')[0]
    playlist_info = sp.playlist_tracks(playlist_id)
    youtube_links = []
    for item in playlist_info['items']:
        track_info = item['track']
        search_query = f"{track_info['name']} {', '.join([artist['name'] for artist in track_info['artists']])} official video"
        videos_search = VideosSearch(search_query, limit=1)
        results = videos_search.result()
        if results['result']:
            youtube_links.append(results['result'][0]['link'])
    return youtube_links

def download_youtube_video_as_mp3(youtube_link):
    try:
        yt = YouTube(youtube_link)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if audio_stream:
            temp_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            audio_stream.download(temp_download_path)
            print(f"Downloaded MP3 file to: {temp_download_path}")
        else:
            print(f"No suitable audio stream found for the specified YouTube video: {youtube_link}")
    except Exception as e:
        print(f"An error occurred: {e}")

def downloadSongs(spotify_link):
    youtube_links = get_youtube_links_from_spotify_link(spotify_link)
    for i, youtube_link in enumerate(youtube_links, start=1):
        download_youtube_video_as_mp3(youtube_link)
