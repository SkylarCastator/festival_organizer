import requests


class SpotifyManager:
    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        })

        auth_data = auth_response.json()
        self.access_token = auth_data['access_token']
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        print ("Connected")

    def find_playlists(self, USERNAME):
        playlist_url = f'https://api.spotify.com/v1/users/{USERNAME}/playlists'
        playlist_response = requests.get(playlist_url, headers=self.headers)
        playlist_data = playlist_response.json()
        return playlist_data['items']

    def search_playlist_for_artist(self, playlist, artists_to_search):
        artist_data = {}
        for artist in artists_to_search:
            artist_data[artist] = []

        playlist_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist["id"]}/tracks'
        playlist_tracks_response = requests.get(playlist_tracks_url, headers=self.headers)
        playlist_tracks_data = playlist_tracks_response.json()

        for track in playlist_tracks_data['items']:
            track_artists = [artist['name'] for artist in track['track']['artists']]
            for artist in artists_to_search:
                if artist in track_artists:
                    artist_data[artist].append(track['track']['name'])

        return artist_data