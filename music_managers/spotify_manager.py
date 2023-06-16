import requests


class SpotifyManager:
    def __init__(self, client_id, client_secret):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        })

        auth_data = auth_response.json()
        self.access_token = auth_data['access_token']
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        print ("Connected to spotify")

    def find_playlists(self, username):
        """
        Returns a list of playlist from a user
        :param username: Name of user searched
        """
        playlist_url = f'https://api.spotify.com/v1/users/{username}/playlists'
        playlist_response = requests.get(playlist_url, headers=self.headers)
        playlist_data = playlist_response.json()
        return playlist_data['items']

    def search_playlist_for_artist(self, playlist, artists_to_search):
        """
        Creates a dictionary with keys being the artist and the value being all the music of the artist
        :param playlist: List of playlists to search
        :param artists_to_search: List of artist to search for
        """
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

    def search_spotify_playlists(self, spotify_user, artists_to_search):
        """
        Finds a user's account and iterates through the user's playlist to find artist at the festival
        :param artists_to_search: List of artist to search for
        """
        playlists = self.find_playlists(spotify_user)
        playlist_count_data = {}
        for artist in artists_to_search:
            playlist_count_data[artist] = 0

        print("Please wait while we search your spotify account")
        for playlist in playlists:
            artist_information = self.search_playlist_for_artist(playlist, artists_to_search)
            for artist_data in artist_information:
                if len(artist_information[artist_data]) > 0:
                    playlist_count_data[artist_data] += len(artist_information[artist_data])

        return playlist_count_data
