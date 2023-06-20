from datetime import datetime, timedelta


class FestivalPlanner:
    def search_user_account(self, festival_information, playlist_count_data):
        liked_artist_dictionary = {}
        for artist_data in playlist_count_data:
            if playlist_count_data[artist_data] > 0:
                if artist_data in festival_information:
                    liked_artist_dictionary[artist_data] = festival_information[artist_data]

        return self.sort_artist_conflicts(liked_artist_dictionary)

    def sort_artist_conflicts(self, artists_dict):
        """
        From the list of artist in the user's playlist, find the available shows and organize
        them into a schedule.
        :param artists_dict: Artist in playlist
        """
        artists_start_times = [(artist, details['start-time'], details['end-time'], details['stage']) for
                               artist, details in artists_dict.items()]
        artists_start_times.sort(key=lambda x: (x[1], x[2]))

        recommended_artists = []
        conflicting_artist = []
        conflicts = {}
        for p1 in range(len(artists_start_times)):
            for p2 in range(p1+1, len(artists_start_times)):
                if self.check_conflicts(artists_start_times[p1], artists_start_times[p2]):
                    if artists_start_times[p1][0] not in conflicts:
                        conflicts[artists_start_times[p1][0]] = artists_start_times
                    if artists_start_times[p2][0] not in conflicts:
                        conflicts[artists_start_times[p2][0]] = artists_start_times
        for artist, start_time, end_time, stage in artists_start_times:
            if artist in conflicts:
                conflicting_artist.append((artist, start_time, end_time, stage))
            else:
                recommended_artists.append((artist, start_time, end_time, stage))

        return recommended_artists, conflicting_artist

    def check_conflicts(self, artist_original, artist_check):
        """
        Checks if 2 shows have conflict with eachother
        :param artist_original: Show to check
        :param artist_check: Show to check against
        :return: Returns a bool if there is a conflict
        """
        original_start, original_end = self.get_datetime_start_and_end(artist_original[1], artist_original[2])
        check_start, check_end = self.get_datetime_start_and_end(artist_check[1], artist_check[2])

        if check_start <= original_start < check_end:
            return True
        if check_start < original_end < check_end:
            return True
        if original_start <= check_start < original_end:
            return True
        if original_start < check_end < original_end:
            return True
        return False

    def get_datetime_start_and_end(self, artist_start_time, artist_end_time):
        """
        Converts the start and end times to register different days so its easier to calculate an overnight show
        :param artist_start_time: Start time of the show
        :param artist_end_time: End time of the show
        :returns: Returns the show start and end time with the day calculation
        """
        start_time = datetime.strptime(artist_start_time, '%I:%M %p').time()
        end_time = datetime.strptime(artist_end_time, '%I:%M %p').time()

        dummy_date = datetime.today().date()

        if start_time.strftime('%p') == 'AM':
            tomorrow_date = datetime.today().date() + timedelta(days=1)
            start = datetime.combine(tomorrow_date, start_time)
        else:
            start = datetime.combine(dummy_date, start_time)

        if end_time.strftime('%p') == 'AM':
            tomorrow_date = datetime.today().date() + timedelta(days=1)
            end = datetime.combine(tomorrow_date, end_time)
        else:
            end = datetime.combine(dummy_date, end_time)

        return start, end



