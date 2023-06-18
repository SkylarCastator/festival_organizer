import json


class FestivalInformation:
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
        for lineup in self.concert_data["line_ups"]:
            for artist in lineup["shows"]:
                artists_to_search.append(artist)
        return artists_to_search

    def get_all_artist_for_date(self, date):
        artists_to_search = []
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                for artist in lineup["shows"]:
                    artists_to_search.append(artist)
                return artists_to_search
        return artists_to_search

    def get_show_data(self, date, artist):
        data = {}
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                data = lineup["shows"][artist]
                return data
        return data

    def get_shows_for_date(self, date):
        data = {}
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                data = lineup["shows"]
                return data
        return data

    def get_all_stages(self):
        stages = []
        for artist in self.concert_data["shows"]:
            if self.concert_data["shows"][artist]['stage'] not in stages:
                stages.append(self.concert_data["shows"][artist]['stage'])
        return stages

    def get_all_festival_dates(self):
        dates = []
        for lineup in self.concert_data["line_ups"]:
            dates.append(lineup["date"])
        return dates

