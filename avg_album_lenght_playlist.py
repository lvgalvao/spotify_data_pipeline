import spotipy
import csv
import boto3
from datetime import datetime

from config.playlist import spotify_playlist
from tools.playlist import get_artists_from_playlist

# import os

# # Set the environment variable
# os.environ['SPOTIPY_CLIENT_ID'] = 'SPOTIPY_CLIENT_ID'
# os.environ['SPOTIPY_CLIENT_SECRET'] = 'SPOTIPY_CLIENT_SECRET'

spotify_object = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())


final_data_dictionary = {
    'Year Relased': [],
    'Album Length': [],
    'Album Name': [],
    'Artist Name': []
}

PLAYLIST = 'energy_boost'

def gather_data_local():
    # For every artist we're looking for
    final_data_dictionary = {
        'Year Released': [],
        'Album Length': [],
        'Album Name': [],
        'Artist Name': []
    }
    with open("rapcaviar_albums.csv", 'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []

        artists = get_artists_from_playlist(spotify_playlist()[PLAYLIST])

        # for artist in artists.keys():
        for artist in list(artists.keys()):
            print(artist)
            artists_albums = spotify_object.artist_albums(artist, album_type='album', limit=50)
            # For all of their albums
            for album in artists_albums['items']:
                if 'GB' and 'US' in album['available_markets']:
                    key = album['name'] + album['artists'][0]['name'] + album['release_date'][:4]
                    if key not in albums_obtained:
                        albums_obtained.append(key)
                        album_data = spotify_object.album(album['uri'])
                        # For every song in the album
                        album_length_ms = 0
                        for song in album_data['tracks']['items']:
                            album_length_ms = song['duration_ms'] + album_length_ms
                        writer.writerow({'Year Released': album_data['release_date'][:4],
                                         'Album Length': album_length_ms,
                                         'Album Name': album_data['name'],
                                         'Artist Name': album_data['artists'][0]['name']})
                        final_data_dictionary['Year Released'].append(album_data['release_date'][:4])
                        final_data_dictionary['Album Length'].append(album_length_ms)
                        final_data_dictionary['Album Name'].append(album_data['name'])
                        final_data_dictionary['Artist Name'].append(album_data['artists'][0]['name'])

    return final_data_dictionary
if __name__ == '__main__':
    gather_data_local()