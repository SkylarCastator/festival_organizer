import json


class FestivalInformation:
    def __init__(self):
        self.concert_data = {}

    def load_concert_details(self, festival_data_file):
        """
        Loads a json file with the festival set times and artist
        :param festival_data_file: Path to the json file
        """
        with open(festival_data_file, "r") as f:
            dict = json.load(f)
            self.concert_data = dict

    def get_all_artist(self):
        """
        Gets a list of all artist for the entire festival
        :returns: Returns a list of artist for the entire festival
        """
        artists_to_search = []
        for lineup in self.concert_data["line_ups"]:
            for artist in lineup["shows"]:
                artists_to_search.append(artist)
        return artists_to_search

    def get_all_artist_for_date(self, date):
        """
        Searches a festival date to get artist for that day
        :param date: Date to be searched
        :return: Returns a list of artist for that day
        """
        artists_to_search = []
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                for artist in lineup["shows"]:
                    artists_to_search.append(artist)
                return artists_to_search
        return artists_to_search

    def get_show_data(self, date, artist):
        """
        Gets all the information an artist for a date
        :param  date: The date to be searched
        :param artist: The artist data to be returned
        :return: Returns the data for an artist show
        """
        data = {}
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                data = lineup["shows"][artist]
                return data
        return data

    def get_shows_for_date(self, date):
        """
        Get all the show data for a festival date
        :param date: The date of the festival to search
        :return: Returns a dictionary of all the shows for a date
        """
        data = {}
        for lineup in self.concert_data["line_ups"]:
            if lineup["date"] == date:
                data = lineup["shows"]
                return data
        return data

    def get_all_stages(self):
        """
        Gets all the available stages for the festival
        :return: List of all the stage names
        """
        stages = []
        for artist in self.concert_data["shows"]:
            if self.concert_data["shows"][artist]['stage'] not in stages:
                stages.append(self.concert_data["shows"][artist]['stage'])
        return stages

    def get_all_festival_dates(self):
        """
        Gets all the available days for the festival
        :returns: Returns a list of dates of the festival
        """
        dates = []
        for lineup in self.concert_data["line_ups"]:
            dates.append(lineup["date"])
        return dates

