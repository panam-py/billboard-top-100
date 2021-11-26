from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"
SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

date = input("Enter the date you want to travel to in this format YYYY-MM-DD: ")
username = input("What is your spotify username: ")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, username=username, redirect_uri="https://example.com", scope="playlist-modify-private"))
user_details = sp.current_user()
user_id = user_details['id']


response = requests.get(f"{BILLBOARD_URL}/{date}/")
print("Collecting Songs.....")
soup = BeautifulSoup(response.text, "html.parser")

songs = soup.select(selector=".a-no-trucate")

songs = [song.getText() for song in songs]
songs = [song.split("\n")[1] for song in songs]
actualSongs = []
artists = []

for song in range(0, len(songs), 2):
    actualSongs.append(songs[song])

for artist in range(1, len(songs), 2):
    artists.append(songs[artist])

for i in range(0, len(actualSongs)):
    print(f"{i+1}. {actualSongs[i]}: {artists[i]}")


song_ids = []
for i in actualSongs:
    if len(i) > 1:
        song = sp.search(i, type="track", limit=1)
        song_uri = song['tracks']['items'][0]['id']
        song_ids.append(song_uri)

print("Creating a spotify playlist.......")
playlist = sp.user_playlist_create(user_id, name=f"{date} BILLBOARD 100", public=False, description=f"Billboard's hot 100 for {date}")
print("Playlist created!")
playlist_id = playlist['id']


add_tracks = sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_ids)
print(f"The hot 100 tracks for {date} have been successfully added to the spotify playlist!")