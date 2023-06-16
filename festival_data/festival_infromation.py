import json


class FestivalInfromation:
    def __init__(self):
        self.concert_data = {}
        pass

    def load_concert_details(self, festival_data_file):
        """
        Loads a json file with the festival set times and artist
        :param festival_data_file: Path to the json file
        """
        with open(festival_data_file, "r") as f:
            dict = json.load(f)
            self.concert_data = dict

    def get_all_artist(self):
        artists_to_search = []
        for artist in self.concert_data["shows"]:
            artists_to_search.append(artist)
        return artists_to_search

    def get_all_stages(self):
        stages = []
        for artist in self.concert_data["shows"]:
            if self.concert_data["shows"][artist]['stage'] not in stages:
                stages.append(self.concert_data["shows"][artist]['stage'])
        return stages

    def get_all_show_times(self):
        pass
