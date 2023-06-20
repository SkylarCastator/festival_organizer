import streamlit as st
import pandas as pd


@st.cache_data
def get_playlist_data(_spotify_manager, spotify_user, _fest_info):
    playlist_data = _spotify_manager.search_spotify_playlists(spotify_user, _fest_info.get_all_artist())
    return playlist_data

@st.cache_data
def generate_festival_solver_tables(playlist_data, _fest_info, show_dates, _festival_planner_instance):
    recommended_tables = {}
    conflict_tables = {}
    for date in show_dates:
        shows = _fest_info.get_shows_for_date(date)
        #playlist_day_data = _spotify_manger.search_spotify_playlists(spotify_user,
        #                                                            _fest_info.get_all_artist_for_date(
        #                                                            date))
        recommended, conflicts = _festival_planner_instance.search_user_account(shows, playlist_data)
        recommended_data = {
            'Artist': [],
            'Start Time': [],
            'End Time': [],
            'Stage': []
        }
        for artist_recommended in recommended:
            artist, start_time, end_time, stage = artist_recommended
            recommended_data["Artist"].append(artist)
            recommended_data["Start Time"].append(start_time)
            recommended_data["End Time"].append(end_time)
            recommended_data["Stage"].append(stage)

        recommended_df = pd.DataFrame(recommended_data)
        recommended_tables[date] = recommended_df

        conflict_data = {
            'Artist': [],
            'Start Time': [],
            'End Time': [],
            'Stage': []
        }
        for conflict in conflicts:
            artist, start_time, end_time, stage = conflict
            conflict_data["Artist"].append(artist)
            conflict_data["Start Time"].append(start_time)
            conflict_data["End Time"].append(end_time)
            conflict_data["Stage"].append(stage)

        conflict_df = pd.DataFrame(conflict_data)
        conflict_tables[date] = conflict_df
    return recommended_tables, conflict_tables