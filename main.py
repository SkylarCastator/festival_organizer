import json
from spotify_manager import SpotifyManager


def load_concert_details():
    file_path = f"edc_saturday_2023.json"
    with open(file_path, "r") as f:
        dict = json.load(f)
        return dict


def sort_artists(artists_dict):
    artists_start_times = [(artist, details['start-time'], details['end-time'], details['stage']) for artist, details in artists_dict.items()]
    artists_start_times.sort(key=lambda x: (x[1], x[2]))
    recommended_artists = []
    conflicts = []
    current_end_time = None

    for artist, start_time, end_time, stage in artists_start_times:
        if current_end_time is None or start_time >= current_end_time:
            recommended_artists.append((artist, start_time, end_time, stage))
            current_end_time = end_time
        else:
            conflicts.append((artist, start_time, end_time, stage))

    return recommended_artists, conflicts


if __name__ == "__main__":
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    REDIRECT_URI = 'google.com'

    spotify_instance = SpotifyManager(CLIENT_ID, CLIENT_SECRET)
    concert_data = load_concert_details()
    artists_to_search = []
    for artist in concert_data:
        artists_to_search.append(artist)
    playlists = spotify_instance.find_playlists("username")

    playlist_count_data = {}
    for artist in artists_to_search:
        playlist_count_data[artist] = 0

    print("Please wait while we search your spotify account")
    for playlist in playlists:
        artist_information = spotify_instance.search_playlist_for_artist(playlist, artists_to_search)
        for artist_data in artist_information:
            if len(artist_information[artist_data]) > 0:
                playlist_count_data[artist_data] += len(artist_information[artist_data])

    liked_artist_dictionary = {}
    for artist_data in playlist_count_data:
        if playlist_count_data[artist_data] > 0:
            liked_artist_dictionary[artist_data] = concert_data[artist_data]

    recommended, conflicts = sort_artists(liked_artist_dictionary)

    print("We did a search of your Spotify library and found artist you have added to playlists.")
    print("Recommended artists:")
    for artist_recommended in recommended:
        artist, start_time, end_time, stage = artist_recommended
        print(f"{artist}: {stage} : {start_time} - {end_time}")

    print("\nConflicting shows:")
    for conflict in conflicts:
        artist, start_time, end_time, stage = conflict
        print(f"{artist}: {stage} : {start_time} - {end_time}")




