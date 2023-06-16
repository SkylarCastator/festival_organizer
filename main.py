import json
from music_managers.spotify_manager import SpotifyManager


class FestivalPlanner:
    def __init__(self, festival_data_file):
        self.festival_data_file = festival_data_file
        client_id = ''
        client_secret = ''
        redirect_uri = 'google.com'
        self.spotify_user = ""
        #self.spotify_instance = SpotifyManager(client_id, client_secret)

    def search_user_account(self):
        concert_data = self.load_concert_details(self.festival_data_file)
        artists_to_search = []
        for artist in concert_data:
            artists_to_search.append(artist)

        playlist_count_data = self.spotify_instance.search_spotify_playlists(artists_to_search)

        liked_artist_dictionary = {}
        for artist_data in playlist_count_data:
            if playlist_count_data[artist_data] > 0:
                liked_artist_dictionary[artist_data] = concert_data[artist_data]

        recommended, conflicts = self.sort_artists(liked_artist_dictionary)
        self.show_suggestion_results(recommended, conflicts)

    def load_concert_details(self, festival_data_file):
        """
        Loads a json file with the festival set times and artist
        :param festival_data_file: Path to the json file
        """
        with open(festival_data_file, "r") as f:
            dict = json.load(f)
            return dict

    def sort_artists(self, artists_dict):
        """
        From the list of artist in the user's playlist, find the available shows and organize
        them into a schedule.
        :param artists_dict: Artist in playlist
        """
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

    def show_suggestion_results(self, recommended, conflicts):
        """
        Display results of the search to the user
        :param recommended: A list of recommended shows to see
        :param conflicts: A list of shows that have conflicts
        """
        print("We did a search of your Spotify library and found artist you have added to playlists.")
        print("Recommended artists:")
        for artist_recommended in recommended:
            artist, start_time, end_time, stage = artist_recommended
            print(f"{artist}: {stage} : {start_time} - {end_time}")

        print("\nConflicting shows:")
        for conflict in conflicts:
            artist, start_time, end_time, stage = conflict
            print(f"{artist}: {stage} : {start_time} - {end_time}")


#if __name__ == "__main__":
#    file_path = f"festival_data/edc_sunday_2023.json"
#    festival_planner_instance = FestivalPlanner(file_path)





